from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views import generic
from ..models import Post, Comment
from ...course.models import Course
from ...main.models import Category, Tag
from django.db.models import Q


# def blog_view(request):
#     ctx = {
#
#     }
#     return render(request, 'blog/blog.html', ctx)
#
#
# def blog_detail_view(request, pk):
#     ctx = {
#
#     }
#
#     return render(request, 'blog/blog-single.html', ctx)


class BlogView(generic.ListView):
    queryset = Post.objects.all()
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx['categories'] = Category.objects.all()
        ctx['tags'] = Tag.objects.all()
        ctx['recent_courses'] = Course.objects.order_by('-id')[:3]
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        cat = self.request.GET.get('cat')
        tag = self.request.GET.get('tag')
        q_condition = Q()
        if q:
            q_condition = Q(title__icontains=q)
        cat_condition = Q()
        if cat:
            cat_condition = Q(category__title__exact=cat)
        tag_condition = Q()
        if tag:
            tag_condition = Q(tags__title__exact=tag)
        qs = qs.filter(q_condition, cat_condition, tag_condition)
        return qs



class BlogDetailView(generic.View):
    template_name = 'blog/blog-single.html'
    queryset = Post.objects.all()
    pk_url_kwarg = 'pk'

    def get_object(self, request, pk):
        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            raise Http404
        return post


    def get_context_data(self, request, pk):
        ctx = {
            "object": self.get_object(request, pk)
        }
        return ctx

    def get(self, request, pk, *args, **kwargs):
        ctx = self.get_context_data(request, pk)
        comments = Comment.objects.filter(post_id=pk, parent_comment__isnull=True)
        ctx['comments'] = comments
        return render(request, self.template_name, ctx)

    def post(self, request, pk, *args, **kwargs):
        ctx = self.get_context_data(request, pk)
        if not request.user.is_authenticated:
            return redirect('account:login')
        comment_id = request.GET.get('comment_id', None)
        user_id = request.user.id
        body = request.POST.get('body')
        if body:
            obj = Comment.objects.create(author_id=user_id, post_id=pk, body=body, parent_comment_id=comment_id)
            return redirect(reverse('blog:blog_detail', kwargs={'pk': pk}) + f'#comment_{obj.id}')
        return render(request, self.template_name, ctx)


