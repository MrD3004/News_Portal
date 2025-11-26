from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse


class CustomUser(AbstractUser):
    """
    Custom user model with role-based access and subscription relationships.
    """
    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("editor", "Editor"),
        ("journalist", "Journalist"),
        ("publisher", "Publisher"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="reader")

    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        blank=True,
        related_name="subscribed_readers",
        help_text="Publishers this user is subscribed to (if reader)."
    )
    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="followers",
        help_text="Journalists this user is subscribed to (if reader)."
    )

    # Override groups/permissions to avoid clashes with AbstractUser
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def role_label(self):
        """Return the human-readable role name (safe helper)."""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)


class Publisher(models.Model):
    """
    Represents a publishing entity with associated editors and journalists.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="owned_publishers",   # plural, since one user can own many
        limit_choices_to={"role": "publisher"},
        help_text="User who owns this publisher (must have role 'publisher')."
    )

    editors = models.ManyToManyField(
        CustomUser,
        related_name="editor_publishers",
        blank=True,
        limit_choices_to={"role": "editor"},
        help_text="Editors assigned to this publisher."
    )
    journalists = models.ManyToManyField(
        CustomUser,
        related_name="journalist_publishers",
        blank=True,
        limit_choices_to={"role": "journalist"},
        help_text="Journalists assigned to this publisher."
    )

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"

    def get_absolute_url(self):
        return reverse("publisher_detail", kwargs={"pk": self.pk})


class Article(models.Model):
    """
    News article submitted by a journalist and optionally approved by an editor.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(max_length=300, blank=True, help_text="Optional short summary for previews.")

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "journalist"},
        help_text="The journalist who wrote this article."
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        help_text="The publisher this article belongs to."
    )

    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        status = "Approved" if self.approved else "Pending"
        return f"{self.title} ({status})"

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})


class Newsletter(models.Model):
    """
    Periodic newsletter authored by a journalist.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(max_length=300, blank=True, help_text="Optional short summary for previews.")

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "journalist"},
        help_text="The journalist who authored this newsletter."
    )
    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
        blank=True,
        help_text="Articles included in this newsletter."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"

    def __str__(self):
        return f"{self.title} (by {self.author.username})"

    def get_absolute_url(self):
        return reverse("newsletter_detail", kwargs={"pk": self.pk})








