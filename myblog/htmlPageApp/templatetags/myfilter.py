# coding=utf-8
from django import template
register = template.Library()

@register.filter
def str_cut(str):
        return str[0:50]