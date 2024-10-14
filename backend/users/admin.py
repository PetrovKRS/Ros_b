from django.contrib import admin
from core.models import (
    Employee, EmployeeKeyPeople, EmployeeBusFactor,
    EmployeeTrainingApplication, EmployeeGrade,
    EmployeeSkill, EmployeeCompetency, EmployeePosition, EmployeeDevelopmentPlan, EmployeeEngagement
)
from users.models import ManagerTeam

class EmployeeKeyPeopleInline(admin.TabularInline):
    model = EmployeeKeyPeople
    extra = 1


class EmployeeBusFactorInline(admin.TabularInline):
    model = EmployeeBusFactor
    extra = 1


class EmployeeTrainingApplicationInline(admin.TabularInline):
    model = EmployeeTrainingApplication
    extra = 1


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1  # количество пустых форм для добавления новых записей


class EmployeeCompetencyInline(admin.TabularInline):
    model = EmployeeCompetency
    extra = 1


class EmployeeGradeInline(admin.TabularInline):
    model = EmployeeGrade
    extra = 1


class EmployeePositionInline(admin.TabularInline):
    model = EmployeePosition
    extra = 1


class EmployeeDevelopmentPlanInline(admin.TabularInline):
    model = EmployeeDevelopmentPlan
    extra = 1


class EmployeeAssesmentInline(admin.TabularInline):
    model = EmployeeEngagement
    extra = 1


class EmployeeEngagementInline(admin.TabularInline):
    model = EmployeeEngagement
    extra = 1
    
@admin.register(Employee)  # Регистрация модели через декоратор
class UserAdmin(admin.ModelAdmin):
    inlines = [
        EmployeeKeyPeopleInline,
        EmployeeBusFactorInline,
        EmployeeTrainingApplicationInline,
        EmployeeSkillInline,  # Инлайн для скиллов
        EmployeeCompetencyInline,  # Инлайн для компетенций
        EmployeeGradeInline,
        EmployeePositionInline,
        EmployeeDevelopmentPlanInline,
        EmployeeEngagementInline
    ]

    list_display = (
        'pk', 'employee_id', 'email', 'first_name', 'last_name'
    )
    search_fields = (
        'email', 'first_name', 'last_name'
    )
    list_filter = (
        'email', 'first_name', 'last_name'
    )

# Админка для ManagerTeam
@admin.register(ManagerTeam)  # Регистрация модели через декоратор
class ManagerTeamAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser'
    )
    search_fields = (
        'email', 'first_name', 'last_name'
    )
    list_filter = (
        'email', 'first_name', 'last_name', 'is_staff', 'is_superuser'
    )