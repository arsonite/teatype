# Copyright (C) 2024-2025 Burak Günaydin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# System imports
import os
import random

# Package imports
import pytest

# From system imports
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint

# From package imports
from teatype.hsdb import HSDBAttribute, HSDBModel, HybridStorage
from teatype.logging import hint, println
from teatype.util import generate_id, stopwatch

##################
# Example Models #
##################

# Assume these are your models derived from BaseModel.
class StudentModel(HSDBModel):
    age    = HSDBAttribute(int, required=True)
    gender = HSDBAttribute(str, required=True)
    height = HSDBAttribute(int, description='Height in cm', required=True)
    name   = HSDBAttribute(str, required=True)
    # school = HSDBAttribute(type=HSDBRelation)
    
class SchoolModel(HSDBModel):
    address = HSDBAttribute(str, required=True)
    name    = HSDBAttribute(str, required=True)
    
####################
# Helper Functions #
####################

def create_student(i:int, random_first_names, random_sur_names, random_schools):
    """
    Creates a student object with random attributes.
    """
    student = StudentModel({
        'age': random.randint(13, 23),
        'height': random.randint(140, 200),
        'name': f'{random.choice(random_first_names)} {random.choice(random_sur_names)}',
        'school': random.choice([random_school.id for random_school in random_schools])
    })
    return student.id, student

def create_students_parallel(number_of_students, random_first_names, random_sur_names, random_schools):
    """
    Creates students in parallel using ProcessPoolExecutor.
    """
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = dict(
            executor.map(
                create_student,
                range(number_of_students),
                [random_first_names] * number_of_students,
                [random_sur_names] * number_of_students,
                [random_schools] * number_of_students
            )
        )
    return results

#############
#  Fixtures #
#############

@pytest.fixture(scope='module')
def random_first_names():
    return [
        'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi',
        'Ivan', 'Judy', 'Kevin', 'Linda', 'Michael', 'Nancy', 'Oscar', 'Pamela',
        'Quincy', 'Rachel', 'Steve', 'Tina', 'Ursula', 'Victor', 'Wendy', 'Xander',
    ]

@pytest.fixture(scope='module')
def random_sur_names():
    return [
        'Anderson', 'Baker', 'Carter', 'Davidson', 'Edwards', 'Fisher', 'Garcia',
        'Hernandez', 'Ivanov', 'Johnson', 'Kowalski', 'Lopez', 'Martinez', 'Nelson',
        'Olsen', 'Perez', 'Quinn', 'Rodriguez', 'Smith', 'Taylor', 'Unger', 'Vasquez',
        'Williams', 'Xu', 'Young', 'Zhang',
    ]

@pytest.fixture(scope='module')
def random_schools():
    return [
        SchoolModel({'address': '123 Main St', 'name': 'Howard High'}),
        SchoolModel({'address': '456 ElmSt', 'name': 'Jefferson High'}),
        SchoolModel({'address': '789 Oak St', 'name': 'Lincoln High'}),
        SchoolModel({'address': '101 Pine St', 'name': 'Madison High'}),
        SchoolModel({'address': '112 Birch St', 'name': 'Monroe High'}),
        SchoolModel({'address': '131 Maple St', 'name': 'Roosevelt High'}),
        SchoolModel({'address': '415 Cedar St', 'name': 'Washington High'}),
        SchoolModel({'address': '161 Walnut St', 'name': 'Wilson High'})
    ]

@pytest.fixture
def hybrid_storage():
    return HybridStorage(cold_mode=True)

##########
# PyTest #
##########

@pytest.mark.parametrize('number_of_students', [1111])
def test_create_students_parallel(number_of_students,
                                  random_first_names,
                                  random_sur_names,
                                  random_schools,
                                  hybrid_storage):
    """
    Test student creation in parallel and database update.
    """
    println()
    
    db = hybrid_storage.index_database._db
    for school in random_schools:
        db.update({school.id: school})
    
    if number_of_students == 1:
        stopwatch('Creating student')
        student = create_student(0, random_first_names, random_sur_names, random_schools)
        students = {student[0]: student[1]}
        stopwatch()
    else:
        stopwatch('Creating students in parallel')
        students = create_students_parallel(number_of_students, random_first_names, random_sur_names, random_schools)
        stopwatch()
    println()

    assert isinstance(students, dict)
    assert len(students.keys()) == number_of_students
    # Ensure all students are instances of StudentModel
    for student in students.values():
        assert isinstance(student, StudentModel)

    stopwatch('Index DB update')
    # Simulate and verify database update
    db.update(students)
    stopwatch()
    
    total_database_entries = len(db.keys())
    println()
    print(f'Total generated students: {total_database_entries}')
    
    # Create a query chain that does not execute immediately.
    # query1 = StudentModel.query.where('height').greater_than(150).filter_by('name').sort_by('age')
    queryset = StudentModel.query.where('height').greater_than(150)
    # query is now a representation like:
    print(queryset) # e.g. <HSDBQuery conditions=[('name', '==', ...?), ('height', '>', 150)] sort_by=age>
    # Execute query
    queryset.collect()
    
    # Create a query with chained where's for bonus usage:
    single_query = (
        StudentModel.query
        .where('name').equals('jennifer')
        .where('age').less_than(20)
        #  .where('school.name').equals('Howard High')
    )