from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from blog.models import Post
import logging

user_model = get_user_model()

logger = logging.getLogger(__name__)

from django import template

register = template.Library()

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": posts}


@register.simple_tag(takes_context=True)
def author_details_tag(context):
    request = context["request"]
    current_user = request.user
    post = context["post"]
    author = post.author

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html("{}{}{}", prefix, name, suffix)


@register.filter
def author_details(user, current_user=None):
  if not isinstance(user, user_model):
    return ''
  
  if user == current_user:
    return format_html('<strong>Me</strong>')
  
  if user.first_name and user.last_name:
    name =  escape(f'{user.first_name} {user.last_name}')
  else:
    name =  escape(f'{user.username}')
  
  if user.email:
    email = escape(user.email)
#     prefix = f'<a href="mailto:{email}">'
    prefix = format_html('<a href="mailto:{}">', user.email)
    suffix = '</a>'
  else:
    prefix, suffix = '', ''
    
  return mark_safe(f'{prefix}{name}{suffix}')


@register.simple_tag
def row(extra_classes=""):
  return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
  return format_html('</div>')


@register.simple_tag
def col(extra_classes=""):
  return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
  return format_html('</div>')