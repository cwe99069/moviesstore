from django.contrib import admin
from .models import Report
# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        for report in queryset:
            review = report.review
            review.reported = False
            review.save()
        queryset.delete()
admin.site.register(Report, MyModelAdmin)