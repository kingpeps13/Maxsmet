# utils/data_manager.py - Работа с данными

import json
import os
import streamlit as st

# Пути к файлам
PRICE_FILE = 'data/price_list.json'
ESTIMATES_FILE = 'data/estimates.json'
MATERIALS_FILE = 'data/materials_estimates.json'

# ========== ПРАЙС-ЛИСТ ==========

def load_price_list():
    """Загрузка прайс-листа из JSON файла"""
    try:
        if os.path.exists(PRICE_FILE):
            with open(PRICE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            default_data = get_default_price_data()
            save_price_list(default_data)
            return default_data
    except Exception as e:
        st.error(f"Ошибка загрузки прайс-листа: {e}")
        return get_default_price_data()

def save_price_list(data):
    """Сохранение прайс-листа в JSON файл"""
    try:
        os.makedirs(os.path.dirname(PRICE_FILE), exist_ok=True)
        with open(PRICE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Ошибка сохранения прайс-листа: {e}")
        return False

def get_default_price_data():
    """Начальные данные для прайс-листа"""
    return {
        "Монтажные": {
            "Отделка": {
                "Грунтовка стен": {"unit": "м²", "price": 60},
                "Штукатурка стен": {"unit": "м²", "price": 350},
                "Укладка плитки": {"unit": "м²", "price": 750},
                "Укладка ламината": {"unit": "м²", "price": 310}
            },
            "Строительство": {
                "Кладка перегородки": {"unit": "м²", "price": 660},
                "Монтаж ГКЛ": {"unit": "м²", "price": 510},
                "Устройство стяжки": {"unit": "м²", "price": 750}
            },
            "Сантехника": {
                "Установка ванны": {"unit": "шт", "price": 2800},
                "Установка унитаза": {"unit": "шт", "price": 1100},
                "Установка смесителя": {"unit": "шт", "price": 930}
            },
            "Электрика": {
                "Монтаж розетки": {"unit": "шт", "price": 210},
                "Монтаж провода": {"unit": "п.м.", "price": 110},
                "Монтаж светильника": {"unit": "шт", "price": 370}
            },
            "Разное": {
                "Вынос мусора": {"unit": "мешок", "price": 50},
                "Доставка материала": {"unit": "машина", "price": 1250}
            }
        },
        "Демонтажные": {
            "Отделка": {
                "Демонтаж плитки": {"unit": "м²", "price": 150},
                "Разборка ламината": {"unit": "м²", "price": 150},
                "Демонтаж перегородок": {"unit": "м²", "price": 1700}
            },
            "Строительство": {
                "Демонтаж ГКЛ": {"unit": "м²", "price": 150},
                "Разборка стяжки": {"unit": "м²", "price": 350},
                "Демонтаж бетонных конструкций": {"unit": "м²", "price": 1200}
            },
            "Сантехника": {
                "Демонтаж ванны": {"unit": "шт.", "price": 800},
                "Демонтаж унитаза": {"unit": "шт.", "price": 500},
                "Демонтаж смесителя": {"unit": "шт.", "price": 370}
            },
            "Электрика": {
                "Демонтаж проводки": {"unit": "п.м.", "price": 90},
                "Демонтаж люстры": {"unit": "шт", "price": 220},
                "Демонтаж розеток": {"unit": "шт", "price": 90}
            },
            "Разное": {
                "Демонтаж вентиляции": {"unit": "п.м.", "price": 310},
                "Демонтаж коробов": {"unit": "п.м.", "price": 150}
            }
        }
    }

# ========== СМЕТЫ НА РАБОТЫ ==========

def save_estimate(data):
    """Сохранение сметы на работы"""
    try:
        os.makedirs(os.path.dirname(ESTIMATES_FILE), exist_ok=True)
        
        # Загружаем существующие сметы
        estimates = load_estimates()
        estimates.append(data)
        
        with open(ESTIMATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(estimates, f, ensure_ascii=False, indent=2, default=str)
        return True
    except Exception as e:
        st.error(f"Ошибка сохранения сметы: {e}")
        return False

def load_estimates():
    """Загрузка всех смет на работы"""
    try:
        if os.path.exists(ESTIMATES_FILE):
            with open(ESTIMATES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Ошибка загрузки смет: {e}")
        return []

# ========== СМЕТЫ НА МАТЕРИАЛЫ ==========

def save_materials_estimate(data):
    """Сохранение сметы на материалы"""
    try:
        os.makedirs(os.path.dirname(MATERIALS_FILE), exist_ok=True)
        
        estimates = load_materials_estimates()
        estimates.append(data)
        
        with open(MATERIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(estimates, f, ensure_ascii=False, indent=2, default=str)
        return True
    except Exception as e:
        st.error(f"Ошибка сохранения сметы материалов: {e}")
        return False

def load_materials_estimates():
    """Загрузка всех смет на материалы"""
    try:
        if os.path.exists(MATERIALS_FILE):
            with open(MATERIALS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Ошибка загрузки смет материалов: {e}")
        return []

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def get_categories():
    return ["Отделка", "Строительство", "Сантехника", "Электрика", "Разное"]

def get_work_types():
    return ["Монтажные", "Демонтажные"]

def add_work(work_type, category, work_name, unit, price):
    """Добавить новую работу"""
    data = load_price_list()
    
    if work_type not in data:
        data[work_type] = {}
    if category not in data[work_type]:
        data[work_type][category] = {}
    
    data[work_type][category][work_name] = {
        'unit': unit,
        'price': price
    }
    
    return save_price_list(data)

def delete_work(work_type, category, work_name):
    """Удалить работу"""
    data = load_price_list()
    
    if work_type in data and category in data[work_type]:
        if work_name in data[work_type][category]:
            del data[work_type][category][work_name]
            return save_price_list(data)
    return False

def update_work(work_type, category, work_name, unit, price):
    """Обновить работу"""
    data = load_price_list()
    
    if work_type in data and category in data[work_type]:
        if work_name in data[work_type][category]:
            data[work_type][category][work_name] = {
                'unit': unit,
                'price': price
            }
            return save_price_list(data)
    return False
