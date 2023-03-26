from django.urls import path
# from .views import blog_view, blog_detail_view
from .views import BlogView, BlogDetailView

urlpatterns = [
    # path('', blog_view, name='blogs'),
    # path('detail/<int:pk>/', blog_detail_view, name='blog_detail'),
    path('', BlogView.as_view(), name='blog'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]
