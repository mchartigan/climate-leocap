# climate-leocap
Orbital capacity assessment for LEO and VLEO with a shrinking atmosphere due to climate change.

## Getting Started
`basic_pyssem_test.py` should be a working test of one of the pySSEM examples, found in `pyssem/pyssem/simulation_configurations`. To run pySSEM properly, install all the dependencies using `pip install -r pyssem/requirements.txt` (ensuring `pip` points to the correct Python installation). Once done, the test script should run without error.

## Workspace Management
pySSEM creates a few output folders in the root directory that should be ignored during commits, so as to not pollute the repository with large files. Any outputs that seem pertinent to share, however, can be added as a subdirectory under `/out/`. There is currently one subdirectory already existing, `example_sim/`, which contains the output generated by my (Mark's) machine when running `basic_pyssem_test.py`. The main outputs are the figures, under `example_sim/figures/`, and a binary file containing the model output data -- `example_sim/scenario-properties-baseline.pkl`. There are a couple commented-out lines in `basic_pyssem_test.py` to load this data so that you're able to avoid repetitive runs of the same model configuration.
