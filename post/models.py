import uuid
from django.db import models
from django.contrib.auth import get_user_model

from post.utils import post_image_path, post_default_image

UserModel = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    post_image = models.ImageField(
        upload_to=post_image_path, default=post_default_image)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{class_name}(id: {_id}, user: {user}, title: {title})>".format(
            class_name=self.__class__.__name__,
            _id=self.id,
            user=self.user.username,
            title=self.title
        )


class SavePost(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="saved_posts")
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_saved_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{class_name}(id: {_id}, user: {user}, post: {post})>".format(
            class_name=self.__class__.__name__,
            _id=self.id,
            user=self.user.username,
            post=self.post.title
        )


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_of_comments")
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{class_name}(id: {_id}, user: {user}, post: {post}, content: {content})>".format(
            class_name=self.__class__.__name__,
            _id=self.id,
            user=self.user.username,
            post=self.post.title,
            content=self.content[:10]
        )


class Like(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False, serialize=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_of_likes")
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{class_name}(id: {_id}, user: {user}, post: {post})>".format(
            class_name=self.__class__.__name__,
            _id=self.id,
            user=self.user.username,
            post=self.post.title
        )
