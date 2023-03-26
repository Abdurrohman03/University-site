from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from ..models import Course, Lesson, LessonFiles
from apps.main.models import Category, Tag
from apps.main.v1.forms import SubscribeForm


# def course_view(request):
#     courses = Course.objects.order_by('-id')
#     category_list = Category.objects.all()
#     tags = Tag.objects.all()
#     recent_courses = Course.objects.order_by('-id')[:3]
#
#     cat = request.GET.get('cat')
#     tag = request.GET.get('tag')
#     if cat:
#         courses = courses.filter(category__title__exact=cat)
#     if tag:
#         courses = courses.filter(tags__title__exact=tag)
#
#     form = SubscribeForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('.')
#
#     ctx = {
#         'object_list': courses,
#         'category_list': category_list,
#         'tags': tags,
#         'recent_courses': recent_courses,
#         'form': form,
#     }
#     return render(request, 'course/courses.html', ctx)
#
#
# def course_detail(request, pk):
#     course = get_object_or_404(Course, id=pk)
#     ctx = {
#         'object': course,
#     }
#     return render(request, 'course/course-single.html', ctx)
#


class CourseListView(ListView):
    queryset = Course.objects.all()
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx['categories'] = Category.objects.all()
        ctx['tags'] = Tag.objects.all()
        ctx['recent_courses'] = Course.objects.order_by('-id')[:3]
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET.get('tag')
        cat = self.request.GET.get('cat')
        q = self.request.GET.get('q')
        q_condition = Q()
        if q:
            q_condition = Q(title__icontains=q)
        q_category = Q()
        if cat:
            q_category = Q(category__title__exact=cat)
        q_tag = Q()
        if tag:
            q_tag = Q(tags__title__exact=tag)
        qs = qs.filter(q_condition, q_category, q_tag)
        return qs



class CourseDetailView(DetailView):
    queryset = Course.objects.all()
    template_name = 'course/course_detail.html'

    def get_context_data(self,*args, **kwargs):
        ctx = super().get_context_data()
        ctx['recent_courses'] = Course.objects.order_by('-id')[:3]
        ctx['categories'] = Category.objects.all()
        ctx['randomly_5_courses'] = Course.objects.order_by('?')[:5]
        ctx['tags'] = Tag.objects.all()
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET.get('tag')
        cat = self.request.GET.get('cat')
        q = self.request.GET.get('q')
        q_condition = Q()
        if q:
            q_condition = Q(title__icontains=q)
        q_category = Q()
        if cat:
            q_category = Q(category__title__exact=cat)
        q_tag = Q()
        if tag:
            q_tag = Q(tags__title__exact=tag)
        qs = qs.filter(q_condition, q_category, q_tag)
        return qs



def lesson_detail(request, course_id, pk):
    lesson = Lesson.objects.get(id=pk)
    main_video = LessonFiles.objects.filter(lesson_id=pk, is_main=True).first()
    # course = Course.objects.get(id=course_id)
    randomly_5_courses = Course.objects.order_by('?')[:5]

    ctx = {
        "lesson": lesson,
        "randomly_5_courses": randomly_5_courses,
        "main_video": main_video,
    }
    return render(request, 'course/course_lesson.html', ctx)


