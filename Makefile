free-surface-paper.pdf: free-surface-paper.tex free-surface-paper.bib figures
	pdflatex free-surface-paper
	bibtex free-surface-paper
	pdflatex free-surface-paper
	pdflatex free-surface-paper

.PHONY: figures
figures:
	make -C figures

.PHONY: clean
clean:
	make clean -C figures; \
	rm -f *.spl *.bbl *.blg *.aux *.log free-surface-paper.pdf
