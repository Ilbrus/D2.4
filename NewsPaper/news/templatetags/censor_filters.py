from django import template

register = template.Library()

black_list_word = ['шляпа', 'жопа', 'пиво']

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Не пременимо не к строке!')
    for word in black_list_word:
        value = value.replace(word[1:], '*' * (len(word)-1))
        
       # Возвращаемое функцией значение подставится в шаблон.
    return value