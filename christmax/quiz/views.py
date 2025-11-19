from django.views.generic import TemplateView

from .models import Category, Question, Trophy, UserStatistics


class QuizDevView(TemplateView):
    """Development page to showcase seeded data with i18n."""

    template_name = 'quiz/dev.html'

    def get_context_data(self, **kwargs):
        """Add seeded data to context."""
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        context['questions'] = Question.objects.select_related('category').all()

        context['trophies'] = Trophy.objects.all()

        context['difficulty_choices'] = Question.DifficultyLevel.choices

        return context
