from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12, blank=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(50.0), MaxValueValidator(500.0)])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True)
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    user_image = models.ImageField(upload_to='images/', blank=True)


class Order(models.Model):
    STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Confirmed'), (2, 'On Hold')]
    courses = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, related_name="Orders", on_delete=models.CASCADE)
    order_date = timezone.now()
    order_status = models.IntegerField(default=1, choices=STATUS_CHOICES)

    def total_cost(self):
        cost = 0
        for course in self.courses.all():
            cost += course.price
        return cost

    def total_items(self):
        return self.courses.all().count()


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
