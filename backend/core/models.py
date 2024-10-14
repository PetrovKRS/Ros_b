from enum import Enum
from wsgiref.validate import validator

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.formats import date_format
from django.views.decorators.http import condition
from django_filters.utils import verbose_field_name
from social_core.utils import first

from users.models import ManagerTeam
import uuid

class Employee(models.Model):
    """ Модель сотрудника. """

    employee_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False,  # Поле не должно редактироваться
        default=uuid.uuid4,  # Генерация уникального идентификатора
    )
    first_name = models.CharField(
        max_length=21,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=21,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name='E-mail'
    )
    status = models.CharField(
        max_length=50
    )
    registration_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата регистрации сотрудника'
    )
    last_login_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата последнего входа сотрудника',
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = (
            'first_name',
            'last_name',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('employee_id', 'email'),
                name='unique_first_name_email',
                violation_error_message='Сотрудник с таким именем и почтой уже существует.'
            ),
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"


class AssesmentSkill(models.Model):
    assesmentskill_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название оценки',
    )

    class Meta:
        verbose_name = 'Оценка навыка'
        verbose_name_plural = 'Оценки навыков'
        ordering = (
            'assesmentskill_name',
        )


class EmployeeAssesmentSkill(models.Model):
    """ Модель -Оценка сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='assesments_skills',
    )
    assesmentskill = models.ForeignKey(
        AssesmentSkill,
        on_delete=models.CASCADE,
        verbose_name='Оценка навыка сотрудника',
    )
    assesment = models.IntegerField(
        default=0,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100)
        ),
        verbose_name='Оценка навыка сотрудника',
    )

    class Meta:
        verbose_name = 'Оценка навыка сотрудника'
        verbose_name_plural = 'Оценки навыков сотрудников'
        ordering = (
        'employee',
    )


class DevelopmentPlan(models.Model):
    """ Модель -План развития-."""

    plan_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название плана',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Кол-во сотрудников с планом развития',
    )


    class Meta:
        verbose_name = 'План развития'
        verbose_name_plural = 'Планы развития'
        ordering = (
            'plan_name',
        )

    def __str__(self):
        return self.plan_name


class EmployeeDevelopmentPlan(models.Model):
    """ Модель -План развития сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='development_plans',
    )
    development_plan = models.ForeignKey(
        DevelopmentPlan,
        on_delete=models.CASCADE,
        verbose_name='План развития',
    )
    performance_score = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(10)
        ),
        verbose_name='Процент развития',
    )
    add_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления сотрудника в план развития',
    )

    class Meta:
        verbose_name = 'План развития сотрудника'
        verbose_name_plural = 'Планы развития сотрудников'
        ordering = (
            'development_plan',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('employee', 'development_plan'),
                name='unique_employee_development_plan'
            ),
        )

    def __str__(self):
        return f"{self.employee} - {self.development_plan}"
    

class Engagement(models.Model):
    """ Модель -Вовлеченность-. """

    engagement_name = models.CharField(
        max_length=255,
        verbose_name='Название вовлеченности',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество вовлеченных сотрудников',
    )

    class Meta:
        verbose_name = 'Вовлеченность'
        verbose_name_plural = 'Вовлеченности'
        ordering = (
            'engagement_name',
        )

    def __str__(self):
        return self.engagement_name


class EmployeeEngagement(models.Model):
    """ Модель -Вовлеченность сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='engagements',
    )
    engagement = models.ForeignKey(
        Engagement,
        on_delete=models.CASCADE,
        related_name='employee_engagements',
        verbose_name='Вовлеченность',
    )
    performance_score = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(10)
        ),
        verbose_name='Уровень вовлеченности сотрудника',
    )
    add_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата вовлечения сотрудника',
    )

    class Meta:
        verbose_name = 'Вовлеченность сотрудника'
        verbose_name_plural = 'Вовлеченность сотрудников'
        ordering = (
            'performance_score',
        )

    def __str__(self):
        return f"{self.employee} - {self.engagement}"
    

class KeyPeople(models.Model):
    """ Модель -Key People-. """

    key_people_name = models.CharField(
        max_length=255,
        verbose_name='Название key people',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников Key People'
    )

    class Meta:
        verbose_name = 'Key people'
        verbose_name_plural = "Key people's"
        ordering = (
            'key_people_name',
        )

    def __str__(self):
        return self.key_people_name


class EmployeeKeyPeople(models.Model):
    """ Модель -Key People сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='keys_people',
    )
    key_people = models.ForeignKey(
        KeyPeople,
        on_delete=models.CASCADE,
        verbose_name='Key people',
    )
    add_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления ключевого сотрудника',
    )

    class Meta:
        verbose_name = 'Key People сотрудника'
        verbose_name_plural = 'Key People сотрудников'
        ordering = (
            'key_people',
        )

    def __str__(self):
        return f"{self.employee} - {self.key_people}"
    

class TrainingApplication(models.Model):
    """ Модель -Заявка на обучение-. """

    training_name = models.CharField(
        max_length=255,
        verbose_name='Название обучения',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников на обучении',
    )

    class Meta:
        verbose_name = 'Заявка на обучение'
        verbose_name_plural = 'Заявки на обучение'
        ordering = (
            'training_name',
        )

    def __str__(self):
        return self.training_name


class EmployeeTrainingApplication(models.Model):
    """ Модель -Заявка на обучение сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='training_applications',
    )
    training_application = models.ForeignKey(
        TrainingApplication,
        on_delete=models.CASCADE,
        verbose_name='Заявка на обучение',
    )
    add_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления заявки на обучение',
    )

    class Meta:
        verbose_name = 'Заявка на обучение сотрудника'
        verbose_name_plural = 'Заявки на обучение сотрудников'
        ordering = (
            'training_application',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('employee', 'training_application'),
                name='unique_employee_training_application'
            ),
        )

    def __str__(self):
        return f"{self.employee} - {self.training_application}"    
    

class BusFactor(models.Model):
    """ # Модель -Bus Фактор-. """

    bus_factor_name = models.CharField(
        max_length=255,
        verbose_name='Название Bus фактора',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с этим Bus фактором',
    )

    class Meta:
        verbose_name = 'Bus Фактор'
        verbose_name_plural = 'Bus Факторы'
        ordering = (
            'bus_factor_name',
        )

    def __str__(self):
        return self.bus_factor_name


class EmployeeBusFactor(models.Model):
    """ Модель -Bus Фактор сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='bus_factors',
    )
    bus_factor = models.ForeignKey(
        BusFactor,
        on_delete=models.CASCADE,
        verbose_name='Bus фактор',
    )
    add_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления bud-фактора сотрудника',
    )

    class Meta:
        verbose_name = 'Bus Фактор сотрудника'
        verbose_name_plural = 'Bus Факторы сотрудников'
        ordering = (
            'bus_factor',
        )

    def __str__(self):
        return f"{self.employee} - {self.bus_factor}"
    

class GradeTypeEnum(Enum):
    JUNIOR = 'junior'
    MIDDLE = 'middle'
    SENIOR = 'senior'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]


class Grade(models.Model):
    """ Модель -Класс-. """

    grade_name = models.CharField(
        max_length=255,
        verbose_name='Название класса',
    )
    grade_type = models.CharField(
        max_length=100,
        choices=GradeTypeEnum.choices(),
        default=GradeTypeEnum.JUNIOR,
        verbose_name='Тип класса',
    )

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = (
            'grade_name',
        )

    def __str__(self):
        return self.grade_name


class EmployeeGrade(models.Model):
    """ Модель -Класс сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='grades',
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        verbose_name='Класс',
    )

    class Meta:
        verbose_name = 'Класс сотрудника'
        verbose_name_plural = 'Классы сотрудников'
        ordering = (
            'grade',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('employee', 'grade'),
                name='unique_employee_grade'
            ),
        )

    def __str__(self):
        return f"{self.employee} - {self.grade}"


class KeySkill(models.Model):
    """ Модель -Ключевой навык-. """

    skill_name = models.CharField(
        max_length=255,
        verbose_name='Название ключевого навыка',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данным ключевым навыком',
    )

    class Meta:
        verbose_name = 'Ключевой навык'
        verbose_name_plural = 'Ключевые навыки'
        ordering = (
            'skill_name',
        )

    def __str__(self):
        return self.skill_name


class EmployeeKeySkill(models.Model):
    """ Модель -Ключевой навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='key_skills',
    )
    key_skill = models.ForeignKey(
        KeySkill,
        on_delete=models.CASCADE,
        verbose_name='Ключевой навык',
    )
    skill_level = models.CharField(
        max_length=255,
        verbose_name='Уровень ключевого навыка сотрудника',
    )
    add_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления ключевого навыка сотрудника',
    )

    class Meta:
        verbose_name = 'Ключевой навык сотрудника'
        verbose_name_plural = 'Ключевые навыки сотрудников'
        ordering = (
            'key_skill',
        )

    def __str__(self):
        return f"{self.employee} - {self.key_skill} ({self.skill_level})"


class Team(models.Model):
    """ Модель команды. """

    team_name = models.CharField(
        max_length=255,
        verbose_name='Название команды',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Слаг команды',
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.team_name


class EmployeeTeam(models.Model):
    """ Модель -Команда сотрудника-. """

    manager  = models.ForeignKey(
        ManagerTeam,
        on_delete=models.CASCADE,
        related_name='teams',
        verbose_name='Менеджер команды',
    )
    employee = models.ManyToManyField(
        Employee,
        related_name='teams',
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name='Команда',
    )

    class Meta:
        verbose_name = 'Команда сотрудника'
        verbose_name_plural = 'Команды сотрудников'
        ordering = (
            'team',
        )

    def __str__(self):
        return f"{self.employee} - {self.team}"


class Position(models.Model):
    """ Модель -Должность-. """

    position_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название должности',
    )
    grade_count = models.IntegerField(
        default=0,
        verbose_name='Количество грейдов, связанных с должностью'
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = (
            'position_name',
        )

    def __str__(self):
        return self.position_name


class PositionGrade(models.Model):

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='position_grades',
        verbose_name='Должность',
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='grade_positions',
        verbose_name='Грейд',
    )
    ate_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления грейда к должности'
    )

    class Meta:
        verbose_name = 'Грейд сотрудника'
        verbose_name_plural = 'Грейды сотрудников'
        ordering = (
            'position',
        )

    def __str__(self):
        return f"{self.employee} - {self.position} ({self.grade})"


class EmployeePosition(models.Model):
    """ Модель -Должность сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='positions',
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name='Должность',
    )

    class Meta:
        verbose_name = 'Должность сотрудника'
        verbose_name_plural = 'Должности сотрудников'
        ordering = (
            'position',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('employee', 'position'),
                name='unique_employee_position'
            ),
        )

    def __str__(self):
        return f"{self.employee} - {self.position}"


class SkillTypeEnum(Enum):
    HARD = 'hard'
    SOFT = 'soft'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]


class Competency(models.Model):
    """ Модель -Компетенция-. """

    competency_name = models.CharField(
        max_length=255,
        verbose_name='Название компетенции',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данной компетенцией'
    )
    competency_type = models.CharField(
        max_length=100,
        choices=SkillTypeEnum.choices(),
        default=SkillTypeEnum.HARD,
        verbose_name='Тип компетенции',
    )

    class Meta:
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'
        ordering = (
            'competency_name',
        )

    def __str__(self):
        return self.competency_name


class PositionCompetency(models.Model):
    """ Модель -Должность к компетенции-. """

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='competencies',
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Должность к компетенции'
        verbose_name_plural = 'Должности к компетенциям'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'position',
                    'competency'
                ),
                name='unique_position_competency'
            ),
        )

    def __str__(self):
        return f"{self.position} - {self.competency}"


class TeamPosition(models.Model):
    """ Модель -Должность для команды-. """

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Должность для команды'
        verbose_name_plural = 'Должности для команд'
        ordering = (
            'team',
        )

    def __str__(self):
        return f"{self.team} - {self.position}"


class EmployeeCompetency(models.Model):
    """ Модель -Компетенция сотрудника-. """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='employee_competencies',
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
        verbose_name='Компетенция',
    )
    competency_level = models.CharField(
        max_length=255,
        verbose_name='Уровень компетенции сотрудника',
    )
    planned_result = models.FloatField(
        default=0.0,
        verbose_name='Плановая оценка',
    )
    actual_result = models.FloatField(
        default=0.0,
        verbose_name='Фактическая оценка',
    )

    class Meta:
        verbose_name = 'Компетенция сотрудника'
        verbose_name_plural = 'Компетенции сотрудников'
        ordering = ('competency',)
        constraints = (
            models.UniqueConstraint(
                fields=('employee', 'competency'),
                name='unique_employee_competency'
            ),
        )

    def __str__(self):
        return f"{self.employee} - {self.competency} ({self.competency_level})"
    



class Skill(models.Model):
    """ Модель -Навык- с выбором типа навыка (hard или soft). """

    skill_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название навыка',
    )
    skill_type = models.CharField(
        max_length=4,
        choices=SkillTypeEnum.choices(),
        default=SkillTypeEnum.HARD,
        verbose_name='Тип навыка',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данным навыком',
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = (
            'skill_name',
        )

    def __str__(self):
        return f'{self.skill_name} ({self.skill_type})'


class EmployeeSkill(models.Model):
    """ Модель -Навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='skills',
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Навык',
    )
    skill_level = models.IntegerField(
        default=0,
        verbose_name='Уровень навыка сотрудника',
    )
    planned_result = models.FloatField(
        default=0.0,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(5)
        ),
        verbose_name='Плановая оценка',
    )
    actual_result = models.FloatField(
        default=0.0,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(5)
        ),
        verbose_name='Фактическая оценка',
    )

    class Meta:
        verbose_name = 'Навык сотрудника'
        verbose_name_plural = 'Навыки сотрудников'
        ordering = (
            'skill',
        )
        constraints = (
            models.UniqueConstraint(
                fields=('employee', 'skill'),
                name='unique_employee_skill'
            ),
        )

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.skill.skill_name} ({self.skill_level})"


class SkillForCompetency(models.Model):
    """ Модель -Навык для компетенции-. """

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Навык для компетенции'
        verbose_name_plural = 'Навыки для компетенций'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'skill',
                    'competency'
                ),
                name='unique_skill_competency'
            ),
        )

    def __str__(self):
        return f"{self.skill} - {self.competency}"
    

class ExpectedSkill(models.Model):
    """ Модель -Ожидаемый навык-. """

    expected_skill_name = models.CharField(
        max_length=255,
        verbose_name='Название ожидаемого навыка',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данным ожидаемым навыком',
    )

    class Meta:
        verbose_name = 'Ожидаемый навык'
        verbose_name_plural = 'Ожидаемые навыки'
        ordering = (
            'expected_skill_name',
        )

    def __str__(self):
        return self.expected_skill_name


class EmployeeExpectedSkill(models.Model):
    """ Модель -Ожидаемый навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='expected_skills',
    )
    expected_skill = models.ForeignKey(
        ExpectedSkill,
        on_delete=models.CASCADE,
        verbose_name='Ожидаемый навык',
    )

    class Meta:
        verbose_name = 'Ожидаемый навык сотрудника'
        verbose_name_plural = 'Ожидаемые навыки сотрудниов'
        ordering = (
            'expected_skill',
        )

    def __str__(self):
        return f"{self.employee} - {self.expected_skill} ({self.skill_level})"


class CompetencyForExpectedSkill(models.Model):
    """ Модель -Компетенция для ожидаемого навыка-. """

    expected_skill = models.OneToOneField(
        ExpectedSkill,
        on_delete=models.CASCADE,
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Компетенция для ожидаемого навыка'
        verbose_name_plural = 'Компетенции для ожидаемых навыков'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'expected_skill',
                    'competency'
                ),
                name='unique_expected_skill_competency'
            ),
        )

    def __str__(self):
        return f"{self.expected_skill} - {self.competency}"

