import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# 1. Inicializace prostředí
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_crypto_price(symbol):
    """
    Externí nástroj: Zavolá Binance API a vrátí cenu kryptoměny.
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return f"Aktuální cena {data['symbol']} je {data['price']} USDT."
    except Exception as e:
        return f"Chyba při získávání ceny pro {symbol}: {str(e)}"

def run_crypto_agent(user_prompt):
    """
    Hlavní logika agenta: Rozhodování o použití nástroje a zpracování odpovědi.
    """
    # Definice nástrojů (Tools) pro OpenAI
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_crypto_price",
                "description": "Získá aktuální cenu kryptoměny v USDT z burzy Binance. Parametr symbol musí končit na USDT (např. BTCUSDT).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Symbol kryptoměny, např. BTCUSDT nebo ETHUSDT",
                        }
                    },
                    "required": ["symbol"],
                },
            },
        }
    ]

    messages = [{"role": "user", "content": user_prompt}]

    # První volání modelu
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Pokud model vyžaduje nástroj
    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            function_args = json.loads(tool_call.function.arguments)
            print(f"--- Volám nástroj pro: {function_args.get('symbol')} ---")
            
            # Spuštění Python funkce
            function_response = get_crypto_price(symbol=function_args.get("symbol"))

            # Odeslání výsledku zpět modelu
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "get_crypto_price",
                "content": function_response,
            })

        # Druhé volání modelu pro finální odpověď
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return final_response.choices[0].message.content
    
    return response_message.content

if __name__ == "__main__":
    # Ukázka spuštění
    print("Vítejte v Crypto Agentovi!")
    query = input("Na jakou kryptoměnu se chcete zeptat? ")
    answer = run_crypto_agent(query)
    print("\nOdpověď AI:")
    print(answer)