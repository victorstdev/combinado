import os
import json
import sys
from datetime import datetime
import google.generativeai as genai

# Configuração da API
chave = os.environ.get("GEMINI_API_KEY")
if not chave:
    print("❌ Erro: Chave GEMINI_API_KEY não encontrada.")
    sys.exit(1)

genai.configure(api_key=chave)

def gerar_puzzle():
    print("🤖 Consultando o Gemini 2.5 Flash...")

    # ATUALIZAÇÃO: Usando o modelo disponível na sua lista
    modelo_nome = 'models/gemini-2.5-flash'
    
    try:
        # Configuração para garantir resposta em JSON
        model = genai.GenerativeModel(
            modelo_nome,
            generation_config={"response_mime_type": "application/json"}
        )
    except Exception as e:
        print(f"Erro ao configurar o modelo {modelo_nome}: {e}")
        sys.exit(1)

    prompt = """
    Crie um jogo estilo 'Connections' (NYT) em Português do Brasil.
    Gere um JSON com 4 grupos de 4 palavras.
    
    Regras:
    1. Temas variados (Cultura BR, Objetos, Gramática, Lugares, etc).
    2. Importante: Crie "red herrings" (palavras que parecem pertencer a um grupo mas são de outro).
    3. Importante: deixe o jogo mais complicado, evitando temas óbvios ou muito simples.
    4. Use palavras comuns, mas evite palavras muito fáceis ou muito difíceis.
    5. Responda APENAS o JSON válido.

    O formato de saída deve ser EXATAMENTE este:
    {
      "grupos": [
        { "tema": "TEMA 1", "palavras": ["Palavra1", "Palavra2", "Palavra3", "Palavra4"] },
        { "tema": "TEMA 2", "palavras": ["Palavra1", "Palavra2", "Palavra3", "Palavra4"] },
        { "tema": "TEMA 3", "palavras": ["Palavra1", "Palavra2", "Palavra3", "Palavra4"] },
        { "tema": "TEMA 4", "palavras": ["Palavra1", "Palavra2", "Palavra3", "Palavra4"] }
      ]
    }
    """

    try:
        response = model.generate_content(prompt)
        
        # Limpeza de segurança (caso o modelo coloque crases de markdown)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        
        dados_jogo = json.loads(texto)
        return dados_jogo

    except Exception as e:
        print(f"❌ Erro ao gerar ou converter o JSON: {e}")
        # Se der erro, mostra o texto cru para entendermos o que houve
        if 'response' in locals():
            print(f"Resposta crua recebida: {response.text}")
        raise e

if __name__ == "__main__":
    try:
        novo_jogo = gerar_puzzle()
        novo_jogo["data"] = datetime.now().strftime("%Y-%m-%d")
        
        with open("puzzle.json", "w", encoding="utf-8") as f:
            json.dump(novo_jogo, f, ensure_ascii=False, indent=2)
            
        print("✅ Sucesso! Arquivo 'puzzle.json' gerado com Gemini 2.5.")
        
    except Exception as e:
        print(f"❌ ERRO FATAL: {e}")
        sys.exit(1)