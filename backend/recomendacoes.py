"""
Módulo de Recomendações Personalizadas
Gera sugestões baseadas no perfil do usuário
"""

def get_recomendacao_personalizada(renda, objetivo, horizonte_tempo, aversao_risco):
    """
    Gera recomendação personalizada baseada no perfil do usuário
    
    Args:
        renda: Renda mensal
        objetivo: 'acumular', 'gerar_renda', 'aposentadoria'
        horizonte_tempo: Anos até o objetivo
        aversao_risco: 'baixa', 'moderada', 'alta'
    """
    
    alocacao = definir_alocacao(aversao_risco, horizonte_tempo)
    aportes = definir_aportes(renda)
    ativos = recomendar_ativos(aversao_risco, objetivo)
    estrategia = definir_estrategia(objetivo, horizonte_tempo)
    
    return {
        'recomendacao': {
            'perfil': {
                'renda_mensal': renda,
                'objetivo': objetivo,
                'horizonte_tempo': horizonte_tempo,
                'aversao_risco': aversao_risco
            },
            'alocacao_sugerida': alocacao,
            'aporte_recomendado': aportes,
            'ativos_sugeridos': ativos,
            'estrategia': estrategia,
            'proximos_passos': get_proximos_passos(aversao_risco)
        }
    }

def definir_alocacao(aversao_risco, horizonte_tempo):
    """Define alocação de ativos baseado em risco e horizonte"""
    
    if horizonte_tempo <= 2:
        # Horizonte curto - mais conservador
        alocacoes = {
            'baixa': {'renda_fixa': 80, 'acoes': 20},
            'moderada': {'renda_fixa': 60, 'acoes': 40},
            'alta': {'renda_fixa': 40, 'acoes': 60}
        }
    elif horizonte_tempo <= 5:
        # Horizonte médio
        alocacoes = {
            'baixa': {'renda_fixa': 70, 'acoes': 30},
            'moderada': {'renda_fixa': 50, 'acoes': 50},
            'alta': {'renda_fixa': 30, 'acoes': 70}
        }
    else:
        # Horizonte longo - mais agressivo
        alocacoes = {
            'baixa': {'renda_fixa': 60, 'acoes': 40},
            'moderada': {'renda_fixa': 40, 'acoes': 60},
            'alta': {'renda_fixa': 20, 'acoes': 80}
        }
    
    return alocacoes.get(aversao_risco, alocacoes['moderada'])

def definir_aportes(renda_mensal):
    """Define aporte mensal recomendado"""
    
    # Recomendação: investir 10-30% da renda
    aporte_minimo = renda_mensal * 0.1
    aporte_ideal = renda_mensal * 0.2
    aporte_maximo = renda_mensal * 0.3
    
    return {
        'minimo': round(aporte_minimo, 2),
        'ideal': round(aporte_ideal, 2),
        'maximo': round(aporte_maximo, 2),
        'mensagem': f'Recomenda-se investir entre {round(aporte_minimo, 2)} e {round(aporte_maximo, 2)} mensalmente'
    }

def recomendar_ativos(aversao_risco, objetivo):
    """Recomenda ativos específicos"""
    
    recomendacoes = {
        'baixa_acumular': [
            {'nome': 'Tesouro Selic', 'percentual': 40, 'razao': 'Segurança e liquidez'},
            {'nome': 'CDI/CDB', 'percentual': 30, 'razao': 'Rendimento previsível'},
            {'nome': 'VGIR11 (ETF Índice)', 'percentual': 30, 'razao': 'Diversificação moderada'}
        ],
        'moderada_acumular': [
            {'nome': 'Tesouro IPCA', 'percentual': 30, 'razao': 'Proteção contra inflação'},
            {'nome': 'IVVB11 (ETF S&P 500)', 'percentual': 35, 'razao': 'Diversificação internacional'},
            {'nome': 'WEGE3 (WEG)', 'percentual': 35, 'razao': 'Ação de crescimento'}
        ],
        'alta_acumular': [
            {'nome': 'VALE3 (Vale)', 'percentual': 25, 'razao': 'Dividendos e crescimento'},
            {'nome': 'WEGE3 (WEG)', 'percentual': 25, 'razao': 'Crescimento'},
            {'nome': 'PETR4 (Petrobras)', 'percentual': 25, 'razao': 'Dividendos'},
            {'nome': 'VGIR11 (ETF)', 'percentual': 25, 'razao': 'Diversificação'}
        ],
        'baixa_gerar_renda': [
            {'nome': 'Tesouro Prefixado', 'percentual': 50, 'razao': 'Renda previsível'},
            {'nome': 'PETR4 (Dividendos)', 'percentual': 50, 'razao': 'Yield de dividendos'}
        ],
        'moderada_gerar_renda': [
            {'nome': 'Tesouro Prefixado', 'percentual': 30, 'razao': 'Renda previsível'},
            {'nome': 'PETR4/VALE3 (Dividendos)', 'percentual': 40, 'razao': 'Yield consistente'},
            {'nome': 'Fundos de Renda', 'percentual': 30, 'razao': 'Diversificação'}
        ],
        'alta_gerar_renda': [
            {'nome': 'Ações com Dividendos', 'percentual': 60, 'razao': 'Yield alto'},
            {'nome': 'Fundos Imobiliários', 'percentual': 40, 'razao': 'Renda mensal'}
        ]
    }
    
    chave = f'{aversao_risco}_{objetivo}'
    return recomendacoes.get(chave, recomendacoes['moderada_acumular'])

def definir_estrategia(objetivo, horizonte_tempo):
    """Define estratégia de investimento"""
    
    estrategias = {
        'acumular': {
            'nome': 'Estratégia de Acumulação',
            'descricao': 'Investimento regular com reinvestimento de dividendos',
            'rebalanceamento': 'Semestral ou anual',
            'dicas': [
                'Invista mensalmente (custo médio)',
                'Reinvista todos os dividendos',
                'Não se preocupe com variações curtas',
                f'Mantenha por {horizonte_tempo}+ anos'
            ]
        },
        'gerar_renda': {
            'nome': 'Estratégia de Renda',
            'descricao': 'Foco em ativos com dividend yield',
            'rebalanceamento': 'Trimestral',
            'dicas': [
                'Procure ações com histórico de dividendos',
                'Diversifique setores',
                'Monitore a sustentabilidade dos dividendos',
                'Considere fundos imobiliários'
            ]
        },
        'aposentadoria': {
            'nome': 'Estratégia para Aposentadoria',
            'descricao': 'Construção de patrimônio de longo prazo',
            'rebalanceamento': 'Anual',
            'dicas': [
                'Comece cedo para aproveitar juros compostos',
                'Aumente aportes conforme renda aumenta',
                'Reduz risco conforme se aproxima do objetivo',
                'Use Tesouro Direto como base'
            ]
        }
    }
    
    return estrategias.get(objetivo, estrategias['acumular'])

def get_proximos_passos(aversao_risco):
    """Próximos passos recomendados"""
    
    passos = {
        'baixa': [
            '1. Abra conta em corretora (gratuito)',
            '2. Investir R$ 100-500 em Tesouro Selic',
            '3. Defina aporte mensal automático',
            '4. Aprenda sobre outros ativos',
            '5. Diversifique conforme aprende'
        ],
        'moderada': [
            '1. Abra conta em corretora',
            '2. Comece com Tesouro Direto (40%)',
            '3. Adicione um ETF como VGIR11 (30%)',
            '4. Compre 1-2 ações com bons fundamentals (30%)',
            '5. Rebalanceie anualmente'
        ],
        'alta': [
            '1. Abra conta em corretora premium',
            '2. Comece análise fundamental de ações',
            '3. Invista em ações com dividendos',
            '4. Acompanhe relatórios trimestrais',
            '5. Considere análise técnica para timing'
        ]
    }
    
    return passos.get(aversao_risco, passos['moderada'])
