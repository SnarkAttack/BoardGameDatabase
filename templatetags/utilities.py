from django import template

register = template.Library()

#TODO: Want this removed, pre-cacluated
@register.filter
def win_percent(plays, wins):
    if plays == 0:
        return 0
    return format((wins/plays)*100, '.2f')