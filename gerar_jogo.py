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
    print("🤖 Consultando o Gemini...")

    # TENTATIVA 1: Usar o modelo Flash específico (mais rápido e barato)
    modelo_nome = 'gemini-1.5-flash-001'
    
    try:
        model = genai.GenerativeModel(
            modelo_nome,
            generation_config={"response_mime_type": "application/json"}
        )
    except:
        # Fallback para o modelo Pro se o Flash falhar na inicialização
        print(f"⚠️ Modelo {modelo_nome} falhou, tentando gemini-1.5-pro-latest...")
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

    prompt = """
    Crie um jogo estilo 'Connections' (NYT) em Português do Brasil.
    Gere um JSON com 4 grupos de 4 palavras.
    
    Regras:
    1. Temas variados (Cultura BR, Objetos, Gramática, etc).
    2. Use "pegadinhas" (palavras que parecem de outro grupo).
    3. Responda APENAS o JSON.

    Formato EXATO:
    {
      "grupos": [
        { "tema": "TEMA 1", "palavras": ["A", "B", "C", "D"] },
        { "tema": "TEMA 2", "palavras": ["E", "F", "G", "H"] },
        { "tema": "TEMA 3", "palavras": ["I", "J", "K", "L"] },
        { "tema": "TEMA 4", "palavras": ["M", "N", "O", "P"] }
      ]
    }
    """

    try:
        response = model.generate_content(prompt)
        
        # Limpeza e conversão do JSON
        texto = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(texto)

    except Exception as e:
        print(f"❌ Erro ao gerar conteúdo: {e}")
        # Se der erro, vamos listar os modelos disponíveis para ajudar no debug
        print("Modelos disponíveis na sua conta:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        raise e

if __name__ == "__main__":
    try:
        novo_jogo = gerar_puzzle()
        novo_jogo["data"] = datetime.now().strftime("%Y-%m-%d")
        
        with open("puzzle.json", "w", encoding="utf-8") as f:
            json.dump(novo_jogo, f, ensure_ascii=False, indent=2)
            
        print("✅ Sucesso! Arquivo gerado.")
        
    except Exception as e:
        print(f"❌ ERRO FATAL: {e}")
        sys.exit(1)