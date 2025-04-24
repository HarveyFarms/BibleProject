from django.contrib import admin
from django.urls import path, include
from frontend_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('sign-in-success/', views.sign_in_success, name='sign-in-success'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('activate/<uid>/<token>/', views.activate, name='activate'),
    path('groups/', views.groups_home, name='groups-home'),
    path('create/', views.create_group, name='create-group'),
    path('leave/', views.leave_group, name='leave-group'),
    path('join/', views.join_group_page, name='join-group-page'),
    path('join/<int:group_id>/', views.join_group, name='join-group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('comment/', views.post_comment, name='post_comment'),
    path('highlight/', views.add_highlight, name='add_highlight'),
    path('group_verses/', views.group_verses, name='group_verses'),
    path('bible/', views.bible_view, name='bible_view'),
    path('fetch-group-data/', views.fetch_group_data, name='fetch_group_data'),
    path("save-highlight/", views.save_highlight, name="save_highlight"),
    ]
