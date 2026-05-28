from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CoachAssignment, CoachFeedback


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Fitness Tracker', {'fields': ('role', 'bio', 'avatar')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')


admin.site.register(CoachAssignment)
admin.site.register(CoachFeedback)
