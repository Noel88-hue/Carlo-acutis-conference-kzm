from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SocialProgram(models.Model):
    CATEGORY_CHOICES = [
        ('outreach', 'Community Outreach'),
        ('education', 'Education'),
        ('health', 'Health & Welfare'),
        ('spiritual', 'Spiritual Activity'),
        ('charity', 'Charity Drive'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=300, blank=True)
    beneficiaries = models.CharField(max_length=200, blank=True)
    participants_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class ProgramPhoto(models.Model):
    program = models.ForeignKey(SocialProgram, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='programs/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.program.title}"


class UpcomingEvent(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=300, blank=True)
    organizer = models.CharField(max_length=200, blank=True)
    contact_info = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    banner = models.ImageField(upload_to='events/', null=True, blank=True)
    registration_link = models.URLField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def is_upcoming(self):
        return self.date >= timezone.now().date()


class FundRecord(models.Model):
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
        ('event', 'Event-Based'),
        ('donation', 'Donation'),
    ]
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='monthly')
    period_label = models.CharField(max_length=100)
    date_recorded = models.DateField()
    source = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_recorded']

    def __str__(self):
        return f"{self.title} - Rs.{self.amount} ({self.period_label})"


class MeetingReport(models.Model):
    title = models.CharField(max_length=200)
    meeting_date = models.DateField()
    venue = models.CharField(max_length=300, blank=True)
    attendees_count = models.PositiveIntegerField(default=0)
    agenda = models.TextField(blank=True)
    minutes = models.TextField()
    decisions_made = models.TextField(blank=True)
    action_items = models.TextField(blank=True)
    next_meeting_date = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='reports/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-meeting_date']

    def __str__(self):
        return f"{self.title} — {self.meeting_date}"


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.caption or f"Gallery image {self.pk}"


class SupportInfo(models.Model):
    """
    Admin-managed content for the public 'Support Our Work' page —
    a transparency/info page (QR code + bank details for those who wish to
    give), not a payment processing feature.
    """
    qr_code = models.ImageField(upload_to='support/', blank=True, null=True,
                                 help_text="Upload the bank/UPI QR code image")
    bank_name = models.CharField(max_length=200, blank=True)
    account_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    ifsc_code = models.CharField(max_length=50, blank=True)
    upi_id = models.CharField(max_length=100, blank=True, help_text="e.g. conference@upi")
    additional_notes = models.TextField(blank=True, help_text="Any extra instructions for contributors")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Support Page Info"
        verbose_name_plural = "Support Page Info"

    def __str__(self):
        return "Support / Giving Page Info"
