from django.urls import path

from .views import MockCreateView, MockEditView, MockHistoryView, MockListView, MockView, RequestInfoView

app_name = 'mock'

urlpatterns = [
    path('new/', MockCreateView.as_view(), name='new_mock'),
    path('list/', MockListView.as_view(), name='mock_list'),
    path('edit/<mock_path>', MockEditView.as_view(), name='mock_edit'),
    path('history/<mock_path>', MockHistoryView.as_view(), name='mock_history'),
    path('history/<mock_path>/<req_path>', RequestInfoView.as_view(), name='req_info'),
    path('<mock_path>', MockView.as_view(), name='mock'),
]
