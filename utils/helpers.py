# utils/helpers.py - Вспомогательные функции

import streamlit as st
from utils.data_manager import load_price_list, load_estimates, load_materials_estimates

def init_session_state():
    """Инициализация всех данных приложения"""
    if 'initialized' in st.session_state:
        return
    
    st.session_state.initialized = True
    
    # Загружаем прайс-лист из файла
    st.session_state.price_list = load_price_list()
    
    # Данные для сметы на работы
    st.session_state.current_estimate = []
    st.session_state.estimates = load_estimates()
    
    # Данные для сметы на материалы
    st.session_state.estimate_materials = []
    st.session_state.materials_estimates = load_materials_estimates()
    
    # Клиенты и объекты
    st.session_state.clients = []
    st.session_state.objects = []

def calculate_cost(quantity, price, discount=0, vat=0):
    """
    ПРАВИЛЬНЫЙ РАСЧЕТ (по закону):
    1. Базовая стоимость = Кол-во × Цена
    2. Скидка = Базовая стоимость × (Скидка % / 100)
    3. Стоимость со скидкой = Базовая стоимость - Скидка
    4. НДС = Стоимость со скидкой × (НДС % / 100)
    5. Итого = Стоимость со скидкой + НДС
    """
    base = quantity * price
    discount_amount = base * (discount / 100)
    after_discount = base - discount_amount
    vat_amount = after_discount * (vat / 100)
    total = after_discount + vat_amount
    
    return {
        'base': base,
        'discount_amount': discount_amount,
        'after_discount': after_discount,
        'vat_amount': vat_amount,
        'total': total
    }
