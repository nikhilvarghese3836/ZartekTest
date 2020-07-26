from django.contrib import admin
from .models import Posts,TagWeight,PostImage
# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    list_display = ['title','description',]
    list_filter = ['title','description',]
    search_fields = ['title','description',]
class TagWeightAdmin(admin.ModelAdmin):
    list_display = ['fk_post','tag','weight']
    list_filter = ['fk_post','tag','weight']
    search_fields = ['fk_post','tag','weight']
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['fk_post','images']
    list_filter = ['fk_post','images']
    search_fields = ['fk_post','images']
admin.site.register(Posts,PostsAdmin)
admin.site.register(TagWeight,TagWeightAdmin)
admin.site.register(PostImage,PostImageAdmin)
