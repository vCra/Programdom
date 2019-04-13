from django.contrib import admin

from .models import *

admin.site.register(Problem)
admin.site.register(ProblemTest)
admin.site.register(Workshop)
admin.site.register(Submission)
admin.site.register(SubmissionTestResult)
admin.site.register(ProblemLanguage)
