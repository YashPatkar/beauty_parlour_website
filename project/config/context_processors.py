"""
Template context: default image and video URLs (replacing emojis with real media).
Use these in templates via {{ default_images.hero }} etc.
"""
# Free-to-use Unsplash images (beauty/salon relevant). Replace with your own static files if needed.
DEFAULT_IMAGES = {
    'hero': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&q=80',  # salon
    'about_spa': 'https://images.unsplash.com/photo-1544161515-4ab6d6c49a2a?w=600&q=80',  # spa/relaxation
    'service_placeholder': 'https://images.unsplash.com/photo-1522338248312-35a2e9c2b0e0?w=600&q=80',  # beauty
    'gallery_hair': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&q=80',
    'gallery_makeup': 'https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=600&q=80',
    'gallery_facial': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=600&q=80',
    'gallery_nail': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=600&q=80',
    'gallery_bridal': 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=600&q=80',
    'gallery_salon': 'https://images.unsplash.com/photo-1633681926022-84c23e8cb2d6?w=600&q=80',
    'team_placeholder': 'https://images.unsplash.com/photo-1599566150813-2c8c56f5d5a5?w=400&q=80',  # person
    'why_booking': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=200&q=80',
    'why_expert': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=200&q=80',
    'why_price': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=200&q=80',
    'why_hygiene': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=200&q=80',
    'contact_cta': 'https://images.unsplash.com/photo-1423666639041-f56000c27a9a?w=400&q=80',  # contact/letter
    'about_mission': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=200&q=80',
    'about_vision': 'https://images.unsplash.com/photo-1633681926022-84c23e8cb2d6?w=200&q=80',
    'about_values': 'https://images.unsplash.com/photo-1544161515-4ab6d6c49a2a?w=200&q=80',
}

# Optional: YouTube embed ID for a short salon/beauty video. Leave empty to use sample HTML5 video instead.
SALON_VIDEO_ID = ''  # e.g. 'ABC123' for https://www.youtube.com/embed/ABC123


def default_media(request):
    return {'default_images': DEFAULT_IMAGES, 'salon_video_id': SALON_VIDEO_ID}


def user_cart_favourites(request):
    """Expose user's cart service IDs and favourite service IDs for templates (users only)."""
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {'user_cart_service_ids': set(), 'user_favourite_service_ids': set()}
    from bookings.models import Cart, UserFavourite
    cart_service_ids = set()
    try:
        cart = Cart.objects.get(user=request.user)
        cart_service_ids = set(cart.items.values_list('service_id', flat=True))
    except Cart.DoesNotExist:
        pass
    favourite_ids = set(
        UserFavourite.objects.filter(user=request.user).values_list('service_id', flat=True)
    )
    return {
        'user_cart_service_ids': cart_service_ids,
        'user_favourite_service_ids': favourite_ids,
    }
