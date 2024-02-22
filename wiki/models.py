from django.urls import reverse
from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=15)
    url_fields = {
        'faculty': 'slug',
    }

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name

    def get_image(self):
        return "/static/img/faculty/%s.png" % self.slug


class Department(models.Model):
    short_name = models.CharField(max_length=4, primary_key=True)
    long_name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    url_fields = {
        'department': 'short_name__iexact',
    }

    class Meta:
        ordering = ['short_name']

    def __str__(self):
        return "Department of %s (%s)" % (self.long_name, self.short_name)

    def get_image(self):
        return "/static/img/department/%s.png" % self.short_name

    def get_large_image(self):
        return "/static/img/department/%s_large.png" % self.short_name


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    number = models.CharField(max_length=5, verbose_name='Course number')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    credits = models.DecimalField(max_digits=2, decimal_places=1)
    url_fields = {
        'department': 'department__short_name__iexact',
        'number': 'number',
    }

    class Meta:
        ordering = ['department__short_name', 'number']

    def __str__(self):
        return "%s %s" % (self.department.short_name, self.number)

    def get_absolute_url(self):
        return reverse('course', kwargs={
            'department': self.department.pk,
            'number': self.number
        })


class Page(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    semester = models.CharField(max_length=6)
    subject = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=20)
    slug = models.SlugField()
    content = models.TextField(null=True)
    maintainer = models.CharField(max_length=20)

    class Meta:
        unique_together = ('course', 'category', 'year', 'semester', 'slug')

    def __str__(self):
        return '%s - %s' % (self.get_title(), self.course)

    def get_title(self):
        if not self.title:
            return self.subject
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('page', kwargs={
            'department': self.course.department.pk,
            'number': self.course.number,
            'category': self.category,
            'semester': self.semester,
            'year': self.year,
            'slug': self.slug,
        })
