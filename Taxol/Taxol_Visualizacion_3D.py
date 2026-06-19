# ==============================================================================
# CODIGO CUANTICO LAB - PROYECTO PAULA (TAXOL)
# VISUALIZACIÓN 3D INTERACTIVA DE ORBITALES HOMO/LUMO
# ==============================================================================

import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("⚛️ CodigoCuanticoLab: Visualización 3D de Orbitales Moleculares")
print("=" * 80)

# ==============================================================================
# PASO 1: CARGAR DATOS DEL JSON
# ==============================================================================
print("\n📂 Paso 1: Cargando datos de orbitales...")

with open("taxol_orbitals_data.json", "r") as f:
    data = json.load(f)

atoms = data["atoms"]
homo_coeff = np.array(data["homo"]["coefficients"])
lumo_coeff = np.array(data["lumo"]["coefficients"])
homo_energy = data["homo"]["energy_eV"]
lumo_energy = data["lumo"]["energy_eV"]

print(f"✅ Datos cargados: {len(atoms)} átomos")
print(f"   HOMO: {homo_energy:.2f} eV")
print(f"   LUMO: {lumo_energy:.2f} eV")

# ==============================================================================
# PASO 2: GENERAR GRID 3D PARA CALCULAR DENSIDAD ELECTRÓNICA
# ==============================================================================
print("\n🔬 Paso 2: Generando grid 3D para densidad electrónica...")

# Crear grid de puntos en el espacio
x = np.linspace(-3, 3, 30)
y = np.linspace(-3, 3, 30)
z = np.linspace(-1, 1, 20)

X, Y, Z = np.meshgrid(x, y, z)
points = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T

# Coordenadas atómicas
atom_coords = np.array([[a['x'], a['y'], a['z']] for a in atoms])

# Para visualización simplificada, usamos los coeficientes directamente
# En una implementación completa, usaríamos funciones de base gaussianas
print(f"✅ Grid generado: {len(points)} puntos")

# ==============================================================================
# PASO 3: CALCULAR DENSIDAD DE ORBITALES (Aproximación visual)
# ==============================================================================
print("\n⚛️ Paso 3: Calculando densidad de orbitales...")

# Simplificación: Usamos los coeficientes ponderados por distancia a átomos
def calculate_orbital_density(points, atom_coords, coefficients):
    """Calcula densidad aproximada del orbital en cada punto"""
    density = np.zeros(len(points))
    
    for i, point in enumerate(points):
        for j, atom_pos in enumerate(atom_coords):
            # Distancia al átomo
            dist = np.linalg.norm(point - atom_pos)
            # Contribución del átomo (decae con distancia)
            if dist < 2.0:  # Solo átomos cercanos
                contribution = coefficients[j % len(coefficients)] * np.exp(-dist**2)
                density[i] += contribution
    
    return density

homo_density = calculate_orbital_density(points, atom_coords, homo_coeff)
lumo_density = calculate_orbital_density(points, atom_coords, lumo_coeff)

print(f"✅ Densidad calculada")

# ==============================================================================
# PASO 4: CREAR VISUALIZACIÓN 3D INTERACTIVA
# ==============================================================================
print("\n🎨 Paso 4: Creando visualización 3D interactiva...")

# Crear figura con 2 subplots (HOMO y LUMO)
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
    subplot_titles=(f'HOMO ({homo_energy:.2f} eV)', f'LUMO ({lumo_energy:.2f} eV)')
)

# Función para agregar orbital a la figura
def add_orbital_to_fig(fig, col, density, points, color_positive, color_negative, title):
    # Filtrar puntos con densidad significativa
    threshold = np.max(np.abs(density)) * 0.1
    mask = np.abs(density) > threshold
    
    if np.sum(mask) > 0:
        filtered_points = points[mask]
        filtered_density = density[mask]
        
        # Colores basados en signo de la densidad
        colors = []
        for d in filtered_density:
            if d > 0:
                colors.append(color_positive)
            else:
                colors.append(color_negative)
        
        # Agregar puntos del orbital
        fig.add_trace(
            go.Scatter3d(
                x=filtered_points[:, 0],
                y=filtered_points[:, 1],
                z=filtered_points[:, 2],
                mode='markers',
                marker=dict(
                    size=3,
                    color=colors,
                    opacity=0.6
                ),
                name=title
            ),
            row=1, col=col
        )

# Agregar HOMO (azul para positivo, rojo para negativo)
add_orbital_to_fig(fig, 1, homo_density, points, 'rgba(0, 100, 255, 0.6)', 'rgba(255, 50, 50, 0.6)', 'HOMO')

# Agregar LUMO (verde para positivo, naranja para negativo)
add_orbital_to_fig(fig, 2, lumo_density, points, 'rgba(0, 255, 100, 0.6)', 'rgba(255, 150, 0, 0.6)', 'LUMO')

# Agregar átomos a ambos subplots
for col in [1, 2]:
    # Carbonos (gris oscuro)
    c_atoms = [a for a in atoms if a['atom'] == 'C']
    fig.add_trace(
        go.Scatter3d(
            x=[a['x'] for a in c_atoms],
            y=[a['y'] for a in c_atoms],
            z=[a['z'] for a in c_atoms],
            mode='markers+text',
            marker=dict(size=10, color='rgb(80, 80, 80)', opacity=0.9),
            text=['C']*len(c_atoms),
            textposition='top center',
            name='Carbono'
        ),
        row=1, col=col
    )
    
    # Hidrógenos (blanco)
    h_atoms = [a for a in atoms if a['atom'] == 'H']
    fig.add_trace(
        go.Scatter3d(
            x=[a['x'] for a in h_atoms],
            y=[a['y'] for a in h_atoms],
            z=[a['z'] for a in h_atoms],
            mode='markers+text',
            marker=dict(size=6, color='rgb(255, 255, 255)', opacity=0.9),
            text=['H']*len(h_atoms),
            textposition='top center',
            name='Hidrógeno'
        ),
        row=1, col=col
    )

# Configurar layout
fig.update_layout(
    title=dict(
        text='Orbitales Moleculares del Benceno (C6H6)<br><sub>Fragmento del Taxol (Paclitaxel)</sub>',
        font=dict(size=20)
    ),
    showlegend=True,
    scene=dict(
        xaxis_title='X (Å)',
        yaxis_title='Y (Å)',
        zaxis_title='Z (Å)',
        aspectmode='cube'
    ),
    scene2=dict(
        xaxis_title='X (Å)',
        yaxis_title='Y (Å)',
        zaxis_title='Z (Å)',
        aspectmode='cube'
    ),
    width=1400,
    height=700
)

# ==============================================================================
# PASO 5: GUARDAR VISUALIZACIÓN
# ==============================================================================
print("\n💾 Paso 5: Guardando visualización interactiva...")

# Guardar como HTML interactivo
fig.write_html("taxol_orbitals_3d.html")
print("✅ Visualización guardada como 'taxol_orbitals_3d.html'")

# Guardar como imagen estática (si tienes kaleido instalado)
try:
    fig.write_image("taxol_orbitals_3d.png", scale=2)
    print("✅ Imagen estática guardada como 'taxol_orbitals_3d.png'")
except:
    print("⚠️ Para guardar imagen estática, instala: pip install kaleido")

print("\n" + "=" * 80)
print("🎉 ¡VISUALIZACIÓN 3D COMPLETADA!")
print("=" * 80)
print("\n📊 ARCHIVOS GENERADOS:")
print("   1. taxol_orbitals_data.json (Datos exactos de PSI4)")
print("   2. taxol_orbitals_3d.html (Visualización interactiva)")
print("   3. taxol_orbitals_3d.png (Imagen estática, si kaleido está instalado)")
print("\n🚀 PRÓXIMOS PASOS:")
print("   1. Abre 'taxol_orbitals_3d.html' en tu navegador")
print("   2. Rota, haz zoom y explora los orbitales HOMO y LUMO")
print("   3. Toma capturas de pantalla para tu post de LinkedIn")
print("   4. Envía la visualización a Paula como ejemplo de tu trabajo")
print("=" * 80)