from pyssem.pyssem import Model
from pyssem.pyssem.utils.plotting.plotting import Plots
import json
import numpy
import pickle
import os

# Load simulation configuration
with open('simple_sim.json') as f:
    simulation_data = json.load(f)

scenario_props = simulation_data['scenario_properties']

# Create an instance of the Model with the simulation parameters
model = Model(
    start_date=scenario_props["start_date"].split("T")[0],
    simulation_duration=scenario_props["simulation_duration"],
    steps=scenario_props["steps"],
    min_altitude=scenario_props["min_altitude"],
    max_altitude=scenario_props["max_altitude"],
    n_shells=scenario_props["n_shells"],
    launch_function=scenario_props["launch_function"],
    integrator=scenario_props["integrator"],
    density_model=scenario_props["density_model"],
    LC=scenario_props["LC"],
    v_imp=scenario_props["v_imp"],
    fragment_spreading=scenario_props["fragment_spreading"],
    baseline=scenario_props["baseline"],
    launch_scenario=scenario_props["launch_scenario"],
    indicator_variables=scenario_props["indicator_variables"],
    SEP_mapping=simulation_data["SEP_mapping"]
)



# Run the model
species = simulation_data["species"]
species_list = model.configure_species(species)
model.run_model()

# Load previous runs
# with open('out/example_sim/scenario-properties-baseline.pkl', 'rb') as file:
#     model.scenario_properties = pickle.load(file)

# Create the plots - will create a new figures folder in working directory
try:
    plot_names = simulation_data["plots"]
    Plots(model.scenario_properties, plot_names)
except Exception as e:
    print(e)
    print("No plots specified in the simulation configuration file.")
