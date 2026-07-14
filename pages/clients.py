# pages/clients.py - Страница клиентов

import streamlit as st
import pandas as pd

def show_clients():
    st.title("👤 Клиенты")
    st.markdown("### Управление клиентами")
    
    # Добавление клиента
    with st.expander("➕ Добавить клиента", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            name = st.text_input("Имя клиента", key="client_name")
        with col2:
            phone = st.text_input("Телефон", key="client_phone")
        with col3:
            st.write("")
            if st.button("➕ Добавить", key="add_client"):
                if name:
                    st.session_state.clients.append({
                        'id': len(st.session_state.clients) + 1,
                        'name': name,
                        'phone': phone
                    })
                    st.success(f"✅ Клиент '{name}' добавлен!")
                    st.rerun()
                else:
                    st.error("Введите имя клиента")
    
    # Отображение списка
    if st.session_state.clients:
        df = pd.DataFrame(st.session_state.clients)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Нет клиентов")
