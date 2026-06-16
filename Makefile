.PHONY: all figures paper clean

all: figures paper

figures:
	python code/generate_figures.py

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode main.tex
	cp paper/main.pdf Synthetic_Data_Age_MMALS_STRATQ_EN.pdf

clean:
	cd paper && latexmk -C
	rm -f Synthetic_Data_Age_MMALS_STRATQ_EN.pdf
