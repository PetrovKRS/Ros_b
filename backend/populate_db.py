import os
import django

# Укажите путь к настройкам вашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Инициализируйте Django
django.setup()
import random
import uuid
from faker import Faker
from datetime import timedelta
from django.utils import timezone
from core.models import (
    Employee, AssesmentSkill, EmployeeAssesmentSkill, DevelopmentPlan, 
    EmployeeDevelopmentPlan, Engagement, EmployeeEngagement, KeyPeople, 
    EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication, 
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, 
    EmployeeKeySkill, Team, EmployeeTeam, Position, EmployeePosition, 
    Competency, PositionCompetency
)

# Инициализация Django и Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

fake = Faker('ru_RU')

def create_employees(n=20):
    """Создать сотрудников."""
    statuses = ['completed', 'in-progress', 'on-hold']
    employees = []
    for _ in range(n):
        employee = Employee.objects.create(
            employee_id=str(uuid.uuid4()),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            status=random.choice(statuses),
            registration_date=fake.date_between(start_date='-5y', end_date='today'),
            last_login_date=fake.date_between(start_date='-1y', end_date='today'),
        )
        employees.append(employee)
    return employees

def create_assesment_skills(n=10):
    """Создать навыки для оценки."""
    skills = []
    for _ in range(n):
        skill = AssesmentSkill.objects.create(
            assesmentskill_name=fake.job(),
        )
        skills.append(skill)
    return skills

def create_development_plans(n=10):
    """Создать планы развития."""
    plans = []
    for _ in range(n):
        plan = DevelopmentPlan.objects.create(
            plan_name=f"Plan {fake.word()}",
            employee_count=random.randint(1, 100)
        )
        plans.append(plan)
    return plans

def create_engagements(n=5):
    """Создать вовлеченности."""
    engagements = []
    for _ in range(n):
        engagement = Engagement.objects.create(
            engagement_name=fake.bs(),
            employee_count=random.randint(1, 50)
        )
        engagements.append(engagement)
    return engagements

def create_key_people(n=5):
    """Создать ключевых людей."""
    key_people = []
    for _ in range(n):
        key_person = KeyPeople.objects.create(
            key_people_name=fake.company(),
            employee_count=random.randint(1, 30)
        )
        key_people.append(key_person)
    return key_people

def create_training_applications(n=5):
    """Создать заявки на обучение."""
    trainings = []
    for _ in range(n):
        training = TrainingApplication.objects.create(
            training_name=f"Training {fake.word()}",
            employee_count=random.randint(1, 50)
        )
        trainings.append(training)
    return trainings

def create_bus_factors(n=5):
    """Создать Bus Факторы."""
    bus_factors = []
    for _ in range(n):
        factor = BusFactor.objects.create(
            bus_factor_name=f"BusFactor {fake.word()}",
            employee_count=random.randint(1, 20)
        )
        bus_factors.append(factor)
    return bus_factors

def create_grades(n=5):
    """Создать классы."""
    grades = []
    for _ in range(n):
        grade = Grade.objects.create(
            grade_name=f"Grade {fake.word()}"
        )
        grades.append(grade)
    return grades

def create_key_skills(n=10):
    """Создать ключевые навыки."""
    skills = []
    for _ in range(n):
        skill = KeySkill.objects.create(
            skill_name=f"Skill {fake.word()}",
            employee_count=random.randint(1, 50)
        )
        skills.append(skill)
    return skills

def create_teams(n=5):
    """Создать команды."""
    teams = []
    for _ in range(n):
        team = Team.objects.create(
            team_name=f"Team {fake.word()}",
            slug=fake.slug()
        )
        teams.append(team)
    return teams

def create_positions(n=5):
    """Создать должности."""
    positions = []
    for _ in range(n):
        position = Position.objects.create(
            position_name=fake.job(),
            grade_count=random.randint(1, 5)
        )
        positions.append(position)
    return positions

def populate_employee_related_models(employees, skills, plans, engagements, key_people, trainings, bus_factors, grades, key_skills):
    """Заполнить зависимые от сотрудников модели."""
    for employee in employees:
        # Оценки навыков
        for skill in random.sample(skills, random.randint(1, 5)):
            EmployeeAssesmentSkill.objects.create(
                employee=employee,
                assesmentskill=skill,
                assesment=random.randint(1, 10)
            )
        
        # Планы развития
        for plan in random.sample(plans, random.randint(1, 3)):
            EmployeeDevelopmentPlan.objects.create(
                employee=employee,
                development_plan=plan,
                performance_score=random.uniform(50.0, 100.0)
            )
        
        # Вовлеченности
        engagement = random.choice(engagements)
        EmployeeEngagement.objects.create(
            employee=employee,
            engagement=engagement,
            performance_score=random.randint(1, 100)
        )
        
        # Key People
        key_person = random.choice(key_people)
        EmployeeKeyPeople.objects.create(
            employee=employee,
            key_people=key_person
        )

        # Заявки на обучение
        training = random.choice(trainings)
        EmployeeTrainingApplication.objects.create(
            employee=employee,
            training_application=training
        )

        # Bus Факторы
        factor = random.choice(bus_factors)
        EmployeeBusFactor.objects.create(
            employee=employee,
            bus_factor=factor
        )
        
        # Грейды
        grade = random.choice(grades)
        EmployeeGrade.objects.create(
            employee=employee,
            grade=grade
        )
        
        # Ключевые навыки
        for key_skill in random.sample(key_skills, random.randint(1, 3)):
            EmployeeKeySkill.objects.create(
                employee=employee,
                key_skill=key_skill,
                skill_level=random.choice(['junior', 'middle', 'senior'])
            )

def main():
    employees = create_employees()
    skills = create_assesment_skills()
    plans = create_development_plans()
    engagements = create_engagements()
    key_people = create_key_people()
    trainings = create_training_applications()
    bus_factors = create_bus_factors()
    grades = create_grades()
    key_skills = create_key_skills()
    teams = create_teams()
    positions = create_positions()

    populate_employee_related_models(
        employees, skills, plans, engagements, key_people, 
        trainings, bus_factors, grades, key_skills
    )

if __name__ == "__main__":
    main()
