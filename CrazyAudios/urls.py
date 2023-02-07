from django.urls import path
from .views import index, play_audio, pause_audio, add_new_audio, upload_pdf, delete_files, change_settings

urlpatterns = [
    path('', index),
    path('play-audio/<str:fl>/<int:i>', play_audio),
    path('pause-audio/<str:fl>/<int:i>', pause_audio),
    path('add-new', add_new_audio),
    path('upload-pdf', upload_pdf),
    path('delete-files', delete_files),
    path('change-settings', change_settings),
]

