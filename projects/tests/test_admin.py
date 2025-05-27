from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from projects.models import Department, Employee, Project

User = get_user_model()

class AdminTest(TestCase):
    def setUp(self):
        # Create superuser
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass123')

        # Create test data
        self.department = Department.objects.create(name='Test Department')
        self.employee = Employee.objects.create(
            name='John Doe',
            department=self.department,
            salary=Decimal('50000.00')
        )
        self.project = Project.objects.create(
            project_name='Test Project',
            employee=self.employee
        )

    def test_department_admin_list(self):
        """Test department admin list view"""
        url = reverse('admin:projects_department_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Department')

    def test_employee_admin_list(self):
        """Test employee admin list view"""
        url = reverse('admin:projects_employee_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '50000.00')

    def test_project_admin_list(self):
        """Test project admin list view"""
        url = reverse('admin:projects_project_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'John Doe')

    def test_department_admin_detail(self):
        """Test department admin detail view"""
        url = reverse('admin:projects_department_change', args=[self.department.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Department')

    def test_employee_admin_detail(self):
        """Test employee admin detail view"""
        url = reverse('admin:projects_employee_change', args=[self.employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '50000.00')

    def test_project_admin_detail(self):
        """Test project admin detail view"""
        url = reverse('admin:projects_project_change', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_department_admin_search(self):
        """Test department admin search"""
        url = reverse('admin:projects_department_changelist')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Department')

    def test_employee_admin_search(self):
        """Test employee admin search"""
        url = reverse('admin:projects_employee_changelist')
        response = self.client.get(url, {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_project_admin_search(self):
        """Test project admin search"""
        url = reverse('admin:projects_project_changelist')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project') 