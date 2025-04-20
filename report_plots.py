import sys
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


def load_scenario_properties(pkl_file_path):
    """
    Load the pickle file containing the scenario properties.
    """
    with open(pkl_file_path, 'rb') as f:
        scenario_props = pickle.load(f)

    print(f"Loaded scenario properties from {pkl_file_path}")
    return scenario_props


def extract_dates(scenario_props):
    """
    Calculates the dates of each time step within the output by adding
    timesteps (in decimal years) to the starting date.
    """
    timesteps = scenario_props.output.t

    if hasattr(scenario_props, 'scen_times_dates'):
        # Convert to proper datetime object if it's not already
        start_date = pd.to_datetime(scenario_props.scen_times_dates[0])

        # Calculate all dates
        dates = []
        for step in timesteps:
            days_to_add = int(step * 365.25)  # Accounting for leap years
            fractional_days = (step * 365.25) % 1
            hours_to_add = int(fractional_days * 24)
            new_date = start_date + pd.Timedelta(days=days_to_add, hours=hours_to_add)
            dates.append(new_date)

        return dates
    else:
        print("No starting date found in scenario_props.scen_times_dates")
        return None


def extract_species_data(scenario_props, prefix):
    """
    Extract data for a specific type of species from scenario properties.
    """
    # Get indices of species with the given prefix

    if prefix == 'debris':
        species_indices = [i for i, name in enumerate(scenario_props.species_names)
                          if (name.startswith('N') or name.startswith('N_') or
                                 name == 'N')]
                           #if (name.startswith('N_500'))]
    else:
        patterns = [f"{prefix}_", prefix] if prefix in ['S', 'B'] else [prefix]
        species_indices = [i for i, name in enumerate(scenario_props.species_names)
                          if any(name.startswith(pattern) for pattern in patterns)]

    # Get names of species
    species_names = [scenario_props.species_names[i] for i in species_indices]

    # Extract data for species
    n_shells = scenario_props.n_shells
    species_data = {}

    for idx, species_name in zip(species_indices, species_names):
        start_idx = idx * n_shells
        end_idx = start_idx + n_shells
        species_data[species_name] = scenario_props.output.y[start_idx:end_idx, :]

    return species_indices, species_names, species_data


def calculate_time_dependent_density(scenario_props):
    """
    Calculate atmospheric density for different altitudes and times.
    """
    # Get altitudes and timestamps
    altitudes = scenario_props.R0_km  # Shell altitudes in km
    timestamps = scenario_props.output.t

    # Initialize array to store density values
    density_values = np.zeros((len(altitudes), len(timestamps)))

    # Calculate density based on the model type
    if hasattr(scenario_props, 'density_model'):
        if scenario_props.density_model.__name__ == 'static_exp_dens_func':
            # Static exponential density model
            print("Using Static Density Model")
            for i, t in enumerate(timestamps):
                density_values[:, i] = scenario_props.density_model(t, altitudes, scenario_props.species, scenario_props)
        # JB2008 time-dependent density model case
        elif hasattr(scenario_props, 'density_data'):
            print("Using JB2008 Time-Dependent Density Model")
            try:
                for i, t in enumerate(timestamps):
                    density_values[:, i] = scenario_props.density_model(
                        t,
                        altitudes,
                        scenario_props.density_data,
                        scenario_props.date_mapping,
                        scenario_props.nearest_altitude_mapping
                    )
            except Exception as e:
                print(f"Error calculating time-dependent density: {e}")
                # Fallback to a simplified calculation
                for i, t in enumerate(timestamps):
                    density_values[:, i] = np.exp(-altitudes / 100)  # Simple exponential model
    else:
        # Fallback to a simplified calculation
        print("Falling back to simplified density calculation")
        for i, t in enumerate(timestamps):
            density_values[:, i] = np.exp(-altitudes / 100)  # Simple exponential model

    # Create meshgrid for contour plotting
    time_mesh, altitude_mesh = np.meshgrid(timestamps, altitudes)

    return time_mesh, altitude_mesh, density_values


def plot_and_return_atmospheric_density(scenario_props, timestamps, dates, output_dir):
    """
    Calculate, plot, and return atmospheric density data for reuse.
    """
    # Calculate time-dependent density
    time_mesh, altitude_mesh, density_mesh = calculate_time_dependent_density(scenario_props)

    # Create figure
    plt.figure(figsize=(14, 8))

    # Create the heatmap
    from matplotlib.colors import LogNorm
    im = plt.pcolormesh(
        timestamps,
        scenario_props.R0_km,
        density_mesh,
        cmap='Blues',
        shading='auto',
        norm=LogNorm()
    )

    # Add a colorbar and label it
    cbar = plt.colorbar(im)
    cbar.set_label('Atmospheric Density (kg/m³)')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Altitude (km)')
    plt.title('Atmospheric Density Heatmap')

    # Select tick positions for dates
    if len(timestamps) > 10:
        num_ticks = 5
        tick_indices = np.linspace(0, len(timestamps)-1, num_ticks, dtype=int)
    else:
        tick_indices = range(len(timestamps))

    # Format date strings to show only year
    date_strings = [dates[idx].strftime('%Y') for idx in tick_indices]

    # Set the tick positions and labels
    plt.xticks([timestamps[i] for i in tick_indices], date_strings, rotation=45)

    plt.tight_layout()

    # Create the figures directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'atmospheric_density_heatmap.png'), dpi=300)
    plt.close()

    # Return the data for reuse in other plots
    return time_mesh, altitude_mesh, density_mesh


def plot_species_heatmap(scenario_props, species_data, timestamps, dates, species_type, 
                         output_dir, density_data=None, num_contours=8, background_alpha=1.0):
    """
    Create a heatmap of species data with optional atmospheric density contours.
    """
    # Set colormap and label based on species type
    cmap_dict = {'S': 'Blues', 'B': 'Reds', 'debris': 'Greens'}
    label_dict = {
        'S': 'Number of Active Satellites', 
        'B': 'Number of Rocket Bodies',
        'debris': 'Number of Debris Objects'
    }
    title_dict = {
        'S': 'Active Satellite Population Heatmap',
        'B': 'Rocket Body Population Heatmap',
        'debris': 'Debris Population Heatmap'
    }
    
    cmap = cmap_dict.get(species_type, 'viridis')
    label = label_dict.get(species_type, 'Number of Objects')
    title_prefix = title_dict.get(species_type, 'Object Population Heatmap')

    # Combine all species data
    n_shells = scenario_props.n_shells
    n_times = len(timestamps)

    # Initialize an array to hold total objects per shell over time
    total_objects = np.zeros((n_shells, n_times))

    # Sum all objects of this type
    for species_data_array in species_data.values():
        total_objects += species_data_array

    """
    # Initialize an array to hold total objects per shell over time
    total_objects = np.zeros((n_shells, n_times))

    # Recursive function to process potentially nested dictionaries
    def add_array_data(data_item):
        nonlocal total_objects
        if isinstance(data_item, np.ndarray) and data_item.shape == (n_shells, n_times):
            # If it's an array with the right shape, add it to the total
            total_objects += data_item
        elif isinstance(data_item, dict):
            # If it's a dictionary, process each value recursively
            for value in data_item.values():
                add_array_data(value)

    # Start the recursive processing
    add_array_data(species_data)
    """

    # Create the heatmap
    plt.figure(figsize=(14, 8))

    # Plot with the appropriate color scheme
    im = plt.pcolormesh(
        timestamps,
        scenario_props.HMid,
        total_objects,
        cmap=cmap,
        shading='auto',
        alpha=background_alpha
    )

    # Add a colorbar
    cbar = plt.colorbar(im)
    cbar.set_label(label)

    # Add density contours if data is provided
    if density_data is not None:
        time_mesh, altitude_mesh, density_mesh = density_data

        # Convert to log scale for better visualization
        log_density = np.log10(density_mesh)

        # Plot the contour lines
        contour = plt.contour(
            time_mesh,
            altitude_mesh,
            log_density,
            levels=num_contours,
            colors='black',
            linewidths=1.5,
            alpha=1
        )

        # Add contour labels
        plt.clabel(contour, inline=True, fontsize=8, fmt='%1.1f')

    # Select tick positions for dates
    if len(timestamps) > 10:
        num_ticks = 5
        tick_indices = np.linspace(0, len(timestamps)-1, num_ticks, dtype=int)
    else:
        tick_indices = range(len(timestamps))

    # Format date strings to show only year
    date_strings = [dates[idx].strftime('%Y') for idx in tick_indices]

    # Set the tick positions and labels
    plt.xticks([timestamps[i] for i in tick_indices], date_strings, rotation=45)

    plt.xlabel('Year')
    plt.ylabel('Altitude (km)')
    title_suffix = " with Atmospheric Density Contours (log₁₀ kg/m³)" if density_data is not None else ""
    plt.title(title_prefix + title_suffix)
    plt.tight_layout()

    # Save the figure
    filename_suffix = "_with_contours" if density_data is not None else ""
    file_prefix = {
        'S': 'active_satellites',
        'B': 'rocket_body_satellites',
        'debris': 'debris'
    }.get(species_type, 'objects')
    
    plt.savefig(os.path.join(output_dir, f'{file_prefix}_heatmap{filename_suffix}.png'), dpi=300)
    plt.close()


def main():
    """
    Main function to run analysis and make plots.
    """
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python report_plots.py path_to_pickle_file [output_directory]")
        sys.exit(1)

    pkl_file_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'figures'
    
    # Load the scenario properties
    scenario_props = load_scenario_properties(pkl_file_path)
    timestamps = scenario_props.output.t
    date_array = extract_dates(scenario_props)

    # Extract satellite and debris data using the unified function
    # The function returns (indices, names, data), but we only need the data dictionaries
    _, _, active_satellite_data = extract_species_data(scenario_props, 'S')
    _, _, rocket_body_satellites = extract_species_data(scenario_props, 'B')
    _, _, debris_data = extract_species_data(scenario_props, 'debris')

    # Calculate atmospheric density once and plot the heatmap
    density_data = plot_and_return_atmospheric_density(scenario_props, timestamps, date_array, output_dir)

    # Create basic heatmaps without contours
    plot_species_heatmap(scenario_props, active_satellite_data, timestamps, date_array, 'S', output_dir)
    plot_species_heatmap(scenario_props, rocket_body_satellites, timestamps, date_array, 'B', output_dir)
    plot_species_heatmap(scenario_props, debris_data, timestamps, date_array, 'debris', output_dir)

    # Create heatmaps with contours
    plot_species_heatmap(scenario_props, active_satellite_data, timestamps, date_array, 'S', 
                        output_dir, density_data=density_data, background_alpha=0.4)
    plot_species_heatmap(scenario_props, rocket_body_satellites, timestamps, date_array, 'B',
                        output_dir, density_data=density_data, background_alpha=0.4)
    plot_species_heatmap(scenario_props, debris_data, timestamps, date_array, 'debris', 
                        output_dir, density_data=density_data, background_alpha=0.4)

    print(f"All plots have been created and saved to the '{output_dir}' directory.")


if __name__ == "__main__":
    main()
