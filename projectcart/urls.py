
from django.contrib import admin
from django.urls import path
from cart.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('email',email,name="email"),
    path('',signin_page,name="signin"),
    path('login/',login_page,name="login"),
    path('home/<str:n>',home,name="home"),
    path('logout/',logout_page,name="logout"),
    path('user_projects/<str:n>',user_projects,name="user_projects"),
    path('add/<str:n>',add,name="add"),
    path('logout/',logout_page,name="logout"),
    path('search/',search,name="search"),
    path('project/<str:n>/<str:p>',project,name="project"),
    path('manage_project/<int:id>',manage_project,name="manage"),
    path('delete_project/<int:id>',delete_project,name="delete"),
    path('edit_project/<int:id>',edit_project,name="edit"),
    path('post_c/<int:id>/<str:n>',post_c,name="post"),
    path('like_me/',like_me,name="l"),


    # forget,reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('change_password/',change_password,name="change_password"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.MEDIA_ROOT)
