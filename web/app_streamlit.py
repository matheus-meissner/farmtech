# web/app_streamlit.py
import streamlit as st
import pandas as pd
import subprocess
from pathlib import Path
import sys, requests

# garante import dos módulos python/
sys.path.append(str(Path(__file__).resolve().parents[1] / "python"))
from calculos import calcular_cana, calcular_cafe
from utils import salvar_csv

from base64 import b64encode
from pathlib import Path

st.set_page_config(
    page_title="FarmTech • Agricultura Digital",
    page_icon="../img/farmtech_icone.png",  # caminho relativo
    layout="wide"
)


img_path = Path(__file__).resolve().parents[1] / "img" / "fundo-fazenda-50.png"
img_base64 = b64encode(open(img_path, "rb").read()).decode()

st.markdown(
    f"""
    <style>
    /* ===== Fonte ===== */

    /* ===== Fundo ===== */
    .stApp {{
        position: relative;
        overflow: hidden;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        z-index: 0;                 /* atrás */
        pointer-events: none;
    }}
    [data-testid="stAppViewContainer"],
    .block-container {{
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        padding-top: 2rem !important;
        position: relative;
        z-index: 1;                 /* na frente */
    }}


    /* ===== Tipografia global ===== */
    .stApp, .stApp * {{
        color: #fff !important;     /* tudo branco por padrão */
    }}

    /* Cabeçalho/Rodapé (remover) */
    [data-testid="stHeader"], footer {{ display: none; }}

    /* ===== Campos de formulário (texto preto) ===== */
    input[type="text"],
    input[type="number"],
    input[type="email"],
    input[type="password"],
    textarea,
    select,
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    /* selectbox (BaseWeb) */
    div[data-baseweb="select"] * {{
        color: #000 !important;
    }}
    /* fundo branco nos inputs (opcional) */
    input, textarea, select {{
        background-color: #fff !important;
    }}
    /* placeholder mais visível */
    input::placeholder,
    textarea::placeholder {{
        color: #666 !important;
    }}

    /* ===== Botões com label preta =====
       Use seletores estáveis: .stButton e data-testid/baseweb  */
    .stButton > button,
    .stButton > button *,
    .stDownloadButton > button,
    .stDownloadButton > button *,
    button[data-baseweb="button"],
    [data-testid="baseButton-primary"],
    [data-testid="baseButton-secondary"] {{
        color: #fff !important;     /* 🔹 texto preto no botão */
        background-color: #e63946 !important; /* vermelho padrão */
    }}

    /* ==== Botões de input ==== */
    /* Botões de incremento/decremento dos number_input */
    .stNumberInput button {{
        background-color: #e63946 !important; /* vermelho padrão */
        color: #fff !important;
        border: 1px solid #b71c1c !important;
        border-radius: 4px !important;
    }}

    /* Ícones dentro dos botões (o + e o -) */
    .stNumberInput button svg {{
        stroke: #fff !important;
        fill: #fff !important;
    }}

    /* Hover: vermelho mais escuro */
    .stNumberInput button:hover {{
        background-color: #c62828 !important;
        border-color: #8e0000 !important;
    }}

    /* ===== Ajuste dos botões +/- ===== */
    .stNumberInput button {{
        background-color: #e63946 !important;  /* vermelho base */
        color: #fff !important;
        border: 1px solid #b71c1c !important;
        padding: 0.25rem 0.75rem !important;
        font-weight: bold;
        box-shadow: none !important;
    }}

    /* Botão de decremento (esquerda) */
    .stNumberInput button:first-of-type {{
        border-radius: 6px 0 0 6px !important;   /* arredonda canto esquerdo */
        border-right: none !important;           /* remove borda duplicada no meio */
    }}

    /* Botão de incremento (direita) */
    .stNumberInput button:last-of-type {{
        border-radius: 0 6px 6px 0 !important;   /* arredonda canto direito */
    }}

    /* Hover: tom mais escuro */
    .stNumberInput button:hover {{
        background-color: #c62828 !important;
        border-color: #8e0000 !important;
    }}

    /* ===== Hover global para todos os botões ===== */
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    button[data-baseweb="button"]:hover,
    [data-testid="baseButton-primary"]:hover,
    [data-testid="baseButton-secondary"]:hover,
    .stButton > button:hover p,
    .stDownloadButton > button:hover p,
    button[data-baseweb="button"]:hover p,
    [data-testid="baseButton-primary"]:hover p,
    [data-testid="baseButton-secondary"]:hover p {{
        background-color: #c62828 !important; /* mesmo vermelho do +/- */
    }}


    /* Garante que ícones dentro dos botões também fiquem brancos */
    .stButton > button:hover svg,
    .stDownloadButton > button:hover svg,
    button[data-baseweb="button"]:hover svg {{
        fill: #fff !important;
        stroke: #fff !important;
    }}

    /* Evita quebra de linha nos rótulos dos widgets (mantém os inputs alinhados) */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] > div {{
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important; /* mostra "..." se faltar espaço */
    display: inline-block !important;
    max-width: 100% !important;
    vertical-align: middle !important;
    }}

    /* Mantém o ícone de ajuda na mesma linha do label */
    [data-testid="stWidgetLabel"] + div [data-testid="stTooltipHoverTarget"],
    [aria-label="Toggle tooltip"] {{
    vertical-align: middle !important;
    }}

    /* Opcional: reduz um pouco a altura do cabeçalho do campo */
    [data-testid="stWidgetLabel"] {{
    line-height: 1.15 !important;
    margin-bottom: 0.25rem !important;
    }}

    /* Opcional: se algum input ainda "escorregar", garanta alinhamento das colunas */
    .stColumn {{
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    }}

    /* Centralizar a barra de abas */
    [role="tablist"] {{
        display: flex !important;
        justify-content: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)



# --- estado ---
if "registros" not in st.session_state:
    st.session_state.registros = []

st.title("FarmTech Solutions • Agricultura Digital")

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Inserir dados",
    "📋 Registros",
    "⬇️ Exportar / 📈 Visualizar",
    "☁️ Clima (Open-Meteo)"
])

# =========================================================
# =============== INSERIR (com espaçamentos) ==============
# =========================================================
with tab1:
    st.subheader("Inserir novo talhão")
    cultura = st.radio("Cultura", ["Cana-de-açúcar", "Café"], horizontal=True)

    if cultura == "Cana-de-açúcar":
        colA, colB, colC, colD = st.columns(4)
        comprimento = colA.number_input("Comprimento (m)", min_value=0.0, step=1.0)
        largura     = colB.number_input("Largura (m)",     min_value=0.0, step=1.0)
        espac_rua   = colC.number_input("Espaçamento entre ruas (m)", min_value=0.1, value=1.5, step=0.1,
                                        help="Usado para calcular nº de ruas e metros de sulco")
        dose_ml_m   = colD.number_input("Dose (mL por metro de sulco)", min_value=0.0, step=10.0)
        produto     = st.text_input("Produto (ex.: herbicida X)", value="herbicida")

        if st.button("Adicionar cana"):
            # passa o espaçamento para o cálculo (nº de ruas e sulco_total)
            calc = calcular_cana(comprimento, largura, espacamento=espac_rua)
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
                # salva também o espaçamento usado (útil para auditoria)
                "espac_rua_m": espac_rua
            }
            st.session_state.registros.append(registro)
            st.success("Cana adicionada!")

    else:  # Café
        colA, colB, colC, colD = st.columns(4)
        raio          = colA.number_input("Raio (m)", min_value=0.0, step=1.0)
        espac_rua_caf = colB.number_input("Espaçamento entre ruas (m)", min_value=0.1, value=3.8, step=0.1)
        espac_pla_caf = colC.number_input("Espaçamento entre plantas (m)", min_value=0.1, value=0.7, step=0.1)
        dose_ml_planta= colD.number_input("Dose (mL por planta)", min_value=0.0, step=10.0)
        produto       = st.text_input("Produto (ex.: fosfato foliar Y)", value="fosfato foliar")

        if st.button("Adicionar café"):
            # passa os espaçamentos para estimar nº de plantas
            calc = calcular_cafe(raio, espac_rua=espac_rua_caf, espac_planta=espac_pla_caf)
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
                "espac_rua_m": espac_rua_caf,
                "espac_planta_m": espac_pla_caf
            }
            st.session_state.registros.append(registro)
            st.success("Café adicionado!")

# ====================================
# =============== REGISTROS ==========
# ====================================
with tab2:
    st.subheader("Registros")
    if st.session_state.registros:
        df = pd.DataFrame(st.session_state.registros)
        st.dataframe(df, use_container_width=True)

        st.markdown("### Remover registros")
        idxs = st.multiselect("Selecione pelo índice", options=list(range(len(df))))
        if st.button("Deletar selecionados"):
            for i in sorted(idxs, reverse=True):
                st.session_state.registros.pop(i)
            st.success("Removidos.")
    else:
        st.info("Nenhum registro ainda. Adicione em **Inserir dados**.")

# =========================================================
# =============== EXPORTAR / VISUALIZAR ===================
# =========================================================
with tab3:
    st.subheader("Exportar CSV e visualizar métricas")

    if st.session_state.registros:
        df = pd.DataFrame(st.session_state.registros)
        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Baixar dados.csv", data=csv_bytes, file_name="dados.csv", mime="text/csv")

        base = Path(__file__).resolve().parents[1] / "python" / "dados.csv"
        if st.button("Salvar dados.csv na pasta python/"):
            salvar_csv(st.session_state.registros, arquivo=str(base))
            st.success(f"Salvo em {base}")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Registros", len(df))
        col2.metric("Área total (m²)", f"{df['area'].fillna(0).sum():.0f}")
        col3.metric("Litros totais", f"{df['litros'].fillna(0).sum():.2f}")
        col4.metric("Plantas (café)", f"{df['plantas'].fillna(0).sum():.0f}")

        st.markdown("### Nutrientes por cultura (média)")
        mean_df = (
            df[["cultura","N","P","K"]]
            .groupby("cultura", as_index=False).mean(numeric_only=True)
            .melt(id_vars="cultura", var_name="Nutriente", value_name="Média (g)")
        )
        st.bar_chart(mean_df, x="Nutriente", y="Média (g)", color="cultura", use_container_width=True)
    else:
        st.info("Nada para exportar ainda.")

    st.markdown("---")
    st.markdown("### Gráficos do R (PNG)")
    r_dir = Path(__file__).resolve().parents[1] / "r"
    png_dir = r_dir / "graficos"

    def _show_png(p: Path, caption: str):
        if p.exists():
            st.image(str(p), caption=caption, use_container_width=True)
        else:
            st.info(f"Arquivo não encontrado: `{p.name}`. Gere com **Rscript graficos.R**.")

    c1, c2 = st.columns(2)
    if c1.button("🔁 Regerar gráficos no R"):
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
        st.rerun()

    colA, colB = st.columns(2)
    with colA:
        _show_png(png_dir / "histograma_area.png", "Distribuição da Área Plantada")
        _show_png(png_dir / "boxplot_insumos.png", "Insumos por Cultura (boxplot/pontos)")
    with colB:
        _show_png(png_dir / "medias_insumos.png", "Média dos Nutrientes por Cultura")

# =========================================================
# =============== CLIMA (Open-Meteo) ======================
# =========================================================
with tab4:
    st.subheader("Clima — Open-Meteo (sem API key)")

    # Layout em 4 colunas (igual ao Inserir dados)
    c1, c2, c3, c4 = st.columns(4)

    cidade = c1.text_input("Cidade (opcional, só para exibir no título)", value="São Paulo")
    lat    = c2.number_input("Latitude",  value=-23.55, step=0.01, format="%.4f")
    lon    = c3.number_input("Longitude", value=-46.63, step=0.01, format="%.4f")
    tz     = c4.selectbox("Timezone", ["America/Sao_Paulo", "UTC"], index=0)


    if st.button("Consultar clima"):
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current_weather=true"
            "&hourly=temperature_2m,precipitation,relative_humidity_2m"
            f"&timezone={tz}"
        )
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            st.error(f"Erro ao consultar Open-Meteo: {e}")
            data = None

        if data:
            st.markdown(f"#### Tempo atual — {cidade}")
            cw = data.get("current_weather", {})
            if cw:
                c1, c2, c3 = st.columns(3)
                c1.metric("Temperatura (°C)", f"{cw.get('temperature', '—')}")
                c2.metric("Vento (km/h)", f"{cw.get('windspeed', '—')}")
                c3.metric("Direção do vento (°)", f"{cw.get('winddirection', '—')}")
                st.caption(f"Hora local: {cw.get('time', '—')}")
            else:
                st.info("Sem dados de tempo atual.")

            hourly = data.get("hourly", {})
            if hourly:
                st.markdown("#### Próximas horas (12h)")
                # Mostra uma pequena tabela com 12 registros
                df_h = pd.DataFrame(hourly)[["time", "temperature_2m", "precipitation"]].head(12)
                df_h.columns = ["Hora", "Temp (°C)", "Precip (mm)"]
                st.dataframe(df_h, use_container_width=True, hide_index=True)
            else:
                st.info("Sem dados horários.")
