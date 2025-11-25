from typing import TypedDict, List, Tuple

def intrest(
        discounts: List[Tuple[float, float, bool]],
        products: List[Tuple[int | float, float, float, bool]]
) -> float:
    return sum(x[0] for x in discounts if x[-1]) + sum(x[2] for x in products if x[-1])

def commission(
        discounts: List[Tuple[float, float, bool]],
        products: List[Tuple[int | float, float, float, bool]]
) -> float:
    return sum(x[1] for x in discounts if x[-1]) + sum(x[3] for x in products if x[-1])