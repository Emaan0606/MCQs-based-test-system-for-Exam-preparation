from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Subject, Question, Test

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'difficulty', 'explanation', 'created_at']
    list_filter = ['subject', 'difficulty']
    search_fields = ['question_text' , 'explanation']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'difficulty', 'num_questions', 'time_limit', 'created_at']
    filter_horizontal = ('questions',)
    actions = ['generate_questions']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:test_id>/generate-questions/', self.admin_site.admin_view(self.generate_questions_view), name='generate-questions'),
        ]
        return custom_urls + urls

    def generate_questions(self, request, queryset):
        for test in queryset:
            if not test.paragraph:
                self.message_user(request, f"❌ Paragraph missing for test: {test.title}", messages.ERROR)
                continue
            test.generate_test()
            test.save()
        self.message_user(request, "✅ Questions generated for valid test(s).")

    generate_questions.short_description = "🧠 Generate Questions Automatically"

    def generate_questions_view(self, request, test_id):
        test = Test.objects.get(id=test_id)
        test.generate_test()
        test.save()
        self.message_user(request, f"✅ Questions generated for test: {test.title}", messages.SUCCESS)
        return redirect(f'/admin/questions/test/{test_id}/change/')
