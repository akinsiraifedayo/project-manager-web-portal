from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

User = get_user_model()

# Unregister the default User admin
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'role_display', 'actions_display')
    list_filter = ('is_active', 'groups', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    list_per_page = 20  # Enable pagination with 20 items per page

    def role_display(self, obj):
        return ', '.join([group.name for group in obj.groups.all()]) or 'No Role'
    role_display.short_description = 'Roles'

    def actions_display(self, obj):
        if obj.is_active:
            button_class = 'danger'
            button_text = 'Deactivate'
            action = 'deactivate'
        else:
            button_class = 'success'
            button_text = 'Reactivate'
            action = 'activate'
        
        return format_html(
            '<a class="button" href="{}?action={}" style="background-color: {};">{}</a>',
            f'/admin/auth/user/{obj.pk}/change/',
            action,
            'red' if button_class == 'danger' else 'green',
            button_text
        )
    actions_display.short_description = 'Actions'
    actions_display.allow_tags = True

    def response_change(self, request, obj):
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'deactivate':
                obj.is_active = False
                obj.save()
            elif action == 'activate':
                obj.is_active = True
                obj.save()
        return super().response_change(request, obj)

    # Add custom CSS for the admin interface
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
