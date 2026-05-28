from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('help/', views.help_view, name='help'),
    path('my-documents/', views.my_documents_view, name='my_documents'),
    path('create-document/', views.create_document_view, name='create_document'),
    path('create-folder/', views.create_folder_view, name='create_folder'),
    path('folder/<int:folder_id>/rename/', views.rename_folder_view, name='rename_folder'),
    path('folder/<int:folder_id>/delete/', views.delete_folder_view, name='delete_folder'),
    path('edit-document/<int:document_id>/', views.edit_document_view, name='edit_document'),
    path('document/<int:document_id>/', views.document_detail_view, name='document_detail'),
    path('recycle-bin/', views.recycle_bin_view, name='recycle_bin'),
    path('document/<int:document_id>/versions/', views.version_history_view, name='document_versions'),
    path('document/<int:document_id>/delete/', views.delete_document_view, name='delete_document'),
    path('document/<int:document_id>/restore/', views.restore_document_view, name='restore_document'),
    path('document/<int:document_id>/delete-permanently/', views.permanent_delete_document_view, name='delete_permanently'),
    path('documents/batch-delete/', views.batch_delete_documents_view, name='batch_delete_documents'),
    path('documents/batch-delete-permanently/', views.batch_delete_permanently_view, name='batch_delete_permanently'),
    path('document/<int:document_id>/export/', views.export_document_view, name='export_document'),
    path('api/preview/', views.preview_api_view, name='preview_api'),
    path('api/autosave/', views.autosave_view, name='autosave_api'),
    path('api/import/', views.import_files_view, name='import_file_api'),
    path('api/share/', views.share_api, name='share_api'),
    path('share-document/<int:document_id>/', views.share_api, name='share_document'),
    path('api/rename/<int:document_id>/', views.rename_api, name='rename_api'),
    path('download/<str:share_token>/', views.download_view, name='download'),
]