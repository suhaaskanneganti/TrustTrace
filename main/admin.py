from django.contrib import admin
from .models import CustomUser, Submission, File

admin.site.register(CustomUser)
admin.site.register(Submission)
admin.site.register(File)
