from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.models import ResearchProject
from resources.models import Resource
from summaries.models import Summary


@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    results = {'projects': [], 'resources': [], 'summaries': []}
    total_count = 0

    if query:
        projects = ResearchProject.objects.filter(
            user=request.user
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        resources = Resource.objects.filter(
            project__user=request.user
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(url__icontains=query)
        ).select_related('project')

        summaries = Summary.objects.filter(
            project__user=request.user
        ).filter(
            Q(title__icontains=query) | Q(content_html__icontains=query)
        ).select_related('project')

        results['projects'] = list(projects)
        results['resources'] = list(resources)
        results['summaries'] = list(summaries)
        total_count = len(results['projects']) + len(results['resources']) + len(results['summaries'])

    return render(request, 'search_app/results.html', {
        'query': query,
        'results': results,
        'total_count': total_count,
    })
