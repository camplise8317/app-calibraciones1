import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Cargar datos
file_path = "calibraciones_2025.csv"
df = pd.read_csv(file_path, encoding="utf-8", sep=";")

# Normalizar valores de las columnas para evitar errores de espacios o mayúsculas
df['Area'] = df['Area'].str.strip().str.lower()
df['Tipo_Item'] = df['Tipo_Item'].str.strip()
df['ItemGradoNombre'] = df['ItemGradoNombre'].str.strip()

# Eliminar valores NaN en la columna de grado
df = df.dropna(subset=['ItemGradoNombre'])

# Interfaz de usuario con Streamlit
st.title("Curvas de Dificultad de Ítems Ancla")

# Selección de área
area = st.selectbox("Selecciona un Área:", sorted(df['Area'].unique()))

# Filtrar datos por área y tipo de ítem "Item ancla"
df_filtrado = df[(df['Area'] == area) & (df['Tipo_Item'] == 'Item ancla')].copy()

if df_filtrado.empty:
    st.warning("No hay datos que coincidan con el área seleccionada.")
else:
    # Reemplazar comas por puntos y convertir a numérico
    df_filtrado['b.(Dificultad)'] = df_filtrado['b.(Dificultad)'].str.replace(',', '.').astype(float)
    df_filtrado = df_filtrado.dropna(subset=['b.(Dificultad)'])
    
    # Selección de grados
    grados_disponibles = sorted(df_filtrado['ItemGradoNombre'].unique())
    grados_seleccionados = st.multiselect("Selecciona los grados que deseas visualizar:", grados_disponibles, default=grados_disponibles)
    
    # Filtrar por los grados seleccionados
    df_filtrado = df_filtrado[df_filtrado['ItemGradoNombre'].isin(grados_seleccionados)]
    
    if df_filtrado.empty:
        st.warning("No hay datos para los grados seleccionados.")
    else:
        colores = plt.colormaps.get_cmap('tab10')
        color_map = {grado: colores(i % 10) for i, grado in enumerate(grados_seleccionados)}
        
        # Crear gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for grado in grados_seleccionados:
            df_grado = df_filtrado[df_filtrado['ItemGradoNombre'] == grado].sort_values(by='b.(Dificultad)')
            df_grado['Índice'] = range(1, len(df_grado) + 1)
            ax.plot(df_grado['Índice'], df_grado['b.(Dificultad)'], linestyle='-', marker='o', markersize=1, color=color_map[grado], label=f"{grado}")
        
        # Línea horizontal en 0
        ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
        
        # Configurar ejes
        ax.set_xlabel("Ítems ordenados de más fácil a más difícil")
        ax.set_ylabel("Dificultad (b)")
        ax.set_title(f"Curvas de Dificultad de Ítems Ancla - {area.capitalize()}")
        ax.legend(title="Grados")
        
        # Ajustar límites de la escala del eje Y entre -3 y 3
        ax.set_ylim(-3, 3)
        
        ax.grid(True, which='both', linestyle='--', alpha=0.6)
        
        # Mostrar gráfico en Streamlit
        st.pyplot(fig)
