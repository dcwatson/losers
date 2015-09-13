# Copyright (c) 2001-2009 Information Management Services, Inc. All Rights Reserved.

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import hashlib

register = template.Library()

@register.filter
def gravatar(email):
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()
    return '//www.gravatar.com/avatar/%s?s=%s&default=mm' % (email_hash, 20)
