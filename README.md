# 📌 Bulletin Board

Веб-приложение "Доска объявлений", разработанное с использованием Django. Позволяет пользователям публиковать, просматривать и управлять объявлениями в различных категориях.

## 🚀 Начало работы

### 📦 Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/BuryatisLesa/Bulletin-board.git
   cd Bulletin-board
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv env
   source env/bin/activate  # Для Windows: env\Scripts\activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Примените миграции и запустите сервер:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

Приложение будет доступно по адресу: `http://127.0.0.1:8000/`

## 🧩 Функциональность

- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление объявлений
- Категоризация объявлений
- Загрузка изображений для объявлений
- Поиск и фильтрация объявлений

## 🗂️ Структура проекта

```plaintext
Bulletin-board/
├── BulletinBoard/        # Основная конфигурация проекта Django
├── accounts/             # Приложение для управления пользователями
├── board/                # Приложение для управления объявлениями
├── media/                # Загруженные пользователями файлы
├── static/               # Статические файлы (CSS, JS, изображения)
├── templates/            # HTML-шаблоны
├── db.sqlite3            # База данных SQLite
├── manage.py             # Утилита управления Django
└── requirements.txt      # Список зависимостей Python
```

## 🛠️ Используемые технологии

- Python 3.x
- Django
- SQLite
- HTML, CSS, JavaScript

## 👤 Автор

**Константин Санданов**  
📧 [kostyansandanov@gmail.com](mailto:kostyansandanov@gmail.com)
