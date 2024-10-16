# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def punto_to_position(puntos):
    max_puntos = 500
    return (puntos / max_puntos) * 100
