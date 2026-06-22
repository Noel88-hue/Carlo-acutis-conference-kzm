from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from django.http import JsonResponse
from .models import SocialProgram, ProgramPhoto, UpcomingEvent, FundRecord, MeetingReport, GalleryImage, SupportInfo
from .forms import (SocialProgramForm, ProgramPhotoForm, UpcomingEventForm,
                    FundRecordForm, MeetingReportForm, GalleryImageForm, SupportInfoForm)


def is_admin(user):
    return user.is_staff or user.is_superuser


# ── Public views ──────────────────────────────────────────────────────────────

def home(request):
    programs = SocialProgram.objects.filter(is_featured=True)[:3]
    events = UpcomingEvent.objects.filter(date__gte=timezone.now().date(), status__in=['planned', 'confirmed'])[:3]
    total_funds = FundRecord.objects.aggregate(total=Sum('amount'))['total'] or 0
    gallery = GalleryImage.objects.filter(is_featured=True)[:6]
    stats = {
        'programs': SocialProgram.objects.count(),
        'events': UpcomingEvent.objects.count(),
        'reports': MeetingReport.objects.count(),
        'funds': total_funds,
    }
    return render(request, 'core/home.html', {
        'programs': programs, 'events': events, 'gallery': gallery, 'stats': stats
    })


def about_view(request):
    return render(request, 'core/about.html')


def programs_list(request):
    category = request.GET.get('category', '')
    programs = SocialProgram.objects.all()
    if category:
        programs = programs.filter(category=category)
    categories = SocialProgram.CATEGORY_CHOICES
    return render(request, 'core/programs_list.html', {
        'programs': programs, 'categories': categories, 'selected_category': category
    })


def program_detail(request, pk):
    program = get_object_or_404(SocialProgram, pk=pk)
    photos = program.photos.all()
    return render(request, 'core/program_detail.html', {'program': program, 'photos': photos})


def events_list(request):
    upcoming = UpcomingEvent.objects.filter(date__gte=timezone.now().date()).exclude(status='cancelled')
    past = UpcomingEvent.objects.filter(date__lt=timezone.now().date())
    return render(request, 'core/events_list.html', {'upcoming': upcoming, 'past': past})


def event_detail(request, pk):
    event = get_object_or_404(UpcomingEvent, pk=pk)
    return render(request, 'core/event_detail.html', {'event': event})


def funds_view(request):
    records = FundRecord.objects.all()
    total = records.aggregate(total=Sum('amount'))['total'] or 0
    by_period = records.values('period_type').annotate(total=Sum('amount'), count=Count('id'))
    return render(request, 'core/funds.html', {'records': records, 'total': total, 'by_period': by_period})


def reports_list(request):
    reports = MeetingReport.objects.all()
    return render(request, 'core/reports_list.html', {'reports': reports})


def report_detail(request, pk):
    report = get_object_or_404(MeetingReport, pk=pk)
    return render(request, 'core/report_detail.html', {'report': report})


def gallery_view(request):
    images = GalleryImage.objects.all()
    return render(request, 'core/gallery.html', {'images': images})


def support_view(request):
    """Public transparency page — QR code + bank details for those who wish
    to contribute, plus the Matthew 6:3-4 verse. Not a payment flow."""
    info = SupportInfo.objects.first()
    return render(request, 'core/support.html', {'info': info})


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ── Admin / Dashboard ─────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    stats = {
        'programs': SocialProgram.objects.count(),
        'events': UpcomingEvent.objects.count(),
        'reports': MeetingReport.objects.count(),
        'total_funds': FundRecord.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'upcoming_events': UpcomingEvent.objects.filter(date__gte=timezone.now().date()).count(),
        'gallery_images': GalleryImage.objects.count(),
    }
    recent_programs = SocialProgram.objects.all()[:5]
    recent_reports = MeetingReport.objects.all()[:5]
    recent_funds = FundRecord.objects.all()[:5]
    upcoming_events = UpcomingEvent.objects.filter(date__gte=timezone.now().date())[:5]
    fund_data = list(FundRecord.objects.values('period_label', 'period_type').annotate(total=Sum('amount')).order_by('-date_recorded')[:12])
    return render(request, 'core/dashboard.html', {
        'stats': stats,
        'recent_programs': recent_programs,
        'recent_reports': recent_reports,
        'recent_funds': recent_funds,
        'upcoming_events': upcoming_events,
        'fund_data': fund_data,
    })


# Programs CRUD
@login_required
def program_create(request):
    form = SocialProgramForm(request.POST or None)
    if form.is_valid():
        prog = form.save(commit=False)
        prog.created_by = request.user
        prog.save()
        messages.success(request, 'Program saved successfully.')
        return redirect('program_photos', pk=prog.pk)
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Add Social Program', 'icon': '🤝'})


@login_required
def program_edit(request, pk):
    program = get_object_or_404(SocialProgram, pk=pk)
    form = SocialProgramForm(request.POST or None, instance=program)
    if form.is_valid():
        form.save()
        messages.success(request, 'Program updated.')
        return redirect('program_detail', pk=pk)
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Edit Program', 'icon': '✏️', 'obj': program})


@login_required
def program_delete(request, pk):
    program = get_object_or_404(SocialProgram, pk=pk)
    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Program deleted.')
        return redirect('programs_list')
    return render(request, 'core/confirm_delete.html', {'obj': program, 'type': 'Program'})


@login_required
def program_photos(request, pk):
    program = get_object_or_404(SocialProgram, pk=pk)
    photos = program.photos.all()
    if request.method == 'POST':
        form = ProgramPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.program = program
            photo.save()
            messages.success(request, 'Photo added.')
            return redirect('program_photos', pk=pk)
    else:
        form = ProgramPhotoForm()
    return render(request, 'core/program_photos.html', {'program': program, 'photos': photos, 'form': form})


@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(ProgramPhoto, pk=pk)
    prog_pk = photo.program.pk
    photo.delete()
    messages.success(request, 'Photo deleted.')
    return redirect('program_photos', pk=prog_pk)


# Events CRUD
@login_required
def event_create(request):
    form = UpcomingEventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        ev = form.save(commit=False)
        ev.created_by = request.user
        ev.save()
        messages.success(request, 'Event added.')
        return redirect('events_list')
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Add Upcoming Event', 'icon': '📅'})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(UpcomingEvent, pk=pk)
    form = UpcomingEventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, 'Event updated.')
        return redirect('event_detail', pk=pk)
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Edit Event', 'icon': '✏️', 'obj': event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(UpcomingEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted.')
        return redirect('events_list')
    return render(request, 'core/confirm_delete.html', {'obj': event, 'type': 'Event'})


# Funds CRUD
@login_required
def fund_create(request):
    form = FundRecordForm(request.POST or None)
    if form.is_valid():
        fund = form.save(commit=False)
        fund.created_by = request.user
        fund.save()
        messages.success(request, 'Fund record added.')
        return redirect('funds')
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Add Fund Record', 'icon': '💰'})


@login_required
def fund_edit(request, pk):
    fund = get_object_or_404(FundRecord, pk=pk)
    form = FundRecordForm(request.POST or None, instance=fund)
    if form.is_valid():
        form.save()
        messages.success(request, 'Fund record updated.')
        return redirect('funds')
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Edit Fund Record', 'icon': '✏️', 'obj': fund})


@login_required
def fund_delete(request, pk):
    fund = get_object_or_404(FundRecord, pk=pk)
    if request.method == 'POST':
        fund.delete()
        messages.success(request, 'Record deleted.')
        return redirect('funds')
    return render(request, 'core/confirm_delete.html', {'obj': fund, 'type': 'Fund Record'})


# Reports CRUD
@login_required
def report_create(request):
    form = MeetingReportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        report = form.save(commit=False)
        report.created_by = request.user
        report.save()
        messages.success(request, 'Report saved.')
        return redirect('report_detail', pk=report.pk)
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Add Meeting Report', 'icon': '📋'})


@login_required
def report_edit(request, pk):
    report = get_object_or_404(MeetingReport, pk=pk)
    form = MeetingReportForm(request.POST or None, request.FILES or None, instance=report)
    if form.is_valid():
        form.save()
        messages.success(request, 'Report updated.')
        return redirect('report_detail', pk=pk)
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Edit Report', 'icon': '✏️', 'obj': report})


@login_required
def report_delete(request, pk):
    report = get_object_or_404(MeetingReport, pk=pk)
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted.')
        return redirect('reports_list')
    return render(request, 'core/confirm_delete.html', {'obj': report, 'type': 'Report'})


# Gallery
@login_required
def gallery_upload(request):
    form = GalleryImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        img = form.save(commit=False)
        img.uploaded_by = request.user
        img.save()
        messages.success(request, 'Image added to gallery.')
        return redirect('gallery')
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Upload Gallery Image', 'icon': '🖼️'})


@login_required
def gallery_delete(request, pk):
    img = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        img.delete()
        messages.success(request, 'Image deleted.')
        return redirect('gallery')
    return render(request, 'core/confirm_delete.html', {'obj': img, 'type': 'Gallery Image'})


@login_required
def support_edit(request):
    info = SupportInfo.objects.first()
    if not info:
        info = SupportInfo()
    form = SupportInfoForm(request.POST or None, request.FILES or None, instance=info)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.updated_by = request.user
        obj.save()
        messages.success(request, 'Support page updated.')
        return redirect('support')
    return render(request, 'core/form_page.html', {'form': form, 'title': 'Edit Support / Giving Page', 'icon': '🙏'})
