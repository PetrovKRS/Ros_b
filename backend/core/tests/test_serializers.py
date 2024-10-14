from rest_framework import serializers
from django.test import TestCase
from core.models import Employee, Skill, EmployeeSkill
from api.serializers import EmployeeSerializer, SkillSerializer

class EmployeeSerializerTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )
        self.serializer = EmployeeSerializer(instance=self.employee)

    def test_employee_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'position', 'worker', 'grade', 'key_people',
            'bus_factor', 'education', 'skills','competencies'})

class SkillSerializerTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(first_name='Jane', last_name='Doe', email='jane.doe@example.com', status='active')
        self.skill = Skill.objects.create(skill_name='Django')
        self.employee_skill = EmployeeSkill.objects.create(employee=self.employee, skill=self.skill, skill_level='Expert')
        self.serializer = SkillSerializer(instance=self.employee_skill)

    def test_skill_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'skill', 'skill_level'})