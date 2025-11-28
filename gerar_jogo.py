import os
import json
from datetime import datetime
from openai import OpenAI

# Configuração da API com a chave do GitHub
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def gerar_puzzle():
    print("🤖 Consultando a IA para criar o desafio de hoje...")

    prompt = """
    Crie um jogo estilo 'Connections' (NYT) ou 'Combinado' (G1) em Português do Brasil.
    
    REGRAS:
    1. Gere 4 grupos de 4 palavras cada.
    2. Os temas devem ser variados (Cultura Pop Brasileira, Comida, Gramática, Geografia, Expressões).
    3. Tente criar "Red Herrings" (palavras que parecem pertencer a um grupo mas são de outro). 
       Exemplo: Se um grupo é "Frutas" (Manga) e outro é "Partes da Camisa" (Manga), isso é bom.
    4. Não use explicações, apenas retorne o JSON cru.
    
    O formato de saída deve ser estritamente este JSON:
    {
      "grupos": [
        { "tema": "NOME DO TEMA 1", "palavras": ["P1", "P2", "P3", "P4"] },
        { "tema": "NOME DO TEMA 2", "palavras": ["P1", "P2", "P3", "P4"] },
        ...
      ]
    }
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "Você é um gerador de jogos de palavras inteligente e criativo focado em cultura brasileira."},
            {"role": "user", "content": prompt}
        ]
    )

    # Pegando o conteúdo da resposta
    conteudo = response.choices[0].message.content
    dados_jogo = json.loads(conteudo)

    # Adicionando a data de hoje para controle
    dados_jogo["data"] = datetime.now().strftime("%Y-%m-%d")

    return dados_jogo

# Execução e Salvamento
if __name__ == "__main__":
    try:
        novo_jogo = gerar_puzzle()
        
        # Salva o arquivo que o site vai ler
        with open("puzzle.json", "w", encoding="utf-8") as f:
            json.dump(novo_jogo, f, ensure_ascii=False, indent=2)
            
        print("✅ Sucesso! Arquivo 'puzzle.json' atualizado.")
        print(json.dumps(novo_jogo, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ Erro ao gerar jogo: {e}")