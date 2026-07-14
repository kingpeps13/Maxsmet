# app.py - Главный файл, управляет навигацией

import streamlit as st
from pages.main import show_main
from pages.price_list import show_price_list
from pages.estimate import show_estimate
from pages.materials import show_materials
from pages.clients import show_clients
from pages.objects import show_objects
from utils.helpers import init_session_state

# Настройка страницы
st.set_page_config(
    page_title="Строительная смета",
    page_icon="🏗️",
    layout="wide"
)

# Инициализация данных
init_session_state()

# Боковая панель
st.sidebar.title("🏗️ Строительная смета")
st.sidebar.markdown("---")

# Навигация
page = st.sidebar.radio(
    "Меню",
    ["Главная", "📋 Смета", "📊 Прайс-лист", "🧾 Материалы", "👤 Клиенты", "🏗️ Объекты"]
)

# Отображение выбранной страницы
if page == "Главная":
    show_main()
elif page == "📊 Прайс-лист":
    show_price_list()
elif page == "📋 Смета":
    show_estimate()
elif page == "🧾 Материалы":
    show_materials()
elif page == "👤 Клиенты":
    show_clients()
elif page == "🏗️ Объекты":
    show_objects()
