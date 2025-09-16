"""
SEP 5 - Commercial-driven Development Scenario Species Definitions for PYSSEM
Based on: "Methods for Generating Publicly Releasable Modelling Inputs to Support Development of Reference Space Environment Scenarios"

This file defines species for the SEP 5 scenario (Commercial-driven Development):
- Low non-market demand for space services
- High market demand for space services
- Medium level of sustainability effort (primary scenario)
- High level of sustainability effort (secondary scenario)
"""

import numpy as np
from pyssem.environment.species import Species
from pyssem.environment.interactions import Interaction

# Define altitude bins (km)
altitude_bins = np.arange(200, 2000, 50)

# ==========================================
# DEFINING SPECIES FOR SEP 5 - COMMERCIAL-DRIVEN DEVELOPMENT
# ==========================================

# =============================================================
# PAYLOADS - ACTIVE SATELLITES
# =============================================================

# Commercial constellation satellites - primary market driver in SEP 5
commercial_constellation = Species(
    name="commercial_constellation_sats",
    description="Commercial constellation satellites (e.g., Starlink, Kuiper)",
    is_man_made=True,
    is_active=True,
    is_trackable=True,
    can_maneuver=True,
    launch_rate_fn=lambda t: 3000 if t < 5 else 2000 if t < 10 else 1500,  # High market demand
    lifetime_fn=lambda alt: 7 if alt < 600 else 8,  # Years
    mass_fn=lambda alt: 300 if alt < 600 else 500,  # kg
    area_fn=lambda alt: 4 if alt < 600 else 6,  # m^2
    initial_number_fn=lambda alt: 6000 if 500 <= alt < 600 else 0,  # Initial Starlink-like constellation
    pmd_success_rate=0.98,  # Medium sustainability level (98%)
    pmd_time=5,  # 5-year PMD time for constellations
    collision_avoidance=True,
    post_failure_activity_time=0.5,  # Years satellite remains partially active after failure
)

# Non-constellation commercial satellites - medium/large communications, Earth observation, etc.
commercial_other = Species(
    name="commercial_other_sats",
    description="Non-constellation commercial satellites",
    is_man_made=True,
    is_active=True,
    is_trackable=True,
    can_maneuver=True,
    launch_rate_fn=lambda t: 50 if t < 5 else 70 if t < 10 else 90,  # Growing trend
    lifetime_fn=lambda alt: 8 if alt < 800 else 10 if alt < 1200 else 12,  # Years
    mass_fn=lambda alt: 1000 if alt < 800 else 2000,  # kg
    area_fn=lambda alt: 15 if alt < 800 else 25,  # m^2
    initial_number_fn=lambda alt: 50 if 600 <= alt < 800 else 30 if 800 <= alt < 1200 else 0,
    pmd_success_rate=0.95,  # Medium sustainability level (95%)
    pmd_time=5,  # 5-year PMD time following best practices
    collision_avoidance=True,
    post_failure_activity_time=1.0,  # Years satellite remains partially active after failure
)

# Government civil satellites (low non-market demand in SEP 5)
gov_civil = Species(
    name="gov_civil_sats",
    description="Government civil satellites (meteorological, Earth observation, etc.)",
    is_man_made=True,
    is_active=True,
    is_trackable=True,
    can_maneuver=True,
    launch_rate_fn=lambda t: 10,  # Low non-market demand
    lifetime_fn=lambda alt: 7 if alt < 700 else 10,  # Years
    mass_fn=lambda alt: 2000 if alt < 700 else 3500,  # kg
    area_fn=lambda alt: 25 if alt < 700 else 40,  # m^2
    initial_number_fn=lambda alt: 5 if 600 <= alt < 700 else 15 if 700 <= alt < 1000 else 0,
    pmd_success_rate=0.90,  # Medium sustainability (90% for government)
    pmd_time=5,  # 5-year PMD time
    collision_avoidance=True,
    post_failure_activity_time=1.0,  # Years satellite remains partially active after failure
)

# Military satellites (low non-market demand in SEP 5)
military = Species(
    name="military_sats",
    description="Military satellites",
    is_man_made=True,
    is_active=True,
    is_trackable=True,
    can_maneuver=True,
    launch_rate_fn=lambda t: 8,  # Low non-market demand
    lifetime_fn=lambda alt: 10 if alt < 1000 else 15,  # Years
    mass_fn=lambda alt: 2500 if alt < 1000 else 4000,  # kg
    area_fn=lambda alt: 30 if alt < 1000 else 45,  # m^2
    initial_number_fn=lambda alt: 10 if 800 <= alt < 1200 else 0,
    pmd_success_rate=0.90,  # Medium sustainability (90% for government)
    pmd_time=5,  # 5-year PMD time
    collision_avoidance=True,
    post_failure_activity_time=1.5,  # Years satellite remains partially active after failure
)

# Small satellites (CubeSats, etc.) - growing commercial and academic use
small_satellites = Species(
    name="small_sats",
    description="Small satellites (CubeSats, etc.) for commercial and academic use",
    is_man_made=True,
    is_active=True,
    is_trackable=True,
    can_maneuver=False,  # Most small sats cannot maneuver
    launch_rate_fn=lambda t: 200 if t < 5 else 150 if t < 10 else 100,  # Declining as constellations dominate
    lifetime_fn=lambda alt: 3 if alt < 500 else 5 if alt < 700 else 7,  # Years
    mass_fn=lambda alt: 10,  # kg (typical CubeSat)
    area_fn=lambda alt: 0.1,  # m^2
    initial_number_fn=lambda alt: 300 if 400 <= alt < 600 else 100 if 600 <= alt < 800 else 0,
    pmd_success_rate=0.98,  # Medium sustainability level (98%)
    pmd_time=5,  # 5-year PMD time
    collision_avoidance=False,
    post_failure_activity_time=0.1,  # Years satellite remains partially active after failure
)

# =============================================================
# ROCKET BODIES AND UPPER STAGES
# =============================================================

# Rocket bodies from commercial launches
rocket_bodies_commercial = Species(
    name="rocket_bodies_commercial",
    description="Rocket bodies and upper stages from commercial launches",
    is_man_made=True,
    is_active=False,
    is_trackable=True,
    can_maneuver=False,
    launch_rate_fn=lambda t: 80 if t < 5 else 70 if t < 10 else 60,  # Decreasing as reusability increases
    lifetime_fn=lambda alt: 2 if alt < 400 else 10 if alt < 600 else 20,  # Years
    mass_fn=lambda alt: 2000 if alt < 500 else 3000,  # kg
    area_fn=lambda alt: 30,  # m^2
    initial_number_fn=lambda alt: 30 if 200 <= alt < 300 else 20 if 300 <= alt < 500 else 10 if 500 <= alt < 700 else 0,
    pmd_success_rate=0.90,  # Medium sustainability level (90% for rocket bodies)
    pmd_time=5,  # 5-year PMD time
    collision_avoidance=False,
    explosion_probability=0.015,  # 1.5% for rocket bodies (medium sustainability)
)

# Rocket bodies from government launches
rocket_bodies_gov = Species(
    name="rocket_bodies_gov",
    description="Rocket bodies and upper stages from government launches",
    is_man_made=True,
    is_active=False,
    is_trackable=True,
    can_maneuver=False,
    launch_rate_fn=lambda t: 15,  # Low non-market demand
    lifetime_fn=lambda alt: 2 if alt < 400 else 10 if alt < 600 else 25,  # Years
    mass_fn=lambda alt: 3000,  # kg
    area_fn=lambda alt: 35,  # m^2
    initial_number_fn=lambda alt: 10 if 300 <= alt < 500 else 5 if 500 <= alt < 700 else 0,
    pmd_success_rate=0.90,  # Medium sustainability level (90% for rocket bodies)
    pmd_time=5,  # 5-year PMD time
    collision_avoidance=False,
    explosion_probability=0.015,  # 1.5% for rocket bodies (medium sustainability)
)

# =============================================================
# INACTIVE/DERELICT SATELLITES
# =============================================================

# Failed or derelict commercial satellites
inactive_commercial = Species(
    name="inactive_commercial_sats",
    description="Failed or derelict commercial satellites",
    is_man_made=True,
    is_active=False,
    is_trackable=True,
    can_maneuver=False,
    launch_rate_fn=lambda t: 0,  # Not directly launched
    lifetime_fn=lambda alt: 10 if alt < 500 else 25 if alt < 800 else 100,  # Years
    mass_fn=lambda alt: 300 if alt < 600 else 1000 if alt < 800 else 2000,  # kg
    area_fn=lambda alt: 4 if alt < 600 else 15 if alt < 800 else 25,  # m^2
    initial_number_fn=lambda alt: 100 if 500 <= alt < 800 else 50 if 800 <= alt < 1200 else 0,
    pmd_success_rate=0.0,  # Already failed satellites
    pmd_time=25,  # Natural decay
    collision_avoidance=False,
    explosion_probability=0.002,  # 0.2% (medium sustainability)
)

# Failed or derelict government satellites
inactive_government = Species(
    name="inactive_government_sats",
    description="Failed or derelict government satellites",
    is_man_made=True,
    is_active=False,
    is_trackable=True,
    can_maneuver=False,
    launch_rate_fn=lambda t: 0,  # Not directly launched
    lifetime_fn=lambda alt: 15 if alt < 700 else 30 if alt < 1000 else 100,  # Years
    mass_fn=lambda alt: 2000 if alt < 1000 else 3500,  # kg
    area_fn=lambda alt: 25 if alt < 1000 else 40,  # m^2
    initial_number_fn=lambda alt: 20 if 700 <= alt < 1000 else 10 if 1000 <= alt < 1500 else 0,
    pmd_success_rate=0.0,  # Already failed satellites
    pmd_time=25,  # Natural decay
    collision_avoidance=False,
    explosion_probability=0.002,  # 0.2% (medium sustainability)
)

# =============================================================
# DEBRIS OBJECTS
# =============================================================

# Large debris (>10 cm)
large_debris = Species(
    name="large_debris",
    description="Large debris objects (>10 cm)",
    is_man_made=True,
    is_active=False,
    is_trackable=True,
    can_maneuver=False,
    launch_rate_fn=lambda t: 0,  # Not directly launched
    lifetime_fn=lambda alt: 5 if alt < 500 else 25 if alt < 800 else 100,  # Years
    mass_fn=lambda alt: 5,  # kg
    area_fn=lambda alt: 0.1,  # m^2
    initial_number_fn=lambda alt: 3000 if 500 <= alt < 800 else 2000 if 800 <= alt < 1200 else 1000 if 1200 <= alt < 1500 else 0,
    pmd_success_rate=0.0,  # Debris doesn't perform PMD
    pmd_time=25,  # Natural decay
    collision_avoidance=False,
)

# Medium debris (1-10 cm)
medium_debris = Species(
    name="medium_debris",
    description="Medium debris objects (1-10 cm)",
    is_man_made=True,
    is_active=False,
    is_trackable=False,  # Not all trackable in this size range
    can_maneuver=False,
    launch_rate_fn=lambda t: 0,  # Not directly launched
    lifetime_fn=lambda alt: 3 if alt < 500 else 15 if alt < 800 else 50,  # Years
    mass_fn=lambda alt: 0.5,  # kg
    area_fn=lambda alt: 0.01,  # m^2
    initial_number_fn=lambda alt: 20000 if 500 <= alt < 800 else 15000 if 800 <= alt < 1200 else 5000 if 1200 <= alt < 1500 else 0,
    pmd_success_rate=0.0,  # Debris doesn't perform PMD
    pmd_time=25,  # Natural decay
    collision_avoidance=False,
)

# Small debris (1mm-1cm) - lethal non-trackable
small_debris = Species(
    name="small_debris",
    description="Small debris objects (1mm-1cm)",
    is_man_made=True,
    is_active=False,
    is_trackable=False,
    can_maneuver=False,
    launch_rate_fn=lambda t: 0,  # Not directly launched
    lifetime_fn=lambda alt: 1 if alt < 500 else 5 if alt < 800 else 25,  # Years
    mass_fn=lambda alt: 0.001,  # kg
    area_fn=lambda alt: 0.0001,  # m^2
    initial_number_fn=lambda alt: 500000 if 500 <= alt < 800 else 300000 if 800 <= alt < 1200 else 100000 if 1200 <= alt < 1500 else 0,
    pmd_success_rate=0.0,  # Debris doesn't perform PMD
    pmd_time=25,  # Natural decay
    collision_avoidance=False,
)

# =============================================================
# INTERACTIONS
# =============================================================

# Define interactions between species
interactions = [
    # Catastrophic collisions between active satellites
    Interaction(
        species_a="commercial_constellation_sats",
        species_b="commercial_constellation_sats",
        interaction_type="collision",
        # Commercial constellations have advanced collision avoidance (Pc threshold 1e-5)
        probability_fn=lambda t, alt: 1e-5 if alt > 400 else 0.0,  
        products={
            "large_debris": lambda alt: 100 if alt < 600 else 150,
            "medium_debris": lambda alt: 500 if alt < 600 else 800, 
            "small_debris": lambda alt: 10000 if alt < 600 else 15000,
        }
    ),
    
    # Collision between constellation satellites and other satellites
    Interaction(
        species_a="commercial_constellation_sats",
        species_b="commercial_other_sats",
        interaction_type="collision",
        probability_fn=lambda t, alt: 5e-5 if alt > 400 else 0.0,
        products={
            "large_debris": lambda alt: 200,
            "medium_debris": lambda alt: 1000,
            "small_debris": lambda alt: 20000,
        }
    ),
    
    # Collisions with debris (a major concern)
    Interaction(
        species_a="commercial_constellation_sats",
        species_b="large_debris",
        interaction_type="collision",
        probability_fn=lambda t, alt: 1e-4 if alt > 400 else 0.0,
        products={
            "large_debris": lambda alt: 50,
            "medium_debris": lambda alt: 300,
            "small_debris": lambda alt: 5000,
            "inactive_commercial_sats": lambda alt: 1,
        }
    ),
    
    # Rocket body explosions (medium sustainability effort - 1.5% of rocket bodies)
    Interaction(
        species_a="rocket_bodies_commercial",
        species_b=None,  # Self-interaction (explosion)
        interaction_type="explosion",
        probability_fn=lambda t, alt: 0.015 if alt > 300 else 0.0,  # 1.5% annual probability
        products={
            "large_debris": lambda alt: 50,
            "medium_debris": lambda alt: 200,
            "small_debris": lambda alt: 5000,
        }
    ),
    
    # Satellite failures (creating inactive satellites)
    Interaction(
        species_a="commercial_constellation_sats",
        species_b=None,  # Self-interaction (failure)
        interaction_type="failure",
        probability_fn=lambda t, alt: 0.02,  # 2% annual failure rate
        products={
            "inactive_commercial_sats": lambda alt: 1,
        }
    ),
    
    # Commercial satellite end-of-life (successful disposal)
    Interaction(
        species_a="commercial_constellation_sats",
        species_b=None,
        interaction_type="eol_success",
        probability_fn=lambda t, alt: 1/7 * 0.98,  # 7-year lifetime, 98% PMD success
        products={}  # Successfully disposed
    ),
    
    # Commercial satellite end-of-life (disposal failure)
    Interaction(
        species_a="commercial_constellation_sats",
        species_b=None,
        interaction_type="eol_failure",
        probability_fn=lambda t, alt: 1/7 * 0.02,  # 7-year lifetime, 2% PMD failure
        products={
            "inactive_commercial_sats": lambda alt: 1,
        }
    ),
    
    # Active debris removal (ADR) - 10 objects per year (medium sustainability)
    Interaction(
        species_a="inactive_commercial_sats",
        species_b=None,
        interaction_type="removal",
        probability_fn=lambda t, alt: 10/2000 if t >= 5 else 0,  # Start ADR after 5 years
        products={}  # Successfully removed
    ),
]

# Export the species collection and interactions for SEP 5
sep5_species = {
    "commercial_constellation_sats": commercial_constellation,
    "commercial_other_sats": commercial_other,
    "gov_civil_sats": gov_civil,
    "military_sats": military,
    "small_sats": small_satellites,
    "rocket_bodies_commercial": rocket_bodies_commercial,
    "rocket_bodies_gov": rocket_bodies_gov,
    "inactive_commercial_sats": inactive_commercial,
    "inactive_government_sats": inactive_government,
    "large_debris": large_debris,
    "medium_debris": medium_debris,
    "small_debris": small_debris,
}

# High sustainability variant (SEP 5H - secondary scenario)
# Here we could define modifications for the high sustainability version
sep5h_species = sep5_species.copy()

# Modify key parameters for high sustainability
sep5h_species["commercial_constellation_sats"].pmd_success_rate = 0.99  # 99% PMD success
sep5h_species["commercial_other_sats"].pmd_success_rate = 0.99  # 99% PMD success
sep5h_species["gov_civil_sats"].pmd_success_rate = 0.95  # 95% PMD success for government
sep5h_species["military_sats"].pmd_success_rate = 0.95  # 95% PMD success for military
sep5h_species["rocket_bodies_commercial"].explosion_probability = 0.01  # 1% explosion probability
sep5h_species["rocket_bodies_commercial"].pmd_success_rate = 0.98  # 98% for commercial rocket bodies

# High sustainability ADR - 15 objects per year
sep5h_interactions = interactions.copy()
sep5h_interactions.append(
    Interaction(
        species_a="inactive_commercial_sats",
        species_b=None,
        interaction_type="removal",
        probability_fn=lambda t, alt: 15/2000 if t >= 5 else 0,  # Start ADR after 5 years, 15 objects/year
        products={}  # Successfully removed
    )
)

# Example usage to initialize PYSSEM
"""
from pyssem.environment.simulator import Simulator

# For medium sustainability (primary scenario)
sim_medium = Simulator(
    species=sep5_species,
    interactions=interactions,
    altitude_bins=altitude_bins,
    simulation_time=50,  # Years
    time_step=0.25,  # Quarterly steps
)

# For high sustainability (secondary scenario)
sim_high = Simulator(
    species=sep5h_species,
    interactions=sep5h_interactions,
    altitude_bins=altitude_bins,
    simulation_time=50,  # Years
    time_step=0.25,  # Quarterly steps
)
"""