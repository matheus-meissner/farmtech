# web/app_streamlit.py
import streamlit as st
import pandas as pd
import subprocess
from pathlib import Path
import sys

# garante import dos módulos python/
sys.path.append(str(Path(__file__).resolve().parents[1] / "python"))
from calculos import calcular_cana, calcular_cafe
from utils import salvar_csv

st.set_page_config(page_title="FarmTech • Agricultura Digital", layout="wide")

# --- estado ---
if "registros" not in st.session_state:
    st.session_state.registros = []

st.title("🌱 FarmTech Solutions — Agricultura Digital")

tab1, tab2, tab3 = st.tabs(["➕ Inserir dados", "📋 Registros", "⬇️ Exportar / 📈 Visualizar"])

# =============== INSERIR ===============
with tab1:
    st.subheader("Inserir novo talhão")
    cultura = st.radio("Cultura", ["Cana-de-açúcar", "Café"], horizontal=True)

    colA, colB, colC = st.columns(3)

    if cultura == "Cana-de-açúcar":
        comprimento = colA.number_input("Comprimento (m)", min_value=0.0, step=1.0)
        largura = colB.number_input("Largura (m)", min_value=0.0, step=1.0)
        dose_ml_m = colC.number_input("Dose (mL por metro de sulco)", min_value=0.0, step=10.0)
        produto = st.text_input("Produto (ex.: herbicida X)", value="herbicida")
        if st.button("Adicionar cana"):
            calc = calcular_cana(comprimento, largura)  # area, ruas, sulco_total, N, P, K
            litros = (dose_ml_m * calc["sulco_total"]) / 1000.0
            registro = {
                "cultura": "Cana-de-açúcar",
                "area": calc["area"],
                "ruas": calc["ruas"],
                "sulco_total": calc["sulco_total"],
                "plantas": None,
                "produto": produto,
                "dose_ml_por_m": dose_ml_m,
                "dose_ml_por_planta": None,
                "litros": litros,
                "N": calc["N"],
                "P": calc["P"],
                "K": calc["K"],
            }
            st.session_state.registros.append(registro)
            st.success("Cana adicionada!")

    else:  # Café
        raio = colA.number_input("Raio (m)", min_value=0.0, step=1.0)
        dose_ml_planta = colB.number_input("Dose (mL por planta)", min_value=0.0, step=10.0)
        produto = colC.text_input("Produto (ex.: fosfato foliar Y)", value="fosfato foliar")
        if st.button("Adicionar café"):
            calc = calcular_cafe(raio)  # area, plantas, N, P, K
            litros = (dose_ml_planta * (calc["plantas"] or 0)) / 1000.0
            registro = {
                "cultura": "Café",
                "area": calc["area"],
                "ruas": None,
                "sulco_total": None,
                "plantas": calc["plantas"],
                "produto": produto,
                "dose_ml_por_m": None,
                "dose_ml_por_planta": dose_ml_planta,
                "litros": litros,
                "N": calc["N"],
                "P": calc["P"],
                "K": calc["K"],
            }
            st.session_state.registros.append(registro)
            st.success("Café adicionado!")

# =============== REGISTROS ===============
with tab2:
    st.subheader("Registros")
    if st.session_state.registros:
        df = pd.DataFrame(st.session_state.registros)
        st.dataframe(df, use_container_width=True)

        # deletar selecionados
        st.markdown("### Remover registros")
        idxs = st.multiselect("Selecione pelo índice", options=list(range(len(df))))
        if st.button("Deletar selecionados"):
            for i in sorted(idxs, reverse=True):
                st.session_state.registros.pop(i)
            st.success("Removidos.")
    else:
        st.info("Nenhum registro ainda. Adicione em **Inserir dados**.")

# =============== EXPORTAR / VISUALIZAR ===============
with tab3:
    st.subheader("Exportar CSV e visualizar métricas")

    if st.session_state.registros:
        df = pd.DataFrame(st.session_state.registros)
        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Baixar dados.csv", data=csv_bytes, file_name="dados.csv", mime="text/csv")

        # Também salvar no diretório original python/ (para o R usar)
        base = Path(__file__).resolve().parents[1] / "python" / "dados.csv"
        if st.button("Salvar dados.csv na pasta python/"):
            salvar_csv(st.session_state.registros, arquivo=str(base))
            st.success(f"Salvo em {base}")

        # KPIs simples
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Registros", len(df))
        col2.metric("Área total (m²)", f"{df['area'].fillna(0).sum():.0f}")
        col3.metric("Litros totais", f"{df['litros'].fillna(0).sum():.2f}")
        col4.metric("Plantas (café)", f"{df['plantas'].fillna(0).sum():.0f}")

        # Gráfico rápido (sem substituir os do R)
        st.markdown("### Nutrientes por cultura (média)")
        mean_df = (
            df[["cultura","N","P","K"]]
            .groupby("cultura", as_index=False).mean(numeric_only=True)
            .melt(id_vars="cultura", var_name="Nutriente", value_name="Média (g)")
        )
        st.bar_chart(mean_df, x="Nutriente", y="Média (g)", color="cultura", use_container_width=True)
    else:
        st.info("Nada para exportar ainda.")

    # --- Gráficos PNG gerados pelo R ---
    st.markdown("---")
    st.markdown("### Gráficos do R (PNG)")
    r_dir = Path(__file__).resolve().parents[1] / "r"
    png_dir = r_dir / "graficos"

    colA, colB = st.columns(2)

    def _show_png(p: Path, caption: str):
        if p.exists():
            st.image(str(p), caption=caption, use_container_width=True)
        else:
            st.info(f"Arquivo não encontrado: `{p.name}`. Gere com **Rscript graficos.R**.")

    # botões utilitários
    c1, c2 = st.columns(2)
    if c1.button("🔁 Regerar gráficos no R"):
        # Requer R no PATH
        res = subprocess.run(
            ["Rscript", "graficos.R"],
            cwd=str(r_dir),
            capture_output=True,
            text=True,
            shell=False
        )
        if res.returncode == 0:
            st.success("Gráficos gerados. Clique em **Recarregar imagens**.")
            if res.stdout:
                st.code(res.stdout)
        else:
            st.error("Falha ao rodar `Rscript graficos.R`.")
            if res.stderr:
                st.code(res.stderr)

    if c2.button("🔄 Recarregar imagens"):
        st.experimental_rerun()

    with colA:
        _show_png(png_dir / "histograma_area.png", "Distribuição da Área Plantada")
        _show_png(png_dir / "boxplot_insumos.png", "Insumos por Cultura (boxplot/pontos)")
    with colB:
        _show_png(png_dir / "medias_insumos.png", "Média dos Nutrientes por Cultura")

st.caption("💡 Dica: depois de salvar o CSV em `python/dados.csv`, rode `Rscript analise.R` e `Rscript graficos.R` para gerar estatísticas e imagens (bg branco).")
