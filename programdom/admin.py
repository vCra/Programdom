from django.contrib import admin

from .models import *

admin.site.register(Module)
admin.site.register(Workshop)
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(SubmissionResult)
