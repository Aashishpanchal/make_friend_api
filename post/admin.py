from django.contrib import admin

from post.models import Post, SavePost, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(SavePost)
class SavePostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
