from django import template
from embed_video.backends import YoutubeBackend

register = template.Library()

@register.simple_tag
def video_thumbnail_url(video_url):
    backend = YoutubeBackend(video_url)
    return backend.get_thumbnail_url()