from django.template.defaultfilters import length
from django.db.models import Avg
from rest_framework import serializers
from users.models import ManagerTeam
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, SkillTypeEnum, Employee, EmployeeAssesmentSkill,
)
from django.urls import reverse
from rest_framework.validators import UniqueTogetherValidator


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Дополнительные данные, которые вы хотите включить в токен
#         token['email'] = user.email  # Например, добавление email в токен

#         return token




class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'employee_id', 'first_name', 'patronymic', 'position'
        )


class CompetencySerializer(serializers.ModelSerializer):
    """ Сериализатор для компетенций сотрудника. """

    competency = serializers.CharField(source='competency.competency_name')

    class Meta:
        model = EmployeeCompetency
        fields = (
            'competency', 'competency_level'
        )
        
class TrainingApplicationSerializer(serializers.ModelSerializer):
    """ Сериализатор для заявок на обучение. """

    training_name = serializers.CharField(source='training_application.training_name')

    class Meta:
        model = EmployeeTrainingApplication
        fields = (
            'id', 'training_name',  # Указываем правильное поле через связь
        )
        

class AssesmentOfPotentionSerializer(serializers.Serializer):
    """ Сериализатор для оценки потенциала сотрудника. """
    assesmentLevel = serializers.SerializerMethodField()
    involvmentLevel = serializers.IntegerField(
        source='engagements.performance_score', default=0)

    def get_assesmentLevel(self, obj):
        average_assessment = obj.assesments_skills.aggregate(Avg('assesment'))['assesment__avg']
        # Если есть средняя оценка, возвращаем её, иначе возвращаем 0
        return average_assessment if average_assessment is not None else 0


class EmployeeSerializer(serializers.ModelSerializer):
    """ Основной сериализатор для сотрудников. """

    worker = serializers.SerializerMethodField()
    position = serializers.CharField(
        source='positions.position.position_name', allow_null=True
    )
    grade = serializers.CharField(
        source='grades.grade.grade_name',
    )
    assesmentOfPotention = AssesmentOfPotentionSerializer(source='*') 

    key_people = serializers.SerializerMethodField()
    bus_factor = serializers.SerializerMethodField()
    education = TrainingApplicationSerializer(source='training_applications', many=True)
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id', 'position', 'worker', 'grade', 'key_people',
            'bus_factor', 'education', 'assesmentOfPotention', 'skill',
        )

    def get_worker(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_skill(self, obj):
        """ Рассчитывает средний уровень навыков сотрудника. """
        skills = obj.skills.all()  # Получаем все связанные навыки
        if not skills:
            return 0  # Если навыков нет, возвращаем 0

        total_skill_level = sum(employee_skill.skill_level for employee_skill in skills)
        average_level = total_skill_level / len(skills)
        return average_level

    # Проверка наличия записи в EmployeeKeyPeople
    def get_key_people(self, obj):
        return EmployeeKeyPeople.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeBusFactor
    def get_bus_factor(self, obj):
        return EmployeeBusFactor.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeTrainingApplication (образование)
    def get_education(self, obj):
        return EmployeeTrainingApplication.objects.filter(employee=obj).exists()


class MetricRequestSerializer(serializers.Serializer):
    employeeIds = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    startPeriod = serializers.DateField(required=True)
    endPeriod = serializers.DateField(required=True)


class IndividualDevelopmentPlanRequestSerializer(serializers.Serializer):

    startPeriod = serializers.DictField(
        child=serializers.CharField(),
        required=True
    )
    endPeriod = serializers.DictField(
        child=serializers.CharField(),
        required=True
    )


class IndividualDevelopmentPlanResponseSerializer(serializers.Serializer):
    dashboard = serializers.ListField(
        child=serializers.DictField()
    )
    completionForToday = serializers.CharField()


class TeamMetricsRequestSerializer(serializers.Serializer):
    startPeriod = serializers.DictField(
        child=serializers.CharField()
    )
    endPeriod = serializers.DictField(
        child=serializers.CharField()
    )


class SkillDomenRequestSerializer(serializers.Serializer):
    skillDomen = serializers.ChoiceField(
        choices=SkillTypeEnum.choices(),
        help_text="Тип навыка: hard или soft"
    )
    
    
class CompetencySerializer(serializers.Serializer):
    competencyId = serializers.IntegerField()
    skillDomen = serializers.CharField()
    competencyName = serializers.CharField()
    plannedResult = serializers.FloatField()
    actualResult = serializers.FloatField()
    

class CompetencyLevelRequestSerializer(serializers.Serializer):
    competencyId = serializers.IntegerField()


class MetricResponseSerializer(serializers.Serializer):
    period = serializers.DictField()
    performance = serializers.CharField()
    
    
class TeamMetricsResponseSerializer(serializers.Serializer):
    period = serializers.DictField(child=serializers.CharField())
    numberOfEmployee = serializers.CharField()
    numberOfBusFactor = serializers.CharField()
    numberOfKeyPeople = serializers.CharField()


class SkillSerializer(serializers.ModelSerializer):
    skillId = serializers.IntegerField(source='id')
    skillName = serializers.CharField(source='skill_name')
    plannedResult = serializers.FloatField()
    actualResult = serializers.FloatField()

    class Meta:
        model = Skill
        fields = ['skillId', 'skillName', 'plannedResult', 'actualResult']


class TeamSkillSerializer(serializers.Serializer):
    numberOfEmployee = serializers.CharField(max_length=10)
    numberOfBusFactor = serializers.CharField(max_length=10)
    numberOfKeyPeople = serializers.CharField(max_length=10)


class IndividualSkillAverageSerializer(serializers.Serializer):
    skillDomen = serializers.CharField()
    skillId = serializers.IntegerField()
    skillName = serializers.CharField()
    plannedResult = serializers.FloatField()
    actualResult = serializers.FloatField()

class SkillLevelRequestSerializer(serializers.Serializer):
    skillId = serializers.IntegerField()
