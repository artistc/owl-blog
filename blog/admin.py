import models
from django.contrib import admin

admin.site.register(models.Article)
admin.site.register(models.Link)
admin.site.register(models.Tag)

class CommentAdmin(admin.ModelAdmin):
	list_filter = ['date_time_added']
admin.site.register(models.Comment, CommentAdmin)
