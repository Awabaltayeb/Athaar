from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'full_name_display', 'role', 'department', 'academic_id', 'is_active')
    list_filter = ('role', 'is_active', 'department')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'academic_id')
    
    fieldsets = UserAdmin.fieldsets + (
        ('بيانات منصة أثَر الأكاديمية', {
            'fields': ('role', 'academic_id', 'department', 'avatar')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('بيانات منصة أثَر الأكاديمية', {
            'fields': ('role', 'academic_id', 'department', 'avatar')
        }),
    )

    def full_name_display(self, obj):
        return obj.get_full_name() or obj.username
    full_name_display.short_description = 'الاسم الكامل'
