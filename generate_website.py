#!/usr/bin/env python
import os,  shlex, subprocess
from jinja2 import Template, Environment, FileSystemLoader
from pprint import pprint
from argparse import ArgumentParser


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
            filepath =  (os.path.join(dirpath, f))#.replace( path, '.')
            if '.html' not in filepath:
                item_dir_fullpath = os.path.abspath(filepath)
                filetree[filepath] = {} # directory content
                dirpath = dirpath#.replace('./pages','.')
                print dirpath, filepath
                keys = ['file_path','title','author', 'date' ] # file info
                filetree[filepath]={}
                filetree[filepath]={ key:None for key in keys }
                filetree[filepath]['file_path'] = (filepath.replace('./pages/',''))
                filetree[filepath]['title'] = ( os.path.split(filepath)[-1]).replace('.md','')
                # TODO: get title from YALM metadata
    return filetree



def generate_menu(menu_dict): # if content or index page

    # list of dir :
    dirs_all = (list(set([ os.path.split(os.path.split(key)[0])[-1] for key in menu_dict.keys()])))
    #dirs_all.remove(path.replace('./','')) # ensure pages/ parent dir is removed
    print dirs_all
    
    for entry in  menu_dict.keys():#in dirs_all:
        print 'file:', entry
    # ask which key has the following folder
    ## what about index.html. it has no folder. Make it an exception
    
    # item_files in menu_dict.iteritems()

    # 
    # loop through dict for creating child li
       # make sure child li is inside parent dir
    
    menu=Template('''
    <ul class="menu_sections">
   {% for item_dir in dirs %} {# loop through dirs_all to create menu sections=li #}

    <li class="menu_sections">{{ item_dir|capitalize }}</li>

        <ul class="menu_items">
        {% for key, value in menu_dict.items() %}

         {% if item_dir in value.file_path  %} {# if filePth is child of item_dir #}

            <li class="menu_items">
    {# if index: path=./; if not path=../#}

    <a href="../{{value.file_path|replace('.md','.html')}}">
    {{value.title|capitalize}}  {# value.date #}
    </a></li>

         {% endif %}

      {% endfor %}
      </ul>


    {% endfor %}
    </ul>''')

    menu_rendered = menu.render(dirs=dirs_all, menu_dict=menu_dict)
    return menu_rendered

def generate_html_pages(site_dict):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template_base.html')
    
    site_menu = generate_menu(site_dict)
    print site_menu
    
    for file_path, file_metadata  in site_dict.iteritems():
        item_dir_fullpath = os.path.abspath(file_path)
        md_file = file_path
        print 'md_file', md_file
        md_title = file_metadata['title']
        html_content = pandoc2html(md_file)
        # assemble different parts to template_base.html            
        output_from_parsed_template = template.render(menu=site_menu, content=html_content, title=md_title)
        html_file=md_file.replace('.md','.html') # TODO: use a method more robust than replace
        html_file_open = open(html_file, 'w')
        html_file_open.write( (output_from_parsed_template).encode('utf-8'))
        html_file_open.close()


# Arguments        
p = ArgumentParser()
p.add_argument("--local", action='store_true', help="use local when running the script on local machine")
args = p.parse_args()

if args.local is True:
    wd = '.'
    os.chdir(wd)                
else:
    wd = '/home/andre/website-prototype' #working directiory
    os.chdir(wd)            

    
content_path = './pages'
site_dict = parse_filetree(content_path)
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

    
