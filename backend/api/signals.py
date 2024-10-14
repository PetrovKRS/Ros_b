from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import (
    EmployeeSkill, Skill, EmployeeCompetency, Competency,
    EmployeeBusFactor, EmployeeKeyPeople, Engagement, EmployeeEngagement,
    PositionGrade, Position, EmployeeTrainingApplication, TrainingApplication,
    EmployeeDevelopmentPlan, DevelopmentPlan, EmployeeKeyPeople, KeyPeople,
)


# Сигнал для пересчета employee_count при добавлении или удалении записи
@receiver(post_save, sender=EmployeeKeyPeople)
@receiver(post_delete, sender=EmployeeKeyPeople)
def update_employee_count(sender, instance, **kwargs):
    key_people = instance.key_people
    # Пересчитываем количество сотрудников, связанных с Key People
    key_people.employee_count = key_people.employees.count()
    key_people.save()


# Сигнал для пересчета employee_count при добавлении или удалении плана развития сотрудника
@receiver(post_save, sender=EmployeeDevelopmentPlan)
@receiver(post_delete, sender=EmployeeDevelopmentPlan)
def update_employee_count(sender, instance, **kwargs):
    development_plan = instance.development_plan
    # Пересчитываем количество сотрудников с планом развития
    development_plan.employee_count = development_plan.employeedevelopmentplan_set.count()
    development_plan.save()


# Сигнал для пересчета employee_count при добавлении или удалении заявки на обучение
@receiver(post_save, sender=EmployeeTrainingApplication)
@receiver(post_delete, sender=EmployeeTrainingApplication)
def update_employee_count(sender, instance, **kwargs):
    training_application = instance.training_application
    # Пересчитываем количество сотрудников, связанных с заявкой на обучение
    training_application.employee_count = training_application.employeetrainingapplication_set.count()
    training_application.save()


# Сигнал для пересчета grade_count при добавлении грейда
@receiver(post_save, sender=PositionGrade)
@receiver(post_delete, sender=PositionGrade)
def update_grade_count(sender, instance, **kwargs):
    position = instance.position
    # Пересчитываем количество грейдов, связанных с должностью
    position.grade_count = position.position_grades.count()
    position.save()


# Сигнал для пересчета employee_count при добавлении или удалении сотрудника
@receiver(post_save, sender=EmployeeEngagement)
@receiver(post_delete, sender=EmployeeEngagement)
def update_employee_count(sender, instance, **kwargs):
    engagement = instance.engagement
    # Пересчитываем количество сотрудников, связанных с вовлеченностью
    engagement.employee_count = engagement.employee_engagements.count()
    engagement.save()


# Сигнал на создание или удаление навыка сотрудника
@receiver([post_save, post_delete], sender=EmployeeSkill)
def update_employee_count(sender, instance, **kwargs):
    skill = instance.skill
    # Подсчет количества сотрудников с данным навыком
    skill.employee_count = EmployeeSkill.objects.filter(skill=skill).count()
    skill.save()


# Сигнал на создание или удаление компетенции сотрудника
@receiver([post_save, post_delete], sender=EmployeeCompetency)
def update_employee_competency_count(sender, instance, **kwargs):
    competency = instance.competency
    # Подсчет количества сотрудников с данной компетенцией
    competency.employee_count = EmployeeCompetency.objects.filter(competency=competency).count()
    competency.save()


# Сигнал для обновления employee_count при добавлении записи EmployeeBusFactor
@receiver(post_save, sender=EmployeeBusFactor)
def update_employee_count_on_save(sender, instance, created, **kwargs):
    if created:
        bus_factor = instance.bus_factor
        bus_factor.employee_count = EmployeeBusFactor.objects.filter(bus_factor=bus_factor).count()
        bus_factor.save()


# Сигнал для обновления employee_count при удалении записи EmployeeBusFactor
@receiver(post_delete, sender=EmployeeBusFactor)
def update_employee_count_on_delete(sender, instance, **kwargs):
    bus_factor = instance.bus_factor
    bus_factor.employee_count = EmployeeBusFactor.objects.filter(bus_factor=bus_factor).count()
    bus_factor.save()


# Сигнал для обновления employee_count при добавлении записи EmployeeKeyPeople
@receiver(post_save, sender=EmployeeKeyPeople)
def update_employee_count_on_save_key_people(sender, instance, created, **kwargs):
    if created:
        key_people = instance.key_people
        key_people.employee_count = EmployeeKeyPeople.objects.filter(key_people=key_people).count()
        key_people.save()

# Сигнал для обновления employee_count при удалении записи EmployeeKeyPeople
@receiver(post_delete, sender=EmployeeKeyPeople)
def update_employee_count_on_delete_key_people(sender, instance, **kwargs):
    key_people = instance.key_people
    key_people.employee_count = EmployeeKeyPeople.objects.filter(key_people=key_people).count()
    key_people.save()