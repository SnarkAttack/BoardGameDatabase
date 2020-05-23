from django import template

register = template.Library()

@register.filter
def get_play_count(value):
    return len(value.all())

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def game_win_percent(plays, wins):
    return format((wins/plays)*100, '.2f')