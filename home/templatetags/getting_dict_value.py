from django.template.defaulttags import register

@register.filter(name='getting_dict_value')
def getting_dict_value(dictionary, key):
    return dictionary[key]