import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artist_promo.settings')
django.setup()

from campaign.models import CampaignLocation, PromoCode

def seed():
    # Locations
    locations = [
        ('City Taxi #42', 'taxi-42'),
        ('Main Bus Terminus', 'bus-main'),
        ('Corner IT Shop', 'corner-it'),
        ('Starlink Hub', 'starlink-hub'),
    ]
    
    for name, slug in locations:
        CampaignLocation.objects.get_or_create(name=name, slug=slug)
        print(f"Location created: {name}")

    # Promo Codes
    codes = [
        ('STAR-LINK-15', '15% Off Starlink Installation', 'STARLINK'),
        ('LAPTOP-FIX-10', '10% Off IT Hardware Repair', 'IT'),
        ('FREE-TECH-AUDIT', 'Free IT Security Audit', 'PARTNER'),
        ('ALBUM-VIP-20', '20% Off Limited Edition Merch', 'PARTNER'),
    ]
    
    for code, desc, r_type in codes:
        PromoCode.objects.get_or_create(code=code, description=desc, reward_type=r_type)
        print(f"PromoCode created: {code}")

if __name__ == "__main__":
    seed()
