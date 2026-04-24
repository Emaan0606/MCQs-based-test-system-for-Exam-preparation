from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from django.contrib.auth import get_user_model

from .models import TestAttempt, UserAnswer

class TestAttemptAdmin(admin.ModelAdmin):
    change_list_template = "admin/performance_chart.html"
    list_display = ('test', 'user', 'started_at')

    def changelist_view(self, request, extra_context=None):
        User = get_user_model()
        total_students = User.objects.filter(is_learner=True).count()

        data = (
            TestAttempt.objects
            .values("test__title")
            .annotate(attempts=Count("id"))
        )

        labels = []
        percentages = []
        colors = []

        for entry in data:
            title = entry["test__title"]
            attempts = entry["attempts"]
            percent = round((attempts / total_students) * 100, 2) if total_students > 0 else 0

            labels.append(title)
            percentages.append(percent)

            # 🎨 Color coding
            if percent >= 60:
                colors.append("#4caf50")  # Green
            elif percent >= 30:
                colors.append("#ff9800")  # Orange
            else:
                colors.append("#f44336")  # Red

        extra_context = {
            "labels": labels,
            "values": percentages,
            "colors": colors,
        }

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(TestAttempt, TestAttemptAdmin)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_option', 'is_correct', 'submitted_at')
    list_filter = ('is_correct', 'submitted_at')
    search_fields = ('user__username', 'question__question_text', 'selected_option')
