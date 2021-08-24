from django.urls import path, include

from .views import UserList, UserDetail, ChatHistoryList, MessageList, UserProfileList

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('chat/', ChatHistoryList.as_view()),
    path('userprofile/', UserProfileList.as_view(), name='user-profile'),
    path('chat/sendmsg/', MessageList.as_view()),
]
