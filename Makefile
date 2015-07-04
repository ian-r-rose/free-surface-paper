free-surface-paper.pdf: free-surface-paper.tex free-surface-paper.bib
	pdflatex free-surface-paper
	bibtex free-surface-paper
	pdflatex free-surface-paper
	pdflatex free-surface-paper

.PHONY: clean
clean:
	rm -f *.spl *.bbl *.blg *.aux *.log free-surface-paper.pdf
