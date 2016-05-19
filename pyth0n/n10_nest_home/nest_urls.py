from django.conf.urls import patterns, url

import os

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

import_nest_home = __import__('%s.pyth0n.n10_nest_home' % NEST_ROOT_DIR, globals(), locals(), ['nest_home'], 0).nest_home
import_project_tracker_main = __import__('%s.pyth0n.project_tracker' % NEST_ROOT_DIR, globals(), locals(), ['main'], 0).main

urlpatterns = patterns('',
    url(r'^$', import_nest_home.home_page_view, name="nest_home"),
    url(r'^loss_triangle/$', import_nest_home.loss_triangle_report_view, name="loss_triangle"),
    url(r'^loss_triangle/glossary/$', import_nest_home.loss_triangle_glossary_view, name="loss_triangle_glossary"),
    url(r'^loss_triangle/alternate_view/$', import_nest_home.loss_triangle_alternate_view_view, name="loss_triangle_alternate_view"),
#   url(r'^loss_triangle/(?P<filters>.*)$', import_nest_home.loss_triangle_report_view,name='shared_url'),
    url(r'update_loss_triangle_report_ajax/$',import_nest_home.update_loss_triangle_report_ajax,name='update_charts_filters'),
    url(r'update_loss_triangle_report_alternate_view_ajax/$',import_nest_home.update_loss_triangle_report_alternate_view_ajax,name='update_alternate_charts_filters'),
    url(r'^daily_snapshot/$', import_nest_home.daily_snapshot_view, name="daily_snapshot"),
    url(r'^pos_dashboard/$', import_nest_home.pos_dashboard_view, name="pos_dashboard"),
    url(r'useful_link/(?P<link>[\w\s]*)$', import_nest_home.useful_link_view,name='useful_link'),
    url(r'nest_survey/$', import_nest_home.nest_survey_view,name='nest_survey'),
    url(r'nest_survey_submitted/$', import_nest_home.nest_survey_submitted_view,name='nest_survey_submitted'),
	url(r'^project_tracker/tickets/$', import_nest_home.project_tracker_view, name="project_tracker"),
	url(r'^project_tracker/initiatives/$', import_nest_home.project_tracker_initiatives_view, name="project_tracker_initiatives"),
	url(r'^tickets/', import_project_tracker_main.TicketList.as_view()),
	url(r'^initiatives/', import_project_tracker_main.InitiativeList.as_view()),
	url(r'^milestones/', import_project_tracker_main.MilestoneList.as_view()),
#	url(r'^initiatives/', import_project_tracker_main.MilestoneList.as_view()),
    url(r'(?P<trashyurl>.*)$', import_nest_home.page_not_found_view,name='pnf404'),
)
