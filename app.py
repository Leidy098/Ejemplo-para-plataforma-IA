import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Análisis de Datos Sintéticos", layout="wide")

st.title("📊 Análisis Gráfico con Datos Sintéticos")
st.markdown("Explora datos generados aleatoriamente con distintas visualizaciones.")

# --- Sidebar: controles ---
st.sidebar.header("⚙️ Configuración")
n = st.sidebar.slider("Número de registros", 50, 2000, 500, step=50)
seed = st.sidebar.number_input("Semilla aleatoria", value=42, step=1)

# --- Generación de datos sintéticos ---
@st.cache_data
def generar_datos(n, seed):
    rng = np.random.default_rng(seed)
    categorias = ["A", "B", "C", "D"]
    df = pd.DataFrame({
        "fecha": pd.date_range("2024-01-01", periods=n, freq="D"),
        "categoria": rng.choice(categorias, size=n),
        "ventas": rng.normal(1000, 250, n).round(2),
        "unidades": rng.integers(1, 100, n),
        "satisfaccion": rng.uniform(1, 5, n).round(2),
    })
    df["ingreso"] = (df["ventas"] * df["unidades"] / 10).round(2)
    return df

df = generar_datos(n, seed)

# --- Métricas ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros", len(df))
c2.metric("Ventas promedio", f"${df['ventas'].mean():,.0f}")
c3.metric("Unidades totales", f"{df['unidades'].sum():,}")
c4.metric("Satisfacción media", f"{df['satisfaccion'].mean():.2f} ⭐")

st.divider()

# --- Gráficos ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ventas en el tiempo")
    fig1 = px.line(df, x="fecha", y="ventas", color="categoria")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Ingreso por categoría")
    resumen = df.groupby("categoria", as_index=False)["ingreso"].sum()
    fig2 = px.bar(resumen, x="categoria", y="ingreso", color="categoria")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Distribución de ventas")
    fig3 = px.histogram(df, x="ventas", nbins=30, color="categoria")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Ventas vs. Unidades")
    fig4 = px.scatter(df, x="unidades", y="ventas", color="categoria",
                      size="satisfaccion", hover_data=["ingreso"])
    st.plotly_chart(fig4, use_container_width=True)

# --- Tabla de datos ---
st.divider()
st.subheader("🔍 Datos")
st.dataframe(df, use_container_width=True)

st.download_button(
    "⬇️ Descargar CSV",
    df.to_csv(index=False).encode("utf-8"),
    "datos_sinteticos.csv",
    "text/csv",
)