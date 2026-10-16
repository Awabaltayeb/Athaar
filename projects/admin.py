from django.contrib import admin
from .models import Category, Project, ProjectMember, ProjectMedia

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1

class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'status', 'course_name', 'semester', 'created_at')
    list_filter = ('status', 'categories', 'semester', 'created_at')
    search_fields = ('title', 'summary', 'technologies', 'created_by__username', 'created_by__first_name')
    inlines = [ProjectMemberInline, ProjectMediaInline]
    filter_horizontal = ('categories',)
