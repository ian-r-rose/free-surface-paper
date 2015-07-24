all: stability.pdf timestep_convergence.pdf timestep_convergence_qi.pdf benchmark_setup.pdf

stability.pdf: stability_region.py
	python stability_region.py

timestep_convergence.pdf: timestep_convergence.py
	python timestep_convergence.py

timestep_convergence_qi.pdf: timestep_convergence_qi.py
	python timestep_convergence_qi.py

benchmark_setup.pdf: benchmark_setup.py
	python benchmark_setup.py

.PHONY: clean
clean:
	rm -f *.pdf *.png
