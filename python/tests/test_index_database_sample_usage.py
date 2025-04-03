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
from teatype.hsdb import HSDBAttribute, HSDBRelation, HSDBModel, HybridStorage
from teatype.logging import hint, log, println
from teatype.util import generate_id, stopwatch

##################
# Example Models #
##################

class CompanyModel(HSDBModel):
    address             = HSDBAttribute(str, required=True)
    industry            = HSDBAttribute(str, required=True)
    name                = HSDBAttribute(str, required=True)
    number_of_employees = HSDBAttribute(int, computed=True)
    public              = HSDBAttribute(bool, required=True)
    revenue             = HSDBAttribute(float, required=True)
    stock_symbol        = HSDBAttribute(str, required=False)
    
class CompanyModel(HSDBModel):
    address = HSDBAttribute(str, required=True)
    name    = HSDBAttribute(str, required=True)
    
class TeamModel(HSDBModel):
    department  = HSDBAttribute(str, required=True)
    company     = HSDBRelation.ManyToOne(CompanyModel, required=True)
    
class EmployeeModel(HSDBModel):
    age         = HSDBAttribute(int, required=True)
    gender      = HSDBAttribute(str, required=True)
    height      = HSDBAttribute(int, description='Height in cm', required=True)
    looks       = HSDBAttribute(str, required=False)
    nationality = HSDBAttribute(str, required=False)
    name        = HSDBAttribute(str, required=True)
    salary      = HSDBAttribute(float, required=True)
    team        = HSDBRelation.ManyToOne(TeamModel, required=True)
    
####################
# Helper Functions #
####################

def create_employee(i:int, random_first_names, random_sur_names, random_teams):
    """
    Creates a employee object with random attributes.
    """
    random.seed()
    gender = random.choice(['male', 'female'])
    employee = EmployeeModel({
        'age': random.randint(18, 67),
        'gender': gender,
        'height': random.randint(140, 200),
        'name': f'{random.choice(random_first_names[0] if gender == "male" else random_first_names[1])} {random.choice(random_sur_names)}',
        'team': random.choice([random_team.id for random_team in random_teams])
    })
    return employee.id, employee

def create_teams(i:int, random_departments, random_names):
    """
    Creates a employee object with random attributes.
    """
    random.seed()
    employee = EmployeeModel({
        'age': random.randint(18, 67),
        'gender': gender,
        'height': random.randint(140, 200),
        'name': f'{random.choice(random_first_names[0] if gender == "male" else random_first_names[1])} {random.choice(random_sur_names)}',
        'company': random.choice([random_company.id for random_company in random_companies])
    })
    return employee.id, employee

def create_employees_sequentially(number_of_employees, random_first_names, random_sur_names, random_teams):
    """
    Creates employees sequentially.
    """
    employees = {}
    for i in range(number_of_employees):
        employee = create_employee(i, random_first_names, random_sur_names, random_teams)
        employees[employee[0]] = employee[1]
    return employees

def create_employees_parallel(number_of_employees, random_first_names, random_sur_names, random_teams):
    """
    Creates employees in parallel using ProcessPoolExecutor.
    """
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = dict(
            executor.map(
                create_employee,
                range(number_of_employees),
                [random_first_names] * number_of_employees,
                [random_sur_names] * number_of_employees,
                [random_teams] * number_of_employees
            )
        )
    return results

#############
#  Fixtures #
#############

@pytest.fixture(scope='module')
def random_first_names():
        return [[
            'Bob', 'Charlie', 'David', 'Frank', 'Ivan', 'Kevin', 'Michael', 'Oscar',
            'Quincy', 'Sam', 'Steve', 'Victor', 'Xander',
        ], [
            'Alice', 'Eve', 'Grace', 'Heidi', 'Judy', 'Linda','Nancy', 'Pamela',
            'Quincy', 'Rachel', 'Sam', 'Tina', 'Ursula', 'Wendy',
        ]]

@pytest.fixture(scope='module')
def random_sur_names():
    return [
        'Anderson', 'Baker', 'Carter', 'Davidson', 'Edwards', 'Fisher', 'Garcia',
        'Hernandez', 'Ivanov', 'Johnson', 'Kowalski', 'Lopez', 'Martinez', 'Nelson',
        'Olsen', 'Perez', 'Quinn', 'Rodriguez', 'Smith', 'Taylor', 'Unger', 'Vasquez',
        'Williams', 'Xu', 'Young', 'Zhang',
    ]

@pytest.fixture(scope='module')
def random_departments():
    return [
        'Engineering', 'Marketing', 'Sales', 'Finance', 'HR', 'IT', 'Customer Support',
        'Legal', 'Product Management', 'Research and Development', 'Quality Assurance',
        'Operations', 'Supply Chain', 'Business Development', 'Public Relations',
        'Data Science', 'Analytics', 'Design', 'Content Creation', 'Social Media',
        'Project Management', 'Administration', 'Facilities Management', 'Security',
        'Training and Development', 'Corporate Strategy', 'Investor Relations',
        'Compliance', 'Risk Management', 'Procurement', 'Logistics', 'Technical Support',
    ]

@pytest.fixture(scope='module')
def random_companies():
    return [
        CompanyModel({
            'address': 'Unter den Linden 6',
            'industry': 'Software & Hardware',
            'name': 'PowerCycle GmbH',
            'public': True,
            'revenue': 123_456.78,
            'stock_symbol': 'PCG',
        }),
        CompanyModel({
            'address': 'Alexanderplatz 1',
            'industry': 'Finance',
            'name': 'Bank of Berlin',
            'public': True,
            'revenue': 987_654.32,
            'stock_symbol': 'BB',
        }),
        CompanyModel({
            'address': 'Kurfürstendamm 1',
            'industry': 'Retail',
            'name': 'Berlin Mall',
            'public': False,
            'revenue': 456_789.01,
            'stock_symbol': 'BM',
        }),
        CompanyModel({
            'address': 'Potsdamer Platz 1',
            'industry': 'Entertainment',
            'name': 'Berlin Cinema',
            'public': True,
            'revenue': 654_321.09,
            'stock_symbol': 'BC',
        }),
        CompanyModel({
            'address': 'Friedrichstraße 1',
            'industry': 'Transportation',
            'name': 'Berlin Transport',
            'public': False,
            'revenue': 321_098.76,
            'stock_symbol': 'BT',
        }),
        CompanyModel({
            'address': 'Unter den Linden 7',
            'industry': 'Telecommunications',
            'name': 'Berlin Telecom',
            'public': True,
            'revenue': 789_012.34,
            'stock_symbol': 'BTT',
        }),
        CompanyModel({
            'address': 'Alexanderplatz 2',
            'industry': 'Real Estate',
            'name': 'Berlin Properties',
            'public': True,
            'revenue': 234_567.89,
            'stock_symbol': 'BP',
        }),
        CompanyModel({
            'address': 'Kurfürstendamm 2',
            'industry': 'Healthcare',
            'name': 'Berlin Health',
            'public': False,
            'revenue': 876_543.21,
            'stock_symbol': 'BH',
        }),
        
    ]

@pytest.fixture
def hybrid_storage(random_companies):
    hybrid_storage = HybridStorage(cold_mode=True)
    for company in random_companies:
        hybrid_storage.index_database._db.update({company.id: company})
    return hybrid_storage

##########
# PyTest #
##########

# @pytest.mark.skip
@pytest.mark.parametrize('number_of_employees, generate_in_parallel, measure_memory_footprint', [
    (111111, True, True),
])
def test_queries(number_of_employees,
                 generate_in_parallel,
                 measure_memory_footprint,
                 random_first_names,
                 random_sur_names,
                 random_companies,
                 hybrid_storage):
    log('--------------------')

    stopwatch('Seeding DB data')
    db = hybrid_storage.index_database._db
    if generate_in_parallel:
        employees = create_employees_parallel(number_of_employees, random_first_names, random_sur_names, random_companies)
    else:
        employees = create_employees_sequentially(number_of_employees, random_first_names, random_sur_names, random_companies)
    db.update(employees)
    total_database_entries = len(db.keys())
    stopwatch()
    log(f'Total data: {total_database_entries}')
    if measure_memory_footprint:
        stopwatch('Measuring memory footprint')
        log(hybrid_storage.index_database.memory_footprint)
        stopwatch()
    println()
    
    # Create a query chain that does not execute immediately.
    log('Test queries:')
    println()
    
    CompanyModel.query.verbose().all()
    
    TeamModel.query.verbose().all()
                      
    EmployeeModel.query.verbose().all()
    
    EmployeeModel.query.w('height').gt(180).verbose().collect()
    
    EmployeeModel.query.where('height').less_than(150) \
                       .where('age').less_than(16) \
                       .sort_by('name') \
                       .filter_by('name') \
                       .verbose() \
                       .collect()
    
    EmployeeModel.query.where('height').less_than(150) \
                       .where('age').less_than(16) \
                       .verbose() \
                       .paginate(0, 10)
    
    EmployeeModel.query.where('height').less_than(150) \
                       .where('age').less_than(16) \
                       .verbose() \
                       .paginate(1, 10)
    
    EmployeeModel.query.where('height').less_than(150) \
                       .where('age').less_than(16) \
                       .verbose() \
                       .paginate(0, 30)
    
    EmployeeModel.query.where('height').less_than(150) \
                       .where('age').less_than(16) \
                       .verbose() \
                       .first()
    
    EmployeeModel.query.where('height').less_than(150) \
                       .where('age').less_than(16) \
                       .verbose() \
                       .last()
    
    company = CompanyModel({
        'address': 'Kolonnenstraße 8',
        'industry': 'Software & Hardware',
        'name': 'enamentis GmbH',
        'public': False,
        'revenue': 0,
    })
    employee = EmployeeModel({
        'age': 30,
        ''
    })
    db.update({employee.id: employee})
    employee_id = employee.id
    EmployeeModel.query.verbose().get(id=employee_id)
    
    log('--------------------')
    
@pytest.mark.skip
def test_relations(hybrid_storage):
    log('--------------------')

    db = hybrid_storage.index_database._db
    
    enamentis_gmbh = CompanyModel({
        'address': 'Kolonnenstraße 8',
        'industry': 'AI Software & Hardware',
        'name': 'enamtnis GmbH',
        'public': False,
        'revenue': 0.0,
    })
    db.update({enamentis_gmbh.id: enamentis_gmbh})
    
    log('--------------------')