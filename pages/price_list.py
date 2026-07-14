# pages/price_list.py - Прайс-лист с управлением

# pages/price_list.py
import streamlit as st
import pandas as pd
from utils.data_manager import load_price_list, save_price_list, get_categories, get_work_types

def show_price_list():
    st.title("📊 Прайс-лист работ")
    st.markdown("### Управление ценами и работами")
    st.markdown("---")
    
    # Загружаем актуальные данные
    st.session_state.price_list = load_price_list()
    
    # Выбор типа работ
    work_types = get_work_types()
    selected_work_type = st.selectbox("Тип работ", work_types)
    
    # Выбор категории
    categories = get_categories()
    selected_category = st.selectbox("Категория", categories)
    
    if not selected_work_type or not selected_category:
        return
    
    # --- ОТОБРАЖЕНИЕ РАБОТ ---
    st.subheader(f"📋 {selected_work_type} - {selected_category}")
    
    # Получаем список работ
    works = st.session_state.price_list.get(selected_work_type, {}).get(selected_category, {})
    
    if works:
        # Создаем DataFrame для отображения
        data = []
        for work_name, info in works.items():
            data.append({
                'Работа': work_name,
                'Ед. изм.': info['unit'],
                'Цена (руб.)': info['price']
            })
        
        df = pd.DataFrame(data)
        
        # Редактируемая таблица
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Работа": st.column_config.TextColumn("Работа", required=True),
                "Ед. изм.": st.column_config.TextColumn("Ед. изм.", required=True),
                "Цена (руб.)": st.column_config.NumberColumn("Цена", format="%.2f"),
            }
        )
        
        # Кнопка сохранения изменений
        if st.button("💾 Сохранить изменения", key="save_changes"):
            # Обновляем данные
            updated_works = {}
            for _, row in edited_df.iterrows():
                if row['Работа'] and row['Ед. изм.']:
                    updated_works[row['Работа']] = {
                        'unit': row['Ед. изм.'],
                        'price': row['Цена (руб.)']
                    }
            
            # Сохраняем в JSON
            price_list = load_price_list()
            price_list[selected_work_type][selected_category] = updated_works
            if save_price_list(price_list):
                st.session_state.price_list = price_list
                st.success("✅ Изменения сохранены!")
                st.rerun()
            else:
                st.error("Ошибка сохранения")
        
        # Удаление работы
        st.markdown("---")
        st.subheader("🗑️ Удалить работу")
        
        work_to_delete = st.selectbox("Выберите работу для удаления", list(works.keys()))
        if st.button("🗑️ Удалить", key="delete_work"):
            if delete_work(selected_work_type, selected_category, work_to_delete):
                st.session_state.price_list = load_price_list()
                st.success(f"✅ Работа '{work_to_delete}' удалена!")
                st.rerun()
            else:
                st.error("Ошибка удаления")
    
    else:
        st.info("Нет работ в этой категории")
    
    # --- ДОБАВЛЕНИЕ НОВОЙ РАБОТЫ ---
    st.markdown("---")
    st.subheader("➕ Добавить новую работу")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        new_name = st.text_input("Название работы", key="new_work_name")
    with col2:
        new_unit = st.text_input("Ед. изм.", key="new_work_unit")
    with col3:
        new_price = st.number_input("Цена (руб.)", min_value=0.0, step=10.0, key="new_work_price")
    
    if st.button("➕ Добавить работу", key="add_work_btn"):
        if new_name and new_unit and new_price > 0:
            if add_work(selected_work_type, selected_category, new_name, new_unit, new_price):
                st.session_state.price_list = load_price_list()
                st.success(f"✅ Работа '{new_name}' добавлена!")
                st.rerun()
            else:
                st.error("Ошибка добавления работы")
        else:
            st.error("Заполните все поля!")
    
    # --- ОТОБРАЖЕНИЕ ВСЕХ КАТЕГОРИЙ ---
    st.markdown("---")
    with st.expander("📊 Показать все категории"):
        st.subheader("Статистика по категориям")
        
        stats = []
        for work_type in get_work_types():
            for category in get_categories():
                count = len(st.session_state.price_list.get(work_type, {}).get(category, {}))
                stats.append({
                    'Тип работ': work_type,
                    'Категория': category,
                    'Кол-во работ': count
                })
        
        stats_df = pd.DataFrame(stats)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
