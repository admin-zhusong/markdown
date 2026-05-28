from django.contrib import admin
from .models import DocumentModel, DocumentVersionModel, ImageModel

@admin.register(DocumentModel)
class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'create_time', 'update_time', 'is_deleted', 'is_shared')
    list_filter = ('is_deleted', 'is_shared', 'create_time')
    search_fields = ('title', 'content')
    readonly_fields = ('create_time', 'update_time')

@admin.register(DocumentVersionModel)
class DocumentVersionModelAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_num', 'create_time', 'remark')
    list_filter = ('create_time',)
    readonly_fields = ('create_time',)

@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('save_name', 'original_name', 'user', 'upload_time')
    list_filter = ('upload_time',)
    readonly_fields = ('upload_time',)
