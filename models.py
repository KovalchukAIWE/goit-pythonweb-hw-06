# models.py
import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, ForeignKey, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Таблиця груп
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    students = relationship("Student", back_populates="group")

# Таблиця студентів
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

# Таблиця викладачів
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    subjects = relationship("Subject", back_populates="teacher")

# Таблиця предметів
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

# Таблиця оцінок
class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    grade = Column(Float, nullable=False)  # можна використовувати Float для збереження середніх значень
    date = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

# Функція для створення двигуна (engine)
def get_engine():
    # Змінити за потребою: тут використовуємо Postgres, запущений у Docker:
    return create_engine('postgresql+psycopg2://postgres:12345@localhost:5432/postgres')
