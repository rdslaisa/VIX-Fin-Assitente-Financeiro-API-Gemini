"""
Módulo de Simulador
Simula resultados de investimentos
"""

import math
from datetime import datetime

def simular_investimento(valor_inicial, aporte_mensal, taxa_anual, anos, ativo='PETR4.SA'):
    """
    Simula um investimento com aportes periódicos
    
    Args:
        valor_inicial: Valor inicial investido
        aporte_mensal: Aporte mensal (0 se não houver)
        taxa_anual: Taxa de retorno anual esperada (em %)
        anos: Horizonte de investimento (em anos)
        ativo: Ticker do ativo (para contexto)
    """
    
    taxa_mensal = taxa_anual / 100 / 12
    meses = anos * 12
    saldo = valor_inicial
    historico = []
    
    # Montante com aporte mensal
    for mes in range(1, meses + 1):
        saldo = saldo * (1 + taxa_mensal) + aporte_mensal
        
        if mes % 12 == 0:  # Registra anualmente
            historico.append({
                'mes': mes,
                'ano': mes // 12,
                'saldo': round(saldo, 2)
            })
    
    # Cálculos finais
    total_investido = valor_inicial + (aporte_mensal * meses)
    ganho = saldo - total_investido
    rentabilidade_percentual = (ganho / total_investido * 100) if total_investido > 0 else 0
    
    return {
        'simulacao': {
            'ativo': ativo,
            'valor_inicial': valor_inicial,
            'aporte_mensal': aporte_mensal,
            'taxa_anual_esperada': taxa_anual,
            'horizonte_anos': anos,
            'total_investido': round(total_investido, 2),
            'valor_final': round(saldo, 2),
            'ganho': round(ganho, 2),
            'rentabilidade_percentual': round(rentabilidade_percentual, 2),
            'historico_anual': historico
        },
        'timestamp': datetime.now().isoformat()
    }

def calcular_rentabilidade(valor_inicial, valor_final, tempo_dias=365):
    """Calcula rentabilidade entre dois valores"""
    ganho = valor_final - valor_inicial
    rentabilidade_percentual = (ganho / valor_inicial * 100)
    rentabilidade_anualizada = (rentabilidade_percentual / tempo_dias) * 365
    
    return {
        'valor_inicial': valor_inicial,
        'valor_final': valor_final,
        'ganho': round(ganho, 2),
        'rentabilidade_percentual': round(rentabilidade_percentual, 2),
        'rentabilidade_anualizada': round(rentabilidade_anualizada, 2)
    }

def calcular_montante_final(capital_inicial, taxa_anual, meses):
    """Calcula juros compostos"""
    taxa_mensal = taxa_anual / 100 / 12
    montante = capital_inicial * ((1 + taxa_mensal) ** meses)
    return round(montante, 2)

def comparar_investimentos(cenarios):
    """Compara múltiplos cenários de investimento"""
    resultados = []
    for cenario in cenarios:
        resultado = simular_investimento(
            cenario['valor_inicial'],
            cenario.get('aporte_mensal', 0),
            cenario['taxa_anual'],
            cenario['anos']
        )
        resultado['nome'] = cenario['nome']
        resultados.append(resultado)
    
    return {'comparacao': resultados}
