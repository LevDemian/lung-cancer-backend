# 📘 Инструкция по запуску проекта

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Запуск Flask-сервера

```bash
py backend/app.py
```

Перейдите на [http://localhost:5000](http://localhost:5000)

## 3. Сборка и запуск через Docker

```bash
docker build -t lung-ai .
docker run -p 5000:5000 lung-ai
```

## 4. Загрузка снимка

Через файл `frontend/upload.html` или напрямую через POST на `/upload`

## 5. Анализ изображения

POST на `/analyze` с телом:

```json
{
  "filename": "example.png"
}
```

## 6. Экспорт данных

GET-запрос на `/export` сохраняет CSV-файл в `data/csv/`

## 7. Графики рисков

Открыть `frontend/visualization.html` в браузере или встроить в Tilda как iframe