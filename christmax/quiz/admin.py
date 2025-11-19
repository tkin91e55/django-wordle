"""Django admin configuration for quiz app."""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Attempt
from .models import Category
from .models import GameSession
from .models import Question
from .models import Trophy
from .models import UserStatistics
from .models import UserTrophy


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category."""

    list_display = ['name', 'get_name_display', 'order']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']

    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        (_('Display'), {'fields': ('icon_class', 'order')}),
    )

    def get_name_display(self, obj):
        """Display the translated category name."""
        return obj.get_name_display()  # type: ignore[attr-defined]

    get_name_display.short_description = _('Display Name')  # type: ignore[attr-defined]


class AttemptInline(admin.TabularInline):
    """Inline display for attempts (used in GameSession)."""

    model = Attempt
    extra = 0
    readonly_fields = ['attempt_number', 'user_answer', 'is_correct', 'attempted_at']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question."""

    list_display = [
        'id',
        'question_text_short',
        'category',
        'difficulty',
        'is_active',
        'created_at',
    ]
    list_filter = ['category', 'difficulty', 'is_active', 'created_at']
    search_fields = ['question_text', 'answer', 'code_snippet']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        (_('Basic Info'), {'fields': ('category', 'difficulty', 'is_active')}),
        (
            _('Question Content'),
            {
                'fields': ('question_text', 'code_snippet', 'answer'),
                'description': _(
                    'Enter the question text and optional code snippet. '
                    'Answer is case-insensitive.'
                ),
            },
        ),
        (_('Help & Explanation'), {'fields': ('hint_text', 'explanation')}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')}),
    )

    def question_text_short(self, obj):
        """Display shortened question text."""
        text = obj.get_question_text('en')  # Use helper method
        return text[:50] + '...' if len(text) > 50 else text

    question_text_short.short_description = _('Question')  # type: ignore[attr-defined]


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    """Admin interface for GameSession."""

    list_display = [
        'id',
        'user',
        'question_short',
        'status_display',
        'score',
        'started_at',
    ]
    list_filter = ['started_at', 'end_at']
    search_fields = ['user__email', 'user__username', 'question__question_text']
    readonly_fields = [
        'started_at',
        'end_at',
        'completed_at',
        'status_display',
    ]
    ordering = ['-started_at']
    inlines = [AttemptInline]

    fieldsets = (
        (_('Session Info'), {'fields': ('user', 'question')}),
        (
            _('Timing'),
            {
                'fields': (
                    'started_at',
                    'end_at',
                    'completed_at',
                )
            },
        ),
        (_('Progress'), {'fields': ('status_display', 'score')}),
    )

    def question_short(self, obj):
        """Display shortened question text."""
        question_text = obj.question.get_question_text('en')
        if len(question_text) > 30:
            return question_text[:30] + '...'
        return question_text

    question_short.short_description = _('Question')  # type: ignore[attr-defined]

    def status_display(self, obj):
        """Display computed status with color coding."""
        status = obj.status
        colors = {
            'IN_PROGRESS': '#17a2b8',  # info blue
            'WON': '#28a745',  # success green
            'LOST': '#dc3545',  # danger red
            'ABANDONED': '#6c757d',  # secondary gray
        }
        color = colors.get(status, '#6c757d')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, status)

    status_display.short_description = _('Status')  # type: ignore[attr-defined]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """Admin interface for Attempt."""

    list_display = [
        'id',
        'game_session',
        'attempt_number',
        'user_answer',
        'is_correct',
        'attempted_at',
    ]
    list_filter = ['is_correct', 'attempted_at']
    search_fields = ['game_session__user__email', 'user_answer']
    readonly_fields = ['attempted_at']
    ordering = ['-attempted_at']

    fieldsets = (
        (_('Attempt Info'), {'fields': ('game_session', 'attempt_number')}),
        (_('Answer'), {'fields': ('user_answer', 'is_correct')}),
        (_('Timestamp'), {'fields': ('attempted_at',)}),
    )


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    """Admin interface for UserStatistics."""

    list_display = ['user', 'player_level', 'experience_points']
    list_filter = ['player_level', 'created_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-experience_points']

    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Level & XP'), {'fields': ('player_level', 'experience_points')}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')}),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make user field read-only when editing."""
        if obj:
            return list(self.readonly_fields) + ['user']
        return self.readonly_fields


@admin.register(Trophy)
class TrophyAdmin(admin.ModelAdmin):
    """Admin interface for Trophy."""

    list_display = ['name', 'code', 'requirement_type']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']

    fieldsets = ((_('Trophy Info'), {'fields': ('code', 'name', 'description')}),)


@admin.register(UserTrophy)
class UserTrophyAdmin(admin.ModelAdmin):
    """Admin interface for UserTrophy."""

    list_display = ['user', 'trophy', 'unlocked_at']
    list_filter = ['unlocked_at', 'trophy']
    search_fields = ['user__email', 'user__username', 'trophy__name']
    readonly_fields = ['unlocked_at']
    ordering = ['-unlocked_at']

    fieldsets = (
        (_('User Trophy'), {'fields': ('user', 'trophy')}),
        (_('Unlocked'), {'fields': ('unlocked_at',)}),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make fields read-only when editing."""
        if obj:
            return list(self.readonly_fields) + ['user', 'trophy']
        return self.readonly_fields
