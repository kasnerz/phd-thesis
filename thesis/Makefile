LATEX=lualatex
#LATEX=pdflatex

SHELL := /bin/bash

CHAPTERS := $(wildcard ch?-*.tex)
# CHAPTERS=ch01-intro.tex ch02-method.tex ch03-conclusion.tex  # complete manually

IMAGES := $(wildcard img/*.svg)
TABLES := $(wildcard tables/*.tex)
APPENDIX := $(wildcard appendix/*.tex)
AUTO_CHAPTERS := $(wildcard 0?-*.tex)
FIGURES := $(wildcard fig/*.png)
TIKZ_FIGURES := $(wildcard fig/*.tex) $(wildcard fig/*/*.tex)
#TIKZ_TEMPLATES := $(wildcard fig/templates/*.tex)

#GNUPLOT_FILES := $(wildcard plots/*.gnu)
#TIKZ_IMAGES := $(wildcard img/*.tex)

all: thesis.pdf vera # camera_abstract_en.pdf camera_abstract_cs.pdf #autoreferat/autoreferat.pdf # autoreferat is not included, but Makefile is nearly ready

.PHONY: all clean


watch: thesis.pdf
	latexmk -r latexmkrc -pdflatex="$(LATEX) %O %S" -pdf -dvi- -ps- -interaction=nonstopmode -synctex=1 -pvc thesis


# triple compilation to make all references and list of contents working
thesis.pdf: thesis.tex *.bib *.tex $(IMAGES) $(FIGURES) $(TABLES) $(TIKZ_FIGURES) $(APPENDIX) $(CHAPTERS)
	latexmk -r latexmkrc -pdflatex="$(LATEX) %O %S" -pdf -dvi- -ps- thesis
	latexmk -r latexmkrc -pdflatex="$(LATEX) %O %S" -pdf -dvi- -ps- thesis
	latexmk -r latexmkrc -pdflatex="$(LATEX) %O %S" -pdf -dvi- -ps- thesis

clean:
	rm -f {camera_abstract_*,thesis}.{aux,acn,acr,bbl,blg,alg,aux,fdb_latexmk,fls,glg,glo,gls,ist,lof,log,lot,out,pdf,toc} ch??-*.{aux,fdb_latexmk,log} camera_abstract*{aux,fdb_latexmk,log}

#clean_auto:
#	rm -f autoreferat/main.{aux,acn,acr,bbl,blg,alg,aux,fdb_latexmk,fls,glg,glo,gls,ist,log,lof,lot,out,pdf,toc} autoreferat/ch??-*.{aux,fdb_latexmk,log} autoreferat/list_of_publications.{aux,fdb_latexmk,log}


normostrany:
	echo `detex $(CHAPTERS) | wc -c` / 1800 | bc -l

#%.pdf: %.svg
#	inkscape -A $*.pdf $*.svg



# abstract needs to be included into SIS as a PDF
abs: camera_abstract_en.pdf camera_abstract_cs.pdf

camera_abstract_en.pdf: camera_abstract_en.tex abstract_en.tex
	latexmk -r latexmkrc -pdflatex="$(LATEX) %O %S" -pdf -dvi- -ps- camera_abstract_en

camera_abstract_cs.pdf: camera_abstract_cs.tex abstract_cs.tex
	latexmk -r latexmkrc -pdflatex="$(LATEX) %O %S" -pdf -dvi- -ps- camera_abstract_cs

#%autoreferat/main.pdf: autoreferat/main.tex biblio.bib autoreferat/*.tex $(IMAGES) $(FIGURES) $(TABLES) $(TIKZ_IMAGES) $(AUTO_CHAPTERS)
#	cp biblio.bib autoreferat/biblio.bib
#	cd autoreferat; latexmk -r latexmkrc -pdflatex="$(LATEX) %O %S" -pdf -dvi- -ps- main

# defense_slides/slides.pdf: defense_slides/slides.tex
# 		cd defense_slides; latexmk  -pdflatex="xelatex %O %S" -pdf -dvi- -ps- slides


# simple continuous integration: git pull & commit & push
.PHONY: ci
ci:
	# make sure git will remember my password
	# git config credential.helper store  # uncomment if you are sure you # want it
	# git pull push dance with possibly uncommited local modifications
	if git pull --no-edit; then echo No changes to hide; else git stash; git pull --no-edit; git stash apply; fi; git commit -am "make ci by $(USER)"; git push


# PDF/A compliance check
# download and unzip the tool
# https://software.verapdf.org/rel/verapdf-installer.zip 
# into vera-pdf/ dir
vera: thesis.pdf
	vera-dir/verapdf thesis.pdf --format text # PASS: good, FAIL: bad
