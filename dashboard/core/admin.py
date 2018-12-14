from django.utils.safestring import mark_safe


def thumbnail(obj):
    if not obj:
        return '-----'
    return mark_safe('<img src="'+obj.url+'" class="img-thumbnail col-md-2 p-0"></div>')
