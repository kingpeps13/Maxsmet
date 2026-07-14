# pages/materials.py - Смета на материалы

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import save_materials_estimate, load_materials_estimates

def show_materials():
    st.title("🧾 Смета на материалы")
    st.markdown("---")
    
    # --- ИНФОРМАЦИЯ О СМЕТЕ ---
    col1, col2 = st.columns(2)
    with col1:
        materials_name = st.text_input("Название сметы на материалы", 
                                      f"Смета материалов №{len(load_materials_estimates()) + 1}")
    with col2:
        materials_date = st.date_input("Дата", datetime.now())
    
    st.markdown("---")
    
    # --- ДОБАВЛЕНИЕ МАТЕРИАЛА ---
    st.subheader("➕ Добавить материал")
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        name = st.text_input("Наименование материала", key="mat_name")
        container = st.text_input("Тара (упаковка)", placeholder="например: 40 кг, 10 л", key="mat_container")
    
    with col2:
        unit = st.text_input("Ед. изм.", key="mat_unit")
    
    with col3:
        qty = st.number_input("Кол-во", min_value=0.0, step=1.0, key="mat_qty")
    
    with col4:
        price = st.number_input("Цена (руб.)", min_value=0.0, step=10.0, key="mat_price")
    
    if st.button("➕ Добавить материал", key="add_mat"):
        if name and unit and qty > 0 and price > 0:
            if 'estimate_materials' not in st.session_state:
                st.session_state.estimate_materials = []
            
            st.session_state.estimate_materials.append({
                'name': name,
                'container': container,
                'unit': unit,
                'quantity': qty,
                'price': price,
                'cost': qty * price
            })
            st.success(f"✅ Материал '{name}' добавлен!")
            st.rerun()
        else:
            st.error("Заполните все поля")
    
    st.markdown("---")
    
    # --- ОТОБРАЖЕНИЕ МАТЕРИАЛОВ ---
    st.subheader("📄 Смета на материалы")
    
    if 'estimate_materials' in st.session_state and st.session_state.estimate_materials:
        df = pd.DataFrame(st.session_state.estimate_materials)
        df.insert(0, '№', range(1, len(df) + 1))
        
        display_cols = ['№', 'name', 'container', 'unit', 'quantity', 'price', 'cost']
        column_config = {
            '№': '№ п/п',
            'name': 'Наименование материала',
            'container': 'Тара',
            'unit': 'Ед. изм.',
            'quantity': 'Кол-во',
            'price': 'Цена, руб.',
            'cost': 'Сумма, руб.'
        }
        
        st.dataframe(
            df[display_cols],
            column_config=column_config,
            hide_index=True,
            use_container_width=True
        )
        
        # --- ИТОГ ---
        st.markdown("---")
        total_cost = df['cost'].sum()
        st.metric("💰 ИТОГО по материалам", f"{total_cost:,.2f} руб.")
        
        # --- КНОПКИ ---
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Сохранить смету материалов", key="save_materials"):
                if materials_name:
                    materials_data = {
                        'name': materials_name,
                        'date': materials_date.strftime("%Y-%m-%d"),
                        'items': st.session_state.estimate_materials.copy(),
                        'total': total_cost
                    }
                    
                    if save_materials_estimate(materials_data):
                        st.session_state.estimate_materials = []
                        st.success("✅ Смета материалов сохранена в data/materials_estimates.json!")
                        st.rerun()
                    else:
                        st.error("Ошибка сохранения")
                else:
                    st.error("Введите название сметы")
        
        with col2:
            if st.button("🗑️ Очистить материалы", key="clear_materials"):
                st.session_state.estimate_materials = []
                st.rerun()
        
        with col3:
            # ЭКСПОРТ В EXCEL
            if st.button("📊 Экспорт в Excel", key="export_materials_excel"):
                output = pd.ExcelWriter('материалы.xlsx', engine='openpyxl')
                df[display_cols].to_excel(output, sheet_name='Материалы', index=False)
                output.close()
                
                with open('материалы.xlsx', 'rb') as f:
                    st.download_button(
                        label="📥 Скачать Excel",
                        data=f,
                        file_name=f"{materials_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    else:
        st.info("Нет добавленных материалов")
