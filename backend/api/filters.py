# from django_filters import rest_framework as filters
# from users.models import Employee


# class EmployeeFilter(filters.FilterSet):
#     position = filters.CharFilter(
#         field_name='positions__position__position_name',
#         lookup_expr='exact'
#     )
#     grade = filters.CharFilter(
#         field_name='grades__grade__grade_name',
#         lookup_expr='exact'
#     )
#     skill = filters.CharFilter(
#         field_name='skills__skill__skill_name',
#         lookup_expr='exact'
#     )
#     competency = filters.CharFilter(
#         field_name='competencies__competency__competency_name'
#     )

#     class Meta:
#         model = Employee
#         fields = (
#             'position', 'grade', 'skill', 'competency'
#         )
