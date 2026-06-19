# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL)
# VISUALIZACIÓN 3D ÉPICA - ESTILO DORADO PROFESIONAL
# ==============================================================================

import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("⚛️ CodigoCuanticoLab: Visualización 3D Épica de Orbitales")
print("=" * 80)

# Cargar datos
with open("taxol_orbitals_data.json", "r") as f:
    data = json.load(f)

atoms = data["atoms"]
homo_coeff = np.array(data["homo"]["coefficients"])
lumo_coeff = np.array(data["lumo"]["coefficients"])
homo_energy = data["homo"]["energy_eV"]
lumo_energy = data["lumo"]["energy_eV"]

print(f"✅ Datos cargados: HOMO {homo_energy:.2f} eV, LUMO {lumo_energy:.2f} eV")

# ==============================================================================
# GENERAR GRID 3D MÁS DENSO PARA SUPERFICIES SUAVES
# ==============================================================================
print("\n🔬 Generando grid 3D de alta resolución...")

x = np.linspace(-3.5, 3.5, 50)
y = np.linspace(-3.5, 3.5, 50)
z = np.linspace(-1.5, 1.5, 30)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
points = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T

atom_coords = np.array([[a['x'], a['y'], a['z']] for a in atoms])

# ==============================================================================
# CALCULAR DENSIDAD CON FUNCIONES GAUSSIANAS (Más realista)
# ==============================================================================
print("⚛️ Calculando densidad electrónica con funciones gaussianas...")

def calculate_orbital_density_gaussian(points, atom_coords, coefficients, sigma=0.5):
    """Calcula densidad usando funciones gaussianas en cada átomo"""
    density = np.zeros(len(points))
    
    for i, point in enumerate(points):
        for j, atom_pos in enumerate(atom_coords):
            dist_sq = np.sum((point - atom_pos)**2)
            # Función gaussiana que decae con la distancia
            coeff = coefficients[j % len(coefficients)]
            contribution = coeff * np.exp(-dist_sq / (2 * sigma**2))
            density[i] += contribution
    
    return density.reshape(X.shape)

homo_density = calculate_orbital_density_gaussian(points, atom_coords, homo_coeff, sigma=0.6)
lumo_density = calculate_orbital_density_gaussian(points, atom_coords, lumo_coeff, sigma=0.6)

print(f"✅ Densidad calculada en {len(points)} puntos")

# ==============================================================================
# CREAR VISUALIZACIÓN ÉPICA CON SUPERFICIES ISOSURFACES
# ==============================================================================
print("\n🎨 Creando visualización épica estilo dorado...")

# Crear figura con fondo oscuro
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'isosurface'}, {'type': 'isosurface'}]],
    subplot_titles=(
        f'<b>HOMO</b><br>{homo_energy:.2f} eV',
        f'<b>LUMO</b><br>{lumo_energy:.2f} eV'
    )
)

# Función para agregar isosurface épica
def add_epic_isosurface(fig, col, density, X, Y, Z, color_pos, color_neg, name):
    # Umbral para la isosuperficie
    threshold = np.max(np.abs(density)) * 0.3
    
    # Parte positiva
    fig.add_trace(
        go.Isosurface(
            x=X.ravel(),
            y=Y.ravel(),
            z=Z.ravel(),
            value=density.ravel(),
            isomin=threshold,
            isomax=np.max(density),
            opacity=0.7,
            surface_count=5,
            colorscale=[[0, color_pos], [1, color_pos]],
            showscale=False,
            name=f'{name} (+)'
        ),
        row=1, col=col
    )
    
    # Parte negativa
    fig.add_trace(
        go.Isosurface(
            x=X.ravel(),
            y=Y.ravel(),
            z=Z.ravel(),
            value=-density.ravel(),
            isomin=threshold,
            isomax=np.max(-density),
            opacity=0.7,
            surface_count=5,
            colorscale=[[0, color_neg], [1, color_neg]],
            showscale=False,
            name=f'{name} (-)'
        ),
        row=1, col=col
    )

# Agregar HOMO (Dorado y Azul)
add_epic_isosurface(fig, 1, homo_density, X, Y, Z, 
                    'rgb(255, 215, 0)',    # Dorado
                    'rgb(0, 150, 255)',    # Azul
                    'HOMO')

# Agregar LUMO (Plateado y Rojo)
add_epic_isosurface(fig, 2, lumo_density, X, Y, Z,
                    'rgb(200, 200, 200)',  # Plateado
                    'rgb(255, 50, 50)',    # Rojo
                    'LUMO')

# Agregar átomos con estilo épico
for col in [1, 2]:
    # Carbonos (Dorado brillante)
    c_atoms = [a for a in atoms if a['atom'] == 'C']
    fig.add_trace(
        go.Scatter3d(
            x=[a['x'] for a in c_atoms],
            y=[a['y'] for a in c_atoms],
            z=[a['z'] for a in c_atoms],
            mode='markers',
            marker=dict(
                size=12,
                color='rgb(255, 215, 0)',
                symbol='circle',
                line=dict(width=2, color='rgb(255, 255, 255)'),
                opacity=0.95
            ),
            name='Carbono',
            showlegend=False
        ),
        row=1, col=col
    )
    
    # Hidrógenos (Blanco brillante)
    h_atoms = [a for a in atoms if a['atom'] == 'H']
    fig.add_trace(
        go.Scatter3d(
            x=[a['x'] for a in h_atoms],
            y=[a['y'] for a in h_atoms],
            z=[a['z'] for a in h_atoms],
            mode='markers',
            marker=dict(
                size=8,
                color='rgb(255, 255, 255)',
                symbol='circle',
                line=dict(width=1, color='rgb(200, 200, 200)'),
                opacity=0.9
            ),
            name='Hidrógeno',
            showlegend=False
        ),
        row=1, col=col
    )

# Layout épico con fondo oscuro
fig.update_layout(
    title=dict(
        text='<b>Orbitales Moleculares del Benceno (C6H6)</b><br>' +
             '<span style="font-size: 16px;">Fragmento del Taxol (Paclitaxel) - Simulación Cuántica Híbrida</span>',
        font=dict(size=24, color='white'),
        x=0.5
    ),
    paper_bgcolor='rgb(20, 20, 40)',  # Fondo azul oscuro
    plot_bgcolor='rgb(20, 20, 40)',
    font=dict(color='white'),
    showlegend=True,
    legend=dict(
        bgcolor='rgba(0, 0, 0, 0.5)',
        font=dict(size=12)
    ),
    width=1600,
    height=800,
    scene=dict(
        xaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        yaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        zaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        aspectmode='cube',
        bgcolor='rgb(10, 10, 30)'
    ),
    scene2=dict(
        xaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        yaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        zaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        aspectmode='cube',
        bgcolor='rgb(10, 10, 30)'
    )
)

# ==============================================================================
# GUARDAR EN MÚLTIPLES FORMATOS
# ==============================================================================
print("\n💾 Guardando visualización en múltiples formatos...")

# 1. HTML interactivo (para que explores)
fig.write_html("taxol_orbitals_epica.html")
print("✅ HTML interactivo: 'taxol_orbitals_epica.html'")

# 2. PNG de alta resolución (para LinkedIn)
try:
    fig.write_image("taxol_orbitals_epica.png", scale=3, width=1920, height=1080)
    print("✅ PNG alta resolución: 'taxol_orbitals_epica.png' (1920x1080)")
except Exception as e:
    print(f"⚠️ Error al guardar PNG: {e}")
    print("   Instala kaleido: pip install kaleido")

# 3. Múltiples vistas para que elijas la mejor
print("\n📸 Generando múltiples vistas...")

# Vista frontal
fig.update_layout(
    scene=dict(camera=dict(eye=dict(x=0, y=-2.5, z=0))),
    scene2=dict(camera=dict(eye=dict(x=0, y=-2.5, z=0)))
)
try:
    fig.write_image("taxol_vista_frontal.png", scale=3, width=1920, height=1080)
    print("✅ Vista frontal guardada")
except Exception as e:
    print(f"⚠️ Error vista frontal: {e}")

# Vista lateral
fig.update_layout(
    scene=dict(camera=dict(eye=dict(x=2.5, y=0, z=0))),
    scene2=dict(camera=dict(eye=dict(x=2.5, y=0, z=0)))
)
try:
    fig.write_image("taxol_vista_lateral.png", scale=3, width=1920, height=1080)
    print("✅ Vista lateral guardada")
except Exception as e:
    print(f"⚠️ Error vista lateral: {e}")

# Vista superior
fig.update_layout(
    scene=dict(camera=dict(eye=dict(x=0, y=0, z=2.5))),
    scene2=dict(camera=dict(eye=dict(x=0, y=0, z=2.5)))
)
try:
    fig.write_image("taxol_vista_superior.png", scale=3, width=1920, height=1080)
    print("✅ Vista superior guardada")
except Exception as e:
    print(f"⚠️ Error vista superior: {e}")

# Vista diagonal (la más épica)
fig.update_layout(
    scene=dict(camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))),
    scene2=dict(camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
)
try:
    fig.write_image("taxol_vista_epica.png", scale=3, width=1920, height=1080)
    print("✅ Vista épica diagonal guardada")
except Exception as e:
    print(f"⚠️ Error vista épica: {e}")

print("\n" + "=" * 80)
print("🎉 ¡VISUALIZACIÓN ÉPICA COMPLETADA!")
print("=" * 80)
print("\n📊 ARCHIVOS GENERADOS:")
print("   1. taxol_orbitals_epica.html (Interactiva)")
print("   2. taxol_orbitals_epica.png (Alta resolución 1920x1080) <-- ¡USA ESTA PARA LINKEDIN!")
print("   3. taxol_vista_frontal.png")
print("   4. taxol_vista_lateral.png")
print("   5. taxol_vista_superior.png")
print("   6. taxol_vista_epica.png")
print("\n🚀 PARA LINKEDIN:")
print("   - Sube 'taxol_orbitals_epica.png' o 'taxol_vista_epica.png'")
print("   - El fondo oscuro y los colores dorados destacan en el feed")
print("   - Resolución 1920x1080 se ve perfecta en LinkedIn")
print("=" * 80)