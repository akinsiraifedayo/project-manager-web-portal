from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from decimal import Decimal
from projects.models import Department, Employee, Project

User = get_user_model()

class DepartmentModelTest(TestCase):
    def test_department_creation(self):
        """Test creating a department"""
        dept = Department.objects.create(name='Test Department')
        self.assertEqual(str(dept), 'Test Department')
        self.assertEqual(dept.name, 'Test Department')

    def test_department_unique_name(self):
        """Test that department names must be unique"""
        Department.objects.create(name='Test Department')
        with self.assertRaises(IntegrityError):
            Department.objects.create(name='Test Department')

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Test Department')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_employee_creation(self):
        """Test creating an employee"""
        employee = Employee.objects.create(
            name='John Doe',
            department=self.department,
            salary=Decimal('50000.00')
        )
        self.assertEqual(str(employee), 'John Doe (Test Department)')
        self.assertEqual(employee.name, 'John Doe')
        self.assertEqual(employee.department, self.department)
        self.assertEqual(employee.salary, Decimal('50000.00'))

    def test_employee_user_link(self):
        """Test linking an employee to a user"""
        employee = Employee.objects.create(
            name='John Doe',
            department=self.department,
            salary=Decimal('50000.00'),
            user=self.user
        )
        self.assertEqual(employee.user, self.user)

    def test_employee_department_protection(self):
        """Test that departments cannot be deleted when they have employees"""
        Employee.objects.create(
            name='John Doe',
            department=self.department,
            salary=Decimal('50000.00')
        )
        with self.assertRaises(IntegrityError):
            self.department.delete()

class ProjectModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Test Department')
        self.employee = Employee.objects.create(
            name='John Doe',
            department=self.department,
            salary=Decimal('50000.00')
        )

    def test_project_creation(self):
        """Test creating a project"""
        project = Project.objects.create(
            project_name='Test Project',
            description='Test Description',
            employee=self.employee
        )
        self.assertEqual(str(project), 'Test Project - Pending')
        self.assertEqual(project.project_name, 'Test Project')
        self.assertEqual(project.employee, self.employee)
        self.assertEqual(project.status, 'PENDING')

    def test_project_status_choices(self):
        """Test project status choices"""
        project = Project.objects.create(
            project_name='Test Project',
            employee=self.employee
        )
        valid_statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'ON_HOLD']
        self.assertIn(project.status, valid_statuses)

    def test_project_employee_null(self):
        """Test that project can exist without an employee"""
        project = Project.objects.create(
            project_name='Test Project',
            description='Test Description'
        )
        self.assertIsNone(project.employee)

    def test_project_timestamps(self):
        """Test that timestamps are automatically set"""
        project = Project.objects.create(
            project_name='Test Project',
            employee=self.employee
        )
        self.assertIsNotNone(project.created_at)
        self.assertIsNotNone(project.updated_at) 