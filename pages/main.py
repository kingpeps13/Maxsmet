# pages/main.py - Главная страница

import streamlit as st

def show_main():
    st.title("🏗️ Строительная смета")
    st.markdown("### Добро пожаловать!")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Смет", len(st.session_state.get('estimates', [])))
    with col2:
        st.metric("📊 Работ в прайсе", 
                 sum(len(works) for cat in st.session_state.price_list.values() 
                    for works in cat.values()))
    with col3:
        st.metric("👤 Клиентов", len(st.session_state.get('clients', [])))
    with col4:
        st.metric("🏗️ Объектов", len(st.session_state.get('objects', [])))
    
    st.markdown("---")
    st.info("💡 Используйте меню слева для навигации по приложению")
