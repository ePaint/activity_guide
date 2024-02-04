from django.template.defaultfilters import register

@register.filter(name='add_class')
def add_class(field, css):
    '''Returns the given key from a dictionary.'''
    return field.as_widget(attrs={"class": f'form-control {css}'})