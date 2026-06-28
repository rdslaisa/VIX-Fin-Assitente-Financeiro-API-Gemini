"""
Exemplos de Uso - VIX Fin API
Como usar a API do VIX Fin programaticamente
"""

import requests
import json

# Configurar base URL
BASE_URL = 'http://localhost:5000/api'

# =====================================
# EXEMPLO 1: Buscar Educação
# =====================================

def exemplo_1_educacao():
    """Exemplo: Carregar conceitos de investimento"""
    print("=" * 50)
    print("EXEMPLO 1: Educação - Conceitos")
    print("=" * 50)
    
    response = requests.get(f'{BASE_URL}/educacao/conceitos')
    data = response.json()
    
    print(f"Conceitos carregados: {len(data['conceitos'])}\n")
    
    for conceito in data['conceitos'][:2]:
        print(f"📚 {conceito['titulo']}")
        print(f"   {conceito['descricao']}\n")

# =====================================
# EXEMPLO 2: Buscar Cotação
# =====================================

def exemplo_2_cotacao():
    """Exemplo: Buscar cotação de uma ação"""
    print("=" * 50)
    print("EXEMPLO 2: Cotações - Buscar Ticker")
    print("=" * 50)
    
    ticker = 'PETR4.SA'
    response = requests.get(f'{BASE_URL}/cotacoes/{ticker}')
    data = response.json()
    
    print(f"Ticker: {data['ticker']}")
    print(f"Preço: R$ {data['preco']}")
    print(f"Variação: {data['variacao']}%")
    print(f"Abertura: R$ {data['abertura']}")
    print(f"Máxima: R$ {data['maxima']}")
    print(f"Mínima: R$ {data['minima']}\n")

# =====================================
# EXEMPLO 3: Simular Investimento
# =====================================

def exemplo_3_simulador():
    """Exemplo: Simular um investimento"""
    print("=" * 50)
    print("EXEMPLO 3: Simulador - Simular Investimento")
    print("=" * 50)
    
    # Dados da simulação
    payload = {
        'valor_inicial': 1000,
        'aporte_mensal': 200,
        'taxa_anual': 12,  # 12% ao ano
        'anos': 10
    }
    
    response = requests.post(f'{BASE_URL}/simulador/simular', json=payload)
    data = response.json()['simulacao']
    
    print(f"Investimento Inicial: R$ {data['valor_inicial']:.2f}")
    print(f"Aporte Mensal: R$ {data['aporte_mensal']:.2f}")
    print(f"Taxa Anual: {data['taxa_anual_esperada']}%")
    print(f"Período: {data['horizonte_anos']} anos\n")
    
    print(f"RESULTADOS:")
    print(f"Total Investido: R$ {data['total_investido']:.2f}")
    print(f"Valor Final: R$ {data['valor_final']:.2f}")
    print(f"Ganho Total: R$ {data['ganho']:.2f}")
    print(f"Rentabilidade: {data['rentabilidade_percentual']:.2f}%\n")

# =====================================
# EXEMPLO 4: Comparar Cenários
# =====================================

def exemplo_4_comparacao():
    """Exemplo: Comparar dois cenários de investimento"""
    print("=" * 50)
    print("EXEMPLO 4: Comparar Cenários")
    print("=" * 50)
    
    # Cenário 1: Conservador
    cenario1 = {
        'valor_inicial': 1000,
        'aporte_mensal': 100,
        'taxa_anual': 6,
        'anos': 10
    }
    
    # Cenário 2: Agressivo
    cenario2 = {
        'valor_inicial': 1000,
        'aporte_mensal': 200,
        'taxa_anual': 12,
        'anos': 10
    }
    
    print("CENÁRIO 1 - Conservador (6% a.a., R$ 100/mês)")
    response1 = requests.post(f'{BASE_URL}/simulador/simular', json=cenario1)
    data1 = response1.json()['simulacao']
    print(f"  Valor Final: R$ {data1['valor_final']:.2f}")
    print(f"  Ganho: R$ {data1['ganho']:.2f}\n")
    
    print("CENÁRIO 2 - Agressivo (12% a.a., R$ 200/mês)")
    response2 = requests.post(f'{BASE_URL}/simulador/simular', json=cenario2)
    data2 = response2.json()['simulacao']
    print(f"  Valor Final: R$ {data2['valor_final']:.2f}")
    print(f"  Ganho: R$ {data2['ganho']:.2f}\n")
    
    diferenca = data2['valor_final'] - data1['valor_final']
    print(f"DIFERENÇA: R$ {diferenca:.2f}\n")

# =====================================
# EXEMPLO 5: Obter Recomendações
# =====================================

def exemplo_5_recomendacoes():
    """Exemplo: Obter recomendações personalizadas"""
    print("=" * 50)
    print("EXEMPLO 5: Recomendações Personalizadas")
    print("=" * 50)
    
    # Perfil do usuário
    perfil = {
        'renda': 5000,
        'objetivo': 'acumular',  # acumular, gerar_renda, aposentadoria
        'horizonte_tempo': 10,
        'aversao_risco': 'moderada'  # baixa, moderada, alta
    }
    
    response = requests.post(f'{BASE_URL}/recomendacoes', json=perfil)
    data = response.json()['recomendacao']
    
    print(f"PERFIL DO INVESTIDOR")
    print(f"Renda Mensal: R$ {data['perfil']['renda_mensal']:.2f}")
    print(f"Objetivo: {data['perfil']['objetivo']}")
    print(f"Horizonte: {data['perfil']['horizonte_tempo']} anos")
    print(f"Perfil de Risco: {data['perfil']['aversao_risco']}\n")
    
    aporte = data['aporte_recomendado']
    print(f"APORTE RECOMENDADO")
    print(f"Mínimo: R$ {aporte['minimo']:.2f}")
    print(f"Ideal: R$ {aporte['ideal']:.2f}")
    print(f"Máximo: R$ {aporte['maximo']:.2f}\n")
    
    print(f"ALOCAÇÃO SUGERIDA")
    for chave, valor in data['alocacao_sugerida'].items():
        print(f"  {chave.replace('_', ' ').title()}: {valor}%\n")
    
    print(f"ATIVOS RECOMENDADOS")
    for ativo in data['ativos_sugeridos'][:3]:
        print(f"  - {ativo['nome']}: {ativo['percentual']}%")
        print(f"    ({ativo['razao']})\n")

# =====================================
# EXEMPLO 6: Buscar Histórico
# =====================================

def exemplo_6_historico():
    """Exemplo: Buscar histórico de preços"""
    print("=" * 50)
    print("EXEMPLO 6: Histórico de Preços")
    print("=" * 50)
    
    ticker = 'VALE3.SA'
    response = requests.get(f'{BASE_URL}/historico/{ticker}?periodo=1mo')
    data = response.json()
    
    print(f"Histórico de {ticker} (últimas 10 linhas)\n")
    print("Data       | Preço (R$) | Volume")
    print("-" * 40)
    
    # Mostrar últimas 10 linhas
    for item in data['dados'][-10:]:
        print(f"{item['data']} | {item['preco']:>10} | {item['volume']:>15}")

# =====================================
# EXEMPLO 7: Classe Wrapper
# =====================================

class VIXFinAPI:
    """Classe wrapper para facilitar o uso da API"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def buscar_cotacao(self, ticker):
        """Buscar cotação de um ativo"""
        response = requests.get(f'{self.base_url}/cotacoes/{ticker}')
        return response.json()
    
    def simular(self, valor_inicial, aporte_mensal, taxa_anual, anos):
        """Simular um investimento"""
        payload = {
            'valor_inicial': valor_inicial,
            'aporte_mensal': aporte_mensal,
            'taxa_anual': taxa_anual,
            'anos': anos
        }
        response = requests.post(f'{self.base_url}/simulador/simular', json=payload)
        return response.json()['simulacao']
    
    def recomendar(self, renda, objetivo, horizonte_tempo, aversao_risco):
        """Obter recomendações"""
        payload = {
            'renda': renda,
            'objetivo': objetivo,
            'horizonte_tempo': horizonte_tempo,
            'aversao_risco': aversao_risco
        }
        response = requests.post(f'{self.base_url}/recomendacoes', json=payload)
        return response.json()['recomendacao']

def exemplo_7_classe():
    """Exemplo: Usar a classe wrapper"""
    print("=" * 50)
    print("EXEMPLO 7: Usando Classe Wrapper")
    print("=" * 50)
    
    api = VIXFinAPI()
    
    # Buscar cotação
    cotacao = api.buscar_cotacao('PETR4.SA')
    print(f"Cotação de PETR4.SA: R$ {cotacao['preco']}\n")
    
    # Simular
    sim = api.simular(1000, 200, 10, 10)
    print(f"Simulação: Valor Final = R$ {sim['valor_final']:.2f}\n")
    
    # Recomendar
    rec = api.recomendar(5000, 'acumular', 10, 'moderada')
    print(f"Aporte ideal: R$ {rec['aporte_recomendado']['ideal']:.2f}\n")

# =====================================
# EXECUTAR EXEMPLOS
# =====================================

if __name__ == '__main__':
    print("\n🚀 EXEMPLOS DE USO - VIX FIN API\n")
    print("Certifique-se de que o servidor está rodando:")
    print("python backend/app.py\n")
    
    try:
        # Executar cada exemplo
        exemplo_1_educacao()
        print()
        
        exemplo_2_cotacao()
        print()
        
        exemplo_3_simulador()
        print()
        
        exemplo_4_comparacao()
        print()
        
        exemplo_5_recomendacoes()
        print()
        
        exemplo_6_historico()
        print()
        
        exemplo_7_classe()
        print()
        
        print("✅ Todos os exemplos executados com sucesso!\n")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("Certifique-se de que está rodando: python backend/app.py\n")
    except Exception as e:
        print(f"❌ Erro: {e}\n")
