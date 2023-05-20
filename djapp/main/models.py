from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        rrat = 0
        for post in self.post_set.all():
            rrat += post.rating * 3
            for comment in post.comment_set.all():
                if comment.user.author == self:
                    rrat += comment.rating
                if post.type == PostType.POST:
                    rrat += comment.rating
            self.rating = rrat
        self.save(update_fields=['rating'])


class Category(models.Model):
    cat_name = models.CharField(max_length=256, unique=True)


class PostType(models.TextChoices):
    POST = 'P', 'Статья'
    NEW = 'N', 'Новость'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=PostType.choices, default=PostType.POST)
    topic = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField()

    def like(self):
        self.rating += 1
        self.save(update_fields=['rating'])

    def dislike(self):
        self.rating -= 1
        self.save(update_fields=['rating'])

    def preview(self):
        return self.text[:20] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField()
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save(update_fields=['rating'])

    def dislike(self):
        self.rating -= 1
        self.save(update_fields=['rating'])
