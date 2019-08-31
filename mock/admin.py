from django.contrib import admin

from .models import Cookie, Method, Mock, Parameter, ParameterValue, Request, RequestHeader, ResponseHeader, Status, \
    UserPermission

admin.site.register(Cookie)
admin.site.register(Method)
admin.site.register(Mock)
admin.site.register(Parameter)
admin.site.register(ParameterValue)
admin.site.register(Request)
admin.site.register(RequestHeader)
admin.site.register(ResponseHeader)
admin.site.register(Status)
admin.site.register(UserPermission)
