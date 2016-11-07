#!/usr/bin/env python
import os,  shlex, subprocess
from jinja2 import Template
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
        if os.path.isdir(item) and 'git' not in item:
            item_dir = item
            item_dir_fullpath = os.path.abspath(item_dir)
            filetree[item_dir] = {} # directory content
            print 'dir >>>>>>', item_dir
            for item_file in os.listdir(item_dir):
                keys = ['file_path','title','author', 'date', 'content' ] # file info
                filetree[item_dir][item_file]={ key:None for key in keys }
                filetree[item_dir][item_file]['file_path'] = (item_dir+'/'+item_file).replace('.md','.html')

                # content conversion: md -> html
                md_file = item_dir_fullpath+'/'+item_file
                print 'md file >>', md_file
                html_content = pandoc2html(md_file)
                filetree[item_dir][item_file]['content'] = html_content
                
    return filetree



def generate_menu(menu_dict):
    menu=Template('''<ul>
    {% for item_dir, item_files in menu_dict.iteritems() %}
    <li>{{ item_dir }}</li>
    <ul>

    {% for item_title in item_files %} 
       <li><a href="{{item_dir}}/{{ item_title }}"> {{ item_title }} </a></li>
    {% endfor %}

    </ul>
    {% endfor %}
    </ul>''')
    menu_rendered = menu.render(menu_dict=menu_dict)
    return menu_rendered

path = '.'
site_dict = parse_filetree(path)
pprint(site_dict)
menu = generate_menu(site_dict)
print
print menu

#     # key top level <li>
# # <ul><li>dir</li>
# #     <li><ul>
# #         <li>file 1</li>
# #         <li>file 2</li>
# #         </ul>
# #     </li>
# #  </ul>

    
