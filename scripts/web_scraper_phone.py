import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Solo móviles españoles válidos: 9 dígitos, empieza por 6 o 7
MOVIL_REGEX = re.compile(r"(6\d{8}|7\d{8})")

AGREGADORES = [
    "tripadvisor.", "booking.", "trivago.", "groupon.", "minube.", "thefork.",
    "elle.com", "verybilbao", "barcelona-life", "viator.", "expedia."
]

# Cargar datos
df = pd.read_csv("../resultados.csv")

# Preparamos la salida
resultados = []

def limpiar_texto(texto):
    return texto.replace("\xa0", " ").replace("\u200b", "").strip()

def extraer_telefono(html):
    soup = BeautifulSoup(html, "html.parser")

    # Buscar en enlaces tel:
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("tel:"):
            telefono = href.replace("tel:", "").replace(" ", "").replace("-", "")
            telefono = limpiar_texto(telefono)
            if MOVIL_REGEX.match(telefono):
                return telefono

    # Buscar en texto general
    texto = limpiar_texto(soup.get_text(separator=" "))
    matches = MOVIL_REGEX.findall(texto)
    if matches:
        return matches[0]

    # Buscar en el footer si no encontró nada
    footer = soup.find("footer")
    if footer:
        footer_text = limpiar_texto(footer.get_text(separator=" "))
        matches_footer = MOVIL_REGEX.findall(footer_text)
        if matches_footer:
            return matches_footer[0]

    return None

def es_agregador(url):
    return any(ag in url for ag in AGREGADORES)

def buscar_telefono_en_web(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            return extraer_telefono(response.text)
    except Exception as e:
        print(f"❌ Error en {url}: {e}")
    return None

# Procesar URLs
for index, row in df.iterrows():
    url = row["url"]
    if es_agregador(url):
        print(f"⛔️ Agregador detectado, ignorando: {url}")
        continue

    print(f"🌐 Visitando: {url}")
    telefono_encontrado = buscar_telefono_en_web(url)
    if telefono_encontrado:
        print(f"✅ Móvil encontrado: {telefono_encontrado}")
    else:
        print("⚠️ No se encontró móvil.")

    resultados.append({
        "categoria": row["categoria"],
        "nombre": row["nombre"],
        "direccion": row["direccion"],
        "telefono": telefono_encontrado if telefono_encontrado else "",
        "url": url
    })

# Guardar resultados
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv("../resultados_con_telefonos.csv", index=False)
print("✅ Proceso completado. Teléfonos añadidos en: ../resultados_con_telefonos.csv")
