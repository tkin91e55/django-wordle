from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Keeps all default Django User fields + behaviors.

    Email-based authentication with optional username.
    """

    # Override email to make it unique and required
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={'unique': _('A user with that email already exists.')},
    )

    # Make username optional (auto-generated from email)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,  # Allow blank in forms
        null=False,  # But still required in DB
        help_text=_('Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )

    # Use email as the primary identifier for auth
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required for createsuperuser (beyond email)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users_user'  # Explicit table name

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """Auto-generate username from email if not provided."""
        if not self.username:
            # Generate username from email: john.doe@example.com → john_doe
            local_part = self.email.split('@')[0]
            base_username = local_part.replace('.', '_').replace('+', '_')[:150]

            # Ensure uniqueness
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f'{base_username}_{counter}'
                counter += 1

            self.username = username

        super().save(*args, **kwargs)


class Profile(models.Model):
    """
    Extended user profile for game-specific data.
    Separated from User model for flexibility.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user')
    )

    player_level = models.PositiveIntegerField(
        _('player level'), default=1, help_text=_('Game progression level')
    )

    display_name = models.CharField(
        _('display name'), max_length=20, blank=True, help_text=_('Name shown to other players')
    )

    experience_points = models.PositiveIntegerField(_('experience points'), default=0)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        db_table = 'users_profile'

    def __str__(self):
        return f"{self.user.email}'s profile"


# Signals for auto-creating profiles
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create Profile when User is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
