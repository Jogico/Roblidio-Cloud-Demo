# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL)
# VISUALIZACIÓN 3D ÉPICA - OPTIMIZADA PARA DASHBOARD (1200x600)
# ==============================================================================

import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

print("⚛️ CodigoCuanticoLab: Visualización 3D Épica (Versión Dashboard)")
print("=" * 80)

# Cargar datos
try:
    with open("taxol_orbitals_data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ Error: No se encontró taxol_orbitals_data.json")
    exit()

atoms = data["atoms"]
homo_coeff = np.array(data["homo"]["coefficients"])
lumo_coeff = np.array(data["lumo"]["coefficients"])
homo_energy = data["homo"]["energy_eV"]
lumo_energy = data["lumo"]["energy_eV"]

print(f"✅ Datos cargados: HOMO {homo_energy:.2f} eV, LUMO {lumo_energy:.2f} eV")

# ==============================================================================
# GENERAR GRID 3D
# ==============================================================================
x = np.linspace(-3.5, 3.5, 45) # Ligera reducción de densidad para velocidad
y = np.linspace(-3.5, 3.5, 45)
z = np.linspace(-1.5, 1.5, 25)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
points = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T
atom_coords = np.array([[a['x'], a['y'], a['z']] for a in atoms])

# ==============================================================================
# CALCULAR DENSIDAD
# ==============================================================================
def calculate_orbital_density_gaussian(points, atom_coords, coefficients, sigma=0.6):
    density = np.zeros(len(points))
    for j, atom_pos in enumerate(atom_coords):
        dist_sq = np.sum((points - atom_pos)**2, axis=1)
        coeff = coefficients[j % len(coefficients)]
        density += coeff * np.exp(-dist_sq / (2 * sigma**2))
    return density.reshape(X.shape)

print("⚛️ Calculando densidades...")
homo_density = calculate_orbital_density_gaussian(points, atom_coords, homo_coeff)
lumo_density = calculate_orbital_density_gaussian(points, atom_coords, lumo_coeff)

# ==============================================================================
# CREAR VISUALIZACIÓN UNIFICADA (SUBPLOTS)
# ==============================================================================
# Ajustamos especificaciones para que quepan en una pantalla estándar
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'isosurface'}, {'type': 'isosurface'}]],
    horizontal_spacing=0.05, # Espacio mínimo entre gráficas
    subplot_titles=(
        f'<b>HOMO</b>: {homo_energy:.2f} eV',
        f'<b>LUMO</b>: {lumo_energy:.2f} eV'
    )
)

def add_epic_isosurface(fig, col, density, color_pos, color_neg, name):
    threshold = np.max(np.abs(density)) * 0.3
    
    # Parte Positiva
    fig.add_trace(go.Isosurface(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        value=density.ravel(),
        isomin=threshold, isomax=np.max(density),
        opacity=0.6, surface_count=3,
        colorscale=[[0, color_pos], [1, color_pos]],
        showscale=False, name=f'{name} (+)'
    ), row=1, col=col)
    
    # Parte Negativa
    fig.add_trace(go.Isosurface(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        value=-density.ravel(),
        isomin=threshold, isomax=np.max(-density),
        opacity=0.6, surface_count=3,
        colorscale=[[0, color_neg], [1, color_neg]],
        showscale=False, name=f'{name} (-)'
    ), row=1, col=col)

# Renderizar HOMO y LUMO
add_epic_isosurface(fig, 1, homo_density, 'rgb(255, 215, 0)', 'rgb(0, 150, 255)', 'HOMO')
add_epic_isosurface(fig, 2, lumo_density, 'rgb(200, 200, 200)', 'rgb(255, 50, 50)', 'LUMO')

# Átomos (Esferas)
for col in [1, 2]:
    c_atoms = [a for a in atoms if a['atom'] == 'C']
    h_atoms = [a for a in atoms if a['atom'] == 'H']
    
    fig.add_trace(go.Scatter3d(
        x=[a['x'] for a in c_atoms], y=[a['y'] for a in c_atoms], z=[a['z'] for a in c_atoms],
        mode='markers', marker=dict(size=6, color='rgb(255, 215, 0)', line=dict(width=1, color='white')),
        showlegend=False
    ), row=1, col=col)

# ==============================================================================
# LAYOUT FINAL OPTIMIZADO PARA STREAMLIT (1200x600)
# ==============================================================================
fig.update_layout(
    title=dict(
        text='<b>Orbitales Moleculares - Fragmento Taxol</b>',
        font=dict(size=20, color='white'),
        x=0.5, y=0.95
    ),
    paper_bgcolor='rgb(10, 14, 20)', 
    plot_bgcolor='rgb(10, 14, 20)',
    font=dict(color='white', size=12),
    width=1150,  # Reducido para que quepa en el st.container
    height=580,  # Altura optimizada para evitar scroll vertical
    margin=dict(l=10, r=10, b=10, t=80),
    showlegend=False,
    scene=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        aspectmode='cube', bgcolor='rgb(5, 8, 12)'
    ),
    scene2=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        aspectmode='cube', bgcolor='rgb(5, 8, 12)'
    )
)

# Guardar
fig.write_html("taxol_orbitals_epica.html", include_plotlyjs='cdn')
print("✅ Archivo unificado generado: taxol_orbitals_epica.html (1150x580)")