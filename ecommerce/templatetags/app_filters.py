from django import template

register = template.Library()


def times(n):
    return range(n)


register.filter('range', times)



# Custom template tags and filters