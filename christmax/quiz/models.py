"""Quiz app models for Django Wordle game."""

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Category(models.Model):
    """Quiz question categories."""

    class CategoryChoices(models.TextChoices):
        HTML = 'HTML', _('HTML')
        PYTHON = 'PYTHON', _('Python')
        DJANGO = 'DJANGO', _('Django')
        JAVASCRIPT = 'JS', _('JavaScript')
        CSS = 'CSS', _('CSS')
        RANDOM = 'RANDOM', _('Random')
        CUSTOM = 'CUSTOM', _('Custom')

    name = models.CharField(
        _('category name'), max_length=20, choices=CategoryChoices.choices, unique=True
    )

    description = models.TextField(_('description'), blank=True)

    icon_class = models.CharField(
        _('icon class'),
        max_length=50,
        blank=True,
        help_text=_('Bootstrap icon class, e.g., bi-code-slash'),
    )

    order = models.PositiveIntegerField(_('display order'), default=0)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order', 'name']
        db_table = 'quiz_category'

    def __str__(self):
        return self.get_name_display()  # type: ignore[attr-defined]


class Question(models.Model):
    """Quiz questions with code snippets and answers."""

    class DifficultyLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', _('Beginner')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        ADVANCED = 'ADVANCED', _('Advanced')
        EXPERT = 'EXPERT', _('Expert')

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='questions', verbose_name=_('category')
    )

    difficulty = models.CharField(
        _('difficulty level'),
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BEGINNER,
    )

    question_text = models.JSONField(
        _('question text'),
        default=dict,
        help_text=_('Question text in multiple languages: {"en": "...", "zh": "..."}'),
    )

    code_snippet = models.TextField(
        _('code snippet'),
        blank=True,
        help_text=_('Optional code snippet to show with the question'),
    )

    answer = models.CharField(
        _('correct answer'), max_length=100, help_text=_('The correct answer (case-insensitive)')
    )

    hint_text = models.JSONField(
        _('hint'),
        default=dict,
        blank=True,
        help_text=_('Hint text in multiple languages: {"en": "...", "zh": "..."}'),
    )

    explanation = models.JSONField(
        _('explanation'),
        default=dict,
        blank=True,
        help_text=_('Explanation in multiple languages: {"en": "...", "zh": "..."}'),
    )

    # Metadata
    is_active = models.BooleanField(_('is active'), default=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ['-created_at']
        db_table = 'quiz_question'
        indexes = [
            models.Index(fields=['category', 'difficulty', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        question = self.get_question_text('en')
        return f'{self.get_difficulty_display()} - {question[:50]}'  # type: ignore[attr-defined]

    def get_question_text(self, language='en'):
        """Get question text in specified language."""
        if isinstance(self.question_text, dict):
            return self.question_text.get(language, self.question_text.get('en', ''))
        return str(self.question_text)  # Fallback for non-dict data

    def get_hint_text(self, language='en'):
        """Get hint text in specified language."""
        if isinstance(self.hint_text, dict):
            return self.hint_text.get(language, self.hint_text.get('en', ''))
        return str(self.hint_text) if self.hint_text else ''

    def get_explanation(self, language='en'):
        """Get explanation in specified language."""
        if isinstance(self.explanation, dict):
            return self.explanation.get(language, self.explanation.get('en', ''))
        return str(self.explanation) if self.explanation else ''

    def clean_answer(self):
        """Normalize answer for comparison."""
        return self.answer.strip().lower()


class GameSession(models.Model):
    """A user's attempt at answering a question with time limit."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='game_sessions',
        verbose_name=_('user'),
    )

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='game_sessions', verbose_name=_('question')
    )

    started_at = models.DateTimeField(_('started at'), auto_now_add=True)

    end_at = models.DateTimeField(
        _('end at'), help_text=_('Timer deadline (when the session expires)')
    )

    completed_at = models.DateTimeField(
        _('completed at'),
        null=True,
        blank=True,
        help_text=_('When user submitted their final answer'),
    )

    score = models.IntegerField(_('score'), default=0)

    class Meta:
        verbose_name = _('game session')
        verbose_name_plural = _('game sessions')
        ordering = ['-started_at']
        db_table = 'quiz_game_session'
        indexes = [
            models.Index(fields=['user', '-started_at']),
            models.Index(fields=['end_at']),  # For expired session queries
        ]

    def __str__(self):
        return f'{self.user.email} - Q{self.question.id} - {self.status}'

    @property
    def status(self):
        """Compute current status from timestamps and attempts.
        Returns:
            str: One of 'IN_PROGRESS', 'WON', 'LOST', 'ABANDONED'
        """
        now = timezone.now()

        if self.completed_at:
            if self.completed_at > self.end_at:
                return 'ABANDONED'

            if self.attempts.filter(is_correct=True).exists():  # type: ignore[attr-defined]
                return 'WON'
            else:
                return 'LOST'

        if now >= self.end_at:
            return 'ABANDONED'
        return 'IN_PROGRESS'


    # ============== METHODS ==============

    def complete(self):
        """Mark session as completed (user made final submission)."""
        if not self.completed_at:
            self.completed_at = timezone.now()
            self.save()

class Attempt(models.Model):
    """Individual answer attempt within a game session."""

    game_session = models.ForeignKey(
        GameSession,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name=_('game session'),
    )

    attempt_number = models.PositiveIntegerField(_('attempt number'))

    user_answer = models.CharField(
        _('user answer'), max_length=100, help_text=_('What the user submitted')
    )

    is_correct = models.BooleanField(_('is correct'), help_text=_('Whether the answer was correct'))

    attempted_at = models.DateTimeField(_('attempted at'), auto_now_add=True)

    class Meta:
        verbose_name = _('attempt')
        verbose_name_plural = _('attempts')
        ordering = ['attempt_number']
        db_table = 'quiz_attempt'
        unique_together = [['game_session', 'attempt_number']]
        indexes = [models.Index(fields=['game_session', 'attempt_number'])]

    def __str__(self):
        status = '✓' if self.is_correct else '✗'
        return f'{self.game_session.user.email} - Q{self.game_session.question.id} - Attempt #{self.attempt_number} {status}'


class UserStatistics(models.Model):
    """Aggregate user statistics for quiz performance."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_stats',
        verbose_name=_('user'),
    )

    player_level = models.PositiveIntegerField(
        _('player level'), default=1, help_text=_('Game progression level')
    )

    experience_points = models.PositiveIntegerField(_('experience points'), default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('user statistics')
        verbose_name_plural = _('user statistics')
        db_table = 'quiz_user_statistics'

    def __str__(self):
        return f"{self.user.email}'s stats"


class Trophy(models.Model):
    """Achievements/trophies users can unlock."""

    class RequirementType(models.TextChoices):
        LEVEL = 'LEVEL', _('Player Level')
        CATEGORY_MASTER = 'CATEGORY_MASTER', _('Category Mastery')
        # Membership
        # Competetition

    code = models.CharField(
        _('trophy code'),
        max_length=50,
        unique=True,
        help_text=_('Unique identifier, e.g., FIRST_WIN, STREAK_10'),
    )

    requirement_type = models.CharField(
        _('requirement type'),
        max_length=30,
        choices=RequirementType.choices,
        default=RequirementType.LEVEL,
    )

    name = models.CharField(_('trophy name'), max_length=100)

    description = models.TextField(_('description'), help_text=_('How to unlock this trophy'))

    class Meta:
        verbose_name = _('trophy')
        verbose_name_plural = _('trophies')
        ordering = ['name']
        db_table = 'quiz_trophy'

    def __str__(self):
        return self.name


class UserTrophy(models.Model):
    """Trophies unlocked by users."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trophies',
        verbose_name=_('user'),
    )

    trophy = models.ForeignKey(
        Trophy, on_delete=models.CASCADE, related_name='user_trophies', verbose_name=_('trophy')
    )

    unlocked_at = models.DateTimeField(_('unlocked at'), auto_now_add=True)

    class Meta:
        verbose_name = _('user trophy')
        verbose_name_plural = _('user trophies')
        ordering = ['-unlocked_at']
        db_table = 'quiz_user_trophy'
        unique_together = [['user', 'trophy']]
        indexes = [models.Index(fields=['user', '-unlocked_at'])]

    def __str__(self):
        return f'{self.user.email} - {self.trophy.name}'


# ============================================================================
# SIGNALS (Auto-create UserStatistics)
# ============================================================================
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_statistics(sender, instance, created, **kwargs):
    """Automatically create UserStatistics when User is created."""
    if created:
        UserStatistics.objects.create(user=instance)
