from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from datetime import datetime, time, date, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import secrets
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Обязательно поменять

DATABASE = 'school_attendance.db'

# Получаем подключение к базе данных
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Закрытие подключения к базе данных
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Запрос данных из базы
def query_db(query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

# Выполнение запроса в базе данных
def execute_db(query, args=()):
    with app.app_context():
        conn = get_db()
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        cur.close()

# Инициализация базы данных
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Команда для инициализации базы данных
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

# Получаем студентов по классу
def get_students_by_class(class_name):
    return query_db('SELECT id, first_name, last_name FROM students WHERE class_name = ? ORDER BY last_name, first_name', [class_name])

# Получаем посещаемость для текущего дня
def get_attendance_for_today(student_ids):
    today = datetime.now().date()
    attendance = {}
    if student_ids:
        rows = query_db('SELECT student_id, status, reason, late_time FROM attendance WHERE student_id IN ({}) AND date = ?'.format(','.join('?' * len(student_ids))), student_ids + [today])
        for row in rows:
            attendance[row['student_id']] = dict(row)
    return attendance

# Функция для очистки посещаемости за предыдущий день
def clear_previous_day_attendance():
    with app.app_context():
        yesterday = date.today() - timedelta(days=1)
        deleted_count = get_db().execute('DELETE FROM attendance WHERE date = ?', [yesterday]).rowcount
        get_db().commit()
        print(f'Очищено {deleted_count} записей посещаемости за {yesterday}.')

# Планировщик задач для очистки базы данных ежедневно в полночь
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_previous_day_attendance, 'cron', hour=0, minute=0)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

# Генерация случайного пароля
def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

# Хеширование пароля
def hash_password(password):
    return generate_password_hash(password)

# Проверка хешированного пароля
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

# Главная страница (логин)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = query_db('SELECT id, hashed_password, class_name, shift FROM class_monitors WHERE login = ?', [login], one=True)

        if user and verify_password(user['hashed_password'], password):
            now = datetime.now().time()
            start_time_1 = time(7, 30)
            end_time_1 = time(23, 50)  #  Временный доступ, нужно изменить на 13:30
            start_time_2 = time(12, 30)
            end_time_2 = time(18, 30)

            shift = None
            if login[-1].isdigit():
                shift = int(login[-1])
            elif login[0].isdigit():
                shift = int(login[0])

            if user['shift'] == 1 and start_time_1 <= now <= end_time_1 and shift == 1:
                session['user_id'] = user['id']
                session['class_name'] = user['class_name']
                session['shift'] = user['shift']
                return redirect(url_for('attendance_table'))
            elif user['shift'] == 2 and start_time_2 <= now <= end_time_2 and shift == 2:
                session['user_id'] = user['id']
                session['class_name'] = user['class_name']
                session['shift'] = user['shift']
                return redirect(url_for('attendance_table'))
            else:
                return render_template('login_monitor.html', error='Доступ разрешен только в указанное время для вашей смены.')
        else:
            return render_template('login_monitor.html', error='Неверный логин или пароль.')
    return render_template('login_monitor.html')

# Таблица посещаемости
@app.route('/attendance', methods=['GET', 'POST'])
def attendance_table():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    class_name = session.get('class_name')
    students = get_students_by_class(class_name)
    student_ids = [student['id'] for student in students]
    today_attendance = get_attendance_for_today(student_ids)
    today = datetime.now().date()

    if request.method == 'POST':
        # Обработка данных для существующих и новых учеников - без изменений
        pass

    today_str = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().time()
    start_time_1 = time(7, 30)
    end_time_1 = time(23, 50) # Временный доступ, нужно изменить на 13:30
    start_time_2 = time(12, 30)
    end_time_2 = time(18, 30)
    access_start_str = ""
    access_end_str = ""
    shift_start_str = ""
    shift_end_str = ""

    if session.get('shift') == 1:
        access_start_str = start_time_1.strftime('%H:%M')
        access_end_str = end_time_1.strftime('%H:%M')
        shift_start_str = start_time_1.strftime('%H:%M')
        shift_end_str = end_time_1.strftime('%H:%M')
    elif session.get('shift') == 2:
        access_start_str = start_time_2.strftime('%H:%M')
        access_end_str = end_time_2.strftime('%H:%M')
        shift_start_str = start_time_2.strftime('%H:%M')
        shift_end_str = end_time_2.strftime('%H:%M')
    else:
        access_start_str = "Нет доступа"
        access_end_str = "Нет доступа"

    return render_template('attendance_table.html', students=students, attendance=today_attendance,
                           today=today_str, class_name=class_name,
                           access_start=access_start_str, access_end=access_end_str,
                           shift_start=shift_start_str, shift_end=shift_end_str)

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('class_name', None)
    session.pop('shift', None)
    return redirect(url_for('login'))

# Функция для добавления администратора (по умолчанию)
def add_admin_user():
    with app.app_context():
        db = get_db()
        password = '1234' # Пароль был заменен на '9v12'
        hashed_password = generate_password_hash(password)
        login = 'admin1'
        class_name = 'admin_class'
        shift = 1  # Или 2

        try:
            db.execute("INSERT INTO class_monitors (login, hashed_password, class_name, shift) VALUES (?, ?, ?, ?)",
                       (login, hashed_password, class_name, shift))
            db.commit()
            print(f"Пользователь '{login}' успешно добавлен.")
        except sqlite3.IntegrityError:
            print(f"Пользователь '{login}' уже существует.")
        finally:
            if db:
                db.close()

if __name__ == '__main__':
    app.config['DATABASE'] = 'school_attendance.db'
    add_admin_user() # Вызываем функцию add_admin_user внутри контекста приложения
    start_scheduler() # Запуск планировщика
    app.run(debug=True)