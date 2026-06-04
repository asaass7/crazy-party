cat > README.md << 'EOF'
# 🎉 Crazy Party - Организация праздников

Веб-приложение для бронирования аниматоров на дни рождения, Новый год и Хэллоуин.

## 🚀 Функционал

- ✅ Регистрация и авторизация пользователей
- ✅ Хэширование паролей (bcrypt)
- ✅ Личный кабинет с редактированием профиля
- ✅ Бронирование аниматоров с выбором даты и времени
- ✅ Просмотр и отмена бронирований
- ✅ Обратная связь и отзывы
- ✅ REST API для услуг и бронирований
- ✅ Адаптивный дизайн
- ✅ Тёмная/светлая тема
- ✅ Анимации при наведении

## 🛠 Технологии

- **Backend:** Python, Flask, Flask-Login, Flask-Bcrypt, Flask-SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Database:** SQLite
- **Templating:** Jinja2

## 📦 Установка и запуск

\`\`\`bash
# Клонировать репозиторий
git clone https://github.com/asaass7/crazy-party.git
cd crazy-party

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
python app.py
\`\`\`

## 📱 Страницы

| Страница | URL |
|----------|-----|
| Главная | `/` |
| Регистрация | `/register` |
| Вход | `/login` |
| Личный кабинет | `/profile` |
| Дни рождения | `/birthday` |
| Новый год | `/newyear` |
| Хэллоуин | `/halloween` |

## 👨‍💻 Автор

**asaass7**

## 📄 Лицензия

MIT
