# from django.urls import path
# from .views import (
#     CourseCreateView, CourseListView, CourseUpdateView, CourseDeleteView,
#     EnrollmentCreateView, EnrollmentListView, EnrollmentUpdateView, EnrollmentDeleteView,
#     ModuleView, ModuleDetailView,TopicView
# )

# urlpatterns = [
#       # Enrollments CRUD
#     path('enrollments/', EnrollmentListView.as_view(), name='enrollments-list'),
#     path('enrollments/create/', EnrollmentCreateView.as_view(), name='enrollments-create'),
#     path('enrollments/<str:enrollment_id>/update/', EnrollmentUpdateView.as_view(), name='enrollments-update'),
    # path('enrollments/<str:enrollment_id>/delete/', EnrollmentDeleteView.as_view(), name='enrollments-delete'),
    
#     # Courses CRUD
#     path('courses/', CourseListView.as_view(), name='courses-list'),
#     path('courses/create/', CourseCreateView.as_view(), name='courses-create'),
#     path('courses/<str:course_id>/update/', CourseUpdateView.as_view(), name='courses-update'),
#     path('courses/<str:course_id>/delete/', CourseDeleteView.as_view(), name='courses-delete'),

#     # Modules CRUD
#     path('modules/', ModuleView.as_view(), name='modules-list-create'),           # GET all / POST create
#     path('modules/<str:module_id>/', ModuleDetailView.as_view(), name='modules-detail'),  # GET single / PUT / DELETE
     
#     path("topics/", TopicView.as_view(), name="topics"), 
#     path("topics/<str:topic_id>/", TopicView.as_view(), name="topic")
# ]

from django.urls import path
from .views import (
    CourseView, CourseDetailView,
    ModuleView,
    TopicView, TopicDetailView,
    EnrollmentCreateView, EnrollmentListView, EnrollmentUpdateView, EnrollmentDeleteView,
    ContentView, UpdateUserProgressView
)

urlpatterns = [
    # Courses
    path("courses/", CourseView.as_view()),
    path("courses/<str:course_id>/", CourseDetailView.as_view()),

    # Modules
    path("modules/", ModuleView.as_view()),
    # path("modules/<str:module_id>/", ModuleDetailView.as_view()),

    # Topics
    path("topics/", TopicView.as_view()),
    path("topics/<str:topic_id>/", TopicDetailView.as_view()),

    path("content/", ContentView.as_view(), name="content-list"),
    path("content/<str:content_id>/", ContentView.as_view(), name="content-detail"),

    path('progress/', UpdateUserProgressView.as_view(), name='update-progress'),


    path('enrollments/', EnrollmentListView.as_view(), name='enrollments-list'),
    path('enrollments/create/', EnrollmentCreateView.as_view(), name='enrollments-create'),
    path('enrollments/<str:enrollment_id>/update/', EnrollmentUpdateView.as_view(), name='enrollments-update'),
    path('enrollments/<str:enrollment_id>/delete/', EnrollmentDeleteView.as_view(), name='enrollments-delete'),
]


