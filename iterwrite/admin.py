from django.contrib import admin
from .models import User, Paper, Comment, Community

admin.site.register(User)
admin.site.register(Paper)
admin.site.register(Comment)
admin.site.register(Community)