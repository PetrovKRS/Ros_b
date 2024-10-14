from django_filters import rest_framework as filters
from core.models import Employee


class EmployeeFilter(filters.FilterSet):
    position = filters.CharFilter(
        field_name='positions__position__position_name',
        lookup_expr='exact',
        label='Должность сотрудника',
    )
    grade = filters.CharFilter(
        field_name='grades__grade__grade_name',
        lookup_expr='exact',
        label='Класс сотрудника',
    )
    skill = filters.CharFilter(
        field_name='skills__skill__skill_name',
        lookup_expr='exact',
        label='Навык сотрудника',
    )
    competency = filters.CharFilter(
        field_name='competencies__competency__competency_name',
        lookup_expr='exact',
        label='Компетенция сотрудника',
    )
    worker = filters.CharFilter(
        field_name='last_name',
        lookup_expr='icontains',
        label='Фамилия сотрудника',
        distinct=True
    )

    class Meta:
        model = Employee
        fields = (
            'position', 'grade', 'skill',
            'competency', 'last_name',
        )
