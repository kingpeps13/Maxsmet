# pages/estimate.py - Страница создания сметы

import streamlit as st
import pandas as pd
from utils.helpers import calculate_cost

def show_estimate():
    st.title("📋 Создание сметы")
    st.markdown("---")
    
    # Настройки сметы
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        estimate_name = st.text_input("Название сметы", 
                                     f"Смета №{len(st.session_state.estimates) + 1}")
    with col2:
        discount = st.number_input("Скидка %", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    with col3:
        vat = st.number_input("НДС %", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
    
    st.markdown("---")
    
    # Добавление работы
    with st.expander("➕ Добавить работу", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Категория", list(st.session_state.price_list.keys()), key="est_cat")
            work_type = st.selectbox("Тип работ", ["Монтажные", "Демонтажные"], key="est_type")
            
            if category and work_type:
                works_dict = st.session_state.price_list[category].get(work_type, {})
                if works_dict:
                    work_name = st.selectbox("Работа", list(works_dict.keys()), key="est_work")
                else:
                    work_name = None
                    st.warning("Нет работ выбранного типа")
        
        with col2:
            if work_name:
                work_info = works_dict[work_name]
                quantity = st.number_input(f"Количество ({work_info['unit']})", 
                                          min_value=0.0, step=0.5, key="est_qty")
                price = work_info['price']
                st.write(f"**Цена за единицу:** {price} руб.")
                
                if quantity > 0:
                    cost_data = calculate_cost(quantity, price, discount, vat)
                    st.success(f"**Стоимость:** {cost_data['total']:.2f} руб.")
                    
                    if st.button("➕ Добавить в смету", key="add_to_estimate"):
                        st.session_state.current_estimate.append({
                            'category': category,
                            'type': work_type,
                            'work': work_name,
                            'unit': work_info['unit'],
                            'quantity': quantity,
                            'price': price,
                            'discount': discount,
                            'vat': vat,
                            'cost': cost_data['total']
                        })
                        st.success(f"✅ Работа '{work_name}' добавлена!")
                        st.rerun()
    
    # Отображение текущей сметы
    st.subheader("📄 Текущая смета")
    
    if st.session_state.current_estimate:
        # Показываем таблицу
        df = pd.DataFrame(st.session_state.current_estimate)
        
        # Выбираем колонки для отображения
        display_cols = ['work', 'quantity', 'unit', 'price', 'discount', 'vat', 'cost']
        column_config = {
            'work': 'Работа',
            'quantity': 'Кол-во',
            'unit': 'Ед.',
            'price': 'Цена',
            'discount': 'Скидка %',
            'vat': 'НДС %',
            'cost': 'Стоимость'
        }
        
        st.dataframe(
            df[display_cols],
            column_config=column_config,
            hide_index=True,
            use_container_width=True
        )
        
        # Итог
        total = sum(item['cost'] for item in st.session_state.current_estimate)
        st.metric("💰 Итого по смете", f"{total:.2f} руб.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Сохранить смету", key="save_estimate"):
                if estimate_name:
                    st.session_state.estimates.append({
                        'name': estimate_name,
                        'date': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                        'items': st.session_state.current_estimate.copy(),
                        'total': total
                    })
                    st.session_state.current_estimate = []
                    st.success("✅ Смета сохранена!")
                    st.rerun()
                else:
                    st.error("Введите название сметы")
        
        with col2:
            if st.button("🗑️ Очистить смету", key="clear_estimate"):
                st.session_state.current_estimate = []
                st.rerun()
    else:
        st.info("Смета пуста. Добавьте работы выше.")
