CREATE TABLE IF NOT EXISTS class_monitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    class_name TEXT NOT NULL,
    shift INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    class_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    late_time TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
