# AI Crypto Agent (OpenAI Tool Calling)
Tento projekt demonstruje jednoduchého AI Agenta, který využívá **Function Calling** od OpenAI k získávání reálných dat z krypto burzy Binance.

## Funkce
- Přijímá dotazy v přirozeném jazyce týkající se ceny kryptoměn (např. "Kolik stojí Bitcoin?" nebo "Jaká je cena Etherea a Litecoinu?").
- Automaticky rozpozná symbol kryptoměny a zavolá veřejné API burzy Binance.
- Formátuje odpověď zpět uživateli.

## Instalace a spuštění
1. Nainstalujte závislosti: `pip install -r requirements.txt`
2. Vytvořte soubor `.env` a vložte svůj `OPENAI_API_KEY`.
3. Spusťte skript: `python crypto_agent.py`
