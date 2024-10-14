from django.shortcuts import render
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from datetime import datetime
from calendar import month_name
from rest_framework import (
    mixins,
    permissions,
    status,
    viewsets,
    exceptions,
    generics
)
from users.models import (
    ManagerTeam,
)
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill, Employee,
    EmployeeAssesmentSkill, AssesmentSkill,
)
from yaml import serialize

from .serializers import (
    EmployeeSerializer,
    IndividualDevelopmentPlanRequestSerializer,
    TeamMetricsRequestSerializer,
    SkillDomenRequestSerializer,
    MetricResponseSerializer,
    CompetencyLevelRequestSerializer,
    SkillLevelRequestSerializer, TeamSkillSerializer,
)
from .filters import EmployeeFilter


class EmployeesViewSet(mixins.ListModelMixin,  # Для получения списка сотрудников
                        mixins.RetrieveModelMixin,  # Для получения конкретного сотрудника по ID
                        viewsets.GenericViewSet): 
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    
    def get_queryset(self):
        team_slug = self.kwargs.get('team_slug')  # Получаем слаг команды
        # user = self.request.user

        # user = ManagerTeam.objects.get(id=1)
        team = Team.objects.get(slug=team_slug)  # Предполагается, что у команды есть связь с slug
        manager = ManagerTeam.objects.get(id=2)  # Предполагается, что у менеджера есть связь с пользователем

        # Возвращаем сотрудников, относящихся к команде текущего менеджера
        return Employee.objects.filter(
            teams__team=team,  # Используем ManyToMany связь
            teams__manager=manager  # Фильтруем по менеджеру
        )


class MetricViewSet(viewsets.GenericViewSet):
    """ . """
    
    def create(self, request, metric_type, employee_id):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = IndividualDevelopmentPlanRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Получаем даты из сериализатора
        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'], 
            serializer.validated_data['endPeriod']
        )

        # Определяем модель по метрике
        model = {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement
        }.get(metric_type)

        if not model:
            return Response({"error": "Invalid metric type."}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем метрики для одного сотрудника по его ID
        dashboard, last_performance = self.get_employee_metrics(employee_id, model, start_date, end_date)

        response_data = {
            "dashboard": [],
            "completionForToday": last_performance
        }

        for entry in dashboard:
            metric_serializer = MetricResponseSerializer(data=entry)
            if metric_serializer.is_valid():
                response_data["dashboard"].append(metric_serializer.data)

        return Response(response_data, status=status.HTTP_200_OK)

    def get_employee_metrics(self, employee_id, model, start_date, end_date):
        dashboard = []

        # Измените фильтрацию, чтобы использовать только один ID
        employee_metrics = model.objects.filter(
            employee__id=employee_id,
            add_date__range=[start_date, end_date]
        )


        if not employee_metrics.exists():
            return dashboard, "0.00"  # Если нет метрик, возвращаем пустой результат

        # Группируем метрики по месяцам
        metrics_by_month = self.group_metrics_by_month(employee_metrics)

        for (year, month), performance in metrics_by_month.items():
            dashboard.append({
                "period": {"month": month_name[month], "year": year},
                "performance": str(performance)
            })

        last_performance = dashboard[-1]['performance'] if dashboard else "0.00"
        return dashboard, last_performance

    def group_metrics_by_month(self, employee_metrics):
        metrics_by_month = {}
        for metric in employee_metrics:
            key = (metric.add_date.year, metric.add_date.month)
            metrics_by_month[key] = metrics_by_month.get(key, 0) + metric.performance_score
        return metrics_by_month

    def convert_to_date(self, start_period, end_period):
        start_date = datetime.strptime(f"{start_period['year']}-{start_period['month']}-13", "%Y-%B-%d").date()
        end_date = datetime.strptime(f"{end_period['year']}-{end_period['month']}-13", "%Y-%B-%d").date()
        return start_date, end_date


class TeamCountEmployeeViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        dashboard = []
        team_slug = kwargs.get('team_slug')
        # Получаем команду по слагу
        try:
            team = EmployeeTeam.objects.get(team__slug=team_slug)
            employees = team.employee.all()  # Получаем всех сотрудников команды

            # Преобразуем даты начала и окончания

            # Получаем количество сотрудников, Bus факторов и Key People
            number_of_employees = employees.count()
            number_of_bus_factors = EmployeeBusFactor.objects.filter(
                employee__in=employees,
            ).count()
            number_of_key_people = EmployeeKeyPeople.objects.filter(
                employee__in=employees,
            ).count()

            # Добавляем результаты в dashboard
            dashboard = {
                "numberOfEmployee": str(number_of_employees),
                "numberOfBusFactor": str(number_of_bus_factors),
                "numberOfKeyPeople": str(number_of_key_people),
            }
            serializer = TeamSkillSerializer(dashboard)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except EmployeeTeam.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)


class TeamMetricViewSet(viewsets.ViewSet):
    def create(self, request, team_slug, metric_type):
        request_serializer = TeamMetricsRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date, end_date = self.convert_to_date(
            request_serializer.validated_data['startPeriod'],
            request_serializer.validated_data['endPeriod']
        )

        try:
            employees = EmployeeTeam.objects.get(team__slug=team_slug).employee.all()
        except EmployeeTeam.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

        model = self.get_metric_model(metric_type)
        if model is None:
            return Response({"error": "Invalid metric type."}, status=status.HTTP_400_BAD_REQUEST)

        metrics_by_month = {}
        for employee in employees:
            for metric in model.objects.filter(employee=employee, add_date__range=[start_date, end_date]):
                key = (metric.add_date.year, metric.add_date.month)
                metrics_by_month[key] = metrics_by_month.get(key, 0) + metric.performance_score

        dashboard = [
            {"period": {"month": month_name[month], "year": year}, "performance": str(performance / len(employees))}
            for (year, month), performance in metrics_by_month.items()
        ]

        completion_for_today = dashboard[-1]['performance'] if dashboard else "0.00"

        # Формируем ответ через сериализатор
        response_data = {
            "dashboard": [],
            "completionForToday": completion_for_today
        }

        for entry in dashboard:
            metric_serializer = MetricResponseSerializer(data=entry)
            if metric_serializer.is_valid():
                response_data["dashboard"].append(metric_serializer.data)

        return Response(response_data, status=status.HTTP_200_OK)

    def convert_to_date(self, start_period, end_period):
        return (datetime.strptime(f"{start_period['year']}-{start_period['month']}-12", "%Y-%B-%d").date(),
                datetime.strptime(f"{end_period['year']}-{end_period['month']}-12", "%Y-%B-%d").date())

    def get_metric_model(self, metric_type):
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement
        }.get(metric_type)


class TeamIndividualCompetenciesViewSet(viewsets.ViewSet):
    """ ViewSet для получения значений оценки компетенции сотрудника/команды. """

    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        request_serializer = SkillDomenRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            skill_domen = request_serializer.validated_data['skillDomen']
            team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

            competencies = self.get_competencies(team, employee_id, skill_domen)
            data = self.prepare_competency_data(competencies, skill_domen)

            # Возвращаем данные в формате {"data": data}
            return Response({"data": data}, status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_competencies(self, team, employee_id, skill_domen):
        if employee_id is not None:
            # Загружаем только одного сотрудника по его ID
            return EmployeeCompetency.objects.filter(
                employee__id=employee_id,
                employee__teams=team,
                competency__competency_type=skill_domen
            )
        else:
            # Загружаем все компетенции сотрудников команды
            return EmployeeCompetency.objects.filter(
                employee__teams=team,
                competency__competency_type=skill_domen
            )

    def prepare_competency_data(self, competencies, skill_domen):
        data = []
        for competency in competencies:
            data.append({
                "competencyId": competency.competency.id,
                "skillDomen": skill_domen.capitalize(),
                "competencyName": competency.competency.competency_name,
                "plannedResult": str(competency.planned_result),
                "actualResult": f"{competency.actual_result:.1f}"
            })
        return data


class CompetencyLevelViewSet(viewsets.ViewSet):
    """ ViewSet для получения уровня компетенций сотрудников. """

    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Валидация данных запроса
        request_serializer = CompetencyLevelRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Получаем данные из запроса
        competency_id = request_serializer.validated_data['competencyId']
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        # Получаем сотрудников команды
        employees = self.get_employees(team, employee_id)

        # Фильтруем компетенции сотрудников
        employee_competencies = EmployeeCompetency.objects.filter(
            employee__in=employees,
            competency__id=competency_id,
        )

        # Если компетенций нет
        if not employee_competencies.exists():
            return Response({"data": []}, status=status.HTTP_200_OK)

        # Формируем данные для ответа
        data = self.prepare_competency_data(employee_competencies)
        return Response({"data": data}, status=status.HTTP_200_OK)

    def get_employees(self, team, employee_id):
        """ Получаем сотрудников команды, фильтруя по employee_id, если передан. """

        return team.employee.filter(id=employee_id) if employee_id else team.employee.all()

    def prepare_competency_data(self, employee_competencies):
        """ Подготавливаем данные для ответа. """

        data = []
        for emp_competency in employee_competencies:
            data.append({
                "employeeId": emp_competency.employee.id,
                "skillDomen": emp_competency.competency.competency_type.capitalize(),
                "assessment": str(emp_competency.competency_level),
                "color": self.get_color_based_on_assessment(emp_competency.competency_level)
            })
        return data

    def get_color_based_on_assessment(self, competency_level):
        """ Метод для определения цвета в зависимости от уровня компетенции. """

        level = int(competency_level)  # Преобразуем строковый уровень в число

        if level <= 33:
            return "red"
        elif 34 <= level <= 66:
            return "yellow"
        elif level >= 67:
            return "green"
        else:
            raise ValueError(f"Invalid competency level: {competency_level}")


class TeamIndividualSkillsViewSet(viewsets.ViewSet):
    """ ViewSet для получения средних значений навыков сотрудника/команды. """

    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return Response(
                {"error": "Method not allowed."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        if 'employeeIds' in self.request.data:
            employee_id = self.request.data.get('employeeIds')
            # Получаем сотрудников по переданным ID
            employees = Employee.objects.filter(id__in=employee_id)
        request_serializer = SkillDomenRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            skill_domen = request_serializer.validated_data['skillDomen']
            team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

            skills = self.get_skills(team, employee_id, skill_domen)
            data = self.prepare_skill_data(skills, skill_domen, team)

            # Возвращаем данные в формате {"data": data}
            return Response({"data": data}, status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_skills(self, team, employee_id, skill_domen):
        if employee_id is not None:
            # Загружаем только одного сотрудника по его ID
            return EmployeeSkill.objects.filter(
                employee__id__in=employee_id,
                employee__teams=team,
                skill__skill_type=skill_domen
            )
        else:
            # Загружаем все компетенции сотрудников команды
            return EmployeeSkill.objects.filter(
                employee__teams=team,
                skill__skill_type=skill_domen
            )

    def prepare_skill_data(self, skills, skill_domen, team):
        data = []
        for skill in skills:

            planned_avg = EmployeeSkill.objects.filter(skill__id=skill.skill.id
                ).aggregate(Avg('planned_result'))['planned_result__avg'] or 0

            actual_avg = EmployeeSkill.objects.filter(skill__id=skill.skill.id
                ).aggregate(Avg('actual_result'))['actual_result__avg'] or 0

            temp = {
                "skillDomen": skill_domen,
                "skillId": skill.skill.id,
                "skillName": skill.skill.skill_name,
                "plannedResult": round(planned_avg, 2),
                "actualResult": round(actual_avg, 2)
            }
            # Проверка, если в data уже есть элемент с таким же skillId
            if not any(d['skillId'] == temp['skillId'] for d in data):
                data.append(temp)
        return data


class SkillLevelViewSet(viewsets.ViewSet):
    """ ViewSet для получения уровня навыков сотрудников. """

    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Валидация данных запроса
        request_serializer = SkillLevelRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Получаем данные из запроса
        skill_id = request_serializer.validated_data['skillId']
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        # Получаем сотрудников команды
        employees = self.get_employees(team, employee_id)

        # Фильтруем компетенции сотрудников
        employee_skills = EmployeeSkill.objects.filter(
            employee__in=employees,
            skill__id=skill_id,
        )

        # Если компетенций нет
        if not employee_skills.exists():
            return Response({"data": []}, status=status.HTTP_200_OK)

        # Формируем данные для ответа
        data = self.prepare_skill_data(employee_skills)
        return Response({"data": data}, status=status.HTTP_200_OK)

    def get_employees(self, team, employee_id):
        """Получаем сотрудников команды, фильтруя по employee_id, если передан."""

        return team.employee.filter(id=employee_id) if employee_id else team.employee.all()

    def prepare_skill_data(self, employee_skills):
        """Подготавливаем данные для ответа."""

        data = []
        for emp_skill in employee_skills:
            data.append({
                "employeeId": emp_skill.employee.id,
                "skillDomen": emp_skill.skill.skill_type.capitalize(),
                "assessment": str(emp_skill.skill_level),
                "color": self.get_color_based_on_assessment(emp_skill.skill_level)
            })
        return data

    def get_color_based_on_assessment(self, skill_level):
        """ Метод для определения цвета в зависимости от уровня навыка. """

        level = int(skill_level)  # Преобразуем строковый уровень в число

        if level <= 33:
            return "red"
        elif 34 <= level <= 66:
            return "yellow"
        elif level >= 67:
            return "green"
        else:
            raise ValueError(f"Invalid skill level: {skill_level}")
