from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,  # Delete employee when user is deleted
        related_name='employee_profiles'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,  # Prevent deletion of departments with employees
        related_name='employees'
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Employee's annual salary"
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.department})"

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name_plural = 'Employees'


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,  # Set to NULL if employee is deleted
        null=True,
        related_name='assigned_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('ON_HOLD', 'On Hold')
        ],
        default='PENDING'
    )

    def __str__(self):
        return f"{self.project_name} - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']
