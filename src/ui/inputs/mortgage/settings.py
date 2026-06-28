import streamlit as st
import modules
import ui

class PrepaymentHelper:
    def __init__(self, mortgage_name: str):
        self.mortgage_name = mortgage_name
        self.mortgage_duration = modules.utils.get_from_state(  # region
                self.mortgage_name,
                "settings",
                "duration"
            ) # endregion
        self.prep_name = f"{mortgage_name}_prep"
        self.sub_ids_list_name = f"{self.prep_name}_ids"
        self.counter_name = f"{self.prep_name}_counter"
        key_namer = "{prep_name}_{key}_{sub_id}".format
        self.key_namer = lambda key, sub_id: key_namer(prep_name=self.prep_name,key=key, sub_id=sub_id)
        if self.sub_ids_list_name not in st.session_state:
            st.session_state[self.sub_ids_list_name] = []
            st.session_state[self.counter_name] = 0
    def single_prepayment(self, sub_id: int) -> None:
        sub_ids_list =sorted(st.session_state[self.sub_ids_list_name], reverse=True)
        subtract = 2*sub_ids_list.index(sub_id)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            prepayment_type = st.selectbox(
                f"Rodzaj przedpłaty",
                options=["Cała rata", "Procent raty", "Kwota nadpłaty"],
                key=self.key_namer("type", sub_id)
            )
        with c2:
            if prepayment_type == "Procent raty":
                value = st.number_input(
                    "Wysokość[%]",
                    min_value=0.0,
                    step=0.1,
                    key=self.key_namer("value", sub_id)
                )
            elif prepayment_type == "Kwota nadpłaty":
                value = st.number_input(
                    "Kwota nadpłaty[zł]",
                    min_value=0,
                    step=100,
                    key=self.key_namer("value", sub_id)
                )
            else:
                value = st.number_input(
                    "Rata całkowita [zł]",
                    min_value=0,
                    step=100,
                    key=self.key_namer("value", sub_id)
                )
        with c3:
            def _get_min_value() -> int | None:
                last_sub_id = max(
                    [i for i in st.session_state[self.sub_ids_list_name] if i < sub_id],
                    default=None
                )
                if last_sub_id:
                    last_end_key = self.key_namer("end", last_sub_id)
                    if last_end_key in st.session_state:
                        return st.session_state[last_end_key] + 1
                return 1
            min_start_nr = _get_min_value()
            max_start_nr = self.mortgage_duration - subtract - 1
            key = self.key_namer("start", sub_id)
            ui.utils.input_number_key_trick(key, min_start_nr, max_start_nr)
            st.number_input(# region
                "Od raty nr",
                min_value=min_start_nr,
                max_value=max_start_nr,
                step=1,
                key=key
            )# endregion
        with c4:
            min_end_nr = st.session_state[self.key_namer("start", sub_id)] + 1
            max_end_nr = self.mortgage_duration - subtract
            key = self.key_namer("end", sub_id)
            ui.utils.input_number_key_trick(key, min_end_nr, max_end_nr, default = self.mortgage_duration)
            st.number_input(  # region
                "Do raty nr",
                min_value=min_end_nr,
                max_value=max_end_nr,
                step=1,
                key=key
            )  # endregion
        with c5:
            st.button(
                "Usuń",
                key=self.key_namer("remove", sub_id),
                on_click=self.remove_prepayment,
                args=(sub_id,)
            )
    def add_prepayment(self):
        st.session_state[self.counter_name] += 1
        new_id = st.session_state[self.counter_name]
        st.session_state[self.sub_ids_list_name].append(new_id)
    def remove_prepayment(self, sub_id: int) -> None:
        st.session_state[self.sub_ids_list_name] = [
            pid for pid in st.session_state[self.sub_ids_list_name] if pid != sub_id
        ]
        del st.session_state[self.key_namer("type", sub_id)]
        del st.session_state[self.key_namer("value", sub_id)]
        del st.session_state[self.key_namer("start", sub_id)]
        del st.session_state[self.key_namer("end", sub_id)]
        del st.session_state[self.key_namer("remove", sub_id)]
    def remove_all_prepayments(self):
        st.session_state[self.counter_name] = 0
        for sub_id in st.session_state[self.sub_ids_list_name]:
            self.remove_prepayment(sub_id)
    def disable_add(self) -> bool:
        sub_ids_list = st.session_state[self.sub_ids_list_name]
        max_sub_id = max(sub_ids_list, default=None)
        max_installment_number = st.session_state.get(
            self.key_namer("end", max_sub_id),
            default=0
        )
        st.session_state["DISABLE_ADD_PREP"] = self.mortgage_duration - 1 <= max_installment_number
    def render(self):
        result = []
        for sub_id in st.session_state[self.sub_ids_list_name]:
            self.single_prepayment(sub_id)
            result.append(
                (
                    st.session_state[self.key_namer("type", sub_id)],
                    st.session_state[self.key_namer("value", sub_id)],
                    st.session_state[self.key_namer("start", sub_id)],
                    st.session_state[self.key_namer("end", sub_id)]
                )
            )
        return result

class Basic:
    def __init__(self, mortgage_name: str)->None:
        self.mortgage_name = mortgage_name
        self.sis = lambda value, *keys: modules.utils.set_in_state(value, mortgage_name, "settings", *keys)
        self.get = lambda *keys: modules.utils.get_from_state(mortgage_name, "settings", *keys)
    def property_value(self):
        property_value = st.number_input(  # region
            label="Wartość niruchom. [zł]",
            min_value=0,
            value=300_000,
            step=1_000,
            format="%d",
        )# endregion
        self.sis(property_value, "property_value")
    def down_payment(self):
        property_value = self.get("property_value")
        min_value = int(property_value * 0.1)
        max_value = int(property_value * 0.99)
        default = int(property_value * 0.2)
        key = f"down_payment_{self.mortgage_name}"
        ui.utils.input_number_key_trick(key, min_value, max_value, default)
        down_payment = st.number_input(# region
            label="Wkład własny [zł]",
            min_value=min_value,
            max_value=max_value,
            step=1_000,
            format="%d",
            key=key,
        )# endregion
        self.sis(down_payment, "down_payment")
        self.sis(property_value - down_payment, "mortgage_amount")
        self.sis(round(1 - down_payment / property_value, 2), "LTV")
    def annual_interest_rate(self):
        annual_interest_rate = st.number_input(  # region
            label="Oprocentowanie [%]",
            min_value=1.0,
            value=7.00,
            step=0.01,
            format="%.2f",
        ) / 100  # endregion
        self.sis(annual_interest_rate, "annual_intrest_rate")
    def commission_rate(self):
        commission_rate = st.number_input(  # region
            label="Prowizja [p.p.]",
            min_value=0.0,
            value=0.0,
            step=0.1,
            format="%.1f",
        ) / 100  # endregion
        self.sis(commission_rate, "commission_rate")
    def duration_years(self):
        self.duration_years = st.number_input(  # region
            label="Czas trwania [lata]",
            min_value=3,
            max_value=35,
            value=25,
            step=1,
            format="%d"
        )  # endregion
    def duration_rest(self):
        duration_months = st.number_input(  # region
            label="[miesiące]",
            min_value=0,
            max_value=11,
            value=0,
            step=1,
            format="%d",
        )  # endregion
        self.sis(int(self.duration_years * 12) + duration_months, "duration")
    def installment_type(self):
        options = ["Stała", "Malejąca"]
        translate = {"Stała": "fixed", "Malejąca": "decreasing"}
        installment_type = st.selectbox(label="Rodzaj raty", options=options)
        self.sis(translate[installment_type], "installment_type")
    def risk_premium(self):
        risk_premium = st.number_input(  # region
            label="Dodatek za LTV > 80% [p.p.]",
            min_value=0.00,
            value=0.25,
            step=0.01,
            format="%.2f",
        ) / 100  # endregion
        self.sis(risk_premium, "risk_premium")
    def render(self) -> None:
        with st.container(border=True):
            st.subheader("Podstawowe Parametry kredytu")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                self.property_value()
                self.annual_interest_rate()
            with col2:
                self.down_payment()
                self.duration_years()
            with col3:
                st.number_input(
                    "Wartość hipoteki [zł]",
                    value=self.get("property_value")-self.get("down_payment"),
                    disabled=True
                )
                self.duration_rest()
            with col4:
                st.number_input("LTV [%]", value=int(100*self.get("LTV")), disabled=True)
                self.installment_type()
            with col5:
                self.commission_rate()
                self.risk_premium()

class Additional:
    def __init__(self, mortgage_name: str) -> None:
        self.mortgage_name = mortgage_name
        self.sis = lambda value, *keys: modules.utils.set_in_state(value, mortgage_name, "settings", *keys)
        self.get = lambda *keys: modules.utils.get_from_state(mortgage_name, "settings", *keys)
    def prepayments(self):
        helper = PrepaymentHelper(self.mortgage_name)
        prepayments = helper.render()
        helper.disable_add()
        col1, col2, _ = st.columns([1, 2, 2])
        with col1:
            st.button("➕ Dodaj przedpłatę", on_click=helper.add_prepayment, disabled=st.session_state["DISABLE_ADD_PREP"])
        with col2:
            st.button("🗑 Wyczyść wszystkie przedpłaty", on_click=helper.remove_all_prepayments)
        self.sis(prepayments, "prepayments")
    def upfront_costs(self):
        c1, c2, c3 = st.columns(3)
        with c1:
            apprisal = st.number_input(  # region
                label="Wycena [zł]",
                min_value=0,
                value=0,
                step=100,
                format="%d",
            )  # endregion
        with c2:
            annex = st.number_input(  # region
                label="Aneks [zł]",
                min_value=0,
                value=0,
                step=100,
                format="%d",
            )  # endregion
        with c3:
            other = st.number_input(  # region
                label="Pozostałe [zł]",
                min_value=0,
                value=0,
                step=10,
                format="%d",
            )# endregion
        self.sis((apprisal,annex,other), "upfront")
    def discounts(self):
        division = [5, 5, 5, 1]
        discounts = []
        labels = ["Lokalizacja", "Klient banku", "Deklaracja wpływów"]
        cols = st.columns(4)
        cols[0].markdown("**Nazwa**")
        cols[1].markdown("**Zniżka marży [p.p.]**")
        cols[2].markdown("**Zniżka prowizji [p.p.]**")
        cols[3].markdown("**Użyj**")
        for label in labels:
            c0, c1, c2, c3 = st.columns(4)
            with c3:
                disabled=not st.toggle(# region
                    "",
                    value=False,
                    key=f"config_basic_reductions_toggle_{label}_{self.mortgage_name}",
                )# endregion
            with c0:
                ui.utils.static_field(label)
            with c1:
                margin = st.number_input(
                    "",
                    min_value=0.0,
                    step=0.01,
                    key=f"config_basic_reductions_margin_{self.mortgage_name}_{label}",
                    label_visibility="collapsed",
                    disabled=disabled) / 100
            with c2:
                commission = st.number_input(
                    "",
                    min_value=0.0,
                    step=0.1,
                    key=f"config_basic_reductions_commission_{self.mortgage_name}_{label}",
                    label_visibility="collapsed",
                    disabled=disabled) / 100
            discounts.append((margin, commission, not disabled))
        self.sis(discounts, "discounts")
    def products(self):
        division = [5, 5, 5, 5, 5, 1]
        products = []
        product_dict = {
            "Ubezp. start": ("% kwoty kredytu", .01),
            "Ubezp. msc": ("zł/100k/msc salda", 5),
            "Karta kredytowa": ("zł/msc", 10),
            "Konto osobiste": ("zł/msc", 10)
        }
        cols = st.columns(division)
        cols[0].markdown("**Nazwa**")
        cols[1].markdown("**Rodzaj ceny**")
        cols[2].markdown("**Cena**")
        cols[3].markdown("**Zniżka marży [p.p.]**")
        cols[4].markdown("**Zniżka prowizji [p.p.]**")

        for i, label in enumerate(product_dict):
            c0, c1, c2, c3, c4, c5 = st.columns(division)
            with c5:
                use =  st.toggle(#region
                    "",
                    value=False,
                    key=f"config_additional_products_toggle_{label}_{self.mortgage_name}"
                )# endregion
            with c0:
                ui.utils.static_field(label)
            with c1:
                ui.utils.static_field(product_dict[label][0])
            with c2:
                step = product_dict[label][1]
                price = st.number_input(
                    "",
                    min_value=type(step)(0),
                    step=step,
                    key=f"config_additional_products_price_{label}_{self.mortgage_name}",
                    label_visibility="collapsed",
                    disabled=not use)
            with c3:
                margin = st.number_input(
                    "",
                    min_value=0.00,
                    step=0.01,
                    key=f"config_additional_products_margin_{label}_{self.mortgage_name}",
                    label_visibility="collapsed",
                    disabled=not use) / 100
            with c4:
                commission = st.number_input(
                    "",
                    min_value=0.0,
                    step=0.1,
                    key=f"config_additional_products_commission_{label}_{self.mortgage_name}",
                    label_visibility="collapsed",
                    disabled=not use) / 100
            products.append((product_dict[label][0], price, margin, commission, use))
        self.sis(products, "products")
    def render(self) -> None:
        with st.expander("Ustawienia dodatkowe", expanded=False):
            with st.expander("Przedpłaty", expanded=False):
                 self.prepayments()
            with st.expander("Podstawowe Koszty Początkowe", expanded=False):
                self.upfront_costs()
            with st.expander("Podstawowe Zniżki", expanded=False):
                self.discounts()
            with st.expander("Produkty dodatkowe", expanded=False):
                self.products()



