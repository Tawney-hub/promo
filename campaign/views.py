from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CampaignLocation, PromoCode, Lead, ScanLog
import random

def home(request):
    source = request.GET.get('src', 'web')
    return render(request, 'campaign/home.html', {'source': source})

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
        # In a real system, you might assign specific codes based on location
        codes = PromoCode.objects.filter(is_active=True)
        if not codes.exists():
            # Fallback if no codes exist
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
        
        return render(request, 'campaign/success.html', {
            'lead': lead,
            'code': promo
        })
    
    return redirect('home')
