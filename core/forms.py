from django import forms
from .models import SocialProgram, ProgramPhoto, UpcomingEvent, FundRecord, MeetingReport, GalleryImage, SupportInfo


class SocialProgramForm(forms.ModelForm):
    class Meta:
        model = SocialProgram
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ProgramPhotoForm(forms.ModelForm):
    class Meta:
        model = ProgramPhoto
        fields = ['image', 'caption']


class UpcomingEventForm(forms.ModelForm):
    class Meta:
        model = UpcomingEvent
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class FundRecordForm(forms.ModelForm):
    class Meta:
        model = FundRecord
        exclude = ['created_by', 'created_at']
        widgets = {
            'date_recorded': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MeetingReportForm(forms.ModelForm):
    class Meta:
        model = MeetingReport
        exclude = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'next_meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'agenda': forms.Textarea(attrs={'rows': 3}),
            'minutes': forms.Textarea(attrs={'rows': 6}),
            'decisions_made': forms.Textarea(attrs={'rows': 3}),
            'action_items': forms.Textarea(attrs={'rows': 3}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption', 'is_featured']


class SupportInfoForm(forms.ModelForm):
    class Meta:
        model = SupportInfo
        exclude = ['updated_at', 'updated_by']
        widgets = {
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }
