

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Department
from .forms import DepartmentForm
from django.contrib import messages

@staff_member_required
def dashboard(request):
    search_query = request.GET.get('q', '')
    departments = Department.objects.filter(name__icontains=search_query)
    return render(request, 'departments/dashboard.html', {'departments': departments})

@staff_member_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Add Department'})

@staff_member_required
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Edit Department'})

@staff_member_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    # Display warning here
    if request.method == 'POST':
        department.status = False  # Soft delete
        department.save()
        messages.warning(request, 'Department deactivated. Reassign employees before deactivation.')
        return redirect('dashboard')
    return render(request, 'departments/confirm_delete.html', {'department': department})
