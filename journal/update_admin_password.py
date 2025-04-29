from werkzeug.security import generate_password_hash
import sqlite3

DATABASE = 'school_attendance.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def execute_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

def add_password_to_admin():
    password = '9v12'
    hashed_password = generate_password_hash(password)
    login = 'admin1'

    query = 'UPDATE class_monitors SET hashed_password = ? WHERE login = ?'
    execute_db(query, (hashed_password, login))
    print(f"Пароль для пользователя '{login}' успешно обновлен.")

if __name__ == '__main__':
    add_password_to_admin()