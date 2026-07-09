from datetime import datetime
from html import escape
import json
from pathlib import Path

import folium
import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components


APARTMENTS_FILE = Path(__file__).resolve().parents[2] / "storage" / "apartments.json"
GEOCODING_CACHE_FILE = (
    Path(__file__).resolve().parents[2] / "storage" / "geocoding_cache.json"
)
GEOCODING_USER_AGENT = "mortgage_app/1.0"
WARSAW_LATITUDE = 52.2297
WARSAW_LONGITUDE = 21.0122

DEFAULT_APARTMENT = {
    "address": "",
    "city": "Warszawa",
    "district": "",
    "area": 50.0,
    "price": 600_000,
    "rooms": 2,
    "floor": 1,
    "building_floors": 5,
    "year_built": 2010,
    "market": "Wtórny",
    "condition": "Do odświeżenia",
    "ownership_form": "",
    "optimal_layout": "Jest",
    "offer_url": "",
    "has_balcony": False,
    "comment": "",
}

MARKETS = ["Wtórny", "Pierwotny"]
CONDITIONS = ["Do remontu", "Do odświeżenia", "Gotowe do wejścia", "Deweloperski"]
OPTIMAL_LAYOUTS = ["Jest", "Do zrobienia", "Do zrobeinia z trudem", "Nie da się"]
APARTMENT_FIELDS = [
    "saved_at",
    "address",
    "city",
    "district",
    "area",
    "price",
    "rooms",
    "floor",
    "building_floors",
    "year_built",
    "market",
    "condition",
    "ownership_form",
    "optimal_layout",
    "offer_url",
    "has_balcony",
    "comment",
]


def render():
    form_tab, table_tab, map_tab = st.tabs(["Formularz", "Tabela", "Mapa"])

    with form_tab:
        _render_form()
    with table_tab:
        _render_table()
    with map_tab:
        _render_map()


def _render_form():
    st.header("Mieszkanie")

    apartment = _normalize_apartment(
        st.session_state.get("apartment", DEFAULT_APARTMENT.copy())
    )

    with st.form("apartment_form"):
        st.subheader("Adres i opis")
        address = st.text_input("Adres", value=apartment["address"])
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("Miasto", value=apartment["city"])
        with col2:
            district = st.text_input("Dzielnica / okolica", value=apartment["district"])
        offer_url = st.text_input("Link do oferty", value=apartment["offer_url"])

        st.subheader("Parametry")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            area = st.number_input(
                "Metraż [m²]",
                min_value=1.0,
                value=float(apartment["area"]),
                step=1.0,
                format="%.2f",
            )
        with col2:
            rooms = st.number_input(
                "Liczba pokoi",
                min_value=1,
                value=int(apartment["rooms"]),
                step=1,
            )
        with col3:
            floor = st.number_input(
                "Piętro",
                min_value=-1,
                value=int(apartment["floor"]),
                step=1,
            )
        with col4:
            building_floors = st.number_input(
                "Pięter w budynku",
                min_value=1,
                value=int(apartment["building_floors"]),
                step=1,
            )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            year_built = st.number_input(
                "Rok budowy",
                min_value=1800,
                max_value=2100,
                value=int(apartment["year_built"]),
                step=1,
            )
        with col2:
            market = st.selectbox(
                "Rynek",
                MARKETS,
                index=_option_index(MARKETS, apartment["market"]),
            )
        with col3:
            condition = st.selectbox(
                "Stan",
                CONDITIONS,
                index=_option_index(CONDITIONS, apartment["condition"]),
            )
        with col4:
            optimal_layout = st.selectbox(
                "Optymalny układ",
                OPTIMAL_LAYOUTS,
                index=_option_index(OPTIMAL_LAYOUTS, apartment["optimal_layout"]),
            )

        ownership_form = st.text_input(
            "Forma własności",
            value=apartment["ownership_form"],
        )

        st.subheader("Koszty")
        price = st.number_input(
            "Cena [zł]",
            min_value=0,
            value=int(apartment["price"]),
            step=10_000,
            format="%d",
        )

        has_balcony = st.checkbox("Balkon / taras", value=apartment["has_balcony"])
        comment = st.text_area("Komentarz", value=apartment["comment"], height=120)

        submitted = st.form_submit_button("Zapisz mieszkanie")

    if submitted:
        saved_apartment = {
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "address": address,
            "city": city,
            "district": district,
            "area": area,
            "price": price,
            "rooms": rooms,
            "floor": floor,
            "building_floors": building_floors,
            "year_built": year_built,
            "market": market,
            "condition": condition,
            "ownership_form": ownership_form,
            "optimal_layout": optimal_layout,
            "offer_url": offer_url,
            "has_balcony": has_balcony,
            "comment": comment,
        }
        _append_apartment(saved_apartment)
        st.session_state["apartment"] = saved_apartment
        st.success("Dane mieszkania zapisane na stałe.")


def _render_table():
    st.header("Tabela mieszkań")

    apartments = _load_apartments()
    if not apartments:
        st.info("Uzupełnij i zapisz formularz mieszkania.")
        return

    matching_indexes = _render_table_filters(apartments)
    if not matching_indexes:
        st.caption(f"Wyświetlane rekordy: 0 z {len(apartments)}")
        st.info("Brak mieszkań dla wybranych filtrów.")
        return

    st.caption(f"Wyświetlane rekordy: {len(matching_indexes)} z {len(apartments)}")

    edited_table = st.data_editor(
        _build_apartments_table(apartments, matching_indexes),
        column_config={
            "record_id": None,
            "Usuń": st.column_config.CheckboxColumn("Usuń"),
            "Rynek": st.column_config.SelectboxColumn("Rynek", options=MARKETS),
            "Stan": st.column_config.SelectboxColumn("Stan", options=CONDITIONS),
            "Optymalny układ": st.column_config.SelectboxColumn(
                "Optymalny układ",
                options=OPTIMAL_LAYOUTS,
            ),
            "Link do oferty": st.column_config.LinkColumn("Link do oferty"),
        },
        disabled=[
            "Data zapisu",
            "Cena za m² [zł]",
            "Koszt całk. [zł]",
        ],
        hide_index=True,
        key="apartments_editor",
        use_container_width=True,
    )

    updated_apartments = _apply_table_changes(apartments, edited_table)
    if updated_apartments != [_normalize_apartment(apartment) for apartment in apartments]:
        _save_apartments(updated_apartments)
        st.toast("Zmiany w tabeli zapisane.")


def _render_map():
    st.header("Mapa")

    apartments = _load_apartments()
    markers, skipped_count = _build_map_markers(apartments)

    warsaw_map = folium.Map(
        location=[WARSAW_LATITUDE, WARSAW_LONGITUDE],
        zoom_start=12,
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr=(
            "Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar "
            "Geographics, and the GIS User Community"
        ),
        control_scale=True,
    )

    for marker in markers:
        folium.Marker(
            [marker["latitude"], marker["longitude"]],
            tooltip=marker["tooltip"],
            popup=folium.Popup(marker["popup"], max_width=340),
        ).add_to(warsaw_map)

    if markers:
        warsaw_map.fit_bounds(
            [
                [marker["latitude"], marker["longitude"]]
                for marker in markers
            ],
            padding=(30, 30),
        )

    st.caption(f"Pinezki na mapie: {len(markers)} z {len(apartments)}")
    if skipped_count:
        st.caption(f"Bez współrzędnych: {skipped_count}")

    components.html(warsaw_map._repr_html_(), height=620)


def _render_table_filters(apartments: list[dict]) -> list[int]:
    normalized_apartments = [
        _normalize_apartment(apartment)
        for apartment in apartments
    ]
    metrics_by_index = [
        _calculate_metrics(apartment)
        for apartment in normalized_apartments
    ]

    with st.expander("Filtry", expanded=False):
        text_col1, text_col2, text_col3 = st.columns(3)
        with text_col1:
            saved_at = st.text_input("Data zapisu zawiera")
            address = st.text_input("Adres zawiera")
        with text_col2:
            city = st.text_input("Miasto zawiera")
            district = st.text_input("Dzielnica zawiera")
        with text_col3:
            ownership_form = st.text_input("Forma własności zawiera")
            comment = st.text_input("Komentarz zawiera")

        select_col1, select_col2, select_col3, select_col4 = st.columns(4)
        with select_col1:
            markets = st.multiselect("Rynek", _unique_values(apartments, "market"))
        with select_col2:
            conditions = st.multiselect("Stan", _unique_values(apartments, "condition"))
        with select_col3:
            optimal_layouts = st.multiselect(
                "Optymalny układ",
                _unique_values(apartments, "optimal_layout"),
            )
        with select_col4:
            balcony_options = st.multiselect(
                "Balkon / taras",
                ["Tak", "Nie"],
            )

        range_col1, range_col2, range_col3 = st.columns(3)
        with range_col1:
            area_range = _number_range_filter(
                "Metraż [m²]",
                [apartment["area"] for apartment in normalized_apartments],
                "area",
                is_float=True,
            )
            price_range = _number_range_filter(
                "Cena [zł]",
                [apartment["price"] for apartment in normalized_apartments],
                "price",
            )
            price_per_sqm_range = _number_range_filter(
                "Cena za m² [zł]",
                [metrics["price_per_sqm"] for metrics in metrics_by_index],
                "price_per_sqm",
            )
        with range_col2:
            total_cost_range = _number_range_filter(
                "Koszt całk. [zł]",
                [metrics["total_cost"] for metrics in metrics_by_index],
                "total_cost",
            )
            rooms_range = _number_range_filter(
                "Pokoje",
                [apartment["rooms"] for apartment in normalized_apartments],
                "rooms",
            )
            floor_range = _number_range_filter(
                "Piętro",
                [apartment["floor"] for apartment in normalized_apartments],
                "floor",
            )
        with range_col3:
            building_floors_range = _number_range_filter(
                "Pięter w budynku",
                [apartment["building_floors"] for apartment in normalized_apartments],
                "building_floors",
            )
            year_built_range = _number_range_filter(
                "Rok budowy",
                [apartment["year_built"] for apartment in normalized_apartments],
                "year_built",
            )

    matching_indexes = []
    for index, apartment in enumerate(normalized_apartments):
        metrics = metrics_by_index[index]
        if not _text_matches(apartment["saved_at"], saved_at):
            continue
        if not _text_matches(apartment["address"], address):
            continue
        if not _text_matches(apartment["city"], city):
            continue
        if not _text_matches(apartment["district"], district):
            continue
        if not _text_matches(apartment["ownership_form"], ownership_form):
            continue
        if not _text_matches(apartment["comment"], comment):
            continue
        if markets and apartment["market"] not in markets:
            continue
        if conditions and apartment["condition"] not in conditions:
            continue
        if optimal_layouts and apartment["optimal_layout"] not in optimal_layouts:
            continue
        if balcony_options and _balcony_label(apartment["has_balcony"]) not in balcony_options:
            continue
        if not _number_in_range(apartment["area"], area_range):
            continue
        if not _number_in_range(apartment["price"], price_range):
            continue
        if not _number_in_range(metrics["price_per_sqm"], price_per_sqm_range):
            continue
        if not _number_in_range(metrics["total_cost"], total_cost_range):
            continue
        if not _number_in_range(apartment["rooms"], rooms_range):
            continue
        if not _number_in_range(apartment["floor"], floor_range):
            continue
        if not _number_in_range(apartment["building_floors"], building_floors_range):
            continue
        if not _number_in_range(apartment["year_built"], year_built_range):
            continue
        matching_indexes.append(index)
    return matching_indexes


def _load_apartments() -> list[dict]:
    if not APARTMENTS_FILE.exists():
        return []
    with APARTMENTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save_apartments(apartments: list[dict]) -> None:
    APARTMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with APARTMENTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(apartments, file, ensure_ascii=False, indent=2)


def _append_apartment(apartment: dict) -> None:
    apartments = _load_apartments()
    apartments.append(apartment)
    _save_apartments(apartments)


def _build_map_markers(apartments: list[dict]) -> tuple[list[dict], int]:
    cache = _load_geocoding_cache()
    cache_changed = False
    markers = []
    skipped_count = 0

    for apartment in apartments:
        normalized = _normalize_apartment(apartment)
        coordinates, was_cached = _geocode_apartment(normalized, cache)
        cache_changed = cache_changed or not was_cached
        if not coordinates:
            skipped_count += 1
            continue
        markers.append(
            {
                "latitude": coordinates["latitude"],
                "longitude": coordinates["longitude"],
                "tooltip": _map_marker_tooltip(normalized),
                "popup": _map_marker_popup(normalized),
            }
        )

    if cache_changed:
        _save_geocoding_cache(cache)

    return markers, skipped_count


def _load_geocoding_cache() -> dict:
    if not GEOCODING_CACHE_FILE.exists():
        return {}
    with GEOCODING_CACHE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save_geocoding_cache(cache: dict) -> None:
    GEOCODING_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with GEOCODING_CACHE_FILE.open("w", encoding="utf-8") as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)


def _geocode_apartment(apartment: dict, cache: dict) -> tuple[dict | None, bool]:
    query = _geocoding_query(apartment)
    if not query:
        return None, True

    cache_key = query.lower()
    if cache_key in cache:
        return cache[cache_key], True

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "json",
                "limit": 1,
                "countrycodes": "pl",
            },
            headers={"User-Agent": GEOCODING_USER_AGENT},
            timeout=8,
        )
        response.raise_for_status()
        results = response.json()
    except requests.RequestException:
        return None, True

    if not results:
        cache[cache_key] = None
        return None, False

    cache[cache_key] = {
        "latitude": float(results[0]["lat"]),
        "longitude": float(results[0]["lon"]),
    }
    return cache[cache_key], False


def _geocoding_query(apartment: dict) -> str:
    address_parts = [
        apartment.get("address", ""),
        apartment.get("city", ""),
        "Polska",
    ]
    return ", ".join(
        str(part).strip()
        for part in address_parts
        if str(part).strip()
    )


def _map_marker_tooltip(apartment: dict) -> str:
    address = apartment["address"] or "Mieszkanie"
    return f"{address}, {apartment['city']}"


def _map_marker_popup(apartment: dict) -> str:
    offer_url = apartment.get("offer_url", "")
    offer_link = ""
    if offer_url:
        escaped_url = escape(offer_url)
        offer_link = f'<br><a href="{escaped_url}" target="_blank">Link do oferty</a>'

    return (
        f"<b>{escape(apartment['address'] or 'Mieszkanie')}</b>"
        f"<br>{escape(apartment['city'])}"
        f"<br>Cena: {apartment['price']:,.0f} zł"
        f"<br>Metraż: {apartment['area']:,.2f} m²"
        f"{offer_link}"
    )


def _build_apartments_table(
    apartments: list[dict],
    indexes: list[int],
) -> pd.DataFrame:
    rows = []
    for index in indexes:
        apartment = _normalize_apartment(apartments[index])
        metrics = _calculate_metrics(apartment)
        rows.append(
            {
                "record_id": index,
                "Usuń": False,
                "Data zapisu": apartment.get("saved_at", ""),
                "Adres": apartment["address"],
                "Miasto": apartment["city"],
                "Dzielnica": apartment["district"],
                "Metraż [m²]": apartment["area"],
                "Cena [zł]": apartment["price"],
                "Cena za m² [zł]": round(metrics["price_per_sqm"]),
                "Koszt całk. [zł]": metrics["total_cost"],
                "Pokoje": apartment["rooms"],
                "Piętro": apartment["floor"],
                "Pięter w budynku": apartment["building_floors"],
                "Rok budowy": apartment["year_built"],
                "Rynek": apartment["market"],
                "Stan": apartment["condition"],
                "Forma własności": apartment["ownership_form"],
                "Optymalny układ": apartment["optimal_layout"],
                "Link do oferty": apartment["offer_url"],
                "Balkon / taras": apartment["has_balcony"],
                "Komentarz": apartment["comment"],
            }
        )
    return pd.DataFrame(rows)


def _apply_table_changes(apartments: list[dict], edited_table: pd.DataFrame) -> list[dict]:
    edited_by_index = {
        int(row["record_id"]): row
        for row in edited_table.to_dict("records")
    }
    deleted_indexes = {
        index
        for index, row in edited_by_index.items()
        if bool(row.get("Usuń", False))
    }

    updated_apartments = []
    for index, apartment in enumerate(apartments):
        if index in deleted_indexes:
            continue
        if index in edited_by_index:
            updated_apartments.append(_apartment_from_table_row(edited_by_index[index]))
        else:
            updated_apartments.append(_normalize_apartment(apartment))
    return updated_apartments


def _apartment_from_table_row(row: dict) -> dict:
    return {
        "saved_at": str(row.get("Data zapisu", "")),
        "address": str(row.get("Adres", "")),
        "city": str(row.get("Miasto", "")),
        "district": str(row.get("Dzielnica", "")),
        "area": _as_float(row.get("Metraż [m²]"), DEFAULT_APARTMENT["area"]),
        "price": _as_int(row.get("Cena [zł]"), DEFAULT_APARTMENT["price"]),
        "rooms": _as_int(row.get("Pokoje"), DEFAULT_APARTMENT["rooms"]),
        "floor": _as_int(row.get("Piętro"), DEFAULT_APARTMENT["floor"]),
        "building_floors": _as_int(
            row.get("Pięter w budynku"),
            DEFAULT_APARTMENT["building_floors"],
        ),
        "year_built": _as_int(row.get("Rok budowy"), DEFAULT_APARTMENT["year_built"]),
        "market": str(row.get("Rynek", DEFAULT_APARTMENT["market"])),
        "condition": str(row.get("Stan", DEFAULT_APARTMENT["condition"])),
        "ownership_form": str(
            row.get("Forma własności", DEFAULT_APARTMENT["ownership_form"])
        ),
        "optimal_layout": str(
            row.get("Optymalny układ", DEFAULT_APARTMENT["optimal_layout"])
        ),
        "offer_url": str(row.get("Link do oferty", DEFAULT_APARTMENT["offer_url"])),
        "has_balcony": bool(row.get("Balkon / taras", DEFAULT_APARTMENT["has_balcony"])),
        "comment": str(row.get("Komentarz", "")),
    }


def _normalize_apartment(apartment: dict) -> dict:
    normalized = DEFAULT_APARTMENT.copy()
    normalized.update(apartment)
    if "saved_at" not in normalized:
        normalized["saved_at"] = ""
    return {
        field: normalized[field]
        for field in APARTMENT_FIELDS
    }


def _unique_values(apartments: list[dict], field: str) -> list[str]:
    return sorted(
        {
            str(_normalize_apartment(apartment).get(field, ""))
            for apartment in apartments
            if _normalize_apartment(apartment).get(field, "")
        }
    )


def _number_range_filter(
    label: str,
    values: list[float | int],
    key: str,
    is_float: bool = False,
) -> tuple[float, float]:
    minimum = min(values)
    maximum = max(values)
    step = 1.0 if is_float else 1
    value_format = "%.2f" if is_float else "%d"

    st.caption(f"{label}: min {minimum:g}, max {maximum:g}")
    from_col, to_col = st.columns(2)
    with from_col:
        from_value = st.number_input(
            "Od",
            value=float(minimum) if is_float else int(minimum),
            step=step,
            format=value_format,
            key=f"filter_{key}_from",
        )
    with to_col:
        to_value = st.number_input(
            "Do",
            value=float(maximum) if is_float else int(maximum),
            step=step,
            format=value_format,
            key=f"filter_{key}_to",
        )
    return from_value, to_value


def _text_matches(value: str, query: str) -> bool:
    if not query:
        return True
    return query.lower() in str(value).lower()


def _number_in_range(value: float | int, selected_range: tuple[float, float]) -> bool:
    lower, upper = selected_range
    if lower > upper:
        lower, upper = upper, lower
    return lower <= value <= upper


def _balcony_label(has_balcony: bool) -> str:
    return "Tak" if has_balcony else "Nie"


def _apartment_search_text(apartment: dict) -> str:
    return " ".join(
        str(apartment.get(field, ""))
        for field in [
            "address",
            "city",
            "district",
            "ownership_form",
            "offer_url",
            "comment",
        ]
    ).lower()


def _as_float(value, default: float) -> float:
    if pd.isna(value):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value, default: int) -> int:
    return int(_as_float(value, default))


def _calculate_metrics(apartment: dict) -> dict:
    total_cost = apartment["price"]
    return {
        "total_cost": total_cost,
        "price_per_sqm": total_cost / apartment["area"],
        "price_per_room": total_cost / apartment["rooms"],
    }


def _option_index(options: list[str], value: str) -> int:
    if value in options:
        return options.index(value)
    return 0


if __name__ == "__main__":
    render()
