# website generator based in markdown files
This is a simple Markdown-to-HTML website generator.

The essential idea behind it is that **no** conversations or processing takes place in the editors computer. Instead conversions take place in the git repository remote, via the Git hook post-receive-hook

Therefore there are no software dependencies for editors, except for Git.

## for editors

### How to
**Create or edit an article:**
* create/edit **only** Mardownd files (.md) inside the sub-folders from the `pages` folder.
* Use plain text editor for editing: e.g. [Sublime Text](http://sublimetext.com/), [gedit](https://wiki.gnome.org/Apps/Gedit), [Brackets](http://brackets.io/), etc. Word and Mac Text editors will add formatting information to the text, which we wont. All formatting should be done explicitly using Markdown (and/or HTML)!
* Avoid using spaces in space in file-names.

**Add images:**
* store your image in the folder `media/`
* include it in an article by using the markdown syntax for images: `![img caption](img location)`
* the image location will always begin with `media/`, follow by the image name
* i.e. `![Troll](media/troll.png)`

Lear more on Markdown syntax at <https://daringfireball.net/projects/markdown/>

**Publish**
From within this folder run `git add --all` to add all new or modified files

Create a commit `git commit --message="describing what change in this commit"`

Push commit to repository (AKA publish) `git push origin chichi` Chichi is the server that holds the website.

visit the website in <http://publicationstation.wdka.hro.nl/prototype/pages/> 

**Note: in the future this operations shall be replace by a GUI**


## For Developers

### Dependencies: 
* Python 2.7
* Python Library: [Jinja](http://jinja.pocoo.org/) templating engine
* [Pandoc](http://pandoc.org/)
* Git

### Important files and folders:
* 'lib/' contains .css, .js, fonts, files
* 'media/' contains images, videos, and audio files 
* templates/template_base.html - the base for all templates.

### Templating Engine Development 
Run locally: `python generate_website.py --local`

### Web development


### Hooks


### Code changes commits
In addition to push your commits to Chichi server `git commit chichi master` also push them to the Github repository `git commit github master` 


# TO DO
## Style
* list to collapsible menus, such as in <http://jasalguero.com/ledld/development/web/expandable-list/>

## Navigation:
* include index.html file that redirects to files chosen to be the landing page

## Programming
* revise receive hook and track it, via ln 
* clean and organize generate_website.py
