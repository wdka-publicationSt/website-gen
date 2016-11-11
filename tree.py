#!/usr/bin/env python
import os,  shlex, subprocess
from jinja2 import Template, Environment, FileSystemLoader
from pprint import pprint


def pandoc2html(md_file):
    # convert md files to html
    args_pandoc = shlex.split( 'pandoc -f markdown -t html5 {infile}'.format(infile=md_file) )
    pandoc = subprocess.Popen(args_pandoc, stdout=subprocess.PIPE)
    html = pandoc.communicate()[0]
    html = html.decode("utf-8")
    return html


def parse_filetree(path):
    # returns as dictionary that holds all info needed to make site:
    # 
    # 'dir_name': {'file_name.md':  {'author': None,
    #                                 'content': None,
    #                                 'date': None,
    #                                 'file_path': 'publications/baaaaar.md',
    #                                 'title': None}    
    filetree = {}
    for (dirpath, dirs, files) in os.walk(path):
        for f in files:
            filepath =  (os.path.join(dirpath, f)).replace( path, '.')
            item_dir_fullpath = os.path.abspath(filepath)
            filetree[filepath] = {} # directory content
            if '.html' not in filepath:
                dirpath = dirpath.replace('./pages','.')
                print dirpath, filepath
                keys = ['file_path','title','author', 'date' ] # file info
                filetree[filepath]={}
                filetree[filepath]={ key:None for key in keys }
                filetree[filepath]['file_path'] = (filepath)
                filetree[filepath]['title'] = ( os.path.split(filepath)[-1]).replace('.md','')
                # TODO: get title from YALM metadata
    pprint(filetree)
    return filetree



def generate_menu(menu_dict): # if content or index page

    
    menu=Template('''
    <ul>
    {% for item_dir, item_files in menu_dict.iteritems() %}
    <li>{{ item_dir }}</li>
    <ul>

    {% for item_title in item_files %} 

    {% if  item_dir  %}
       {% set path='..' %}
        >>>>> {{ item_dir  }}
    {% else %}
       {% set path='.' %}
       >> {{item_dir}}
    {% endif %}

    <li><a href="{{ path }}/{{item_dir}}/{{ item_title|replace('.md','.html') }}"> {{ item_title|replace('.md','') }} </a></li>  {# ../ for content pages ./ for index #}
    {% endfor %}

    </ul>
    {% endfor %}
    </ul>''')

    menu_rendered = menu.render(menu_dict=menu_dict)
    return menu_rendered

def generate_html_pages(site_dict):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template_base.html')
    
    site_menu = generate_menu(site_dict)
    print site_menu
    
    for item_dir, item_files in site_dict.iteritems():
        item_dir_fullpath = os.path.abspath(item_dir)
        for item_file in item_files:

            # content conversion: md -> html
            md_file = site_dict[item_dir][item_file]['file_path']

            md_title = site_dict[item_dir][item_file]['title']

            html_content = pandoc2html(md_file)
            
            # assemble different parts to template_base.html            
            output_from_parsed_template = template.render(menu=site_menu, content=html_content, title=md_title)
            html_file=md_file.replace('.md','.html') # TODO: use a method more robust than replace
            html_file_open = open(html_file, 'w')
            html_file_open.write(output_from_parsed_template)
            html_file_open.close()


            
path = './pages'
site_dict = parse_filetree(path)
#pprint(site_dict)
#generate_html_pages( site_dict )


#     # key top level <li>
# # <ul><li>dir</li>
# #     <li><ul>
# #         <li>file 1</li>
# #         <li>file 2</li>
# #         </ul>
# #     </li>
# #  </ul>

    
