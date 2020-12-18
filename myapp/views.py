from urllib.parse import urlparse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datetime_safe import datetime

from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from .models import Topic, Course, Student


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]

    if request.session.has_key('last_login'):
        login_detail = request.session['last_login']
        return render(request, 'myapp/index.html', {'top_list': top_list, 'last_login': login_detail})
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    about_us = "This is an E-learning Website! Search our Topics to find all available Courses."
    if request.session.has_key('about_visits'):
        request.session['about_visits'] = request.session['about_visits'] + 1
        request.session.set_expiry(300)
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)
    return render(request, 'myapp/about.html', {'about_us': about_us, 'num_times': request.session['about_visits']})


def detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    cour_list = topic.courses.all()
    return render(request, 'myapp/detail.html', {'topic': topic, 'cour_list': cour_list})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            if not length:
                topics = Topic.objects.all().filter(courses__price__lte=max_price)
            else:
                topics = Topic.objects.filter(length=length).filter(courses__price__lte=max_price)

            courselist = []
            for top in topics:
                courselist = courselist + list(top.courses.all())
            return render(request, 'myapp/results.html',
                          {'courselist': courselist, 'name': name})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        stu = Stu
        if stu.count() == 0:
            return render(request, 'myapp/myorders.html', {'message': "You're not a registered student."})
        else:
            return render(request, 'myapp/myorders.html', {'orders': stu.get().Orders.all()})
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=True)
            student = order.student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request, 'myapp/order_response.html', {'courses':
                                                                     courses, 'order': order})
        else:
            return render(request, 'myapp/place_order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})


def review(request):
    user = request.user
    stu = Student.objects.filter(pk=user.pk)
    if stu.count() == 0 or (stu.get().level != 'UG' and stu.get().level != 'PG'):
        return render(request, 'myapp/review.html', {'message': "You're  not Student or not an Undergraduate or "
                                                                "Postgraduate."})
    else:
        if request.method == 'POST':
            form = ReviewForm(request.POST)


            if form.is_valid():
                rating = form.cleaned_data['rating']
                if 0 < rating < 5:
                    rev = form.save(commit=True)
                    rev.rating = rating

                    rev.reviewer = form.cleaned_data['reviewer']
                    rev.course.num_reviews = rev.course.num_reviews + 1
                    rev.course.save()
                    return redirect('myapp:index')
                else:
                    return render(request, 'myapp/review.html', {'form': form, 'message': 'You must enter a rating '
                                                                                          'between 1 and 5!'})
            else:
                return render(request, 'myapp/review.html', {'form': form})
        else:
            form = ReviewForm()
            return render(request, 'myapp/review.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600)
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required(login_url="myapp:user_login")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required(login_url="myapp:user_login")
def myaccount(request):
    user = request.user

    stu = Student.objects.filter(pk=user.pk)

    if stu.count() == 0:
        return render(request, 'myapp/myaccount.html', {'message': "You're not a registered student."})
    else:
        return render(request, 'myapp/myaccount.html',
                      {'first_name': stu.get().first_name, 'last_name': stu.get().last_name,
                       'topics': stu.get().interested_in.all(), 'courses': stu.get().registered_courses.all(), "image":stu.get().user_image.url})


@login_required
def myorders(request):
    user = request.user
    stu = Student.objects.filter(pk=user.pk)
    if stu.count() == 0:
        return render(request, 'myapp/myorders.html', {'message': "You're not a registered student."})
    else:
        return render(request, 'myapp/myorders.html', {'orders': stu.get().Orders.all()})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            myfile = request.FILES['user_image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            courses = form.cleaned_data['registered_courses']
            topics = form.cleaned_data['interested_in']
            stu = Student.objects.get(username=username)
            for c in courses:
                stu.registered_courses.add(c)
            for t in topics:
                stu.interested_in.add(t)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('myapp:index')

    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
