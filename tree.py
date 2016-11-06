#!/usr/bin/env python
import os
from jinja2 import Template

def filetree2dict(path):
    # returns the publishable part of the filetree
    # as dictionary { dir: [child files] }
    filetree = {}
    for item in os.listdir(path): #os.walk(path)
        if os.path.isdir(item) and 'git' not in item:
            item_dir = item
            filetree[item_dir] = [] 
            print 'dir >>>>>>', item_dir
            for item_file in os.listdir(item_dir):
                filetree[item_dir].append(item_file)
                print 'file >>', item_file
    return filetree

path = '.'
menu_dict = filetree2dict(path)
print menu_dict


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
print menu_rendered
    # key top level <li>
# <ul><li>dir</li>
#     <li><ul>
#         <li>file 1</li>
#         <li>file 2</li>
#         </ul>
#     </li>
#  </ul>

    
