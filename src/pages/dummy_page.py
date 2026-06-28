import streamlit as st


DEFAULT_APARTMENT = {
    "name": "",
    "address": "",
    "city": "",
    "district": "",
    "area": 50.0,
    "price": 600_000,
    "rooms": 2,
    "floor": 1,
    "building_floors": 5,
    "year_built": 2010,
    "market": "Wtórny",
    "condition": "Do odświeżenia",
    "monthly_admin_fee": 600,
    "renovation_budget": 0,
    "parking_price": 0,
    "storage_price": 0,
    "has_balcony": False,
    "has_elevator": True,
    "comment": "",
}


def render():
    form_tab, table_tab = st.tabs(["Formularz", "Tabela"])

    with form_tab:
        _render_form()
    with table_tab:
        _render_summary()


def _render_form():
    st.header("Mieszkanie")

    apartment = st.session_state.get("apartment", DEFAULT_APARTMENT.copy())

    with st.form("apartment_form"):
        st.subheader("Adres i opis")
        name = st.text_input("Nazwa robocza", value=apartment["name"])
        address = st.text_input("Adres", value=apartment["address"])
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("Miasto", value=apartment["city"])
        with col2:
            district = st.text_input("Dzielnica / okolica", value=apartment["district"])

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

        col1, col2, col3 = st.columns(3)
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
                ["Wtórny", "Pierwotny"],
                index=["Wtórny", "Pierwotny"].index(apartment["market"]),
            )
        with col3:
            condition = st.selectbox(
                "Stan",
                ["Do remontu", "Do odświeżenia", "Gotowe do wejścia", "Deweloperski"],
                index=[
                    "Do remontu",
                    "Do odświeżenia",
                    "Gotowe do wejścia",
                    "Deweloperski",
                ].index(apartment["condition"]),
            )

        st.subheader("Koszty")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            price = st.number_input(
                "Cena [zł]",
                min_value=0,
                value=int(apartment["price"]),
                step=10_000,
                format="%d",
            )
        with col2:
            monthly_admin_fee = st.number_input(
                "Czynsz admin. [zł/mies.]",
                min_value=0,
                value=int(apartment["monthly_admin_fee"]),
                step=50,
                format="%d",
            )
        with col3:
            renovation_budget = st.number_input(
                "Budżet remontu [zł]",
                min_value=0,
                value=int(apartment["renovation_budget"]),
                step=5_000,
                format="%d",
            )
        with col4:
            parking_price = st.number_input(
                "Miejsce parkingowe [zł]",
                min_value=0,
                value=int(apartment["parking_price"]),
                step=5_000,
                format="%d",
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            storage_price = st.number_input(
                "Komórka lokatorska [zł]",
                min_value=0,
                value=int(apartment["storage_price"]),
                step=1_000,
                format="%d",
            )
        with col2:
            has_balcony = st.checkbox("Balkon / taras", value=apartment["has_balcony"])
        with col3:
            has_elevator = st.checkbox("Winda", value=apartment["has_elevator"])

        comment = st.text_area("Komentarz", value=apartment["comment"], height=120)

        submitted = st.form_submit_button("Zapisz mieszkanie")

    if submitted:
        st.session_state["apartment"] = {
            "name": name,
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
            "monthly_admin_fee": monthly_admin_fee,
            "renovation_budget": renovation_budget,
            "parking_price": parking_price,
            "storage_price": storage_price,
            "has_balcony": has_balcony,
            "has_elevator": has_elevator,
            "comment": comment,
        }
        st.success("Dane mieszkania zapisane.")


def _render_summary():
    st.header("Tabela mieszkania")

    apartment = st.session_state.get("apartment")
    if not apartment:
        st.info("Uzupełnij i zapisz formularz mieszkania.")
        return

    metrics = _calculate_metrics(apartment)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cena", _format_pln(apartment["price"]))
    col2.metric("Cena za m²", _format_pln(metrics["price_per_sqm"]))
    col3.metric("Koszt całkowity", _format_pln(metrics["total_cost"]))
    col4.metric("Koszt / pokój", _format_pln(metrics["price_per_room"]))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Metraż", f"{apartment['area']:.2f} m²")
    col2.metric("Pokoje", apartment["rooms"])
    col3.metric("Piętro", f"{apartment['floor']} / {apartment['building_floors']}")
    col4.metric("Czynsz / m²", _format_pln(metrics["admin_fee_per_sqm"]))

    st.subheader("Dane")
    st.json(apartment)


def _calculate_metrics(apartment: dict) -> dict:
    total_cost = (
        apartment["price"]
        + apartment["renovation_budget"]
        + apartment["parking_price"]
        + apartment["storage_price"]
    )
    return {
        "total_cost": total_cost,
        "price_per_sqm": total_cost / apartment["area"],
        "price_per_room": total_cost / apartment["rooms"],
        "admin_fee_per_sqm": apartment["monthly_admin_fee"] / apartment["area"],
    }


def _format_pln(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ") + " zł"


if __name__ == "__main__":
    render()
