from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import ResearchProject
from .models import Resource
from .forms import ResourceForm


@login_required
def resource_create(request, project_pk):
    project = get_object_or_404(ResearchProject, pk=project_pk, user=request.user)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.project = project
            resource.save()
            messages.success(request, f'Resource "{resource.title}" added successfully.')
            return redirect('projects:detail', pk=project.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResourceForm()
    return render(request, 'resources/create.html', {'form': form, 'project': project})


@login_required
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk, project__user=request.user)
    project = resource.project
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, f'Resource "{resource.title}" updated successfully.')
            return redirect('projects:detail', pk=project.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/edit.html', {'form': form, 'resource': resource, 'project': project})


@login_required
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk, project__user=request.user)
    project = resource.project
    if request.method == 'POST':
        title = resource.title
        if resource.file:
            resource.file.delete(save=False)
        resource.delete()
        messages.success(request, f'Resource "{title}" deleted successfully.')
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'resources/confirm_delete.html', {'resource': resource, 'project': project})
