from django.contrib import admin
from .models import Department

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)
    search_fields = ('department_name',)
    list_filter = ('department_name',)

# Register the admin site
admin.site.site_header = "Network Admin Panel"
admin.site.site_title = "Network Portal"
admin.site.index_title = "Welcome to the Admin Portal of network"
