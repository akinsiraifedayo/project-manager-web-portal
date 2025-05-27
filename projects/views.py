from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Project

# Create your views here.

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        # If user is staff, show all projects
        if self.request.user.is_staff:
            return Project.objects.all()
        # Otherwise, show only projects assigned to the user
        return Project.objects.filter(employee__user=self.request.user)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add permission flags to context
        context['can_edit'] = self.can_edit_project(self.object)
        context['can_delete'] = self.can_delete_project(self.object)
        return context

    def can_edit_project(self, project):
        user = self.request.user
        return user.is_staff or (project.employee and project.employee.user == user)

    def can_delete_project(self, project):
        return self.can_edit_project(project)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/project_form.html'
    fields = ['project_name', 'description', 'employee', 'status']
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # If not staff, can only assign to self
        if not self.request.user.is_staff:
            form.fields['employee'].queryset = form.fields['employee'].queryset.filter(user=self.request.user)
        return form

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'projects/project_form.html'
    fields = ['project_name', 'description', 'employee', 'status']
    success_url = reverse_lazy('project-list')

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return user.is_staff or (project.employee and project.employee.user == user)

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # If not staff, can only assign to self
        if not self.request.user.is_staff:
            form.fields['employee'].queryset = form.fields['employee'].queryset.filter(user=self.request.user)
        return form

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')
    
    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return user.is_staff or (project.employee and project.employee.user == user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)
