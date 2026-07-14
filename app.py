# app.py - Строительная смета

import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Строительная смета",
    page_icon="🏗️",
    layout="wide"
)

# Инициализация данных
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.page = "Главная"

# Боковая панель
st.sidebar.title("🏗️ Строительная смета")
st.sidebar.markdown("---")

# Меню навигации
page = st.sidebar.radio(
    "Меню",
    ["Главная", "📋 Смета", "📊 Прайс-лист", "🧾 Материалы", "👤 Клиенты", "🏗️ Объекты", "📁 Архив"]
)

# Отображение выбранной страницы
if page == "Главная":
    st.title("🏗️ Строительная смета")
    st.markdown("### Добро пожаловать!")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Смет", "0")
    with col2:
        st.metric("👤 Клиентов", "0")
    with col3:
        st.metric("🏗️ Объектов", "0")
    
    st.info("ℹ️ Используйте меню слева для навигации")

elif page == "📋 Смета":
    st.title("📋 Создание сметы")
    st.info("🚧 Страница в разработке")

elif page == "📊 Прайс-лист":
    st.title("📊 Прайс-лист")
    st.info("🚧 Страница в разработке")

elif page == "🧾 Материалы":
    st.title("🧾 Материалы")
    st.info("🚧 Страница в разработке")

elif page == "👤 Клиенты":
    st.title("👤 Клиенты")
    st.info("🚧 Страница в разработке")

elif page == "🏗️ Объекты":
    st.title("🏗️ Объекты")
    st.info("🚧 Страница в разработке")

elif page == "📁 Архив":
    st.title("📁 Архив смет")
    st.info("🚧 Страница в разработке")
