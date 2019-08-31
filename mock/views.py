import random, re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from .models import Cookie, Method, Mock, Parameter, ParameterValue, Request, RequestHeader, ResponseHeader, Status, \
    UserPermission
from .forms import MockForm


class MockCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'mock_form.html'

    def get(self, request):
        users = User.objects.all().exclude(username=request.user.username)
        context = {
            'form': MockForm(),
            'tags': ResponseHeader.STANDARD_HEADER_TAGS,
            'placeholders': ResponseHeader.STANDARD_HEADER_PLACEHOLDERS,
            'descriptions': ResponseHeader.STANDARD_HEADER_DESCRIPTIONS,
            'users': users,
        }
        return render(request, 'mock_form.html', context=context)

    def post(self, request):
        form = MockForm(request.POST)
        if form.is_valid():
            mock = form.save(commit=False)
            mock.user = self.request.user
            mock.save()
            tag_list = request.POST.getlist('tag')
            value_list = request.POST.getlist('value')
            standard_headers_list = request.POST.getlist('standard_value')
            for index in range(len(tag_list)):
                header = ResponseHeader()
                header.mock = mock
                header.tag = tag_list[index]
                header.value = value_list[index]
                header.save()
            for index in range(len(standard_headers_list)):
                if standard_headers_list[index] is not '':
                    header = ResponseHeader()
                    header.mock = mock
                    header.tag = ResponseHeader.STANDARD_HEADER_TAGS[index]
                    header.value = standard_headers_list[index]
                    header.is_standard = True
                    header.save()
            permission = UserPermission(mock=mock, user=request.user)
            permission.save()
            user_list = request.POST.getlist('user_permissions')
            for username in user_list:
                user = get_object_or_404(User, username=username)
                permission = UserPermission(mock=mock, user=user)
                permission.save()
            return HttpResponseRedirect(mock.get_absolute_url())


class MockListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'mock_list.html'

    def get(self, request):
        mocks = Mock.objects.filter(userpermission__user__username=request.user.username).order_by('create_date')

        context = {
            'mocks': mocks,
        }

        return render(request, 'mock_list.html', context=context)


def replace_templates(request, string, seq):
    string = string.replace('<% seq %>', str(seq))
    string = string.replace('<% rand %>', str(random.randint(0, 100)))

    reg = re.compile('<% (.*?) %>')
    match_list = reg.findall(string)
    for match in match_list:
        try:
            string = string.replace('<% ' + match + ' %>', request.headers[match])
        except KeyError:
            string = string.replace('<% ' + match + ' %>', 'undefined')
    return string


class MockView(View):

    def common(self, request, mock_path):
        mock = get_object_or_404(Mock, mock_path=mock_path, is_active=True)
        custom_headers = ResponseHeader.objects.filter(mock=mock, is_standard=False)
        standard_headers = ResponseHeader.objects.filter(mock=mock, is_standard=True)

        content = replace_templates(request=request, string=mock.response_body, seq=mock.call_no)
        response = HttpResponse(content=content, status=mock.status.status_code)
        for header in custom_headers:
            value = replace_templates(request=request, string=header.value, seq=mock.call_no)
            response.setdefault(header.tag, value)
        for header in standard_headers:
            value = replace_templates(request=request, string=header.value, seq=mock.call_no)
            response[header.tag] = value
        mock.call_no += 1
        mock.save()

        req = Request(mock=mock,
                      method=Method.objects.get(method=request.method),
                      host=request.get_host(),
                      port=request.get_port(),
                      path=request.get_full_path(),
                      scheme=request.scheme,
                      body=request.body.decode('utf-8'),
                      req_no=mock.call_no)
        req.save()
        for key in request.headers.keys():
            header = RequestHeader(request=req, tag=key, value=request.headers.get(key))
            header.save()

        if request.method == 'GET':
            for param_tag in request.GET.keys():
                param = Parameter(request=req, tag=param_tag)
                param.save()
                for param_value in request.GET.getlist(param_tag):
                    value = ParameterValue(parameter=param, value=param_value)
                    value.save()
        elif request.method == 'POST':
            for param_tag in request.POST.keys():
                param = Parameter(request=req, tag=param_tag, is_post=True)
                param.save()
                for param_value in request.POST.getlist(param_tag):
                    value = ParameterValue(parameter=param, value=param_value)
                    value.save()
        for cookie_tag in request.COOKIES.keys():
            cookie = Cookie(request=req, tag=cookie_tag, value=request.COOKIES.get(cookie_tag))
            cookie.save()
        return response

    def get(self, request, mock_path):
        return self.common(request, mock_path)

    def post(self, request, mock_path):
        return self.common(request, mock_path)


class MockEditView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'mock_edit.html'

    def get(self, request, mock_path):
        mock = get_object_or_404(Mock, mock_path=mock_path)
        try:
            UserPermission.objects.get(mock=mock, user=request.user)
        except UserPermission.DoesNotExist:
            raise Http404
        standard_headers = ResponseHeader.objects.filter(mock=mock, is_standard=True)
        custom_headers = ResponseHeader.objects.filter(mock=mock, is_standard=False)
        users = User.objects.all().exclude(username=request.user.username)
        for user in users:
            try:
                UserPermission.objects.get(mock=mock, user=user)
                user.perm = True
            except UserPermission.DoesNotExist:
                user.perm = False
        standard_header_values = [''] * 37
        for header in standard_headers:
            standard_header_values[ResponseHeader.STANDARD_HEADER_TAGS.index(header.tag)] = header.value

        form = MockForm()
        form.fields['title'].initial = mock.title
        form.fields['status'].initial = mock.status
        form.fields['response_body'].initial = mock.response_body
        form.fields['is_active'].initial = mock.is_active

        context = {
            'form': form,
            'tags': ResponseHeader.STANDARD_HEADER_TAGS,
            'placeholders': ResponseHeader.STANDARD_HEADER_PLACEHOLDERS,
            'descriptions': ResponseHeader.STANDARD_HEADER_DESCRIPTIONS,
            'values': standard_header_values,
            'custom_headers': custom_headers,
            'users': users,
        }
        return render(request, 'mock_edit.html', context=context)

    def post(self, request, mock_path):
        mock = get_object_or_404(Mock, mock_path=mock_path)

        try:
            UserPermission.objects.get(mock=mock, user=request.user)
        except UserPermission.DoesNotExist:
            raise Http404

        mock.title = request.POST.get('title')
        mock.status = Status.objects.filter(status_code=int(request.POST.get('status')))[0]
        mock.response_body = request.POST.get('response_body')
        mock.is_active = True if request.POST.get('is_active') == 'on' else False
        mock.save()

        tag_list = request.POST.getlist('tag')
        value_list = request.POST.getlist('value')
        standard_headers_list = request.POST.getlist('standard_value')
        ResponseHeader.objects.filter(mock=mock).delete()
        for index in range(len(tag_list)):
            header = ResponseHeader()
            header.mock = mock
            header.tag = tag_list[index]
            header.value = value_list[index]
            header.save()
        for index in range(len(standard_headers_list)):
            if standard_headers_list[index] is not '':
                header = ResponseHeader()
                header.mock = mock
                header.tag = ResponseHeader.STANDARD_HEADER_TAGS[index]
                header.value = standard_headers_list[index]
                header.is_standard = True
                header.save()
        UserPermission.objects.filter(mock=mock).delete()
        permission = UserPermission(mock=mock, user=request.user)
        permission.save()
        user_list = request.POST.getlist('user_permissions')
        for username in user_list:
            user = get_object_or_404(User, username=username)
            permission = UserPermission(mock=mock, user=user)
            permission.save()

        return HttpResponseRedirect(mock.get_absolute_url())


class MockHistoryView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'mock_history.html'

    def get(self, request, mock_path):
        mock = get_object_or_404(Mock, mock_path=mock_path)
        try:
            UserPermission.objects.get(mock=mock, user=request.user)
        except UserPermission.DoesNotExist:
            raise Http404
        requests = Request.objects.filter(mock=mock).order_by('timestamp')

        context = {
            'requests': requests,
            'mock_path': mock_path,
        }

        return render(request, 'mock_history.html', context=context)


class RequestInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'req_info.html'

    def get(self, request, mock_path, req_path):
        req = get_object_or_404(Request, req_path=req_path)
        try:
            mock = get_object_or_404(Mock, mock_path=mock_path)
            UserPermission.objects.get(mock=mock, user=request.user)
        except UserPermission.DoesNotExist:
            raise Http404
        headers = RequestHeader.objects.filter(request=req)
        cookies = Cookie.objects.filter(request=req)
        get_parameters = Parameter.objects.filter(request=req, is_post=False)
        for parameter in get_parameters:
            parameter.values = ParameterValue.objects.filter(parameter=parameter)

        post_parameters = Parameter.objects.filter(request=req, is_post=True)
        for parameter in post_parameters:
            parameter.values = ParameterValue.objects.filter(parameter=parameter)

        context = {
            'req': req,
            'headers': headers,
            'cookies': cookies,
            'get_parameters': get_parameters,
            'post_parameters': post_parameters,
        }

        return render(request, 'req_info.html', context=context)
