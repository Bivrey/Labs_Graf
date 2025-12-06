import sqlite3

sql_script = """
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    faculty TEXT NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    email TEXT UNIQUE,
    enrollment_year INTEGER NOT NULL CHECK(enrollment_year BETWEEN 2015 AND 2025),
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    credits INTEGER NOT NULL CHECK(credits BETWEEN 1 AND 10)
);

CREATE TABLE enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade REAL CHECK(grade BETWEEN 2.0 AND 5.0),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE INDEX idx_students_group ON students(group_id);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);

CREATE VIEW student_grades AS
SELECT
    s.name AS student,
    g.name AS "group",
    c.title AS course,
    e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.id
JOIN groups g ON s.group_id = g.id
JOIN courses c ON e.course_id = c.id;

INSERT INTO groups (name, faculty) VALUES
('ИУ7-61Б', 'ИУ'),
('ИУ7-62Б', 'ИУ'),
('ФН4-81Б', 'ФН'),
('РК9-01М', 'РК');

INSERT INTO students (name, group_id, email, enrollment_year) VALUES
('Иванов Иван Иванович', 1, 'ivanov@bmstu.ru', 2023),
('Петрова Анна Сергеевна', 1, 'petrova@bmstu.ru', 2023),
('Сидоров Алексей Владимирович', 2, 'sidorov@bmstu.ru', 2022),
('Кузнецова Мария Дмитриевна', 3, 'kuznetsova@bmstu.ru', 2024),
('Смирнов Дмитрий Андреевич', 4, 'smirnov@bmstu.ru', 2023),
('Волкова Елена Павловна', 1, 'volkova@bmstu.ru', 2023),
('Морозов Артём Игоревич', 2, 'morozov@bmstu.ru', 2022),
('Новикова Ольга Викторовна', 3, 'novikova@bmstu.ru', 2024);

INSERT INTO courses (title, credits) VALUES
('Математический анализ', 6),
('Программирование на Python', 5),
('Физика', 5),
('Инженерная графика', 3),
('Базы данных', 4),
('Английский язык', 2);

INSERT INTO enrollments (student_id, course_id, grade) VALUES
(1, 1, 4.5), (1, 2, 5.0), (1, 3, 4.0),
(2, 1, 4.8), (2, 2, 4.7), (2, 6, 5.0),
(3, 2, 4.2), (3, 4, 3.8), (3, 5, NULL),
(4, 3, 4.6), (4, 6, 4.5),
(5, 5, 4.9), (5, 2, 4.3),
(6, 1, 4.7), (6, 2, 5.0),
(7, 5, NULL), (7, 6, 4.0),
(8, 3, 4.1), (8, 6, 4.8);
"""

conn = sqlite3.connect('university.db')
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()
conn.close()

print("База university.db успешно создана!")