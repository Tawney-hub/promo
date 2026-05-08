from django.db import models

class CampaignLocation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PromoCode(models.Model):
    CODE_TYPES = [
        ('IT', 'IT Equipment'),
        ('STARLINK', 'Starlink Service'),
        ('PARTNER', 'Partner Offer'),
    ]
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    reward_type = models.CharField(max_length=20, choices=CODE_TYPES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.get_reward_type_display()})"

class Lead(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    location = models.ForeignKey(CampaignLocation, on_delete=models.SET_NULL, null=True)
    unlocked_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

class ScanLog(models.Model):
    location = models.ForeignKey(CampaignLocation, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan at {self.location.name} on {self.scanned_at}"

class MediaContent(models.Model):
    # Music Section
    youtube_url = models.URLField(default="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    music_title = models.CharField(max_length=200, default="Midnight Protocol")
    
    # IT Section
    it_ad_title = models.CharField(max_length=200, default="Premium IT Support")
    it_ad_desc = models.TextField(default="Get 15% off your first Starlink installation.")
    it_ad_link = models.URLField(default="https://example.com")
    
    # Linked Campaign
    featured_promo = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

class MusicTrack(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default="YOUTHinIT")
    audio_file = models.FileField(upload_to='music/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} - {self.title}"
