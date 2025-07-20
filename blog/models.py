from django.db import models
from django.urls import reverse

from django.conf import settings
from taggit.managers import TaggableManager
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image= models.ImageField(upload_to='category/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)


    

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})
    def get_posts_count(self):
        return self.posts.count()


    def __str__(self):
        return self.name
# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        # خليها مؤقتًا تقبل null علشان نعمل الترحيل
        Category, on_delete=models.CASCADE, related_name='posts', null=True,
        blank=True)
    tags = TaggableManager()
    image=models.ImageField(upload_to='blog/', blank=True, null=True)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("single-blog", kwargs={"pk": self.pk})

    def get_related_posts_by_tags(self):
        related_blogs = Blog.objects.filter(
            tags__in=self.tags.all()).distinct()
        return related_blogs


class Comments(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"
    

class Reply(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.comment.blog.title}"    