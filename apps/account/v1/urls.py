from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView,\
    PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import RegisterView, logout_view, profile_info, profile_update, my_courses


urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),

    path('profile_info/', profile_info, name='profile_info'),
    path('profile_update/<int:pk>', profile_update, name='profile_update'),
    path('my_courses/', my_courses, name='my_courses'),

    # change password
    path('password_change/',
         PasswordChangeView.as_view(template_name='account/change_password/password_change_form.html', success_url=reverse_lazy('account:password_change_done')),
         name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='account/change_password/password_change_done.html'),
         name='password_change_done'),

    # reset password
    path('password_reset/send/',
         PasswordResetView.as_view(template_name='account/reset_password/password_reset_form.html',
                                   email_template_name='account/reset_password/password_reset_email.html',
                                   success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='account/reset_password/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(template_name='account/reset_password/password_reset_confirm.html',
                                          success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='account/reset_password/password_reset_complete.html'),
         name='password_reset_complete'),

]
