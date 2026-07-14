# pages/objects.py - Страница объектов

import streamlit as st
import pandas as pd

def show_objects():
    st.title("🏗️ Объекты")
    st.markdown("### Управление объектами")
    
    # Добавление объекта
    with st.expander("➕ Добавить объект", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            name = st.text_input("Название объекта", key="obj_name")
        with col2:
            address = st.text_input("Адрес", key="obj_address")
        with col3:
            st.write("")
            if st.button("➕ Добавить", key="add_obj"):
                if name:
                    st.session_state.objects.append({
                        'id': len(st.session_state.objects) + 1,
                        'name': name,
                        'address': address
                    })
                    st.success(f"✅ Объект '{name}' добавлен!")
                    st.rerun()
                else:
                    st.error("Введите название объекта")
    
    # Отображение списка
    if st.session_state.objects:
        df = pd.DataFrame(st.session_state.objects)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Нет объектов")
