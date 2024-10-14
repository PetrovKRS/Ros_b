from django.core.management.base import BaseCommand
from faker import Faker
import random
from core.models import (Employee, DevelopmentPlan, EmployeeDevelopmentPlan, Engagement, EmployeeEngagement,
                          KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
                          BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
                          Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
                          TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
                          ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill)

class Command(BaseCommand):
    help = 'Заполняет базу данных фиктивными данными'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Заполняем модель Employee
        employees = []
        

        # Заполняем модель DevelopmentPlan
        development_plans = []
        for _ in range(10):
            plan = DevelopmentPlan.objects.create(
                plan_name=fake.bs(),
                employee_count=0
            )
            development_plans.append(plan)

        # Заполняем модель EmployeeDevelopmentPlan
        for employee in employees:
            plan = random.choice(development_plans)
            EmployeeDevelopmentPlan.objects.create(
                employee=employee,
                development_plan=plan,
                development_progress=round(random.uniform(0, 100), 2)
            )
            plan.employee_count += 1
            plan.save()

        # Заполняем модель Engagement
        engagements = []
        for _ in range(10):
            engagement = Engagement.objects.create(
                engagement_name=fake.company_suffix(),
                employee_count=0
            )
            engagements.append(engagement)

        # Заполняем модель EmployeeEngagement
        for employee in employees:
            engagement = random.choice(engagements)
            EmployeeEngagement.objects.create(
                employee=employee,
                engagement=engagement,
                engagement_level=random.randint(1, 10)
            )
            engagement.employee_count += 1
            engagement.save()

        # Заполняем модель KeyPeople
        key_people_list = []
        for _ in range(10):
            key_people = KeyPeople.objects.create(
                key_people_name=fake.job(),
                employee_count=0
            )
            key_people_list.append(key_people)

        # Заполняем модель EmployeeKeyPeople
        for employee in employees:
            key_people = random.choice(key_people_list)
            EmployeeKeyPeople.objects.create(
                employee=employee,
                key_people=key_people
            )
            key_people.employee_count += 1
            key_people.save()

        # Заполняем модель TrainingApplication
        training_apps = []
        for _ in range(10):
            training_app = TrainingApplication.objects.create(
                training_name=fake.catch_phrase(),
                employee_count=0
            )
            training_apps.append(training_app)

        # Заполняем модель EmployeeTrainingApplication
        for employee in employees:
            training_app = random.choice(training_apps)
            EmployeeTrainingApplication.objects.create(
                employee=employee,
                training_application=training_app
            )
            training_app.employee_count += 1
            training_app.save()

        # Заполняем модель BusFactor
        bus_factors = []
        for _ in range(10):
            bus_factor = BusFactor.objects.create(
                bus_factor_name=fake.catch_phrase(),
                employee_count=0
            )
            bus_factors.append(bus_factor)

        # Заполняем модель EmployeeBusFactor
        for employee in employees:
            bus_factor = random.choice(bus_factors)
            EmployeeBusFactor.objects.create(
                employee=employee,
                bus_factor=bus_factor
            )
            bus_factor.employee_count += 1
            bus_factor.save()

        # Заполняем модель Grade
        grades = []
        for _ in range(10):
            grade = Grade.objects.create(
                grade_name=fake.job()
            )
            grades.append(grade)

        # Заполняем модель EmployeeGrade
        for employee in employees:
            grade = random.choice(grades)
            EmployeeGrade.objects.create(
                employee=employee,
                grade=grade
            )

        # Заполняем модель KeySkill
        key_skills = []
        for _ in range(10):
            skill = KeySkill.objects.create(
                skill_name=fake.bs(),
                employee_count=0
            )
            key_skills.append(skill)

        # Заполняем модель EmployeeKeySkill
        for employee in employees:
            skill = random.choice(key_skills)
            EmployeeKeySkill.objects.create(
                employee=employee,
                key_skill=skill,
                skill_level=fake.word()
            )
            skill.employee_count += 1
            skill.save()

        # Аналогичным образом заполним остальные модели...

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
