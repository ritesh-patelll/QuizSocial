from django.template.defaulttags import register

@register.filter(name='getting_value_in_list_dict')
def getting_value_in_list_dict(h, key):
    for i in h:
        if str(key) in i:
            return True
    return None
