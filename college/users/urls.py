from django.urls import path
from .views import UserRegisterView , UserLoginView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]

#     path('users/', UserListView.as_view()),
#     path('users/create/', UserCreateView.as_view()),
#     path('users/<int:user_id>/update/', UserUpdateView.as_view()),
#     path('users/<int:user_id>/delete/', UserDeleteView.as_view()),
#     # path('register/', view1.register_view, name='register'),
#     # path('login/', view1.login_view, name='login'),

