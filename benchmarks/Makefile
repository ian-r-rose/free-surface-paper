all: perturb_spectrum tau_sensitivity timestep_convergence timestep_convergence_qi amr

.PHONY: perturb_spectrum tau_sensitivity timestep_convergence timestep_convergence_qi amr

plugin/libplugins.so: plugin/plugins.cc
	./build_plugin.sh

perturb_spectrum: plugin/libplugins.so
	make -C perturb_spectrum

tau_sensitivity: plugin/libplugins.so
	make -C tau_sensitivity

timestep_convergence: plugin/libplugins.so
	make -C timestep_convergence

timestep_convergence_qi: plugin/libplugins.so
	make -C timestep_convergence_qi

amr:
	make -C amr
