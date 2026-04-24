from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.test_list_view, name='test_list'),
    path('test/<int:pk>/attempt/', views.test_attempt_view, name='test_attempt'),
    path('test/result/<int:pk>/', views.test_result_view, name='test_result'),
    path('my-attempts/', views.my_attempts_view, name='my_attempts'),
    path('performance-history/', views.performance_history_view, name='performance_history'),
    path('performance-history/data/', views.performance_history_data_view, name='performance_history_data'),
]

