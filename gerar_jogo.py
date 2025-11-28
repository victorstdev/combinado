import os
import json
import sys
from datetime import datetime
import google.generativeai as genai

# Configuração da API do Google
chave = os.environ.get("GEMINI_API_KEY")
if not chave:
    print("❌ Erro: Chave GEMINI_API_KEY não encontrada.")
    sys.exit(1)

genai.configure(api_key=chave)

def gerar_puzzle():
    print("🤖 Consultando o Gemini para criar o desafio...")

    # Configuração do modelo para forçar resposta JSON
    model = genai.GenerativeModel('gemini-1.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = """
    Crie um jogo estilo 'Connections' (NYT) em Português do Brasil.
    Gere um JSON com 4 grupos de 4 palavras.
    
    Regras:
    1. Temas variados (Cultura BR, Objetos, Gramática, etc).
    2. Use "pegadinhas" (palavras que parecem de outro grupo).
    3. Responda APENAS o JSON, sem markdown.

    O formato deve ser EXATAMENTE este:
    {
      "grupos": [
        { "tema": "NOME DO TEMA", "palavras": ["P1", "P2", "P3", "P4"] },
        ... (total de 4 grupos)
      ]
    }
    """

    try:
        response = model.generate_content(prompt)
        
        # O Gemini já deve retornar JSON puro devido à configuração, 
        # mas garantimos limpando espaços extras
        texto_limpo = response.text.strip()
        
        dados_jogo = json.loads(texto_limpo)
        return dados_jogo

    except Exception as e:
        print(f"Erro na geração ou conversão do JSON: {e}")
        print("Resposta recebida:", response.text if 'response' in locals() else "Nada")
        raise e

if __name__ == "__main__":
    try:
        novo_jogo = gerar_puzzle()
        
        # Adiciona a data
        novo_jogo["data"] = datetime.now().strftime("%Y-%m-%d")
        
        # Salva o arquivo
        with open("puzzle.json", "w", encoding="utf-8") as f:
            json.dump(novo_jogo, f, ensure_ascii=False, indent=2)
            
        print("✅ Sucesso! Arquivo 'puzzle.json' gerado com Gemini.")
        
    except Exception as e:
        print(f"❌ ERRO FATAL: {e}")
        sys.exit(1)