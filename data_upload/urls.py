from django.urls import path
from .views import upload_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
     path('admin/', admin.site.urls),
    path('', include('data_upload.urls')),
]
