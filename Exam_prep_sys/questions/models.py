# questions app models

from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=200, null=True, blank=True)
    option2 = models.CharField(max_length=200, null=True, blank=True)
    option3 = models.CharField(max_length=200, null=True, blank=True)
    option4 = models.CharField(max_length=200, null=True, blank=True)
    correct_answer = models.CharField(max_length=200)
    explanation = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class Test(models.Model):
    title = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)
    difficulty = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    num_questions = models.IntegerField(default=5)
    time_limit = models.IntegerField(help_text="Time limit in minutes")
    paragraph = models.TextField(blank=True, null=True)  # Input paragraph
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_test(self):
        if not self.paragraph:
            return  # Or optionally raise an exception or log a message

        from .utils import generate_mcq_questions
        generated = generate_mcq_questions(self.paragraph, self.num_questions)
        for item in generated:
            options = item.get('options', [])
            if len(options) < 4 or not item.get('question') or not item.get('answer'):
                continue  # skip incomplete data

            q = Question.objects.create(
                subject=self.subject,
                question_text=item['question'],
                option1=options[0],
                option2=options[1],
                option3=options[2],
                option4=options[3],
                correct_answer=item['answer'],
                explanation=f"The correct answer is '{item['answer']}' based on the context of the paragraph." ,
                difficulty=self.difficulty
            )
            self.questions.add(q)