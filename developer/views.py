from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .utils import searchProjects, paginateProjects
from django.contrib import messages

# Create your views here.


def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context = {

        'projects': projects,
        ' search_query': search_query,
        'custom_range': custom_range



    }

    return render(request, 'developer/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm
    tags = project_obj.tags.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.getVoteCount

        messages.success(request, 'review submitted successfully!')
        return redirect('project', pk=project_obj.id)

    context = {

        'form': form,
        'project': project_obj,
        'tags': tags,
        # 'review':review

    }

    # return redirect(reverse('project', kwargs={'pk': project.pk}))

    return render(request, "developer/single-project.html", context)


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        # together with the enctype="multipart/form-data" in a project_form.html will help you render media files
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {

        'form': form,
        'profile': profile
    }
    return render(request, "create_project.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    # quiring only that user s projects
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {

        'form': form
    }
    return render(request, "projects/update_project.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    # because we are passing it as object in the html
    context = {'object': project}
    return render(request, 'delete_template.html', context)
