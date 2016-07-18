texargs = -interaction nonstopmode -halt-on-error -file-line-error

.PHONY: figures
figures:
	make -C figures

.PHONY: clean
clean:
	make clean -C figures; \
	rm -f *.spl *.bbl *.blg *.aux *.log free-surface-paper.pdf
