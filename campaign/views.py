from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import CampaignLocation, PromoCode, Lead, ScanLog, MediaContent, MusicTrack
import random
import csv

def home(request):
    source = request.GET.get('src', 'web')
    media = MediaContent.objects.select_related('featured_promo').first()
    if not media:
        media = MediaContent.objects.create()
    
    tracks = MusicTrack.objects.all().order_by('-created_at')
    
    claim_count = Lead.objects.filter(unlocked_code=media.featured_promo).count() if media.featured_promo else 0
    current_location = CampaignLocation.objects.filter(slug=source).first()
    
    context = {
        'source': source,
        'media': media,
        'claim_count': claim_count,
        'current_location': current_location,
        'music_tracks': tracks,
    }
    return render(request, 'campaign/home.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'campaign/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@staff_member_required
def upload_music(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        title = request.POST.get('title')
        artist = request.POST.get('artist', 'YOUTHinIT')
        audio_file = request.FILES.get('audio_file')
        
        MusicTrack.objects.create(
            title=title,
            artist=artist,
            audio_file=audio_file
        )
        messages.success(request, "Music track uploaded successfully!")
    return redirect('dashboard')
@staff_member_required
def create_location(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        CampaignLocation.objects.create(name=name, slug=slug)
        messages.success(request, f"Location '{name}' created successfully!")
    return redirect('dashboard')

@staff_member_required
def create_promo(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        desc = request.POST.get('description')
        reward_type = request.POST.get('reward_type', 'PARTNER')
        PromoCode.objects.create(code=code, description=desc, reward_type=reward_type)
        messages.success(request, f"Promo Code '{code}' created successfully!")
    return redirect('dashboard')

@staff_member_required
def update_media_content(request):
    if request.method == 'POST':
        media = MediaContent.objects.first()
        if not media:
            media = MediaContent.objects.create()
        
        media.youtube_url = request.POST.get('youtube_url', media.youtube_url)
        media.music_title = request.POST.get('music_title', media.music_title)
        media.it_ad_title = request.POST.get('it_ad_title', media.it_ad_title)
        media.it_ad_desc = request.POST.get('it_ad_desc', media.it_ad_desc)
        media.it_ad_link = request.POST.get('it_ad_link', media.it_ad_link)
        
        promo_id = request.POST.get('featured_promo')
        if promo_id:
            media.featured_promo_id = promo_id
        
        media.save()
        messages.success(request, "Media content updated successfully!")
    return redirect('dashboard')

def scan_landing(request, slug):
    location = get_object_or_404(CampaignLocation, slug=slug)
    
    # Log the scan
    ScanLog.objects.create(
        location=location,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )
    
    # Redirect to home with source context
    return redirect(f'/?src={slug}')

def claim_reward(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        source_slug = request.POST.get('source', 'web')
        
        location = CampaignLocation.objects.filter(slug=source_slug).first()
        
        # Pick a random active promo code for the MVP
        codes = PromoCode.objects.filter(is_active=True)
        if not codes.exists():
            promo = PromoCode.objects.create(
                code="VIP2026", 
                description="General 10% Discount", 
                reward_type="PARTNER"
            )
        else:
            promo = random.choice(codes)
            
        lead = Lead.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            location=location,
            unlocked_code=promo
        )
        
        # Send Email Notification (Fail silently if SMTP not configured)
        try:
            subject = f"New Lead Captured: {full_name}"
            message = f"Name: {full_name}\nPhone: {phone}\nEmail: {email}\nSource: {location.name if location else 'Direct'}\nCode: {promo.code}"
            send_mail(subject, message, 'noreply@artistpromo.com', ['admin@artistpromo.com'], fail_silently=True)
        except:
            pass
        
        return render(request, 'campaign/success.html', {
            'lead': lead,
            'code': promo
        })
    
    return redirect('home')

@staff_member_required
def dashboard(request):
    # Overall Metrics
    total_scans = ScanLog.objects.count()
    total_leads = Lead.objects.count()
    total_codes = PromoCode.objects.count()
    
    conversion_rate = (total_leads / total_scans * 100) if total_scans > 0 else 0
    
    # Location Performance (Scans per Location)
    location_stats = CampaignLocation.objects.annotate(
        scan_count=Count('scanlog'),
        lead_count=Count('lead')
    ).order_by('-scan_count')
    
    # Recent Activity
    recent_leads = Lead.objects.select_related('location', 'unlocked_code').order_by('-created_at')[:8]
    
    # Promo Code distribution
    code_usage = PromoCode.objects.annotate(
        usage_count=Count('lead')
    ).filter(usage_count__gt=0).order_by('-usage_count')

    media = MediaContent.objects.first()
    if not media:
        media = MediaContent.objects.create()
    
    all_promos = PromoCode.objects.filter(is_active=True)
    
    context = {
        'total_scans': total_scans,
        'total_leads': total_leads,
        'total_codes': total_codes,
        'conversion_rate': round(conversion_rate, 1),
        'location_stats': location_stats,
        'recent_leads': recent_leads,
        'code_usage': code_usage,
        'media': media,
        'all_promos': all_promos,
        'music_tracks': MusicTrack.objects.all().order_by('-created_at'),
    }
    
    return render(request, 'campaign/dashboard.html', context)

@staff_member_required
def export_leads_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="campaign_leads.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email', 'Location', 'Promo Code', 'Captured At'])
    
    leads = Lead.objects.select_related('location', 'unlocked_code').all().order_by('-created_at')
    
    for lead in leads:
        writer.writerow([
            lead.full_name,
            lead.phone,
            lead.email,
            lead.location.name if lead.location else 'Direct',
            lead.unlocked_code.code if lead.unlocked_code else 'N/A',
            lead.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
        
    return response
