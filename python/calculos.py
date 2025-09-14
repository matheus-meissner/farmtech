import math

# --- Cana-de-açúcar (retângulo) ---
def calcular_cana(comprimento, largura, espacamento=1.5):
    area = comprimento * largura
    num_ruas = int(largura // espacamento)
    sulco_total = num_ruas * comprimento

    # Insumos médios (g/m²)
    N = 5 * area
    P = 10 * area
    K = 13 * area

    return {
        "area": area,
        "ruas": num_ruas,
        "sulco_total": sulco_total,
        "N": N,
        "P": P,
        "K": K
    }

# --- Café (círculo) ---
def calcular_cafe(raio, espac_rua=3.8, espac_planta=0.7):
    area = math.pi * (raio ** 2)
    
    # Aproximação por área / (espaçamento rua * planta)
    num_plantas = int(area / (espac_rua * espac_planta))

    # Insumos médios (g/m²)
    N = 16 * area
    P = 9 * area
    K = 6 * area

    return {
        "area": area,
        "plantas": num_plantas,
        "N": N,
        "P": P,
        "K": K
    }
