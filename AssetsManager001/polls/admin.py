
from django.contrib import admin

# from .models import Choice,Question
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']
# 
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]
# 
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)

from .models import Device_history,Devices,Users
admin.site.register(Device_history)
admin.site.register(Devices)
admin.site.register(Users)