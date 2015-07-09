all: stability.pdf timestep_convergence.pdf

stability.pdf: stability_region.py
	python stability_region.py

timestep_convergence.pdf:
	python timestep_convergence.py

.PHONY: clean
clean:
	rm -f *.pdf *.png
