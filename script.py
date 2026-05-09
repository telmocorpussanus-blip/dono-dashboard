import feedparser, json, datetime
from urllib.parse import quote

# AQUI ESTÃO AS TUAS 7 TESES. Podes mudar as palavras depois.
EMPRESAS = {
  "MSFT": {"nome": "Microsoft", "tese": "Alugo o escritório digital ao mundo", "manter": ["azure","copilot","365"], "vender": ["commodity","separar","margem"]},
  "AMZN": {"nome": "Amazon", "tese": "Cobro portagem e alugo a internet", "manter": ["aws","backlog","entrega"], "vender": ["perder quota","temu","capex"]},
  "NVDA": {"nome": "NVIDIA", "tese": "Vendo a única pá das minas de IA", "manter": ["cuda","blackwell"], "vender": ["chips próprios","china"]},
  "D4S": {"nome": "Daiichi", "tese": "Faço mísseis contra cancro", "manter": ["enhertu","fabrico"], "vender": ["parceiros","falhar","perdas"]},
  "NVO": {"nome": "Novo Nordisk", "tese": "Tiro a fome com hormona", "manter": ["wegovy","produção"], "vender": ["corte preços","lilly"]},
  "SLM": {"nome": "Sallie Mae", "tese": "Empresto a jovens", "manter": ["defaults","buyback"], "vender": ["perdão","governo"]},
  "O": {"nome": "Realty Income", "tese": "Compro lojas, distribuo renda", "manter": ["ocupação","affo"], "vender": ["inquilinos","dividendo"]}
}

def analisar(ticker, titulo):
    t = titulo.lower()
    e = EMPRESAS[ticker]
    if any(p in t for p in e["vender"]): return f"🔴 {titulo[:70]}"
    if any(p in t for p in e["manter"]): return f"✓ {titulo[:70]}"
    return f"• {titulo[:70]}"

resultado = {"data": datetime.datetime.now().isoformat(), "empresas": []}

for ticker, dados in EMPRESAS.items():
    query = quote(f"{dados['nome']} stock")
    feed = feedparser.parse(f"https://news.google.com/rss/search?q={query}&hl=en&gl=US&ceid=US:en")
    sinais = [analisar(ticker, e.title) for e in feed.entries[:3]]

    status = "verde"
    if any("🔴" in s for s in sinais): status = "vermelho"
    elif ticker in ["NVDA", "D4S"]: status = "amarelo"

    resultado["empresas"].append({
        "ticker": ticker, "nome": dados["nome"], "tese": dados["tese"],
        "status": status, "sinais": sinais
    })

with open("dados.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)
