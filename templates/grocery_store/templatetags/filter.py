from django import template
register = template.Library()
 
@register.simple_tag
def mul(value,args):
    return (value * args)
