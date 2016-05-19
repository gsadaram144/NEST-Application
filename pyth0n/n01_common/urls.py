from django.conf.urls import patterns, include, url

import os

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

import_nest_urls = __import__('%s.pyth0n.n10_nest_home' % NEST_ROOT_DIR, globals(), locals(), ['nest_urls'], 0).nest_urls

urlpatterns = patterns('',
    url(r'^' , include(import_nest_urls)),
)
