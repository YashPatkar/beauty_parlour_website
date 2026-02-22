"""
Seed script: adds sample Services and Staff for testing booking and payment.
Run from project folder: python python_seed.py
"""
import os
import sys
import django

# Setup Django so we can use the ORM
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import Service, Staff

# Same placeholder image URL used site-wide for services (from config.context_processors DEFAULT_IMAGES)
SERVICE_IMAGE_URL = 'https://images.pexels.com/photos/853427/pexels-photo-853427.jpeg?cs=srgb&dl=pexels-delbeautybox-211032-853427.jpg&fm=jpg'


def run():
    # Locations (branches)
    locations = ['Chembur', 'Bandra', 'Andheri West', 'Powai', 'Juhu', 'Santacruz', 'Malad']

    # Services – 20 items with same image_url (existing placeholder)
    services_data = [
        {'name': 'Haircut & Styling', 'description': 'Professional haircut and styling for all hair types. Includes wash and blow dry.', 'price': 500, 'duration_minutes': 45, 'location': 'Chembur', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Facial', 'description': 'Cleansing facial with massage and mask. Suitable for all skin types.', 'price': 800, 'duration_minutes': 60, 'location': 'Chembur', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Bridal Makeup', 'description': 'Full bridal makeup with trial session. Includes contouring and long-lasting finish.', 'price': 5000, 'duration_minutes': 120, 'location': 'Bandra', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Manicure', 'description': 'Nail shaping, cuticle care and polish. Gel polish available.', 'price': 300, 'duration_minutes': 30, 'location': 'Andheri West', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Pedicure', 'description': 'Foot soak, scrub and nail care. Relaxing foot massage included.', 'price': 400, 'duration_minutes': 45, 'location': 'Andheri West', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Hair Colour', 'description': 'Full hair colour or highlights. Premium colour brands used.', 'price': 1500, 'duration_minutes': 90, 'location': 'Bandra', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Threading', 'description': 'Eyebrow and upper lip threading. Quick and precise.', 'price': 150, 'duration_minutes': 20, 'location': 'Chembur', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Waxing (Full Arms)', 'description': 'Full arms waxing with natural wax. Smooth and long-lasting.', 'price': 350, 'duration_minutes': 30, 'location': 'Santacruz', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Waxing (Full Legs)', 'description': 'Full legs waxing with natural wax. Includes after-care lotion.', 'price': 600, 'duration_minutes': 45, 'location': 'Santacruz', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Party Makeup', 'description': 'Glamorous party makeup with false lashes. Photo-ready finish.', 'price': 1200, 'duration_minutes': 75, 'location': 'Juhu', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Hair Spa', 'description': 'Deep conditioning hair spa with steam. Restores shine and strength.', 'price': 900, 'duration_minutes': 60, 'location': 'Powai', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Cleanup', 'description': 'Basic face cleanup: cleansing, scrubbing and mask. Good for regular upkeep.', 'price': 600, 'duration_minutes': 45, 'location': 'Chembur', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Bleach', 'description': 'Face bleach for even skin tone. Gentle formula for sensitive skin.', 'price': 500, 'duration_minutes': 40, 'location': 'Malad', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Nail Art', 'description': 'Creative nail art and designs. Gel or regular polish.', 'price': 450, 'duration_minutes': 45, 'location': 'Bandra', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Keratin Treatment', 'description': 'Smoothing keratin treatment for frizz-free, silky hair.', 'price': 3500, 'duration_minutes': 150, 'location': 'Bandra', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Mehendi (Hands)', 'description': 'Traditional mehendi design for hands. Wedding and party designs.', 'price': 800, 'duration_minutes': 90, 'location': 'Juhu', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Body Massage', 'description': 'Relaxing full-body massage with aromatic oils. 60 minutes.', 'price': 1500, 'duration_minutes': 60, 'location': 'Powai', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Head Massage', 'description': 'Stress-relief head and shoulder massage. Improves blood circulation.', 'price': 400, 'duration_minutes': 30, 'location': 'Santacruz', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'D Tan', 'description': 'De-tan treatment for face and body. Removes sun damage and tan.', 'price': 1100, 'duration_minutes': 60, 'location': 'Malad', 'image_url': SERVICE_IMAGE_URL},
        {'name': 'Ladies Haircut', 'description': 'Precision ladies haircut with styling. Includes wash and blow dry.', 'price': 600, 'duration_minutes': 50, 'location': 'Andheri West', 'image_url': SERVICE_IMAGE_URL},
    ]
    for s in services_data:
        obj, created = Service.objects.get_or_create(name=s['name'], defaults=s)
        if not created:
            updated = False
            if getattr(obj, 'location', None) != s.get('location'):
                obj.location = s.get('location', '')
                updated = True
            if getattr(obj, 'image_url', None) != s.get('image_url'):
                obj.image_url = s.get('image_url', '')
                updated = True
            if updated:
                obj.save()
        print(f"  Service: {obj.name} ({obj.location or '—'}) - {'created' if created else 'exists'}")

    # Staff – 12 members with specializations
    staff_data = [
        {'name': 'Priya Sharma', 'specialization': 'Hair & Makeup'},
        {'name': 'Anita Desai', 'specialization': 'Skincare & Facials'},
        {'name': 'Meera Patel', 'specialization': 'Bridal & Party Makeup'},
        {'name': 'Sneha Reddy', 'specialization': 'Nail Art & Manicure'},
        {'name': 'Kavita Nair', 'specialization': 'Hair Colour & Styling'},
        {'name': 'Ritu Verma', 'specialization': 'Threading & Waxing'},
        {'name': 'Divya Iyer', 'specialization': 'Facials & Cleanup'},
        {'name': 'Pooja Singh', 'specialization': 'Bridal Makeup & Mehendi'},
        {'name': 'Neha Kapoor', 'specialization': 'Hair Spa & Treatments'},
        {'name': 'Shweta Joshi', 'specialization': 'Body & Head Massage'},
        {'name': 'Anjali Menon', 'specialization': 'Skin Treatments & D Tan'},
        {'name': 'Neha Gupta', 'specialization': 'General Beauty & Grooming'},
    ]
    for s in staff_data:
        obj, created = Staff.objects.get_or_create(name=s['name'], defaults=s)
        print(f"  Staff: {obj.name} - {'created' if created else 'exists'}")

    print("\nDone. You can now test booking, search and payment.")


if __name__ == '__main__':
    run()
