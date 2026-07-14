# utils/data_manager.py - Работа с данными прайс-листа

import json
import os
import streamlit as st

# Путь к файлу с данными
DATA_FILE = 'data/price_list.json'

def load_price_list():
    """Загрузка прайс-листа из JSON файла"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Если файла нет - создаем с начальными данными
            default_data = get_default_data()
            save_price_list(default_data)
            return default_data
    except Exception as e:
        st.error(f"Ошибка загрузки данных: {e}")
        return get_default_data()

def save_price_list(data):
    """Сохранение прайс-листа в JSON файл"""
    try:
        # Создаем папку если её нет
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Ошибка сохранения данных: {e}")
        return False

def get_default_data():
    """Начальные данные для прайс-листа"""
    return {
        "Монтажные": {
            "Отделка": {
                "Грунтовка стен": {"unit": "м²", "price": 60},
                "Штукатурка стен": {"unit": "м²", "price": 350},
                "Укладка плитки": {"unit": "м²", "price": 750}
            },
            "Строительство": {
                "Кладка перегородки": {"unit": "м²", "price": 660},
                "Монтаж ГКЛ": {"unit": "м²", "price": 510}
            },
            "Сантехника": {
                "Установка ванны": {"unit": "шт", "price": 2800}
            },
            "Электрика": {
                "Монтаж розетки": {"unit": "шт", "price": 210}
            },
            "Разное": {
                "Вынос мусора": {"unit": "мешок", "price": 50}
            }
        },
        "Демонтажные": {
            "Отделка": {
                "Демонтаж плитки": {"unit": "м²", "price": 150},
                "Разборка ламината": {"unit": "м²", "price": 150}
            },
            "Строительство": {
                "Демонтаж ГКЛ": {"unit": "м²", "price": 150}
            },
            "Сантехника": {
                "Демонтаж ванны": {"unit": "шт.", "price": 800}
            },
            "Электрика": {
                "Демонтаж проводки": {"unit": "п.м.", "price": 90}
            },
            "Разное": {
                "Демонтаж вентиляции": {"unit": "п.м.", "price": 310}
            }
        }
    }

def get_categories():
    """Получить список всех категорий"""
    return ["Отделка", "Строительство", "Сантехника", "Электрика", "Разное"]

def get_work_types():
    """Получить список типов работ"""
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
