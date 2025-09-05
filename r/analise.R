# r/analise.R
# -----------------------------
# Lê ../python/dados.csv, calcula estatísticas
# (médias e desvios) e imprime no terminal.
# Também salva um resumo em r/estatisticas_resumo.csv

# ---- Funções auxiliares ----
safe_mean <- function(x) mean(x, na.rm = TRUE)
safe_sd   <- function(x) sd(x, na.rm = TRUE)

to_numeric <- function(v) suppressWarnings(as.numeric(v))

# ---- Localização do arquivo ----
candidatos <- c("../python/dados.csv", "./dados.csv", "./python/dados.csv")
arquivo <- candidatos[file.exists(candidatos)][1]
if (is.na(arquivo)) {
  stop("dados.csv não encontrado. Gere pelo app Python e rode novamente.")
}

# ---- Leitura ----
df <- read.csv(arquivo, sep = ",", dec = ".", stringsAsFactors = FALSE, check.names = FALSE)

# Espera-se que o CSV tenha colunas como:
# cultura, area, ruas, sulco_total, plantas, N, P, K
# Converter o que for numérico
cols_num <- intersect(c("area","ruas","sulco_total","plantas","N","P","K"), names(df))
for (c in cols_num) df[[c]] <- to_numeric(df[[c]])

# ---- Estatísticas gerais ----
cat("\n================= ESTATÍSTICAS GERAIS =================\n")
cat("Registros:", nrow(df), "\n")

if ("area" %in% names(df)) {
  cat(sprintf("Área (m²): média = %.2f | desvio = %.2f\n", safe_mean(df$area), safe_sd(df$area)))
}

if (all(c("N","P","K") %in% names(df))) {
  cat(sprintf("N (g): média = %.2f | desvio = %.2f\n", safe_mean(df$N), safe_sd(df$N)))
  cat(sprintf("P (g): média = %.2f | desvio = %.2f\n", safe_mean(df$P), safe_sd(df$P)))
  cat(sprintf("K (g): média = %.2f | desvio = %.2f\n", safe_mean(df$K), safe_sd(df$K)))
}

# ---- Estatísticas por cultura ----
if ("cultura" %in% names(df)) {
  cat("\n================ POR CULTURA ================\n")
  culturas <- unique(df$cultura)
  resumo_list <- list()

  for (cult in culturas) {
    sub <- df[df$cultura == cult, , drop = FALSE]
    if (nrow(sub) == 0) next

    linha <- list(
      cultura = cult,
      n = nrow(sub),
      area_media = if ("area" %in% names(sub)) safe_mean(sub$area) else NA_real_,
      area_desvio = if ("area" %in% names(sub)) safe_sd(sub$area) else NA_real_,
      N_media = if ("N" %in% names(sub)) safe_mean(sub$N) else NA_real_,
      N_desvio = if ("N" %in% names(sub)) safe_sd(sub$N) else NA_real_,
      P_media = if ("P" %in% names(sub)) safe_mean(sub$P) else NA_real_,
      P_desvio = if ("P" %in% names(sub)) safe_sd(sub$P) else NA_real_,
      K_media = if ("K" %in% names(sub)) safe_mean(sub$K) else NA_real_,
      K_desvio = if ("K" %in% names(sub)) safe_sd(sub$K) else NA_real_
    )
    resumo_list[[length(resumo_list) + 1]] <- linha

    cat(sprintf("\n> %s (n = %d)\n", cult, nrow(sub)))
    if ("area" %in% names(sub)) {
      cat(sprintf("Área (m²): média = %.2f | desvio = %.2f\n", linha$area_media, linha$area_desvio))
    }
    if ("N" %in% names(sub)) {
      cat(sprintf("N (g): média = %.2f | desvio = %.2f\n", linha$N_media, linha$N_desvio))
    }
    if ("P" %in% names(sub)) {
      cat(sprintf("P (g): média = %.2f | desvio = %.2f\n", linha$P_media, linha$P_desvio))
    }
    if ("K" %in% names(sub)) {
      cat(sprintf("K (g): média = %.2f | desvio = %.2f\n", linha$K_media, linha$K_desvio))
    }
  }

  # Exportar resumo por cultura
  if (length(resumo_list) > 0) {
    resumo_df <- do.call(rbind.data.frame, resumo_list)
    # Garantir nomes simples
    names(resumo_df) <- c("cultura","n",
                          "area_media","area_desvio",
                          "N_media","N_desvio",
                          "P_media","P_desvio",
                          "K_media","K_desvio")
    write.csv(resumo_df, file = "estatisticas_resumo.csv", row.names = FALSE)
    cat("\nArquivo gerado: r/est
