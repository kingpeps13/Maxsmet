# pages/price_list.py - Страница прайс-листа

import streamlit as st
import pandas as pd

def show_price_list():
    st.title("📊 Прайс-лист работ")
    st.markdown("### Управление ценами и работами")
    st.markdown("---")
    
    # Выбор категории
    categories = list(st.session_state.price_list.keys())
    selected_category = st.selectbox("Выберите категорию", categories)
    
    if not selected_category:
        return
    
    category_data = st.session_state.price_list[selected_category]
    
    # Две вкладки
    tab1, tab2 = st.tabs(["🔧 Монтажные", "🔨 Демонтажные"])
    
    with tab1:
        show_work_table(selected_category, 'Монтажные')
    
    with tab2:
        show_work_table(selected_category, 'Демонтажные')
    
    # Добавление новой работы
    st.markdown("---")
    st.subheader("➕ Добавить новую работу")
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        new_name = st.text_input("Название работы", key="new_name")
    with col2:
        new_unit = st.text_input("Ед. изм.", key="new_unit")
    with col3:
        new_price = st.number_input("Цена", min_value=0.0, step=10.0, key="new_price")
    with col4:
        new_type = st.selectbox("Тип", ["Монтажные", "Демонтажные"], key="new_type")
    
    if st.button("➕ Добавить работу", key="add_work_btn"):
        if new_name and new_unit and new_price > 0:
            if new_type not in st.session_state.price_list[selected_category]:
                st.session_state.price_list[selected_category][new_type] = {}
            
            st.session_state.price_list[selected_category][new_type][new_name] = {
                'unit': new_unit,
                'price': new_price
            }
            st.success(f"✅ Работа '{new_name}' добавлена!")
            st.rerun()
        else:
            st.error("Заполните все поля!")

def show_work_table(category, work_type):
    """Отображение таблицы работ определенного типа"""
    st.subheader(work_type)
    
    works = st.session_state.price_list[category].get(work_type, {})
    
    if not works:
        st.info(f"Нет {work_type.lower()} работ в этой категории")
        return
    
    # Создаем DataFrame
    data = []
    for work, info in works.items():
        data.append({
            'Работа': work,
            'Ед. изм.': info['unit'],
            'Цена (руб.)': info['price']
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
