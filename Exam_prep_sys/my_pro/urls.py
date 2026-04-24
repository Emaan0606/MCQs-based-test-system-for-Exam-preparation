from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('question/', include('questions.urls')),
    path('performance/', include('performance.urls')),
]
