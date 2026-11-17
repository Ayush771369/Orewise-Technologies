"""Simplified terminal settling model for an isolated spherical particle."""

def terminal_velocity_sphere(diameter_m, particle_density, fluid_density=1000.0,
                             viscosity=0.001, gravity=9.81):
    if diameter_m <= 0 or viscosity <= 0 or particle_density <= fluid_density:
        raise ValueError("Diameter and viscosity must be positive; particle density must exceed fluid density.")

    # Iteratively solve: net particle weight = drag force.
    # Sphere volume V = pi*d^3/6; projected area A = pi*d^2/4.
    import math
    volume = math.pi * diameter_m**3 / 6.0
    area = math.pi * diameter_m**2 / 4.0
    net_weight = (particle_density - fluid_density) * volume * gravity

    velocity = max(1e-9, (net_weight / (0.5 * 0.44 * fluid_density * area)) ** 0.5)
    for _ in range(500):
        reynolds = fluid_density * velocity * diameter_m / viscosity
        if reynolds < 1000:
            cd = (24.0 / reynolds) * (1.0 + 0.15 * reynolds**0.687) if reynolds > 0 else 1e12
        else:
            cd = 0.44
        new_velocity = (2.0 * net_weight / (cd * fluid_density * area)) ** 0.5
        if abs(new_velocity - velocity) <= max(1e-12, velocity * 1e-8):
            velocity = new_velocity
            break
        velocity = new_velocity

    reynolds = fluid_density * velocity * diameter_m / viscosity
    if reynolds < 0.2:
        regime = "Stokes / creeping-flow range"
    elif reynolds < 1000:
        regime = "Intermediate (Schiller–Naumann correlation)"
    else:
        regime = "Higher Reynolds number (constant-drag approximation)"
    return {"velocity_m_s": velocity, "reynolds_number": reynolds, "regime": regime}
