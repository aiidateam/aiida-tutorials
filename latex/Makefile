deps:=$(wildcard sections/*.tex)

temp_files = $(shell find . -name "*aux" -o -name "*log" -o -name "*toc" -o -name "*out" -o -name "*-clean.tex" -o -name "*.db" -o -name "*.md")

all: $(patsubst %.tex, %.pdf, $(wildcard *.tex))

%.pdf: %.tex $(deps)
	pdflatex ${LATEX_INTERACTION_MODE} $< && pdflatex $< && pdflatex $<


.PHONY: all clean distclean 

clean:
	rm -f ${temp_files}

markdown: $(deps)
	./de-macro.py AiiDA_tutorial.tex
	pandoc -s --filter pandocfilter.py AiiDA_tutorial-clean.tex -t markdown_github-fenced_code_attributes -o AiiDA_tutorial-clean.md

rst: $(deps)
	./de-macro.py AiiDA_tutorial.tex
	pandoc -s --filter pandocfilter.py AiiDA_tutorial-clean.tex -t rst -o AiiDA_tutorial-clean.rst


distclean: clean
	rm -f AiiDA_tutorial.pdf AiiDA_tutorial_online.pdf 
