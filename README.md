# 🌱 FarmTech Solutions • Agricultura Digital

Bem-vindo ao repositório da **FarmTech Solutions**, uma aplicação desenvolvida como parte da disciplina de **Inteligência Artificial aplicada à Agricultura Digital** (FIAP).  
O objetivo do projeto é digitalizar cálculos agrícolas para aumentar a produtividade, unindo **Python + R + Streamlit** com integração a **APIs públicas de clima**.

---

## 🚀 Funcionalidades

✅ Suporte a **duas culturas agrícolas**:  
- 🌾 **Cana-de-açúcar** (área retangular)  
- ☕ **Café** (área circular)

✅ **Cálculo de área plantada** com base em figuras geométricas.

✅ **Manejo de insumos (N, P, K)** por área:  
- Nitrogênio (N)  
- Fósforo (P)  
- Potássio (K)  

✅ Estimativa de:  
- Ruas e metros de sulco (cana)  
- Número de plantas (café)  
- Litros de insumo necessários  

✅ **CRUD de registros** (inserir, listar, atualizar, deletar).  
✅ **Exportação para CSV**.  
✅ **Estatísticas em R**: média, desvio padrão e gráficos.  
✅ **Integração com API pública (Open-Meteo)** para consultar dados climáticos.  
✅ Interface amigável em **Streamlit**, com abas para **dados, exportação e clima**.  

---

## 🛠️ Estrutura do Projeto

📦 farmtech
┣ 📂 python
┃ ┣ app.py # CLI com menu de opções (terminal)
┃ ┣ dados.py # CRUD dos vetores de culturas
┃ ┣ calculos.py # Funções de cálculo (área, insumos, etc.)
┃ ┣ utils.py # Funções utilitárias (salvar CSV)
┃ ┣ dados.csv # Arquivo gerado/exportado com registros
┃
┣ 📂 web
┃ ┣ app_streamlit.py # Interface gráfica em Streamlit
┃
┣ 📂 r
┃ ┣ graficos.R # Script R para gerar estatísticas e gráficos
┃ ┣ 📂 graficos # PNGs exportados pelo R (histograma, boxplot, médias)
┃
┣ 📂 img # Imagens usadas na interface
┣ README.md # Este arquivo
┣ INSTRUCOES.txt # Requisitos da atividade avaliativa
┣ video.txt # Link do vídeo no YouTube

yaml
Copiar código

---

## ▶️ Como Executar

### 1) 📦 Instalar dependências
Certifique-se de ter **Python 3.10+** e **R** instalados.  
No Python, instale os pacotes:

```bash
pip install -r requirements.txt
Pacotes principais: streamlit, pandas, requests

2) 💻 Rodar a versão em terminal (CLI)
bash
Copiar código
cd python
python app.py
Menu interativo disponível:

Inserir dados

Listar dados

Atualizar dados

Deletar dados

Salvar e sair

3) 🌐 Rodar a versão com interface gráfica (Streamlit)
bash
Copiar código
cd web
streamlit run app_streamlit.py
Abas disponíveis:

➕ Inserir dados

📋 Registros (com edição e exclusão)

📈 Visualizar métricas + Exportar CSV + Gráficos em R

☁️ Consultar clima (API Open-Meteo)

4) 📊 Estatísticas em R
Entre na pasta r/ e rode:

bash
Copiar código
Rscript graficos.R
Isso gera gráficos em .png dentro da pasta r/graficos/:

📊 Histograma da área plantada

📦 Boxplot dos insumos

📈 Médias de nutrientes por cultura

5) ☁️ Consultar Clima (API Open-Meteo)
Na aba Clima do Streamlit:

Informe latitude/longitude

Escolha timezone

Clique em Consultar clima

Exibe:

Temperatura atual 🌡️

Vento e direção 💨

Precipitação prevista ☔

📹 Demonstração em Vídeo
O vídeo completo está disponível em:
👉 Link no arquivo video.txt

📑 Resumo Acadêmico
Conforme solicitado na disciplina de Formação Social, o resumo do artigo da Embrapa está incluído na entrega (formato Word/PDF).

🤝 Colaboração
Este projeto foi desenvolvido em equipe, utilizando GitHub para versionamento colaborativo.
Contribuições são bem-vindas!

👨‍💻 Autores
Equipe FarmTech Solutions — FIAP 🌐