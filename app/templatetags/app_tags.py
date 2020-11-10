from django import template

register = template.Library()


@register.filter(name='get_status')
def get_status(value):
    statuses = {
        "W":"در انتظار پاسخ",
        "A":"قبول",
        "R":"رد",
        "F":"مناسب برای آینده"
    }
    return statuses[value]
