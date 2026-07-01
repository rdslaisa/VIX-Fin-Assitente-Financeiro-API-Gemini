"""
Assistente Virtual para Investimentos - Backend
Sistema educacional de investimentos com análise de mercado e simulador
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json

from educacao import get_conceitos, get_tipos_investimento
from cotacoes import get_cotacao_acao, get_historico_preco, get_cotacao_moedas
from simulador import simular_investimento, calcular_rentabilidade
from recomendacoes import get_recomendacao_personalizada
from gemini_atena_chat import get_resposta_chat

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
CORS(app)

# Rotas de Educação
@app.route('/api/educacao/conceitos', methods=['GET'])
def conceitos():
    """Retorna conceitos básicos de investimento"""
    return jsonify(get_conceitos())

@app.route('/api/educacao/tipos', methods=['GET'])
def tipos_investimento():
    """Retorna tipos de investimento disponíveis"""
    return jsonify(get_tipos_investimento())

# Rotas de Cotações
@app.route('/api/cotacoes/<ticker>', methods=['GET'])
def cotacao(ticker):
    """Obtém cotação atual de um ativo, sempre em tempo real (sem cache)"""
    try:
        dados = get_cotacao_acao(ticker.upper())
        if 'erro' in dados:
            return jsonify(dados), 404
        return jsonify(dados)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/historico/<ticker>', methods=['GET'])
def historico(ticker):
    """Obtém histórico de preços de um ativo"""
    try:
        periodo = request.args.get('periodo', '1y')
        dados = get_historico_preco(ticker.upper(), periodo)
        return jsonify(dados)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/moedas', methods=['GET'])
def moedas():
    """Obtém cotações de moedas e cripto em tempo real (sem cache)"""
    try:
        dados = get_cotacao_moedas()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'erro': f'Falha ao obter cotações de moedas: {str(e)}'}), 502

# Rotas de Simulador
@app.route('/api/simulador/simular', methods=['POST'])
def simular():
    """Simula um investimento"""
    data = request.get_json(silent=True) or {}
    try:
        resultado = simular_investimento(
            valor_inicial=float(data['valor_inicial']),
            aporte_mensal=float(data.get('aporte_mensal', 0)),
            taxa_anual=float(data['taxa_anual']),
            anos=int(data['anos']),
            ativo=data.get('ativo', 'PETR4.SA')
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# Rotas de Recomendações
@app.route('/api/recomendacoes', methods=['POST'])
def recomendacoes():
    """Gera recomendações personalizadas"""
    perfil = request.get_json(silent=True) or {}
    try:
        recomendacao = get_recomendacao_personalizada(
            renda=float(perfil.get('renda', 0)),
            objetivo=perfil.get('objetivo', 'acumular'),
            horizonte_tempo=int(perfil.get('horizonte_tempo', 5)),
            aversao_risco=perfil.get('aversao_risco', 'moderado')
        )
        return jsonify(recomendacao)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# Rota de Chat com IA (Gemini)
@app.route('/api/chat', methods=['POST'])
def chat():
    """Recebe mensagem do usuário e retorna resposta do assistente (Gemini)."""
    data = request.get_json(silent=True) or {}
    mensagem = data.get('mensagem', '')
    historico = data.get('historico', [])

    if not mensagem.strip():
        return jsonify({'erro': 'Envie uma mensagem.'}), 400

    resultado = get_resposta_chat(mensagem, historico)
    if 'erro' in resultado:
        return jsonify(resultado), 502
    return jsonify(resultado), 200

# Rota inicial
@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    """Verifica saúde da API"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Modo desenvolvimento
    app.run(debug=True, host='0.0.0.0', port=5000)
