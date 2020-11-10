from . import views

from django.conf.urls import url

urlpatterns = [
    url('^$',views.index),
    url('employee/?$', views.employee_login),
    url('employee/panel?$', views.employee_panel),
    url('employee/panel/resume?$', views.employee_panel_resume),
    url('company/?$', views.company_login),
    url('company/panel?$', views.company_panel),
    url('company/panel/resume?$', views.company_panel_resume),
    url('company/panel/job?$', views.company_panel_job),
    url('company/(?P<company_id>[0-9]+)?$', views.index),
    url('opportunity/(?P<opportunity_id>[1-9]+)?$', views.info),
    url('opportunity/(?P<opportunity_id>[1-9]+)/comment?$', views.info_comment),
    url('search?$', views.search),
    url('logout$', views.logout_view),
]