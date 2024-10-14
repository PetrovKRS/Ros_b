from django.test import TestCase
from core.models import Employee, Skill, EmployeeSkill, DevelopmentPlan

class EmployeeModelTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            status="active"
        )

    def test_employee_string_representation(self):
        self.assertEqual(str(self.employee), "John Doe ({})".format(self.employee.employee_id))
class SkillModelTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(skill_name='Python')

    def test_skill_string_representation(self):
        self.assertEqual(str(self.skill), 'Python')

class EmployeeSkillModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name='Jane',
            last_name='Doe',
            employee_id='E456'
        )
        self.skill = Skill.objects.create(skill_name='Django')
        self.employee_skill = EmployeeSkill.objects.create(
            employee=self.employee,
            skill=self.skill,
            skill_level='Expert'
        )

    def test_employee_skill_string_representation(self):
        self.assertEqual(str(self.employee_skill), "Jane Doe - Django (Expert)")
