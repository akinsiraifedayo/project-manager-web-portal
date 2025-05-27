from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.db.models import Count
from projects.models import Department, Employee, Project


class PopulateDataTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_populate_data_command(self):
        """Test the populate_data command creates all required records"""
        # Run the command
        call_command('populate_data', stdout=self.out)
        
        # Check the output
        self.assertIn('Departments created successfully', self.out.getvalue())
        self.assertIn('Employees and Users created successfully', self.out.getvalue())
        self.assertIn('Projects created successfully', self.out.getvalue())

        # Verify departments
        departments = Department.objects.all()
        self.assertEqual(departments.count(), 3)
        self.assertTrue(departments.filter(name='Legal').exists())
        self.assertTrue(departments.filter(name='IT').exists())
        self.assertTrue(departments.filter(name='Finance').exists())

        # Verify employees
        employees = Employee.objects.all()
        self.assertEqual(employees.count(), 7)
        
        # Check specific employees
        alice = Employee.objects.get(name='Alice Johnson')
        self.assertEqual(alice.department.name, 'Legal')
        self.assertEqual(alice.salary, 60000.00)

        charlie = Employee.objects.get(name='Charlie Daniels')
        self.assertEqual(charlie.department.name, 'IT')
        self.assertEqual(charlie.salary, 80000.00)

        # Verify projects
        projects = Project.objects.all()
        self.assertEqual(projects.count(), 7)

        # Check employees with multiple projects
        employees_with_projects = Employee.objects.annotate(
            project_count=Count('assigned_projects')
        ).filter(project_count__gt=1)
        
        self.assertEqual(employees_with_projects.count(), 3)
        
        # Check specific project assignments
        diana = Employee.objects.get(name='Diana Ross')
        self.assertEqual(diana.assigned_projects.count(), 2)
        self.assertTrue(
            diana.assigned_projects.filter(
                project_name__in=['Budget Review', 'Internal Audit']
            ).exists()
        )

    def test_idempotency(self):
        """Test that running the command multiple times doesn't create duplicates"""
        # Run command twice
        call_command('populate_data', stdout=self.out)
        call_command('populate_data', stdout=self.out)

        # Verify counts remain the same
        self.assertEqual(Department.objects.count(), 3)
        self.assertEqual(Employee.objects.count(), 7)
        self.assertEqual(Project.objects.count(), 7)

    def test_data_relationships(self):
        """Test that all relationships are correctly established"""
        call_command('populate_data', stdout=self.out)

        # Test IT department and its employees
        it_dept = Department.objects.get(name='IT')
        it_employees = it_dept.employees.all()
        self.assertEqual(it_employees.count(), 3)
        self.assertTrue(
            it_employees.filter(name__in=['Bob Smith', 'Charlie Daniels']).exists()
        )

        # Test project assignments for Charlie Daniels
        charlie = Employee.objects.get(name='Charlie Daniels')
        charlie_projects = charlie.assigned_projects.all()
        self.assertEqual(charlie_projects.count(), 2)
        self.assertTrue(
            charlie_projects.filter(
                project_name__in=['Data Migration', 'Security Enhancement']
            ).exists()
        ) 