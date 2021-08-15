from django.urls import path, include
from .views import UserList, UserDetail, ChatList, ChatDetail

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('chats/', ChatList.as_view()),
    path('chats/<int:pk>/', ChatDetail.as_view()),
]
