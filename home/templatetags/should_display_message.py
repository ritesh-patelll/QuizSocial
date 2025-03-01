from django.template.defaulttags import register

@register.filter(name='should_display_message')
def should_display_message(user, message):
    if message.message.startswith("Successfully signed in as"):
        return False
    return True