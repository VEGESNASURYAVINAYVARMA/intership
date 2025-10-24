from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.list_quizzes, name='list_quizzes'),
    path('quizzes/create/', views.create_quiz, name='create_quiz'),
    path('quizzes/<str:quiz_id>/', views.retrieve_quiz, name='retrieve_quiz'),  # <-- match the function name
    path('quizzes/<str:quiz_id>/update/', views.update_quiz, name='update_quiz'),
    path('quizzes/<str:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
]
