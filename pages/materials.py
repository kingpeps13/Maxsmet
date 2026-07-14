# pages/materials.py - Страница материалов

import streamlit as st
import pandas as pd

def show_materials():
    st.title("🧾 Материалы")
    st.markdown("### Управление материалами в смете")
    
    # Инициализация материалов
    if 'estimate_materials' not in st.session_state:
        st.session_state.estimate_materials = []
    
    # Добавление материала
    with st.expander("➕ Добавить материал", expanded=True):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            name = st.text_input("Наименование материала", key="mat_name")
        with col2:
            unit = st.text_input("Ед. изм.", key="mat_unit")
        with col3:
            qty = st.number_input("Количество", min_value=0.0, step=1.0, key="mat_qty")
        with col4:
            price = st.number_input("Цена", min_value=0.0, step=10.0, key="mat_price")
        
        if st.button("➕ Добавить материал", key="add_mat"):
            if name and unit and qty > 0 and price > 0:
                st.session_state.estimate_materials.append({
                    'name': name,
                    'unit': unit,
                    'quantity': qty,
                    'price': price,
                    'cost': qty * price
                })
                st.success(f"✅ Материал '{name}' добавлен!")
                st.rerun()
            else:
                st.error("Заполните все поля")
    
    # Отображение материалов
    if st.session_state.estimate_materials:
        df = pd.DataFrame(st.session_state.estimate_materials)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        total = sum(m['cost'] for m in st.session_state.estimate_materials)
        st.metric("💰 Итого материалы", f"{total:.2f} руб.")
        
        if st.button("🗑️ Очистить материалы"):
            st.session_state.estimate_materials = []
            st.rerun()
    else:
        st.info("Нет добавленных материалов")
