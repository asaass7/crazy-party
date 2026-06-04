from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, date, time
import re

# Импортируем db из models
from models import db, User, Booking, Feedback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crazy-party-secret-key-2026-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создание таблиц БД
with app.app_context():
    db.create_all()
    print("✅ База данных создана!")

# Счётчик посещений через сессию
@app.before_request
def count_visits():
    if 'visit_count' in session:
        session['visit_count'] += 1
    else:
        session['visit_count'] = 1

# Контекстный процессор для передачи переменных во все шаблоны
@app.context_processor
def inject_globals():
    return {
        'visit_count': session.get('visit_count', 1),
        'current_year': datetime.now().year,
        'now': date.today().isoformat()
    }

# ========== ОСНОВНЫЕ МАРШРУТЫ ==========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Валидация
        errors = {}
        
        if not username or len(username) < 2:
            errors['username'] = 'Имя должно содержать минимум 2 символа'
        
        if not email or '@' not in email or '.' not in email:
            errors['email'] = 'Введите корректный email'
        
        if not phone or len(re.sub(r'\D', '', phone)) < 10:
            errors['phone'] = 'Введите корректный номер телефона'
        
        if not password or len(password) < 6:
            errors['password'] = 'Пароль должен содержать минимум 6 символов'
        
        if password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают'
        
        # Проверка уникальности
        if User.query.filter_by(username=username).first():
            errors['username'] = 'Это имя уже занято'
        
        if User.query.filter_by(email=email).first():
            errors['email'] = 'Этот email уже зарегистрирован'
        
        if errors:
            for key, msg in errors.items():
                flash(msg, 'error')
            return render_template('register.html', form_data=request.form)
        
        # Создание пользователя
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, phone=phone, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Регистрация успешна! Добро пожаловать, {username}!', 'success')
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'С возвращением, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        phone = request.form.get('phone', '').strip()
        
        errors = {}
        
        if not username or len(username) < 2:
            errors['username'] = 'Имя должно содержать минимум 2 символа'
        
        if not phone or len(re.sub(r'\D', '', phone)) < 10:
            errors['phone'] = 'Введите корректный номер телефона'
        
        # Проверка уникальности имени
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != current_user.id:
            errors['username'] = 'Это имя уже занято'
        
        if errors:
            for key, msg in errors.items():
                flash(msg, 'error')
        else:
            current_user.username = username
            current_user.phone = phone
            db.session.commit()
            flash('Профиль обновлён!', 'success')
    
    # Получаем бронирования пользователя
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    
    return render_template('profile.html', bookings=bookings)

# ========== УСЛУГИ И БРОНИРОВАНИЕ ==========

@app.route('/birthday')
def birthday():
    animators = [
        {'id': 1, 'name': 'Иван Иванов', 'desc': 'Интерактивный квест с множеством активных игр'},
        {'id': 2, 'name': 'Василий Вакуленко', 'desc': 'Весёлое времяпрепровождение с пользой для детей'},
        {'id': 3, 'name': 'Мария Мариева', 'desc': 'Творческий незабываемый вечер'}
    ]
    return render_template('birthday.html', animators=animators, service_type='birthday')

@app.route('/newyear')
def newyear():
    animators = [
        {'id': 1, 'name': 'Константин Морковкин', 'desc': 'Уютная посиделка, куча подарков и отличная атмосфера'},
        {'id': 2, 'name': 'Прохор Шаляпов', 'desc': 'Тур по самым культовым новогодним местам мира'},
        {'id': 3, 'name': 'Антон Максименко', 'desc': 'Вкусный ужин под живую музыку'}
    ]
    return render_template('newyear.html', animators=animators, service_type='newyear')

@app.route('/halloween')
def halloween():
    animators = [
        {'id': 1, 'name': 'Джон Райкард', 'desc': 'Занимательный и жуткий квест'},
        {'id': 2, 'name': 'Франсуа Летескье', 'desc': 'Праздник в средневековом стиле'},
        {'id': 3, 'name': 'Криштиану Роналду', 'desc': 'Самая жуткая ночь в древнем замке'}
    ]
    return render_template('halloween.html', animators=animators, service_type='halloween')

@app.route('/booking/<service_type>/<animator_name>', methods=['GET', 'POST'])
@login_required
def booking(service_type, animator_name):
    if request.method == 'POST':
        booking_date = request.form.get('booking_date')
        booking_time = request.form.get('booking_time')
        
        try:
            # Парсинг даты и времени
            date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
            time_obj = datetime.strptime(booking_time, '%H:%M').time()
            
            # Проверка: дата не может быть в прошлом
            if date_obj < date.today():
                flash('Дата не может быть в прошлом', 'error')
                return render_template('booking.html', service_type=service_type, animator_name=animator_name)
            
            # Создание бронирования
            booking = Booking(
                user_id=current_user.id,
                animator_name=animator_name,
                service_type=service_type,
                booking_date=date_obj,
                booking_time=time_obj,
                status='confirmed'
            )
            db.session.add(booking)
            db.session.commit()
            
            flash(f'Аниматор {animator_name} успешно забронирован на {booking_date} в {booking_time}!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            flash('Ошибка при бронировании. Проверьте корректность данных.', 'error')
            return render_template('booking.html', service_type=service_type, animator_name=animator_name)
    
    return render_template('booking.html', service_type=service_type, animator_name=animator_name)

@app.route('/cancel_booking/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        flash('У вас нет прав для отмены этого бронирования', 'error')
        return redirect(url_for('profile'))
    
    booking.status = 'cancelled'
    db.session.commit()
    flash(f'Бронирование аниматора {booking.animator_name} отменено', 'info')
    return redirect(url_for('profile'))

# ========== ОБРАТНАЯ СВЯЗЬ ==========

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        errors = {}
        
        if not name:
            errors['name'] = 'Введите ваше имя'
        if not email or '@' not in email:
            errors['email'] = 'Введите корректный email'
        if not message or len(message) < 10:
            errors['message'] = 'Сообщение должно содержать минимум 10 символов'
        
        if errors:
            for key, msg in errors.items():
                flash(msg, 'error')
            return render_template('feedback.html', form_data=request.form)
        
        # Сохранение отзыва
        feedback = Feedback(
            user_id=current_user.id if current_user.is_authenticated else None,
            name=name,
            email=email,
            message=message
        )
        db.session.add(feedback)
        db.session.commit()
        
        flash('Спасибо за ваш отзыв!', 'success')
        return redirect(url_for('index'))
    
    return render_template('feedback.html')

# ========== REST API ==========

@app.route('/api/services', methods=['GET'])
def api_get_services():
    """GET /api/services - получение списка услуг"""
    services = [
        {'id': 'birthday', 'name': 'Дни рождения', 'price': 'от 5000 ₽'},
        {'id': 'newyear', 'name': 'Новый год', 'price': 'от 8000 ₽'},
        {'id': 'halloween', 'name': 'Хэллоуин', 'price': 'от 7000 ₽'}
    ]
    return jsonify({'success': True, 'services': services})

@app.route('/api/bookings', methods=['GET'])
@login_required
def api_get_bookings():
    """GET /api/bookings - получение бронирований текущего пользователя"""
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    bookings_data = [{
        'id': b.id,
        'animator_name': b.animator_name,
        'service_type': b.service_type,
        'booking_date': b.booking_date.strftime('%Y-%m-%d'),
        'booking_time': b.booking_time.strftime('%H:%M'),
        'status': b.status
    } for b in bookings]
    return jsonify({'success': True, 'bookings': bookings_data})

@app.route('/api/bookings', methods=['POST'])
@login_required
def api_create_booking():
    """POST /api/bookings - создание бронирования через API"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    
    required_fields = ['animator_name', 'service_type', 'booking_date', 'booking_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
    
    try:
        date_obj = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
        time_obj = datetime.strptime(data['booking_time'], '%H:%M').time()
        
        if date_obj < date.today():
            return jsonify({'success': False, 'error': 'Date cannot be in the past'}), 400
        
        booking = Booking(
            user_id=current_user.id,
            animator_name=data['animator_name'],
            service_type=data['service_type'],
            booking_date=date_obj,
            booking_time=time_obj,
            status='confirmed'
        )
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({'success': True, 'booking_id': booking.id}), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ========== ЗАПУСК ==========

if __name__ == '__main__':
    app.run(debug=True)# Version 1.0.0
