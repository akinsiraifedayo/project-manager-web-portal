from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from projects.models import Department, Employee, Project
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data from the requirements'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database...')

        # Create Departments
        departments_data = [
            {'name': 'Legal'},
            {'name': 'IT'},
            {'name': 'Finance'},
        ]

        for dept_data in departments_data:
            Department.objects.get_or_create(
                name=dept_data['name']
            )
        self.stdout.write(self.style.SUCCESS('Departments created successfully'))

        # Create Employees and Users
        employees_data = [
            {
                'name': 'Ifedayo Akinsira',
                'department_name': 'IT',
                'salary': '100000.00',
                'email': 'akinsiraolympicson@gmail.com',
                'is_admin': True
            },
            {'name': 'Alice Johnson', 'department_name': 'Legal', 'salary': '60000.00'},
            {'name': 'Bob Smith', 'department_name': 'IT', 'salary': '75000.00'},
            {'name': 'Charlie Daniels', 'department_name': 'IT', 'salary': '80000.00'},
            {'name': 'Diana Ross', 'department_name': 'Finance', 'salary': '50000.00'},
            {'name': 'Ethan Ray', 'department_name': 'Legal', 'salary': '62000.00'},
            {'name': 'Fiona Lee', 'department_name': 'Finance', 'salary': '55000.00'},
        ]

        for emp_data in employees_data:
            department = Department.objects.filter(
                name=emp_data['department_name']
            ).first()
            
            if department:
                # Split name into first and last name
                name_parts = emp_data['name'].split()
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:])
                
                # Create user with lowercase username
                username = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}"
                
                # Use provided email if available, otherwise generate one
                email = emp_data.get('email', f"{username}@example.com")
                
                user, _ = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'is_staff': emp_data.get('is_admin', False),
                        'is_superuser': emp_data.get('is_admin', False)
                    }
                )
                # Set password
                user.set_password('userpassword123')
                # Ensure admin status is set even if user already existed
                if emp_data.get('is_admin', False):
                    user.is_staff = True
                    user.is_superuser = True
                user.save()

                # Create or update employee
                employee, created = Employee.objects.get_or_create(
                    name=emp_data['name'],
                    defaults={
                        'department': department,
                        'salary': Decimal(emp_data['salary']),
                        'user': user
                    }
                )
                
                if not created:
                    employee.user = user
                    employee.save()
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Department {emp_data['department_name']} not found for employee {emp_data['name']}"
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('Employees and Users created successfully'))

        # Create Projects
        projects_data = [
            {'project_name': 'CMS Upgrade', 'employee_name': 'Bob Smith'},
            {'project_name': 'Data Migration', 'employee_name': 'Charlie Daniels'},
            {'project_name': 'Budget Review', 'employee_name': 'Diana Ross'},
            {'project_name': 'Internal Audit', 'employee_name': 'Diana Ross'},
            {'project_name': 'Security Enhancement', 'employee_name': 'Charlie Daniels'},
            {'project_name': 'Legal Case Automation', 'employee_name': 'Alice Johnson'},
            {'project_name': 'Compliance Tracker', 'employee_name': 'Alice Johnson'},
        ]

        for proj_data in projects_data:
            employee = Employee.objects.filter(
                name=proj_data['employee_name']
            ).first()
            
            if employee:
                Project.objects.get_or_create(
                    project_name=proj_data['project_name'],
                    defaults={
                        'employee': employee,
                        'description': f"Sample project assigned to {employee.name}"
                    }
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Employee {proj_data['employee_name']} not found for project {proj_data['project_name']}"
                    )
                )

        self.stdout.write(self.style.SUCCESS('Projects created successfully'))
        self.stdout.write(self.style.SUCCESS('All data has been populated successfully!')) 