"""
Módulo de Chat com IA (Gemini)
Integração com a API do Google Gemini para tirar dúvidas sobre investimentos.

"""
import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para os.environ
load_dotenv()

# GEMINI_API_KEY= chave de acesso para a API GEMINI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Modelo gratuito mais atual (verifique aistudio.google.com se mudar)
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Instrução de sistema: mantém o assistente focado e dentro do escopo educacional
SYSTEM_PROMPT = (
    "Você é a Atena, assistente virtual do VIX Fin, uma plataforma educacional de investimentos. "
    "Você é uma assistente feminina e deve se referir a si mesma no feminino. "
    "Responda em português do Brasil, de forma clara, simples e didática, focada em educação "
    "financeira para iniciantes. "
    "Você pode explicar qualquer conceito, ativo, estratégia ou cenário de investimento de forma "
    "completa e informativa, mas NUNCA incentive, sugira ou recomende a compra ou venda de qualquer "
    "ativo específico. Explique o que é, como funciona e quais são os riscos, mas deixe sempre "
    "claro que a decisão é do usuário e que recomendações reais devem ser feitas por um profissional "
    "certificado (CVM/ANBIMA). "
    "Seja concisa: respostas curtas e diretas, de no máximo 15 frases, a menos que o usuário "
    "peça mais detalhes."
)


def get_resposta_chat(mensagem, historico=None):
    """
    Envia a mensagem do usuário para o Gemini e retorna a resposta em texto.

    historico: lista opcional de mensagens anteriores no formato
               [{"role": "user"|"model", "text": "..."}], para manter contexto.
    """
    if not GEMINI_API_KEY:
        return {
            "erro": "GEMINI_API_KEY não configurada no servidor. "
                    "Defina a variável de ambiente antes de rodar o app.py."
        }

    if not mensagem or not mensagem.strip():
        return {"erro": "Mensagem vazia."}

    contents = []

    # Reconstrói o histórico da conversa, se houver
    if historico:
        for item in historico[-10:]:  # limita contexto às últimas 10 trocas
            role = "model" if item.get("role") == "model" else "user"
            contents.append({
                "role": role,
                "parts": [{"text": item.get("text", "")}]
            })

    contents.append({
        "role": "user",
        "parts": [{"text": mensagem.strip()}]
    })

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 400
        }
    }

    try:
        resposta = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=20,
            headers={"Content-Type": "application/json"}
        )
        resposta.raise_for_status()
        dados = resposta.json()

        candidatos = dados.get("candidates", [])
        if not candidatos:
            return {"erro": "O modelo não retornou nenhuma resposta."}

        partes = candidatos[0].get("content", {}).get("parts", [])
        texto = "".join(p.get("text", "") for p in partes).strip()

        if not texto:
            return {"erro": "Resposta vazia do modelo."}

        return {"resposta": texto}

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status == 429:
            return {"erro": "Limite de uso gratuito do Gemini atingido. Tente novamente em alguns instantes."}
        if status in (401, 403):
            return {"erro": "API key do Gemini inválida ou sem permissão."}
        return {"erro": f"Erro na API do Gemini: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"erro": f"Falha de conexão com o Gemini: {str(e)}"}
    except Exception as e:
        return {"erro": f"Erro inesperado: {str(e)}"}