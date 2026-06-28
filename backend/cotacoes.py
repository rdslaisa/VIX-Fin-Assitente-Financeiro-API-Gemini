"""
Módulo de Cotações
Integração com yfinance para obter dados de mercado

"""
import yfinance as yf
import requests
from datetime import datetime, timedelta

FALLBACK_COTACOES = {
    'PETR4.SA': {
        'preco': 4.95,
        'abertura': 4.90,
        'maxima': 4.98,
        'minima': 4.88,
        'volume': 1000000
    }
}

# URL da API de moedas (sempre em tempo real, sem cache)
def get_cotacao_moedas():
    """Busca cotações de moedas/cripto em tempo real via Yahoo Finance.

    Usa a mesma fonte das ações (já comprovadamente acessível na rede),
    evitando depender da AwesomeAPI, que pode estar bloqueada em alguns
    ambientes de rede (ex: certos Codespaces/firewalls corporativas).
    """

    def _buscar_seguro(ticker):
        try:
            return _buscar_cotacao_diaria(ticker)
        except Exception:
            return None

    usd_brl = _buscar_seguro("BRL=X")       # 1 USD em BRL
    eur_brl = _buscar_seguro("EURBRL=X")    # 1 EUR em BRL
    btc_brl = _buscar_seguro("BTC-BRL")
    eth_brl = _buscar_seguro("ETH-BRL")

    # Fallback: se o par direto em BRL não existir no Yahoo, converte via USD
    if not btc_brl and usd_brl:
        btc_usd = _buscar_seguro("BTC-USD")
        if btc_usd:
            btc_brl = {
                'preco': round(btc_usd['preco'] * usd_brl['preco'], 2),
                'variacao': btc_usd['variacao'],
                'timestamp': btc_usd['timestamp']
            }

    if not eth_brl and usd_brl:
        eth_usd = _buscar_seguro("ETH-USD")
        if eth_usd:
            eth_brl = {
                'preco': round(eth_usd['preco'] * usd_brl['preco'], 2),
                'variacao': eth_usd['variacao'],
                'timestamp': eth_usd['timestamp']
            }

    def _montar(nome, dados):
        if not dados:
            return None
        return {
            'nome': nome,
            'valor': dados['preco'],
            'variacao': dados['variacao'],
            'atualizado': dados.get('timestamp')
        }

    resultado = {
        'dolar': _montar('Dólar Americano/Real Brasileiro', usd_brl),
        'euro': _montar('Euro/Real Brasileiro', eur_brl),
        'bitcoin': _montar('Bitcoin/Real Brasileiro', btc_brl),
        'ethereum': _montar('Ethereum/Real Brasileiro', eth_brl),
    }

    if not any(resultado.values()):
        raise RuntimeError('Nenhuma cotação de moeda disponível no momento.')

    return resultado


def _normalizar_ticker(ticker):
    """Normaliza o ticker para consulta com yfinance e fallback.

    Regras:
    - Índices (começam com ^) e tickers já com sufixo (com '.' ou ':') ficam como estão.
    - Tickers de ações brasileiras seguem o padrão B3: 4 letras + 1-2 números (ex: PETR4, VALE3) -> .SA
    - Demais tickers (ex: AAPL, MSFT, BTC-USD) ficam como estão, sem sufixo .SA.
    """
    if not ticker:
        return ticker

    ticker = ticker.strip().upper()

    if ticker.startswith('^') or '.' in ticker or ':' in ticker:
        return ticker

    # Padrão típico de ticker da B3: letras seguidas de números (PETR4, VALE3, WEGE3, ITUB4...)
    import re
    if re.fullmatch(r'[A-Z]{4}\d{1,2}', ticker):
        return f'{ticker}.SA'

    return ticker


def _get_cotacao_fallback(ticker):
    """Retorna dados de fallback para alguns tickers comuns."""
    dados = FALLBACK_COTACOES.get(ticker)
    if not dados:
        return None

    return {
        'ticker': ticker,
        'preco': dados['preco'],
        'abertura': dados['abertura'],
        'maxima': dados['maxima'],
        'minima': dados['minima'],
        'volume': dados['volume'],
        'variacao': dados['variacao'],
        'timestamp': datetime.now().isoformat(),
        'fonte': 'fallback'
    }


def _buscar_cotacao_diaria(ticker):
    """Busca cotações diárias recentes via endpoint de chart do Yahoo Finance."""
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, timeout=20, headers=headers)
    response.raise_for_status()

    payload = response.json()
    result = payload.get('chart', {}).get('result', [None])[0]
    if not result:
        return None

    meta = result.get('meta', {})
    timestamps = result.get('timestamp', [])
    quotes = result.get('indicators', {}).get('quote', [{}])[0]
    closes = quotes.get('close', [])
    opens = quotes.get('open', [])
    highs = quotes.get('high', [])
    lows = quotes.get('low', [])
    volumes = quotes.get('volume', [])

    if not timestamps or not closes:
        return None

    close_values = [float(v) for v in closes if v is not None]
    open_values = [float(v) for v in opens if v is not None]
    high_values = [float(v) for v in highs if v is not None]
    low_values = [float(v) for v in lows if v is not None]
    volume_values = [int(v) for v in volumes if v is not None]

    if len(close_values) < 2:
        return None

    ultima = close_values[-1]
    anterior = close_values[-2]
    variacao = ((ultima - anterior) / anterior) * 100 if anterior else 0

    return {
        'ticker': ticker,
        'preco': round(ultima, 2),
        'abertura': round(open_values[-1], 2) if open_values else round(ultima, 2),
        'maxima': round(max(high_values[-1], ultima), 2) if high_values else round(ultima, 2),
        'minima': round(min(low_values[-1], ultima), 2) if low_values else round(ultima, 2),
        'volume': volume_values[-1] if volume_values else 0,
        'variacao': round(variacao, 2),
        'timestamp': datetime.now().isoformat(),
        'fonte': 'yahoo_chart_daily'
    }


def get_cotacao_acao(ticker):
    """Obtém cotação atual de um ativo"""
    ticker = _normalizar_ticker(ticker)

    try:
        dados_diarios = _buscar_cotacao_diaria(ticker)
        if dados_diarios:
            return dados_diarios
    except Exception:
        pass

    try:
        ativo = yf.Ticker(ticker)
        dados = ativo.history(period='5d')
        if len(dados) >= 2:
            ultima_linha = dados.iloc[-1]
            preco_anterior = dados.iloc[-2]['Close']
            variacao_percentual = ((ultima_linha['Close'] - preco_anterior) / preco_anterior) * 100
            return {
                'ticker': ticker,
                'preco': round(float(ultima_linha['Close']), 2),
                'abertura': round(float(ultima_linha['Open']), 2),
                'maxima': round(float(ultima_linha['High']), 2),
                'minima': round(float(ultima_linha['Low']), 2),
                'volume': int(ultima_linha['Volume']),
                'variacao': round(float(variacao_percentual), 2),
                'timestamp': datetime.now().isoformat(),
                'fonte': 'yfinance_history'
            }
    except Exception:
        pass

    fallback = _get_cotacao_fallback(ticker)
    if fallback:
        return fallback

    return {'erro': f'Ativo {ticker} não encontrado ou indisponível no momento. Tente outro ticker.'}


def get_historico_preco(ticker, periodo='1y'):
    """Obtém histórico de preços diários."""
    ticker = _normalizar_ticker(ticker)

    try:
        response = requests.get(
            f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range={periodo}',
            timeout=20,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response.raise_for_status()

        payload = response.json()
        result = payload.get('chart', {}).get('result', [None])[0]
        if not result:
            raise ValueError('Sem dados de histórico')

        quotes = result.get('indicators', {}).get('quote', [{}])[0]
        timestamps = result.get('timestamp', [])
        closes = quotes.get('close', [])
        volumes = quotes.get('volume', [])

        historico = []
        ultimos = closes[-10:]
        ultimos_volumes = volumes[-10:]
        for idx, ts in enumerate(timestamps[-10:]):
            if idx >= len(ultimos):
                break
            data = datetime.fromtimestamp(ts)
            historico.append({
                'data': data.strftime('%Y-%m-%d'),
                'preco': round(float(ultimos[idx]), 2),
                'volume': int(ultimos_volumes[idx]) if idx < len(ultimos_volumes) else 0
            })

        return {
            'ticker': ticker,
            'periodo': periodo,
            'dados': historico,
            'ultima_atualizacao': datetime.now().isoformat(),
            'fonte': 'yahoo_chart_daily'
        }
    except Exception as e:
        return {'erro': f'Erro ao obter histórico: {str(e)}'}


def get_multiplos_ativos(tickers):
    """Obtém cotações de múltiplos ativos"""
    resultados = []
    for ticker in tickers:
        resultados.append(get_cotacao_acao(ticker))
    return resultados


def get_ativos_recomendados():
    """Retorna lista de ativos recomendados para iniciantes"""
    ativos = [
        {'ticker': 'PETR4.SA', 'nome': 'Petrobras', 'tipo': 'Ação de Dividendos'},
        {'ticker': 'VALE3.SA', 'nome': 'Vale', 'tipo': 'Ação de Dividendos'},
        {'ticker': 'WEGE3.SA', 'nome': 'WEG', 'tipo': 'Ação de Crescimento'},
        {'ticker': 'VGIR11.SA', 'nome': 'Vanguard Índice Brasil', 'tipo': 'ETF'},
        {'ticker': 'IVVB11.SA', 'nome': 'iShares S&P 500', 'tipo': 'ETF'},
        {'ticker': 'BRDT11.SA', 'nome': 'Brasil Renda Fixa', 'tipo': 'Fundo'},
    ]

    # Obter cotações em tempo real (sem cache)
    for ativo in ativos:
        cotacao = get_cotacao_acao(ativo['ticker'])
        ativo['cotacao'] = cotacao

    return {'ativos_recomendados': ativos}


