from django_distill import distill_path

from wiki import views
from wiki.models import Course, Page


def get_home():
    return None

def get_all_courses():
    for course in Course.objects.all():
        yield {
            'department': course.department.pk,
            'number': course.number,
        }


def get_all_pages():
    for page in Page.objects.all():
        yield {
            'department': page.course.department.pk,
            'number': page.course.number,
            'category': page.category,
            'semester': page.semester,
            'year': page.year,
            'slug': page.slug,
        }


urlpatterns = [
    distill_path('',
                 views.home,
                 name='home',
                 distill_func=get_home,
                 distill_file='index.html'),
    distill_path('<slug:department>_<slug:number>/',
                 views.course,
                 name='course',
                 distill_func=get_all_courses),
    distill_path('<slug:department>_<slug:number>/<slug:category>/<slug:semester>-<int:year>/<slug:slug>',
                 views.page,
                 name='page',
                 distill_func=get_all_pages),
]
