import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from projects.models import ResearchProject
from .models import ComparisonTable
from .forms import ComparisonTableForm


@login_required
def comparison_create(request, project_pk):
    project = get_object_or_404(ResearchProject, pk=project_pk, user=request.user)
    if request.method == 'POST':
        form = ComparisonTableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.project = project
            table.table_data = {
                'columns': ['Feature'],
                'rows': [{'name': 'Item 1', 'cells': ['']}]
            }
            table.save()
            messages.success(request, f'Comparison table "{table.title}" created.')
            return redirect('comparisons:editor', pk=table.pk)
    else:
        form = ComparisonTableForm()
    return render(request, 'comparisons/create.html', {'form': form, 'project': project})


@login_required
def comparison_editor(request, pk):
    table = get_object_or_404(ComparisonTable, pk=pk, project__user=request.user)
    project = table.project

    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            table_data = body.get('table_data')
            title = body.get('title', table.title)
            if table_data is not None:
                table.table_data = table_data
                table.title = title
                table.save()
                return JsonResponse({'status': 'ok', 'message': 'Table saved successfully.'})
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data.'}, status=400)

    return render(request, 'comparisons/editor.html', {
        'table': table,
        'project': project,
        'table_data_json': json.dumps(table.table_data),
    })


@login_required
def comparison_delete(request, pk):
    table = get_object_or_404(ComparisonTable, pk=pk, project__user=request.user)
    project = table.project
    if request.method == 'POST':
        title = table.title
        table.delete()
        messages.success(request, f'Comparison table "{title}" deleted.')
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'comparisons/confirm_delete.html', {'table': table, 'project': project})


@login_required
@require_POST
def ai_generate_comparison(request, project_pk):
    project = get_object_or_404(ResearchProject, pk=project_pk, user=request.user)
    api_key = settings.ANTHROPIC_API_KEY
    if not api_key:
        return JsonResponse({'error': 'OpenAI API key not configured.'}, status=400)

    try:
        body = json.loads(request.body)
        items = body.get('items', [])
        if not items or len(items) < 2:
            return JsonResponse({'error': 'Please provide at least 2 items to compare.'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request data.'}, status=400)

    items_str = ', '.join(items)
    prompt = f"""You are creating a comparison table for a research project.

Project: {project.title}
Items to compare: {items_str}

Generate a structured comparison table with 5-8 relevant comparison criteria/features.
For each criterion, provide a brief (1-2 sentence) comparison for each item.

Respond with valid JSON in exactly this format:
{{
  "columns": ["Feature", "{items[0]}", "{items[1]}"{', "' + '", "'.join(items[2:]) + '"' if len(items) > 2 else ''}],
  "rows": [
    {{
      "name": "Criterion 1",
      "cells": ["value for {items[0]}", "value for {items[1]}"{', "value"' * (len(items) - 2) if len(items) > 2 else ''}]
    }}
  ]
}}

Include criteria like: Overview, Key Features, Use Cases, Pros, Cons, Pricing/Cost, Performance, and any domain-specific criteria relevant to the items."""

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        message = client.chat.completions.create(
            model="gpt-5.4-mini",
            max_completion_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.choices[0].message.content.strip()

        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start >= 0 and end > start:
            table_data = json.loads(raw[start:end])
            return JsonResponse({'table_data': table_data})
        else:
            return JsonResponse({'error': 'Could not parse AI response.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'AI generation failed: {str(e)}'}, status=500)
