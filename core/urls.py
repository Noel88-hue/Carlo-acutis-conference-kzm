from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Programs
    path('programs/', views.programs_list, name='programs_list'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    path('programs/add/', views.program_create, name='program_create'),
    path('programs/<int:pk>/edit/', views.program_edit, name='program_edit'),
    path('programs/<int:pk>/delete/', views.program_delete, name='program_delete'),
    path('programs/<int:pk>/photos/', views.program_photos, name='program_photos'),
    path('photos/<int:pk>/delete/', views.photo_delete, name='photo_delete'),

    # Events
    path('events/', views.events_list, name='events_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/add/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Funds
    path('funds/', views.funds_view, name='funds'),
    path('funds/add/', views.fund_create, name='fund_create'),
    path('funds/<int:pk>/edit/', views.fund_edit, name='fund_edit'),
    path('funds/<int:pk>/delete/', views.fund_delete, name='fund_delete'),

    # Reports
    path('reports/', views.reports_list, name='reports_list'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/add/', views.report_create, name='report_create'),
    path('reports/<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),

    # Gallery
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/upload/', views.gallery_upload, name='gallery_upload'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),

    # Support / Giving
    path('support/', views.support_view, name='support'),
    path('support/edit/', views.support_edit, name='support_edit'),
]
