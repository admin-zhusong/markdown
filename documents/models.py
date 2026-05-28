from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

def generate_share_token():
    return str(uuid.uuid4())[:20]

class FolderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    delete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class DocumentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    folder = models.ForeignKey(FolderModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    title = models.CharField(max_length=200, default='未命名文档')
    content = models.TextField(default='')
    original_filename = models.CharField(max_length=200, default='', blank=True)
    tags = models.CharField(max_length=500, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    delete_time = models.DateTimeField(null=True, blank=True)
    is_shared = models.BooleanField(default=False)
    share_token = models.CharField(max_length=50, default='', blank=True)
    share_expire = models.DateTimeField(null=True, blank=True)
    share_password = models.CharField(max_length=128, default='', blank=True)

    def __str__(self):
        return self.title

    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []

class DocumentVersionModel(models.Model):
    document = models.ForeignKey(DocumentModel, on_delete=models.CASCADE, related_name='versions')
    content = models.TextField()
    version_num = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return f'{self.document.title} - v{self.version_num}'

class ImageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    document = models.ForeignKey(DocumentModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    image_path = models.FileField(upload_to='images/')
    original_name = models.CharField(max_length=200)
    save_name = models.CharField(max_length=200)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.save_name
