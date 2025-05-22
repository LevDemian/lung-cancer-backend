import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Настройка страницы
st.set_page_config(page_title="Диагностика рака лёгких", layout="wide")

# Стиль (бело-голубая тема)
st.markdown("""
    <style>
    .main { background-color: #f0f9ff; }
    .sidebar .sidebar-content { background-color: #e6f2ff; }
    h1 { color: #0068c9; }
    </style>
    """, unsafe_allow_html=True)

# Заголовок
st.title("Медицинская диагностика рака лёгких")

# Форма ввода данных
with st.form("patient_data"):
    st.header("Данные пациента")
    col1, col2 = st.columns(2)
    with col1:
        last_name = st.text_input("Фамилия")
        first_name = st.text_input("Имя")
        middle_name = st.text_input("Отчество")
    with col2:
        birth_date = st.date_input("Дата рождения", datetime.now())
        snils = st.text_input("СНИЛС")
    anamnesis = st.text_area("Анамнез")
    submit_patient = st.form_submit_button("Сохранить данные")

# Загрузка изображений
st.header("Анализ снимков")
uploaded_file = st.file_uploader("Загрузите МРТ/КТ/рентген", type=["jpg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Загруженный снимок", width=300)
    
    # Здесь будет вызов ML-модели
    st.warning("Здесь будет анализ модели (аномалии + вероятность рака)")

# Сохранение в CSV
if submit_patient and last_name and first_name:
    data = {
        "Фамилия": [last_name],
        "Имя": [first_name],
        "Отчество": [middle_name],
        "Дата рождения": [birth_date],
        "СНИЛС": [snils],
        "Анамнез": [anamnesis],
        "Дата записи": [datetime.now()]
    }
    df = pd.DataFrame(data)
    
    if not os.path.exists("patients.csv"):
        df.to_csv("patients.csv", index=False)
    else:
        existing_df = pd.read_csv("patients.csv")
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv("patients.csv", index=False)
    
    st.success("Данные пациента сохранены!")
