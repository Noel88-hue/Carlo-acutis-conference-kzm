from django.contrib import admin
from .models import SocialProgram, ProgramPhoto, UpcomingEvent, FundRecord, MeetingReport, GalleryImage, SupportInfo


class ProgramPhotoInline(admin.TabularInline):
    model = ProgramPhoto
    extra = 1


@admin.register(SocialProgram)
class SocialProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'venue', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')
    inlines = [ProgramPhotoInline]


@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'venue')
    list_filter = ('status',)
    search_fields = ('title', 'description')


@admin.register(FundRecord)
class FundRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'period_type', 'period_label', 'date_recorded')
    list_filter = ('period_type',)
    search_fields = ('title', 'source')


@admin.register(MeetingReport)
class MeetingReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'meeting_date', 'attendees_count')
    search_fields = ('title', 'minutes')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'uploaded_at', 'is_featured')


@admin.register(SupportInfo)
class SupportInfoAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_name', 'updated_at')
