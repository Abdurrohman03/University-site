from django.shortcuts import render, redirect
from apps.blog.models import Post
from ..models import FAQ, Category
from .forms import SubscribeForm, ContactForm
from apps.course.models import Course
from ...account.models import Profile


def index(request):
    categories = Category.objects.all()
    randomly_5_courses = Course.objects.order_by('?')[:5]
    teachers = Profile.objects.filter(role=1).order_by('?')[:3]
    last_post = Post.objects.last()
    recent_posts = Post.objects.exclude(id=last_post.id).order_by('-id')[:4]

    form = SubscribeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('.')
    ctx = {
        'form': form,
        'categories': categories,
        'randomly_5_courses': randomly_5_courses,
        'last_post': last_post,
        'recent_posts': recent_posts,
        'teachers': teachers,
    }
    return render(request, 'main/index.html', ctx)


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('.')

    form1 = SubscribeForm(request.POST or None)
    if form1.is_valid():
        form1.save()
        return redirect('.')
    ctx = {
        'form': form,
        'form1': form1,
    }
    return render(request, 'main/contact.html', ctx)


def about(request):
    faq = FAQ.objects.order_by('-id')

    form = SubscribeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('.')
    ctx = {
        'faq': faq,
        'form': form,
    }
    return render(request, 'main/about.html', ctx)
