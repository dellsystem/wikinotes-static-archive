import collections

from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect, render

from wiki.models import Course, Page


def home(request):
    courses = Course.objects.annotate(n=Count('page')).order_by('-n')

    context = {
        'courses': courses,
    }

    return render(request, "home.html", context)


def course(request, department, number):
    try:
        course = Course.objects.get(department=department, number=number)
    except Course.DoesNotExist:
        raise Http404

    pages = collections.defaultdict(list)
    for page in course.page_set.all():
        category = page.category.replace('-', ' ').capitalize()
        pages[category].append(page)

    context = {
        'course': course,
        'pages': pages.items(),
    }

    return render(request, "course.html", context)


def page(request, department, number, category, semester, year, slug):
    try:
        page = Page.objects.get(
            course__department=department,
            course__number=number,
            category=category,
            semester=semester,
            year=year,
            slug=slug
        )
    except Page.DoesNotExist:
        raise Http404

    context = {
        'page': page,
    }

    return render(request, "page.html", context)
