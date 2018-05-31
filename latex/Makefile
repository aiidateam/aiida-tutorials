deps:=$(wildcard sections/*.tex)
temp_files = $(shell find . -name "*aux" -o -name "*log" -o -name "*toc" -o -name "*out")

all: $(patsubst %.tex, %.pdf, $(wildcard *.tex))

%.pdf: %.tex $(deps)
	pdflatex ${LATEX_INTERACTION_MODE} $< && pdflatex $< && pdflatex $<


.PHONY: all clean distclean 

clean:
	rm -f ${temp_files}


distclean: clean
	rm -f AiiDA_tutorial.pdf AiiDA_tutorial_online.pdf 
