import sqlite3

DATABASE = 'school_attendance.db'

def execute_db(query, args=()):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

def update_admin_class():
    login = 'admin1'
    new_class_name = '9v'
    query = 'UPDATE class_monitors SET class_name = ? WHERE login = ?'
    execute_db(query, (new_class_name, login))
    print(f"Класс пользователя '{login}' успешно обновлен на '{new_class_name}'.")

if __name__ == '__main__':
    update_admin_class()