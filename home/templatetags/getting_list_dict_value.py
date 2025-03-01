from django.template.defaulttags import register

@register.filter(name='getting_list_dict_value')
def getting_list_dict_value(h, key):
    for i in h:
        if str(key) in i:
            return i[str(key)]
    return None
