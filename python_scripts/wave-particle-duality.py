import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from svgwrite import Drawing
import argparse
import os
from matplotlib.colors import Normalize

def double_slit_intensity(x, wavelength, slit_width, slit_distance, screen_distance):
    """
    Calculate the intensity pattern on the screen for a double-slit experiment.
    
    Parameters:
        x: Array of positions on the screen (meters)
        wavelength: Wavelength of light (meters)
        slit_width: Width of each slit (meters)
        slit_distance: Distance between centers of slits (meters)
        screen_distance: Distance from slits to screen (meters)
        
    Returns:
        Intensity pattern on the screen
    """
    # Wave number
    k = 2 * np.pi / wavelength
    
    # Single slit diffraction factor
    alpha = (k * slit_width * x) / (2 * screen_distance)
    # Use np.where to handle alpha=0 case
    sinc = np.where(alpha != 0, np.sin(alpha) / alpha, 1.0)
    
    # Double slit interference factor
    beta = (k * slit_distance * x) / (2 * screen_distance)
    cos_term = np.cos(beta) ** 2
    
    # Total intensity
    intensity = (sinc ** 2) * cos_term
    
    return intensity

def simulate_quantum_particles(wavelength, slit_width, slit_distance, screen_distance, 
                               num_particles=1000, screen_width=0.1):
    """
    Simulate quantum particles passing through a double slit.
    
    Parameters:
        wavelength: Wavelength of particles (meters)
        slit_width: Width of each slit (meters)
        slit_distance: Distance between slits (meters)
        screen_distance: Distance from slits to screen (meters)
        num_particles: Number of particles to simulate
        screen_width: Width of the screen (meters)
        
    Returns:
        Array of particle positions on the screen
    """
    # Create probability distribution based on the intensity pattern
    x = np.linspace(-screen_width/2, screen_width/2, 1000)
    intensity = double_slit_intensity(x, wavelength, slit_width, slit_distance, screen_distance)
    
    # Normalize to create a probability distribution
    intensity_normalized = intensity / np.sum(intensity)
    
    # Sample particle positions based on the probability distribution
    particle_indices = np.random.choice(len(x), size=num_particles, p=intensity_normalized)
    particle_positions = x[particle_indices]
    
    # Add some uncertainty to particle positions (Heisenberg uncertainty principle)
    # Momentum uncertainty is inversely proportional to slit width
    # Position uncertainty is proportional to wavelength and inversely proportional to slit width
    position_uncertainty = wavelength / (2 * slit_width)
    particle_positions += np.random.normal(0, position_uncertainty, num_particles)
    
    return particle_positions

def create_svg(intensity, particle_positions, filename, wavelength, slit_width, 
               screen_width=0.1, height=400, width=800):
    """
    Create an SVG visualization of the double-slit experiment.
    
    Parameters:
        intensity: Array of intensity values
        particle_positions: Array of particle positions on the screen
        filename: Output filename
        wavelength: Wavelength of light (meters)
        slit_width: Width of each slit (meters)
        screen_width: Width of the screen (meters)
        height: Height of the SVG in pixels
        width: Width of the SVG in pixels
    """
    dwg = Drawing(filename, size=(width, height), profile='tiny')
    
    # Background
    dwg.add(dwg.rect((0, 0), (width, height), fill='black'))
    
    # Map screen coordinates to SVG coordinates
    x_min, x_max = -screen_width/2, screen_width/2
    x_scale = width / (x_max - x_min)
    
    # Draw intensity pattern as a series of colored lines
    x_coords = np.linspace(x_min, x_max, len(intensity))
    max_intensity = np.max(intensity)
    intensity_scaled = intensity / max_intensity * (height * 0.8)
    
    # Add intensity pattern as a curve
    points = []
    for i, x in enumerate(x_coords):
        x_svg = (x - x_min) * x_scale
        y_svg = height - intensity_scaled[i] - height * 0.1
        points.append((x_svg, y_svg))
    
    # Add the intensity curve
    dwg.add(dwg.polyline(points, stroke='rgb(100,200,255)', stroke_width=2, fill='none'))
    
    # Add filled area below the curve
    filled_points = points + [(width, height), (0, height)]
    dwg.add(dwg.polygon(filled_points, fill='rgba(100,200,255,0.3)', stroke='none'))
    
    # Map particle positions to SVG and draw them
    for pos in particle_positions:
        x_svg = (pos - x_min) * x_scale
        if 0 <= x_svg <= width:  # Only draw particles that fall within the SVG width
            # Use a gradient color based on position (blue-white-red)
            position_fraction = (pos - x_min) / (x_max - x_min)
            
            # Simple blue-white-red gradient
            if position_fraction < 0.5:
                r = int(position_fraction * 2 * 255)
                g = int(position_fraction * 2 * 255)
                b = 255
            else:
                r = 255
                g = int((1 - position_fraction) * 2 * 255)
                b = int((1 - position_fraction) * 2 * 255)
            
            # Draw the particle as a small circle
            dwg.add(dwg.circle(center=(x_svg, height * 0.2), r=1.5, 
                               fill=f'rgb({r},{g},{b})', 
                               stroke='none'))
    
    # Add experiment details
    # Convert wavelength to nm for display
    wavelength_nm = wavelength * 1e9
    # Convert slit_width to micrometers for display
    slit_width_um = slit_width * 1e6
    
    dwg.add(dwg.text(f"Wavelength: {wavelength_nm:.1f} nm", 
                    insert=(20, 30), fill='white', font_size='16px'))
    dwg.add(dwg.text(f"Slit width: {slit_width_um:.1f} μm", 
                    insert=(20, 60), fill='white', font_size='16px'))
    
    # Add experiment diagram (simplified)
    # Source
    dwg.add(dwg.circle(center=(width/2, height-30), r=5, fill='yellow', stroke='none'))
    # Slits
    slit_y = height-80
    dwg.add(dwg.rect((width/2-15, slit_y-10), (30, 20), fill='gray'))
    dwg.add(dwg.rect((width/2-10, slit_y-10), (4, 20), fill='black'))
    dwg.add(dwg.rect((width/2+6, slit_y-10), (4, 20), fill='black'))
    
    # Add title
    dwg.add(dwg.text("Double-Slit Experiment: Wave-Particle Duality", 
                    insert=(width/2, 30), fill='white', font_size='20px', 
                    text_anchor='middle'))
    
    dwg.save()

def main():
    parser = argparse.ArgumentParser(description='Simulate the double-slit experiment.')
    parser.add_argument('--wavelength', type=float, default=500e-9,
                        help='Wavelength of light in meters (default: 500 nm)')
    parser.add_argument('--slit_width', type=float, default=100e-6,
                        help='Width of each slit in meters (default: 100 micrometers)')
    parser.add_argument('--slit_distance', type=float, default=500e-6,
                        help='Distance between slits in meters (default: 500 micrometers)')
    parser.add_argument('--screen_distance', type=float, default=1.0,
                        help='Distance from slits to screen in meters (default: 1 meter)')
    parser.add_argument('--num_particles', type=int, default=1000,
                        help='Number of particles to simulate (default: 1000)')
    parser.add_argument('--output', type=str, default='double_slit.svg',
                        help='Output SVG file (default: double_slit.svg)')
    
    args = parser.parse_args()
    
    # Create array of positions on the screen
    screen_width = 0.1  # 10 cm wide screen
    x = np.linspace(-screen_width/2, screen_width/2, 1000)
    
    # Calculate intensity pattern
    intensity = double_slit_intensity(x, args.wavelength, args.slit_width, 
                                     args.slit_distance, args.screen_distance)
    
    # Simulate particle positions
    particle_positions = simulate_quantum_particles(
        args.wavelength, args.slit_width, args.slit_distance, 
        args.screen_distance, args.num_particles, screen_width)
    
    # Create SVG visualization
    create_svg(intensity, particle_positions, args.output, 
              args.wavelength, args.slit_width)
    
    print(f"SVG visualization saved to {args.output}")

def create_wavelength_series(base_output_name="wavelength_series",
                           wavelengths=None,
                           slit_width=100e-6,
                           slit_distance=500e-6,
                           screen_distance=1.0,
                           num_particles=1000):
    """
    Create a series of SVG files with varying wavelengths.
    """
    if wavelengths is None:
        # Default range of visible light: 380-750 nm
        wavelengths = np.linspace(380e-9, 750e-9, 5)
    
    screen_width = 0.1  # 10 cm wide screen
    x = np.linspace(-screen_width/2, screen_width/2, 1000)
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    for i, wavelength in enumerate(wavelengths):
        # Calculate intensity pattern
        intensity = double_slit_intensity(x, wavelength, slit_width, 
                                        slit_distance, screen_distance)
        
        # Simulate particle positions
        particle_positions = simulate_quantum_particles(
            wavelength, slit_width, slit_distance, 
            screen_distance, num_particles, screen_width)
        
        # Create SVG visualization
        output_file = f"output/{base_output_name}_{i+1}.svg"
        create_svg(intensity, particle_positions, output_file, 
                  wavelength, slit_width)
        
        print(f"Created SVG for wavelength {wavelength*1e9:.1f} nm: {output_file}")

def create_slit_width_series(base_output_name="slit_width_series",
                           wavelength=500e-9,
                           slit_widths=None,
                           slit_distance=500e-6,
                           screen_distance=1.0,
                           num_particles=1000):
    """
    Create a series of SVG files with varying slit widths.
    """
    if slit_widths is None:
        # Range of slit widths from very narrow to wide relative to wavelength
        slit_widths = np.logspace(-6, -4, 5)  # 1 μm to 100 μm
    
    screen_width = 0.1  # 10 cm wide screen
    x = np.linspace(-screen_width/2, screen_width/2, 1000)
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    for i, slit_width in enumerate(slit_widths):
        # Calculate intensity pattern
        intensity = double_slit_intensity(x, wavelength, slit_width, 
                                        slit_distance, screen_distance)
        
        # Simulate particle positions
        particle_positions = simulate_quantum_particles(
            wavelength, slit_width, slit_distance, 
            screen_distance, num_particles, screen_width)
        
        # Create SVG visualization
        output_file = f"output/{base_output_name}_{i+1}.svg"
        create_svg(intensity, particle_positions, output_file, 
                  wavelength, slit_width)
        
        print(f"Created SVG for slit width {slit_width*1e6:.1f} μm: {output_file}")

if __name__ == "__main__":
    main()
    
    # Uncomment the following lines to create series of simulations with different parameters
    # create_wavelength_series()
    # create_slit_width_series()