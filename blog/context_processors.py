def site_settings(request):
    return {
        'site_name': 'My Blog',  # Now {{ site_name }} works in ALL templates
        'current_year': 2025,
    }