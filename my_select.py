# my_select.py
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import get_engine, Student, Grade, Subject, Teacher, Group

engine = get_engine()
Session = sessionmaker(bind=engine)

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    session = Session()
    result = (
        session.query(
            Student,
            func.avg(Grade.grade).label("avg_grade")
        )
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    session.close()
    return result

# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id: int):
    session = Session()
    result = (
        session.query(
            Student,
            func.avg(Grade.grade).label("avg_grade")
        )
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    session.close()
    return result

# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_id: int):
    session = Session()
    result = (
        session.query(
            Group,
            func.avg(Grade.grade).label("avg_grade")
        )
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    session.close()
    return result

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    session = Session()
    avg_grade = session.query(func.avg(Grade.grade)).scalar()
    session.close()
    return avg_grade

# 5. Знайти які курси (предмети) читає певний викладач.
def select_5(teacher_id: int):
    session = Session()
    result = session.query(Subject).filter(Subject.teacher_id == teacher_id).all()
    session.close()
    return result

# 6. Знайти список студентів у певній групі.
def select_6(group_id: int):
    session = Session()
    result = session.query(Student).filter(Student.group_id == group_id).all()
    session.close()
    return result

# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id: int, subject_id: int):
    session = Session()
    result = (
        session.query(Student, Grade)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    session.close()
    return result

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id: int):
    session = Session()
    subjects = session.query(Subject.id).filter(Subject.teacher_id == teacher_id).subquery()
    avg_grade = session.query(func.avg(Grade.grade)).filter(Grade.subject_id.in_(subjects)).scalar()
    session.close()
    return avg_grade

# 9. Знайти список курсів, які відвідує певний студент.
def select_9(student_id: int):
    session = Session()
    result = (
        session.query(Subject)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    session.close()
    return result

# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_id: int, teacher_id: int):
    session = Session()
    result = (
        session.query(Subject)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    session.close()
    return result

# Приклад використання (можна перевіряти функції через виклики)
if __name__ == '__main__':
    top_students = select_1()
    print("ТОП 5 студентів з найвищим середнім балом:")
    for student, avg in top_students:
        print(f"{student.name} - {avg:.2f}")
