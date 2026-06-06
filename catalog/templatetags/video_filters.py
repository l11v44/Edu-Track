from django import template
import re
from urllib.parse import urlparse, parse_qs

register = template.Library()


@register.filter(name='get_youtube_id')
def get_youtube_id(url):
    if not url:
        return ""
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]

    return url