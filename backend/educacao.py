"""
Módulo de Educação Financeira
Conceitos e tipos de investimento para iniciantes
"""

def get_conceitos():
    """Retorna conceitos básicos de investimento"""
    return {
        'conceitos': [
            {
                'id': 1,
                'titulo': 'O que é Investimento?',
                'descricao': 'Aplicar dinheiro em ativos esperando retorno financeiro futuro.',
                'exemplos': ['Ações', 'Títulos', 'Imóveis', 'Fundos']
            },
            {
                'id': 2,
                'titulo': 'Rentabilidade',
                'descricao': 'O retorno financeiro obtido com o investimento.',
                'formula': 'Rentabilidade = (Valor Final - Valor Inicial) / Valor Inicial × 100'
            },
            {
                'id': 3,
                'titulo': 'Risco',
                'descricao': 'Possibilidade de perder dinheiro no investimento.',
                'niveis': ['Baixo', 'Moderado', 'Alto']
            },
            {
                'id': 4,
                'titulo': 'Diversificação',
                'descricao': 'Distribuir investimentos em diferentes ativos para reduzir risco.',
                'beneficio': 'Reduz impacto de perdas em um único ativo'
            },
            {
                'id': 5,
                'titulo': 'Horizonte de Investimento',
                'descricao': 'Período de tempo que você mantém o investimento.',
                'importancia': 'Define a estratégia e risco adequados'
            }
        ]
    }

def get_tipos_investimento():
    """Retorna tipos de investimento com características"""
    return {
        'tipos': [
            {
                'nome': 'Ações',
                'risco': 'Alto',
                'rentabilidade': 'Alta (variável)',
                'liquidez': 'Alta',
                'descricao': 'Frações de propriedade em empresas',
                'vantagens': ['Rentabilidade potencial', 'Dividendos'],
                'desvantagens': ['Volatilidade', 'Requer análise']
            },
            {
                'nome': 'Tesouro Direto',
                'risco': 'Muito Baixo',
                'rentabilidade': 'Previsível (Taxa Selic + IPCA)',
                'liquidez': 'Alta',
                'descricao': 'Títulos de dívida do governo',
                'vantagens': ['Segurança', 'Rendimento previsível'],
                'desvantagens': ['Menor rentabilidade', 'Carência']
            },
            {
                'nome': 'Fundos de Investimento',
                'risco': 'Variável',
                'rentabilidade': 'Variável',
                'liquidez': 'Alta',
                'descricao': 'Conjunto de investimentos gerenciados por profissionais',
                'vantagens': ['Diversificação', 'Gestão profissional'],
                'desvantagens': ['Taxa de administração', 'Menos transparência']
            },
            {
                'nome': 'ETFs',
                'risco': 'Variável (conforme índice)',
                'rentabilidade': 'Similar ao índice',
                'liquidez': 'Alta',
                'descricao': 'Fundo que replica um índice de mercado',
                'vantagens': ['Diversificação', 'Taxas baixas'],
                'desvantagens': ['Segue índice', 'Sem gestão ativa']
            },
            {
                'nome': 'Renda Fixa',
                'risco': 'Baixo',
                'rentabilidade': 'Média (CDI, taxa prefixada)',
                'liquidez': 'Média',
                'descricao': 'CDBs, Letras de Crédito, Debêntures',
                'vantagens': ['Segurança', 'Previsibilidade'],
                'desvantagens': ['Menor rentabilidade que ações']
            }
        ],
        'dicas': [
            'Comece com Tesouro Direto ou Fundos',
            'Diversifique seus investimentos',
            'Tenha paciência - rentabilidade vem com o tempo',
            'Não acompanhe preços diariamente',
            'Invista de forma regular (método de custo médio)'
        ]
    }

def get_perfis_risco():
    """Retorna perfis de risco e alocações recomendadas"""
    return {
        'conservador': {
            'descricao': 'Prioriza segurança, baixa volatilidade',
            'alocacao': {
                'renda_fixa': 70,
                'tesouro_direto': 20,
                'acoes_etfs': 10
            },
            'alvo_anual': '6-8%'
        },
        'moderado': {
            'descricao': 'Equilibra segurança e rentabilidade',
            'alocacao': {
                'renda_fixa': 40,
                'fundos': 30,
                'acoes_etfs': 30
            },
            'alvo_anual': '10-12%'
        },
        'agressivo': {
            'descricao': 'Busca alta rentabilidade, tolera volatilidade',
            'alocacao': {
                'acoes': 50,
                'etfs': 30,
                'renda_fixa': 20
            },
            'alvo_anual': '15%+'
        }
    }
