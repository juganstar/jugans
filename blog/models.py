from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from better_profanity import profanity


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('rejected', 'Rejected'),
    ('flagged', 'Flagged for Review')
]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        # Auto-publish if no profanity is detected
        if not (profanity.contains_profanity(self.title) or 
                profanity.contains_profanity(self.content)):
            self.status = 'published'  # Auto-accept clean posts
        else:
            self.status = 'flagged'    # Flag for review if profanity exists

        # Generate slug (keep your existing logic)
        if not self.slug:
            self.slug = slugify(self.title)
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1

        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ('-publish_date',)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'