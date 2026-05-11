from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResearchProject
from .forms import ResearchProjectForm


@login_required
def project_list(request):
    projects = ResearchProject.objects.filter(user=request.user)
    return render(request, 'projects/list.html', {'projects': projects})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, f'Project "{project.title}" created successfully.')
            return redirect('projects:detail', pk=project.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResearchProjectForm()
    return render(request, 'projects/create.html', {'form': form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk, user=request.user)
    resources = project.resources.all()
    summaries = project.summaries.all()
    comparisons = project.comparisons.all()
    return render(request, 'projects/detail.html', {
        'project': project,
        'resources': resources,
        'summaries': summaries,
        'comparisons': comparisons,
    })


@login_required
def project_edit(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project "{project.title}" updated successfully.')
            return redirect('projects:detail', pk=project.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResearchProjectForm(instance=project)
    return render(request, 'projects/edit.html', {'form': form, 'project': project})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk, user=request.user)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted successfully.')
        return redirect('projects:list')
    return render(request, 'projects/confirm_delete.html', {'project': project})
