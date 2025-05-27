from django.contrib import admin
from django.db.models import Count, Sum
from .models import Department, Employee, Project


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_count', 'total_salary')
    search_fields = ('name',)

    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Number of Employees'

    def total_salary(self, obj):
        total = obj.employees.aggregate(total=Sum('salary'))['total']
        return f"${total:,.2f}" if total else "$0.00"
    total_salary.short_description = 'Total Salary'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            employee_count=Count('employees'),
            total_salary=Sum('employees__salary')
        )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'department', 'salary', 'project_count', 'user_link')
    list_filter = ('department',)
    search_fields = ('user__first_name', 'user__last_name', 'department__name')
    raw_id_fields = ('user',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'
    get_full_name.admin_order_field = 'user__first_name'

    def project_count(self, obj):
        return obj.assigned_projects.count()
    project_count.short_description = 'Number of Projects'

    def user_link(self, obj):
        if obj.user:
            return obj.user.username
        return '-'
    user_link.short_description = 'User Account'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'employee', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'employee__department')
    search_fields = ('project_name', 'description', 'employee__name')
    raw_id_fields = ('employee',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('project_name', 'description')
        }),
        ('Assignment', {
            'fields': ('employee', 'status')
        }),
    )
