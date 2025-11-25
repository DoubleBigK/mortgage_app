import streamlit as st
from typing import List, Tuple
from modules.utils import format_pln_full, format_to_percentage

def centered_text(text: str, level: int = 1):
    st.markdown(
        f"<h{level} style='text-align:center; margin-bottom:0.4rem;'>{text}</h{level}>",
        unsafe_allow_html=True
    )

def format_months(total_months: int) -> str:
    def _plural_rok(n: int) -> str:
        if n % 10 == 1 and n % 100 != 11:
            return "rok"
        elif n % 10 in (2, 3, 4) and not (12 <= n % 100 <= 14):
            return "lata"
        else:
            return "lat"
    def _plural_miesiac(n: int) -> str:
        if n % 10 == 1 and n % 100 != 11:
            return "miesiąc"
        elif n % 10 in (2, 3, 4) and not (12 <= n % 100 <= 14):
            return "miesiące"
        else:
            return "miesięcy"
    if total_months < 0:
        raise ValueError("Number of months can't be negative")

    years = total_months // 12
    months = total_months % 12

    parts = []

    if years > 0:
        parts.append(f"{years} {_plural_rok(years)}")
    if months > 0 or (years == 0 and months == 0):
        parts.append(f"{months} {_plural_miesiac(months)}")

    return " ".join(parts)

def display_number_composition(number_composition: List[Tuple[str, int, bool]]) -> None:
    def _show_composite():

        emoji = "🔼" if up else "🔽"

        st.markdown(f"""
                            <div style="
                                display:flex;
                                flex-direction:column;
                                align-items:center;
                                text-align:center;
                            ">
                                <div style="font-size:1.2rem;line-height:.8;">
                                    {emoji}
                                </div>
                                <div style="
                                    font-size:0.8rem;
                                    color:#6b7280;
                                    margin-top:0.25rem;
                                    white-space:nowrap;
                                ">
                                    {label}
                                </div>
                                <div style="
                                    font-size:1.2rem;
                                    font-weight:600;
                                    margin-top:0.1rem;
                                    white-space:nowrap;
                                ">
                                    {value}
                                </div>
                            </div>
                            """,
        unsafe_allow_html = True)
    def _get_total():
        _total = sum([i[1] if i[2] else -i[1] for i in number_composition])
        _show_func = format_pln_full if type(_total) == int else format_to_percentage
        _total = _show_func(_total)
        return _total, _show_func
    with st.container(border=True):
        total, show_func = _get_total()
        centered_text(text = total, level = 1)
        cols = st.columns(len(number_composition))
        for col, (label, value, up) in zip(cols, number_composition):
            value = show_func(value)
            with col:
                _show_composite()

def mortgage_display(mortgage_name):
    base = st.session_state[mortgage_name]["details"]["base"]
    extended = st.session_state[mortgage_name]["details"]["extended"]

    def _titles():
        title_cols = st.columns(2)
        for col, text in zip(title_cols, ["Bazowe", "Łączne"]):
            with col:
                centered_text(text, level = 2)
    def _one_row(title, number_composition_base, number_composition_extended):

        st.markdown(
            f"<h3 style='text-align: center;'>{title}</h3>",
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            display_number_composition(number_composition_base)
        with col2:
            display_number_composition(number_composition_extended)
    def _duration():
        centered_text(text="Czas trwania kredytu", level=3)
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                centered_text(text=format_months(len(base["cashflows"]["capital_installment"])), level=2)
        with col2:
            with st.container(border=True):
                centered_text(text=format_months(len(extended["cashflows"]["capital_installment"])), level=2)
    def _tcc_base():
        title = "Całkowity koszt kapitału"
        number_composition_base = [
            ("Odsetki", int(sum(base["cashflows"]["intrest_installment"])), True),
            ("Początkowe", int(sum(base["upfront"].values())), True)
        ]
        number_composition_extended = [
            ("Odsetki", int(sum(extended["cashflows"]["intrest_installment"])), True),
            ("Początkowe", int(sum(extended["upfront"].values())), True),
            ("Dodatkowe", int(sum(extended["cashflows"]["additional_costs"])), True),
        ]
        _one_row(title, number_composition_base, number_composition_extended)
    def _first_payment():
        title = "Pierwsza rata"
        number_composition_base = [
            ("Odsetki", int(base["cashflows"]["intrest_installment"][0]), True),
            ("Kapitał", int(base["cashflows"]["capital_installment"][0]), True)
        ]
        number_composition_extended = [
            ("Odsetki", int(extended["cashflows"]["intrest_installment"][0]), True),
            ("Kapitał", int(extended["cashflows"]["capital_installment"][0]), True),
            ("Przedpłata", int(extended["cashflows"]["prepayments"][0]), True),
            ("Dodatkowe", int(extended["cashflows"]["additional_costs"][0]), True)
        ]
        _one_row(title, number_composition_base, number_composition_extended)
    def _upfront():
        title = "Koszty początkowe"
        number_composition_base = [
            ("Prowizja", base["upfront"]["commission"], True),
            ("Wycena", base["upfront"]["appraisal"], True),
            ("Aneks", base["upfront"]["annex"], True),
            ("Pozostałe", base["upfront"]["other"], True),
        ]

        number_composition_extended = [
            ("Prowizja", extended["upfront"]["commission"], True),
            ("Wycena", extended["upfront"]["appraisal"], True),
            ("Aneks", extended["upfront"]["annex"], True),
            ("Pozostałe", extended["upfront"]["other"], True),
            ("Dodatkowe", extended["upfront"]["additional_cost"], True),
        ]
        _one_row(title, number_composition_base, number_composition_extended)

    _titles()
    _duration()
    _tcc_base()
    _first_payment()
    _upfront()


