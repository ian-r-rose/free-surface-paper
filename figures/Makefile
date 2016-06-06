all: stability_region.pdf timestep_convergence.pdf benchmark_setup.pdf tau_sensitivity.pdf amr.pdf rayleigh_taylor.pdf rayleigh_taylor_setup.pdf

stability_region.pdf: stability_region.py
	python stability_region.py

timestep_convergence.pdf: timestep_convergence.py
	python timestep_convergence.py

benchmark_setup.pdf: benchmark_setup.py
	python benchmark_setup.py

tau_sensitivity.pdf: tau_sensitivity.py
	python tau_sensitivity.py

amr.pdf: amr.py
	python amr.py

rayleigh_taylor.pdf: rayleigh_taylor.py
	python rayleigh_taylor.py

rayleigh_taylor_setup.pdf: rayleigh_taylor_setup.py
	python rayleigh_taylor_setup.py

.PHONY: clean
clean:
	rm -f *.pdf *.png
