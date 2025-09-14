# r/graficos.R
# ---------------------------------------------------
# Gera visualizações dos dados de culturas (cana x café)

# Instalar pacotes se necessário
if (!require(ggplot2)) install.packages("ggplot2", repos = "https://cloud.r-project.org")
if (!require(dplyr))  install.packages("dplyr",  repos = "https://cloud.r-project.org")
if (!require(tidyr))  install.packages("tidyr",  repos = "https://cloud.r-project.org")

library(ggplot2)
library(dplyr)
library(tidyr)

# ---- Leitura (robusta a encoding) ----
ok <- TRUE
tryCatch({
  df <- read.csv("../python/dados.csv", stringsAsFactors = FALSE, fileEncoding = "UTF-8")
}, error = function(e) ok <<- FALSE)

if (!ok) {
  df <- read.csv("../python/dados.csv", stringsAsFactors = FALSE, fileEncoding = "Latin1")
}

# Se cultura vier vazia por encoding, evita NA na legenda
if (!"cultura" %in% names(df)) stop("Coluna 'cultura' não encontrada no CSV.")
df$cultura[is.na(df$cultura) | df$cultura == ""] <- "Desconhecida"

# ---- Garantir colunas numéricas ----
num_cols <- intersect(c("area","N","P","K"), names(df))
for (c in num_cols) df[[c]] <- suppressWarnings(as.numeric(df[[c]]))

# ---- Pasta de saída ----
if (!dir.exists("graficos")) dir.create("graficos")

# ---- Tema base com fonte que suporta acentos ----
base_theme <- theme_minimal(base_size = 14, base_family = "Arial")

# ================================
# 1) Área por cultura: média ± desvio
#    (substitui o histograma_area.png)
# ================================
df_area_stats <- df %>%
  group_by(cultura) %>%
  summarise(
    n      = sum(!is.na(area)),
    media  = mean(area, na.rm = TRUE),
    desvio = sd(area,   na.rm = TRUE),
    .groups = "drop"
  )

# Se houver só 1 ponto em alguma cultura, sd = NA -> usa 0 para não quebrar as barras de erro
df_area_stats$desvio[is.na(df_area_stats$desvio)] <- 0

p1 <- ggplot(df_area_stats, aes(x = cultura, y = media, fill = cultura)) +
  geom_col(width = 0.6, alpha = 0.85) +
  geom_errorbar(aes(ymin = pmax(media - desvio, 0), ymax = media + desvio),
                width = 0.15, linewidth = 0.9) +
  geom_text(aes(label = paste0("n=", n)),
            vjust = -1.2, size = 4) +
  base_theme +
  labs(
    title = "Área Plantada por Cultura — Média ± Desvio-padrão",
    x = "Cultura",
    y = "Área (m²)",
    fill = "Cultura",
    subtitle = "Barras: média | Hastes: ±1 desvio-padrão"
  ) +
  scale_fill_brewer(palette = "Set2") +
  ylim(0, max(df_area_stats$media + df_area_stats$desvio, na.rm = TRUE) * 1.15)

ggsave("graficos/desvio.png", p1, width = 8, height = 5, dpi = 150, bg = "white")

# ================================
# 2) Boxplot dos Insumos (N, P, K)
#    (com fallback para poucos pontos)
# ================================
df_long <- df %>%
  select(cultura, N, P, K) %>%
  pivot_longer(cols = c("N","P","K"), names_to = "Nutriente", values_to = "Valor")

# Verifica se cada grupo tem >= 2 pontos para boxplot
grp_counts <- df_long %>%
  group_by(cultura, Nutriente) %>%
  summarise(n = sum(!is.na(Valor)), .groups = "drop")

tem_poucos <- any(grp_counts$n < 2)

if (tem_poucos) {
  # Usa pontos com média quando há poucos dados
  p2 <- ggplot(df_long, aes(x = Nutriente, y = Valor, color = cultura)) +
    geom_jitter(width = 0.1, height = 0, size = 2, alpha = 0.8, na.rm = TRUE) +
    stat_summary(fun = mean, geom = "point", shape = 18, size = 3, position = position_dodge(width = 0.5)) +
    base_theme +
    labs(
      title = "Insumos por Cultura (pontos e médias)",
      x = "Nutriente",
      y = "Quantidade (g)",
      color = "Cultura"
    ) +
    scale_color_brewer(palette = "Set1")
} else {
  p2 <- ggplot(df_long, aes(x = Nutriente, y = Valor, fill = cultura)) +
    geom_boxplot(alpha = 0.7, na.rm = TRUE) +
    base_theme +
    labs(
      title = "Distribuição dos Insumos por Cultura",
      x = "Nutriente",
      y = "Quantidade (g)",
      fill = "Cultura"
    ) +
    scale_fill_brewer(palette = "Pastel1")
}

ggsave("graficos/boxplot_insumos.png", p2, width = 8, height = 5, dpi = 150, bg = "white")

# ================================
# 3) Médias Comparativas (N, P, K)
# ================================
df_mean <- df_long %>%
  group_by(cultura, Nutriente) %>%
  summarise(Media = mean(Valor, na.rm = TRUE), .groups = "drop")

p3 <- ggplot(df_mean, aes(x = Nutriente, y = Media, fill = cultura)) +
  geom_col(position = "dodge", na.rm = TRUE) +
  base_theme +
  labs(
    title = "Média dos Nutrientes por Cultura",
    x = "Nutriente",
    y = "Média (g)",
    fill = "Cultura"
  ) +
  scale_fill_brewer(palette = "Set1")

ggsave("graficos/medias_insumos.png", p3, width = 8, height = 5, dpi = 150, bg = "white")

cat("\n✅ Gráficos gerados em: r/graficos/\n")
