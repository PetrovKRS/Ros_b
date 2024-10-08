# Generated by Django 4.2 on 2024-10-04 08:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('employee_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='E-mail')),
                ('status', models.CharField(max_length=50)),
                ('registration_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата регистрации сотрудника')),
                ('last_login_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата последнего входа сотрудника')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BusFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_factor_name', models.CharField(max_length=255, verbose_name='Название Bus фактора')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с этим Bus фактором')),
            ],
        ),
        migrations.CreateModel(
            name='Competency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency_name', models.CharField(max_length=255, verbose_name='Название компетенции')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с данной компетенцией')),
            ],
        ),
        migrations.CreateModel(
            name='DevelopmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=255, unique=True, verbose_name='Название плана')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Кол-во сотрудников с планом развития')),
            ],
        ),
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engagement_name', models.CharField(max_length=255, verbose_name='Название вовлеченности')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество вовлеченных сотрудников')),
            ],
        ),
        migrations.CreateModel(
            name='ExpectedSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_skill_name', models.CharField(max_length=255, verbose_name='Название ожидаемого навыка')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с данным ожидаемым навыком')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_name', models.CharField(max_length=255, verbose_name='Название грейда')),
            ],
        ),
        migrations.CreateModel(
            name='KeyPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_people_name', models.CharField(max_length=255, verbose_name='Название key people')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников Key People')),
            ],
        ),
        migrations.CreateModel(
            name='KeySkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=255, verbose_name='Название ключевого навыка')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с данным ключевым навыком')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=255, unique=True, verbose_name='Название должности')),
                ('grade_count', models.IntegerField(default=0, verbose_name='Количество грейдов, связанных с должностью')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=255, verbose_name='Название навыка')),
                ('employee_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255, verbose_name='Название команды')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_name', models.CharField(max_length=255, verbose_name='Название обучения')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников на обучении')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.position')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.team')),
            ],
        ),
        migrations.CreateModel(
            name='SkillForCompetency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.competency')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.skill')),
            ],
        ),
        migrations.CreateModel(
            name='PositionCompetency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.competency')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.position')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTrainingApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('training_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.trainingapplication')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.team')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.CharField(max_length=255, verbose_name='Уровень навыка сотрудника')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.skill')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.position')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeKeySkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.CharField(max_length=255, verbose_name='Уровень ключевого навыка сотрудника')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('key_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.keyskill')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeKeyPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('key_people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.keypeople')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.grade')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeExpectedSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('expected_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.expectedskill')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeEngagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engagement_level', models.IntegerField(verbose_name='Уровень вовлеченности сотрудника')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('engagement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.engagement')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDevelopmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('development_progress', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Процент развития')),
                ('development_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.developmentplan')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeCompetency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency_level', models.CharField(max_length=255, verbose_name='Уровень компетенции сотрудника')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.competency')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeBusFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.busfactor')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompetencyForExpectedSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.competency')),
                ('expected_skill', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.expectedskill')),
            ],
        ),
    ]
