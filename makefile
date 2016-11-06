# find all .md files in the directory
mdsrc=$(shell find . -type f -name "*.md" )


html: $(mdsrc) 
	for file_md in $(mdsrc); do \
	filename=`basename $$file_md .md`; \
	file_html=$$filename.html ; \
	src_html=`pandoc -f markdown -t html $$file_md` ; \
	echo "\033[0;34m     $$file_html \033[00m"; \
	./generate_website.py --content "$$src_html" --title $$file_html  ; \
	done	

test:
	foo=`ls .`; \
	echo $$foo AAA ;

#htmlfile=`basename $$file .md`; \ 


# html_file = foo #$(basename $$file .md)#.html
# echo $html_file 
# done
