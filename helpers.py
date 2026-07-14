# utils/helpers.py - Общие функции и данные

import streamlit as st

def init_session_state():
    """Инициализация всех данных приложения"""
    if 'initialized' in st.session_state:
        return
    
    st.session_state.initialized = True
    
    # Прайс-лист
    st.session_state.price_list = {
        'Потолок': {
            'Монтажные': {
                'Грунтовка потолка': {'unit': 'м²', 'price': 60},
                'Монтаж ГКЛ 1 уровень': {'unit': 'м²', 'price': 700},
            },
            'Демонтажные': {
                'Демонтаж реечного потолка': {'unit': 'м²', 'price': 150},
                'Демонтаж клеевой плитки': {'unit': 'м²', 'price': 65},
            }
        },
        'Стены': {
            'Монтажные': {
                'Штукатурка стен': {'unit': 'м²', 'price': 350},
                'Монтаж ГКЛ': {'unit': 'м²', 'price': 510},
            },
            'Демонтажные': {
                'Демонтаж плитки': {'unit': 'м²', 'price': 150},
                'Демонтаж перегородок': {'unit': 'м²', 'price': 1700},
            }
        },
        'Пол': {
            'Монтажные': {
                'Укладка ламината': {'unit': 'м²', 'price': 310},
                'Укладка плитки': {'unit': 'м²', 'price': 750},
            },
            'Демонтажные': {
                'Разборка ламината': {'unit': 'м²', 'price': 150},
                'Демонтаж плитки': {'unit': 'м²', 'price': 150},
            }
        },
        'Сантехника': {
            'Монтажные': {
                'Установка ванны': {'unit': 'шт', 'price': 2800},
                'Установка унитаза': {'unit': 'шт', 'price': 1100},
            },
            'Демонтажные': {
                'Демонтаж ванны': {'unit': 'шт.', 'price': 800},
                'Демонтаж унитаза': {'unit': 'шт.', 'price': 500},
            }
        },
        'Электрика': {
            'Монтажные': {
                'Монтаж розетки': {'unit': 'шт', 'price': 210},
                'Монтаж провода': {'unit': 'п.м.', 'price': 110},
            },
            'Демонтажные': {
                'Демонтаж проводки': {'unit': 'п.м.', 'price': 90},
                'Демонтаж люстры': {'unit': 'шт', 'price': 220},
            }
        },
        'Разное': {
            'Монтажные': {
                'Вынос мусора': {'unit': 'мешок', 'price': 50},
                'Доставка ГАЗель': {'unit': 'машина', 'price': 1250},
            },
            'Демонтажные': {
                'Демонтаж вентиляции': {'unit': 'п.м.', 'price': 310},
            }
        }
    }
    
    # Данные для сметы
    st.session_state.current_estimate = []
    st.session_state.estimates = []
    st.session_state.clients = []
    st.session_state.objects = []

def calculate_cost(quantity, price, discount=0, vat=0):
    """Расчет стоимости с учетом скидки и НДС"""
    base = quantity * price
    discount_amount = base * (discount / 100)
    after_discount = base - discount_amount
    vat_amount = after_discount * (vat / 100)
    return {
        'base': base,
        'discount_amount': discount_amount,
        'after_discount': after_discount,
        'vat_amount': vat_amount,
        'total': after_discount + vat_amount
    }
