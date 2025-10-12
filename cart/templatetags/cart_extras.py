from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply two numbers and format to 2 decimal places."""
    try:
        return f"{float(value) * float(arg):.2f}"
    except (ValueError, TypeError):
        return "0.00"
