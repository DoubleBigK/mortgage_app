from __future__ import annotations
from typing import Any, TypedDict, get_type_hints, get_origin, get_args, Union, Literal, Annotated
import numpy as np


def _is_typed_dict(tp: Any) -> bool:
    return isinstance(tp, type) and hasattr(tp, "__total__") and hasattr(tp, "__required_keys__")

def _placeholder_for_type(tp: Any) -> Any:
    origin = get_origin(tp)
    args = get_args(tp)
    if origin is Union:
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            return _placeholder_for_type(non_none[0])
        return None

    # --- Annotated[T, ...] ---
    if origin is Annotated:
        # bierzemy "goły" typ bez metadanych
        if args:
            return _placeholder_for_type(args[0])
        return None

    # --- Literal[...] ---
    if origin is Literal:
        # weź pierwszą wartość literalną, jeśli jest
        return args[0] if args else None

    # --- generics: list / dict / tuple / set itp. ---
    if origin is list or tp is list:
        return []
    if origin is set or tp is set:
        return set()
    if origin is dict or tp is dict:
        return {}
    if origin is tuple or tp is tuple:
        # nie próbujemy zgadywać zawartości, pusta krotka wystarczy
        return tuple()

    # --- numpy array ---
    if tp is np.ndarray or origin is np.ndarray:
        return np.array([])

    # --- proste typy wprost ---
    if tp is int:
        return 0
    if tp is float:
        return 0.0
    if tp is bool:
        return False
    if tp is str:
        return ""
    if tp is bytes:
        return b""

    # cokolwiek innego -> None
    return None

def build_template(typed_dict_cls: type[TypedDict]) -> dict[str, Any]:
    template: dict[str, Any] = {}
    hints = get_type_hints(typed_dict_cls)
    for field_name, field_type in hints.items():
        if _is_typed_dict(field_type):
            template[field_name] = build_template(field_type)
        else:
            template[field_name] = _placeholder_for_type(field_type)

    return template
