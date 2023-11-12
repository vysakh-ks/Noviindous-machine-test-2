
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='core'

urlpatterns = [
    path('',views.login_data,name="login_data"),
    path('index/',views.index,name="index"),
    path('logout_user/',views.logout_user,name="logout_user"),
    path('view_course/',views.view_course,name="view_course"),
    path('add_course/',views.add_course,name="add_course"),
    path('profile/',views.profile,name="profile"),
    path('delete_course/<int:id>/',views.delete_course,name="delete_course"),
    path('course_active/<int:id>/',views.course_active,name="course_active"),
    path('course_inactive/<int:id>/',views.course_inactive,name="course_inactive"),
    path('change_password/',views.change_password,name="change_password"),
    path('search',views.search,name="search"),
    path('edit_course/<int:id>/',views.edit_course,name="edit_course"),
    

]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
