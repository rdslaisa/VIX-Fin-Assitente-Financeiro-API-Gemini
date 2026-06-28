#!/usr/bin/env python3
"""
Script de teste - VIX Fin API
Testa os principais endpoints da API
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def print_header(texto):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {texto}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(texto):
    print(f"{Colors.GREEN}✅ {texto}{Colors.END}")

def print_error(texto):
    print(f"{Colors.RED}❌ {texto}{Colors.END}")

def print_info(texto):
    print(f"{Colors.YELLOW}ℹ️  {texto}{Colors.END}")

def test_health():
    """Testa health check"""
    print_header("1. TESTE: Health Check")
    try:
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code == 200:
            data = response.json()
            print_success(f"API está online - Status: {data['status']}")
            print(f"   Timestamp: {data['timestamp']}")
        else:
            print_error(f"Erro: Status {response.status_code}")
    except Exception as e:
        print_error(f"Não foi possível conectar: {e}")

def test_educacao():
    """Testa endpoints de educação"""
    print_header("2. TESTE: Educação - Conceitos")
    try:
        response = requests.get(f'{BASE_URL}/educacao/conceitos')
        if response.status_code == 200:
            data = response.json()
            print_success(f"Carregados {len(data['conceitos'])} conceitos")
            for i, conceito in enumerate(data['conceitos'][:2], 1):
                print(f"\n   {i}. {conceito['titulo']}")
                print(f"      {conceito['descricao'][:60]}...")
        else:
            print_error(f"Erro: Status {response.status_code}")
    except Exception as e:
        print_error(f"Erro ao buscar educação: {e}")

def test_tipos_investimento():
    """Testa tipos de investimento"""
    print_header("3. TESTE: Educação - Tipos de Investimento")
    try:
        response = requests.get(f'{BASE_URL}/educacao/tipos')
        if response.status_code == 200:
            data = response.json()
            print_success(f"Carregados {len(data['tipos'])} tipos de investimento")
            for tipo in data['tipos'][:2]:
                print(f"\n   💡 {tipo['nome']}")
                print(f"      Risco: {tipo['risco']} | Rentabilidade: {tipo['rentabilidade']}")
        else:
            print_error(f"Erro: Status {response.status_code}")
    except Exception as e:
        print_error(f"Erro ao buscar tipos: {e}")

def test_cotacao():
    """Testa busca de cotação"""
    print_header("4. TESTE: Cotações - Buscar Ticker")
    ticker = 'PETR4.SA'
    print_info(f"Buscando cotação de {ticker}...")
    try:
        response = requests.get(f'{BASE_URL}/cotacoes/{ticker}')
        if response.status_code == 200:
            data = response.json()
            if 'erro' in data:
                print_error(data['erro'])
            else:
                print_success(f"Cotação de {data['ticker']} obtida")
                print(f"   Preço: R$ {data['preco']}")
                print(f"   Variação: {data['variacao']}%")
                print(f"   Abertura: R$ {data['abertura']}")
                print(f"   Máxima: R$ {data['maxima']}")
                print(f"   Mínima: R$ {data['minima']}")
        else:
            print_error(f"Erro: Status {response.status_code}")
    except Exception as e:
        print_error(f"Erro ao buscar cotação: {e}")

def test_simulador():
    """Testa simulador"""
    print_header("5. TESTE: Simulador - Simular Investimento")
    payload = {
        'valor_inicial': 1000,
        'aporte_mensal': 200,
        'taxa_anual': 10,
        'anos': 5
    }
    print_info(f"Simulando investimento com: {json.dumps(payload)}")
    try:
        response = requests.post(f'{BASE_URL}/simulador/simular', json=payload)
        if response.status_code == 200:
            data = response.json()['simulacao']
            print_success("Simulação realizada com sucesso!")
            print(f"   Total Investido: R$ {data['total_investido']:.2f}")
            print(f"   Valor Final: R$ {data['valor_final']:.2f}")
            print(f"   Ganho: R$ {data['ganho']:.2f}")
            print(f"   Rentabilidade: {data['rentabilidade_percentual']:.2f}%")
        else:
            print_error(f"Erro: Status {response.status_code}")
    except Exception as e:
        print_error(f"Erro na simulação: {e}")

def test_recomendacoes():
    """Testa recomendações personalizadas"""
    print_header("6. TESTE: Recomendações Personalizadas")
    payload = {
        'renda': 5000,
        'objetivo': 'acumular',
        'horizonte_tempo': 10,
        'aversao_risco': 'moderada'
    }
    print_info(f"Gerando recomendações para: {json.dumps(payload)}")
    try:
        response = requests.post(f'{BASE_URL}/recomendacoes', json=payload)
        if response.status_code == 200:
            data = response.json()['recomendacao']
            print_success("Recomendação gerada com sucesso!")
            print(f"   Perfil: {data['perfil']['aversao_risco']}")
            print(f"   Objetivo: {data['perfil']['objetivo']}")
            aporte = data['aporte_recomendado']
            print(f"   Aporte Recomendado: R$ {aporte['ideal']:.2f}/mês")
            print(f"   Alocação Sugerida:")
            for chave, valor in data['alocacao_sugerida'].items():
                print(f"      - {chave}: {valor}%")
        else:
            print_error(f"Erro: Status {response.status_code}")
    except Exception as e:
        print_error(f"Erro na recomendação: {e}")

def main():
    """Executa todos os testes"""
    print(f"\n{Colors.BLUE}{'#'*60}")
    print("# VIX FIN - TESTE DE API")
    print(f"# {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'#'*60}{Colors.END}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info("Certifique-se de que o servidor está rodando em localhost:5000")
    
    # Executar testes
    test_health()
    test_educacao()
    test_tipos_investimento()
    test_cotacao()
    test_simulador()
    test_recomendacoes()
    
    print(f"\n{Colors.BLUE}{'#'*60}")
    print("# TESTES CONCLUÍDOS")
    print(f"{'#'*60}{Colors.END}\n")

if __name__ == '__main__':
    main()
