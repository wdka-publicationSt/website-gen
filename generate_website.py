#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument("-c", "--content", default="", help="html content injected to the template")
p.add_argument("-t", "--title", default="", help="page title")

args = p.parse_args()
title  = (args.title).decode('utf8') # deals with unicode
content = (args.content).decode('utf8') # deals with unicode

tmpl=Template('''
<!DOCTYPE HTML>
<html>
  <head>    
    <title>{{ title }}</title>    
  </head>

  <body>
    {{ body }}
  </body>
</html>

''')
# from jinja2 import FileSystemLoader
# from jinja2.environment import Environment
# env = Environment()
# env.loader = FileSystemLoader('.')
# tmpl = env.get_template('template_base.html')

rendered = tmpl.render(title=args.title, body=args.content)
print rendered # not rendering the vars


# pages = ('template.html', 'page.html')
# templates = dict((name, open(name, 'rb').read()) for name in pages)
# env.loader = DictLoader(templates)

# template = Template( '{% extends "template_base.html" %}
# {% block title %}title{% endblock %}
# {% block body %}content{% endblock %}
# print "Python content:", content
# {% endblock %}')
