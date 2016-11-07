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
    for item in os.listdir(path): #os.walk(path)
        if os.path.isdir(item) and 'templates' not in item and 'git' not in item:
            item_dir = item
            item_dir_fullpath = os.path.abspath(item_dir)
            filetree[item_dir] = {} # directory content
            print 'dir >>>>>>', item_dir
            for item_file in os.listdir(item_dir):
                if '.html' not in item_file:
                    keys = ['file_path','title','author', 'date' ] # file info
                    filetree[item_dir][item_file]={ key:None for key in keys }
                    filetree[item_dir][item_file]['file_path'] = (item_dir+'/'+item_file)
                    filetree[item_dir][item_file]['title'] = (item_file.replace('.md','')) # TODO: get title from YALM metadata
                
    return filetree



def generate_menu(menu_dict):
    menu=Template('''<ul>
    {% for item_dir, item_files in menu_dict.iteritems() %}
    <li>{{ item_dir }}</li>
    <ul>
    {% for item_title in item_files %} 
       <li><a href="{{item_dir}}/{{ item_title.replace('.md','.html') }}"> {{ item_title.replace('.md','.html') }} </a></li>
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


            
path = '.'
site_dict = parse_filetree(path)
pprint(site_dict)
generate_html_pages( site_dict )


#     # key top level <li>
# # <ul><li>dir</li>
# #     <li><ul>
# #         <li>file 1</li>
# #         <li>file 2</li>
# #         </ul>
# #     </li>
# #  </ul>

    
