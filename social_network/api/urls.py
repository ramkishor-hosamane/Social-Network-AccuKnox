from django.urls import path
from .views import FriendRequestUpdateAPIView, UserCreateAPIView, UserSearchAPIView, FriendRequestCreateAPIView, FriendRequestListAPIView, FriendListAPIView,UserLoginAPIView
urlpatterns = [
    path('signup/', UserCreateAPIView.as_view(), name='user-create'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestCreateAPIView.as_view(), name='friend-request-create'),
    path('friend-requests/', FriendRequestListAPIView.as_view(), name='friend-request-list'),
    path('friends/', FriendListAPIView.as_view(), name='friend-list'),
    path('friend-request/<int:pk>/update/', FriendRequestUpdateAPIView.as_view(), name='friend-request-update'),
]