from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('bot/', views.all_bots, name='bot-list'),
    path('edit/<int:bot_id>', views.edit_bot, name='bot-edit'),
    path('bot/<int:pk>', views.bot_view, name='bot-detail'),
    path('accounts/<int:user_id>/', views.lk, name='lk'),
    path('', views.main),
]
