import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from projects.models import ResearchProject
from .models import Summary, Citation
from .forms import SummaryForm


@login_required
def summary_create(request, project_pk):
    project = get_object_or_404(ResearchProject, pk=project_pk, user=request.user)
    if request.method == 'POST':
        form = SummaryForm(request.POST)
        if form.is_valid():
            summary = form.save(commit=False)
            summary.project = project
            summary.save()
            messages.success(request, f'Summary "{summary.title}" created.')
            return redirect('summaries:editor', pk=summary.pk)
    else:
        form = SummaryForm()
    return render(request, 'summaries/create.html', {'form': form, 'project': project})


@login_required
def summary_editor(request, pk):
    summary = get_object_or_404(Summary, pk=pk, project__user=request.user)
    project = summary.project
    resources = project.resources.all()
    citations = summary.citations.select_related('resource').all()
    citation_map = {c.resource_id: c.citation_number for c in citations}

    if request.method == 'POST':
        content_json = request.POST.get('content_json', '{}')
        content_html = request.POST.get('content_html', '')
        title = request.POST.get('title', summary.title)
        citations_data = request.POST.get('citations', '[]')

        try:
            summary.content_json = json.loads(content_json)
            summary.content_html = content_html
            summary.title = title
            summary.save()

            summary.citations.all().delete()
            citations_list = json.loads(citations_data)
            for c in citations_list:
                resource = project.resources.filter(pk=c['resource_id']).first()
                if resource:
                    Citation.objects.create(
                        summary=summary,
                        resource=resource,
                        citation_number=c['number']
                    )

            messages.success(request, 'Summary saved successfully.')
            return redirect('summaries:editor', pk=summary.pk)
        except (json.JSONDecodeError, KeyError):
            messages.error(request, 'Error saving summary.')

    return render(request, 'summaries/editor.html', {
        'summary': summary,
        'project': project,
        'resources': resources,
        'citations': citations,
        'citation_map': json.dumps(citation_map),
    })


@login_required
def summary_delete(request, pk):
    summary = get_object_or_404(Summary, pk=pk, project__user=request.user)
    project = summary.project
    if request.method == 'POST':
        title = summary.title
        summary.delete()
        messages.success(request, f'Summary "{title}" deleted.')
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'summaries/confirm_delete.html', {'summary': summary, 'project': project})


@login_required
@require_POST
def ai_generate_summary(request, project_pk):
    project = get_object_or_404(ResearchProject, pk=project_pk, user=request.user)
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return JsonResponse({'error': 'OpenAI API key not configured.'}, status=400)

    resources = project.resources.all()
    if not resources:
        return JsonResponse({'error': 'No resources found in this project. Add some resources first.'}, status=400)

    resource_list = []
    for i, r in enumerate(resources, 1):
        desc = r.description or 'No description'
        rtype = 'PDF' if r.resource_type == 'file' else 'URL'
        resource_list.append(f"[{i}] {r.title} ({rtype}): {desc}")

    resources_text = '\n'.join(resource_list)
    prompt = f"""You are a research assistant helping to write an academic summary.

Project: {project.title}
Description: {project.description or 'No description'}

Available resources:
{resources_text}

Please write a comprehensive research summary for this project. Structure it with:
1. An introduction paragraph about the research topic
2. Main themes and findings from the resources (cite them as [1], [2], etc.)
3. A conclusion paragraph

Format the output as HTML with proper paragraph tags (<p>), bold (<strong>), and citation references like <span class="citation" data-ref="1">[1]</span>.
Keep it academic, clear, and well-structured. About 300-400 words."""

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        message = client.chat.completions.create(
            model="gpt-5.4-mini",
            max_completion_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        generated_html = message.choices[0].message.content

        citation_suggestions = []
        for i, r in enumerate(resources, 1):
            if f'[{i}]' in generated_html:
                citation_suggestions.append({'number': i, 'resource_id': r.pk, 'title': r.title})

        return JsonResponse({
            'html': generated_html,
            'citations': citation_suggestions,
        })
    except Exception as e:
        return JsonResponse({'error': f'AI generation failed: {str(e)}'}, status=500)
