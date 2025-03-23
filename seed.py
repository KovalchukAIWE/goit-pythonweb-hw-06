# seed.py
import random
import datetime
from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import get_engine, Group, Student, Teacher, Subject, Grade

fake = Faker()

# Створення сесії
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

def seed_teachers(n=4):
    teachers = []
    for _ in range(n):
        teacher = Teacher(name=fake.name())
        session.add(teacher)
        teachers.append(teacher)
    session.commit()
    return teachers

def seed_groups(n=3):
    groups = []
    for i in range(1, n + 1):
        group = Group(name=f"Group {i}")
        session.add(group)
        groups.append(group)
    session.commit()
    return groups

def seed_subjects(teachers, n=6):
    subjects = []
    for _ in range(n):
        subject = Subject(
            name=fake.word().capitalize(),
            teacher_id=random.choice(teachers).id
        )
        session.add(subject)
        subjects.append(subject)
    session.commit()
    return subjects

def seed_students(groups, n=40):
    students = []
    for _ in range(n):
        student = Student(
            name=fake.name(),
            group_id=random.choice(groups).id
        )
        session.add(student)
        students.append(student)
    session.commit()
    return students

def seed_grades(students, subjects, max_grades=20):
    for student in students:
        # Для кожного студента створимо від 5 до max_grades оцінок (рандомно)
        n_grades = random.randint(5, max_grades)
        for _ in range(n_grades):
            grade = Grade(
                student_id=student.id,
                subject_id=random.choice(subjects).id,
                grade=round(random.uniform(60, 100), 2),  # оцінка від 60 до 100
                date=fake.date_time_between(start_date='-1y', end_date='now')
            )
            session.add(grade)
    session.commit()

def main():
    # Не забудьте запустити міграції перед цим!
    teachers = seed_teachers(n=4)      # 3-5 викладачів
    groups = seed_groups(n=3)          # 3 групи
    subjects = seed_subjects(teachers, n=6)  # 5-8 предметів
    students = seed_students(groups, n=40)   # 30-50 студентів
    seed_grades(students, subjects, max_grades=20)  # до 20 оцінок для кожного студента
    print("База даних заповнена випадковими даними!")

if __name__ == '__main__':
    main()
