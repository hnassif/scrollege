from lecture.models import *
from django.contrib import admin

# class UserProfileAdmin(admin.ModelAdmin):
#    list_display = ('__unicode__', 'fb_username', 'year','is_alum')
#    list_filter = ['is_alum','year', 'is_social_member']

# admin.site.register(UserProfile,UserProfileAdmin)
"""
admin.site.register(Course)
admin.site.register(StudentCourse)
admin.site.register(SessionTransaction)
admin.site.register(Session)
admin.site.register(Question)
"""
admin.site.register(Item)
