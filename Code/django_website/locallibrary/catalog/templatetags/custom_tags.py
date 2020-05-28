# from django import template
#
# register = template.Library()
# # https://www.codementor.io/@hiteshgarg14/creating-custom-template-tags-in-django-application-58wvmqm5f
# from ..models import YourModel
#
#
# @register.simple_tag(name="my_tag")
# def any_function():
#     return YourModel.objects.count()
#
# @register.inclusion_tag('path_to_your_html_file.html')
# def any_function():
#   variable = YourModel.objects.order_by('-publish')[:5]
#   return {'variable': variable}