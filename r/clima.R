# r/clima.R
# ----------------------------------------
# Exemplo simples "Ir além": consulta Open-Meteo
# e imprime no terminal informações meteorológicas.

# Pacotes necessários
if (!require(httr)) install.packages("httr", repos = "https://cloud.r-project.org")
if (!require(jsonlite)) install.packages("jsonlite", repos = "https://cloud.r-project.org")

library(httr)
library(jsonlite)

# Parâmetros (Ajuste para sua cidade)
lat <- -23.55     # São Paulo
lon <- -46.63
tz  <- "America/Sao_Paulo"

url <- paste0(
  "https://api.open-meteo.com/v1/forecast?",
  "latitude=", lat,
  "&longitude=", lon,
  "&current_weather=true",
  "&hourly=temperature_2m,precipitation",
  "&timezone=", tz
)

cat("\nConsultando Open-Meteo...\n")
resp <- GET(url)
stop_for_status(resp)

json <- content(resp, as = "text", encoding = "UTF-8")
data <- fromJSON(json)

# ---- Tempo atual ----
if (!is.null(data$current_weather)) {
  cw <- data$current_weather
  cat("\n===== TEMPO ATUAL =====\n")
  cat(sprintf("Temperatura: %.1f °C\n", cw$temperature))
  cat(sprintf("Vento: %.1f km/h (dir: %d°)\n", cw$windspeed, cw$winddirection))
  cat(sprintf("Hora (local): %s\n", cw$time))
} else {
  cat("\n(Não foi possível ler current_weather)\n")
}

# ---- Resumo de precipitação nas próximas horas ----
if (!is.null(data$hourly)) {
  hrs <- data$hourly
  # Próximas 12 horas (se disponível)
  n <- min(12, length(hrs$time))
  prec <- hrs$precipitation[seq_len(n)]
  tms  <- hrs$time[seq_len(n)]
  total_prec <- sum(prec, na.rm = TRUE)
  cat("\n===== PRÓXIMAS HORAS (12h) =====\n")
  cat(sprintf("Precipitação acumulada: %.1f mm\n", total_prec))
  # Mostra primeiras 5 linhas de exemplo
  cat("\nHora\t\tPrecip(mm)\n")
  head_n <- min(5, n)
  for (i in seq_len(head_n)) {
    cat(sprintf("%s\t%.2f\n", tms[i], prec[i]))
  }
} else {
