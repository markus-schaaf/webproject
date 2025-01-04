from django import template

register = template.Library()

@register.filter
def format_minutes(value):
    try:
        hours = value // 60
        minutes = value % 60
        return f"{hours}Std. {minutes}min" if hours > 0 else f"{minutes}min"
    except (TypeError, ValueError):
        return "0min"
