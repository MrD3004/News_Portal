from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds role-based access control and subscription relationships:
    - Roles: reader, editor, journalist, publisher.
    - Readers can subscribe to publishers and journalists.
    - Publishers, editors, and journalists are linked to publishing workflows.
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
        help_text="Publishers this user is subscribed to (if reader).",
    )
    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="followers",
        help_text="Journalists this user is subscribed to (if reader).",
    )

    # Override groups/permissions to avoid clashes with AbstractUser
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_set", blank=True
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """Return a string representation of the user with role label."""
        return f"{self.username} ({self.get_role_display()})"

    def role_label(self):
        """
        Return the human-readable role name.

        Returns:
            str: Display name of the user's role.
        """
        return dict(self.ROLE_CHOICES).get(self.role, self.role)


class Publisher(models.Model):
    """
    Represents a publishing entity.

    A publisher has:
    - An owner (must have role 'publisher').
    - Associated editors and journalists.
    - A name and description for identification.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="owned_publishers",
        limit_choices_to={"role": "publisher"},
        help_text="User who owns this publisher (must have role 'publisher').",
    )

    editors = models.ManyToManyField(
        CustomUser,
        related_name="editor_publishers",
        blank=True,
        limit_choices_to={"role": "editor"},
        help_text="Editors assigned to this publisher.",
    )
    journalists = models.ManyToManyField(
        CustomUser,
        related_name="journalist_publishers",
        blank=True,
        limit_choices_to={"role": "journalist"},
        help_text="Journalists assigned to this publisher.",
    )

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self):
        """Return a string representation of the publisher with its owner."""
        return f"{self.name} (Owner: {self.owner.username})"

    def get_absolute_url(self):
        """
        Return the canonical URL for this publisher.

        Returns:
            str: URL path to publisher detail view.
        """
        return reverse("publisher_detail", kwargs={"pk": self.pk})


class Article(models.Model):
    """
    News article submitted by a journalist.

    Articles belong to a publisher and may be approved by an editor.
    Each article includes:
    - Title, content, and optional summary.
    - Author (journalist) and publisher.
    - Approval status and timestamps.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(
        max_length=300, blank=True, help_text="Optional short summary for previews."
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "journalist"},
        help_text="The journalist who wrote this article.",
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        help_text="The publisher this article belongs to.",
    )

    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        """Return a string representation of the article with approval status."""
        status = "Approved" if self.approved else "Pending"
        return f"{self.title} ({status})"

    def get_absolute_url(self):
        """
        Return the canonical URL for this article.

        Returns:
            str: URL path to article detail view.
        """
        return reverse("article_detail", kwargs={"pk": self.pk})


class Newsletter(models.Model):
    """
    Periodic newsletter authored by a journalist.

    Newsletters include:
    - Title, content, and optional summary.
    - Author (journalist).
    - Related articles (many-to-many).
    - Creation and update timestamps.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(
        max_length=300, blank=True, help_text="Optional short summary for previews."
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "journalist"},
        help_text="The journalist who authored this newsletter.",
    )
    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
        blank=True,
        help_text="Articles included in this newsletter.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"

    def __str__(self):
        """Return a string representation of the newsletter with its author."""
        return f"{self.title} (by {self.author.username})"

    def get_absolute_url(self):
        """
        Return the canonical URL for this newsletter.

        Returns:
            str: URL path to newsletter detail view.
        """
        return reverse("newsletter_detail", kwargs={"pk": self.pk})
