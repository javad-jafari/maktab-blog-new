from django import template

register = template.Library()

@register.filter(name='convertor')
def convertor(value): 
    ''' convert En digit to Fa digit '''
    numbers={
        '0':'۰',
        '1':'۱',
        '2':'۲',
        '3':'۳',
        '4':'۴',
        '5':'۵',
        '6':'۶',
        '7':'۷',
        '8':'۸',
        '9':'۹'
    }

    for E,P in numbers.items():
        value = value.replace(E,P)
    
    return value