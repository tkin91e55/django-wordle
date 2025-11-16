from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Profile, User


class ProfileInline(admin.StackedInline):
    """Inline admin for Profile - shows profile inside User admin."""

    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'

    fields = ('display_name', 'player_level', 'experience_points', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin - extends Django's UserAdmin.

    Uses username for Django admin login (standard approach).
    """

    # What to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Show profile inline when editing a user
    inlines = (ProfileInline,)

    # Fields to show when viewing/editing a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')},
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to show when creating a new user
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for Profile - standalone view."""

    list_display = ('user', 'display_name', 'player_level', 'experience_points', 'created_at')
    list_filter = ('player_level', 'created_at')
    search_fields = ('user__username', 'user__email', 'display_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Profile Info'), {'fields': ('display_name', 'player_level', 'experience_points')}),
        (_('Metadata'), {'fields': ('created_at', 'updated_at')}),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make user field read-only when editing existing profile."""
        if obj:  # Editing existing profile
            return list(self.readonly_fields) + ['user']
        return self.readonly_fields
