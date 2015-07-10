all: stability.pdf timestep_convergence.pdf timestep_convergence_qi.pdf

stability.pdf: stability_region.py
	python stability_region.py

timestep_convergence.pdf:
	python timestep_convergence.py

timestep_convergence_qi.pdf:
	python timestep_convergence_qi.py

.PHONY: clean
clean:
	rm -f *.pdf *.png
