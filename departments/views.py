

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Department, Employee
from .forms import DepartmentForm

@staff_member_required
def department_list(request):
    query = request.GET.get('q')
    departments = Department.objects.filter(is_active=True)
    if query:
        departments = departments.filter(name__icontains=query) | departments.filter(description__icontains=query)
    return render(request, 'dashboard/department_list.html', {'departments': departments})

@staff_member_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'dashboard/create_department.html', {'form': form})

@staff_member_required
def update_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'dashboard/update_department.html', {'form': form})

@staff_member_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    linked_employees = Employee.objects.filter(department=department)
    if request.method == 'POST':
        if linked_employees.exists():
            messages.warning(request, 'This department has linked employees. Please reassign them before deactivating.')
            return redirect('department_list')
        else:
            department.is_active = False
            department.save()
            messages.success(request, 'Department marked as inactive.')
            return redirect('department_list')
    return render(request, 'dashboard/confirm_delete.html', {'department': department, 'linked_employees': linked_employees})
