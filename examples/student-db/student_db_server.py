# Copyright (C) 2024-2026 Burak Günaydin
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

# Standard-library imports
import random
import sys

# Third-party imports
from teatype.db.hsdb.HSDBServer import HSDBServer
from teatype.logging import *
from teatype.toolkit import stopwatch

# Local imports
from server.models import *

# Define your apps
APPS = [
    'server'
]

MODELS = [
    Class,
    Professor,
    Student,
    University
]

def create_student(i:int, random_first_names, random_sur_names, random_schools):
    """
    Creates a student object with random attributes.
    """
    random.seed()
    gender = random.choice(['male', 'female'])
    student = Student({
        'age': random.randint(13, 23),
        'gender': gender,
        'height': random.randint(140, 200),
        'name': f'{random.choice(random_first_names[0] if gender == "male" else random_first_names[1])} {random.choice(random_sur_names)}',
        'university': random.choice([random_school.id for random_school in random_schools])
    })
    return student.id, student

def create_students_sequentially(number_of_students, random_first_names, random_sur_names, random_schools):
    """
    Creates students sequentially.
    """
    students = {}
    for i in range(number_of_students):
        student = create_student(i, random_first_names, random_sur_names, random_schools)
        students[student[0]] = student[1]
    return students

def create_professor(random_first_names, random_sur_names, random_schools):
    """
    Creates a professor object with random attributes.
    """
    random.seed()
    gender = random.choice(['male', 'female'])
    professor = Professor({
        'age': random.randint(28, 70),
        'gender': gender,
        'height': random.randint(150, 200),
        'name': f'{random.choice(random_first_names[0] if gender == "male" else random_first_names[1])} {random.choice(random_sur_names)}',
        'university': random.choice([random_school.id for random_school in random_schools])
    })
    return professor.id, professor

def create_professors_sequentially(number_of_professors, random_first_names, random_sur_names, random_schools):
    """
    Creates professors sequentially.
    """
    professors = {}
    for i in range(number_of_professors):
        professor = create_professor(random_first_names, random_sur_names, random_schools)
        professors[professor[0]] = professor[1]
    return professors

def random_class_name():
    subjects = [
        'Algebra', 'Biology', 'Chemistry', 'Physics', 'History', 'Literature',
        'Computer Science', 'Economics', 'Philosophy', 'Statistics',
    ]
    sections = ['A', 'B', 'C', '101', '201', '301']
    return f'{random.choice(subjects)} {random.choice(sections)}'

def create_class(random_professors, random_students):
    """
    Creates a class object with a random professor and a random subset of students.
    """
    random.seed()
    class_students = random.sample(random_students, k=min(len(random_students), random.randint(5, 15)))
    class_ = Class({
        'name': random_class_name(),
        'professor': random.choice(random_professors).id,
        'students': [student.id for student in class_students]
    })
    return class_.id, class_

def create_classes_sequentially(number_of_classes, random_professors, random_students):
    """
    Creates classes sequentially.
    """
    classes = {}
    for i in range(number_of_classes):
        class_ = create_class(random_professors, random_students)
        classes[class_[0]] = class_[1]
    return classes

def random_first_names():
        return [[
            'Bob', 'Charlie', 'David', 'Frank', 'Ivan', 'Kevin', 'Michael', 'Oscar',
            'Quincy', 'Sam', 'Steve', 'Victor', 'Xander',
        ], [
            'Alice', 'Eve', 'Grace', 'Heidi', 'Judy', 'Linda','Nancy', 'Pamela',
            'Quincy', 'Rachel', 'Sam', 'Tina', 'Ursula', 'Wendy',
        ]]

def random_sur_names():
    return [
        'Anderson', 'Baker', 'Carter', 'Davidson', 'Edwards', 'Fisher', 'Garcia',
        'Hernandez', 'Ivanov', 'Johnson', 'Kowalski', 'Lopez', 'Martinez', 'Nelson',
        'Olsen', 'Perez', 'Quinn', 'Rodriguez', 'Smith', 'Taylor', 'Unger', 'Vasquez',
        'Williams', 'Xu', 'Young', 'Zhang',
    ]

def random_schools():
    return [
        University({'address': '123 Main St', 'name': 'Howard High'}),
        University({'address': '456 ElmSt', 'name': 'Jefferson High'}),
        University({'address': '789 Oak St', 'name': 'Lincoln High'}),
        University({'address': '101 Pine St', 'name': 'Madison High'}),
        University({'address': '112 Birch St', 'name': 'Monroe High'}),
        University({'address': '131 Maple St', 'name': 'Roosevelt High'}),
        University({'address': '415 Cedar St', 'name': 'Washington High'}),
        University({'address': '161 Walnut St', 'name': 'Wilson High'}),
        University({'address': 'Arcisstraße 21', 'name': 'Technische Universität München'}),
    ]

if __name__ == '__main__':
    # Create HSDBServer instance with your configuration
    server = HSDBServer(
        apps=APPS,
        cold_mode=True,
        cors_allow_all=True,
        debug=True,
        models=MODELS,
        root_urlconf='hsdb_server_urls',
    )
    
    # Seed the database
    stopwatch('Seeding DB data')
    hybrid_storage = server.hybrid_storage
    index_db = hybrid_storage.index_db
    
    # First, create and add universities to the database
    schools = random_schools()
    universities = {str(school.id): school for school in schools}
    index_db.update_directly(universities)
    
    # Then create students with references to the persisted universities
    NUMBER_OF_STUDENTS = 1234
    students = create_students_sequentially(NUMBER_OF_STUDENTS, random_first_names(), random_sur_names(), schools)
    index_db.update_directly(students)
    
    # Then create professors linked to the persisted universities
    NUMBER_OF_PROFESSORS = 40
    professors = create_professors_sequentially(NUMBER_OF_PROFESSORS, random_first_names(), random_sur_names(), schools)
    index_db.update_directly(professors)
    
    # Finally create classes, each with a professor (many-to-one) and students (many-to-many)
    NUMBER_OF_CLASSES = 60
    classes = create_classes_sequentially(NUMBER_OF_CLASSES, list(professors.values()), list(students.values()))
    index_db.update_directly(classes)
    stopwatch()
    
    stopwatch('Measuring memory footprint')
    log(hybrid_storage.index_db.memory_footprint)
    stopwatch()
        
    # Dynamically create and set URL patterns
    urlpatterns = server.create_urlpatterns(
        include_admin=False
    )
    
    student = Student.query.where('age').equals(18).first()
    if student:
        print(student)
        print(student.university)
    else:
        print('No student with age 18 found')
    
    # Demonstrate new features
    print('\n--- New Features Demo ---')
    
    # Model.count() - O(1) using model index
    print(f'Total students: {Student.count()}')
    print(f'Total universities: {University.count()}')
    print(f'Total professors: {Professor.count()}')
    print(f'Total classes: {Class.count()}')
    
    # Model.all() with relation serialization
    print('\n--- Student with expanded university ---')
    students_sample = Student.query.where('age').equals(20).first()
    if students_sample:
        serialized = Student.serialize(students_sample, include_relations=True)
        print(f'With relation ID: {serialized}')
        serialized_expanded = Student.serialize(students_sample, expand_relations=True)
        print(f'With expanded relation: {serialized_expanded}')
    else:
        print('No student with age 20 found for relation demo')
    
    # Model.find_by() - O(1) using field index
    print('\n--- Fast indexed lookup ---')
    male_students = Student.find_by('gender', 'male')
    print(f'Found {len(male_students)} male students using indexed lookup')
    
    # Model.schema() - get model structure
    print('\n--- Model Schema ---')
    import json
    print(json.dumps(Student.schema(), indent=2, default=str))
    
    # Create a temporary module for URL configuration
    import types
    url_module = types.ModuleType('hsdb_server_urls')
    url_module.urlpatterns = urlpatterns
    sys.modules['hsdb_server_urls'] = url_module
        
    # Check if we're running a command or just starting the server
    if len(sys.argv) > 1:
        if sys.argv[1] == 'runserver':
            # Run the development server
            server.run()
        else:
            # Execute any Django management command
            server.execute_command(*sys.argv[1:])
    else:
        # Default: run the server
        server.run()