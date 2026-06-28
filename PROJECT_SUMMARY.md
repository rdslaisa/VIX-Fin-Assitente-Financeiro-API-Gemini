# 🎉 VIX Fin - Assistente Virtual de Investimentos

## ✨ Projeto Completo e Pronto para Usar!

Criei um **assistente virtual educacional completo** para quem está começando a investir. A plataforma é moderna, intuitiva e totalmente funcional.

---

## 📦 O Que Foi Criado

### 🎯 Estrutura
```
VIX Fin/
├── backend/                 # API Python com Flask
│   ├── app.py              # Servidor principal (4 endpoints)
│   ├── educacao.py         # Módulo de conceitos e tipos
│   ├── cotacoes.py         # Integração com yfinance
│   ├── simulador.py        # Simulador de investimentos
│   └── recomendacoes.py    # Engine de recomendações
│
├── frontend/               # Interface Web
│   ├── index.html          # 5 seções principais
│   └── static/
│       ├── style.css       # Design responsivo moderno
│       └── app.js          # Lógica interativa
│
├── requirements.txt        # 7 dependências
├── README.md              # Documentação completa
├── INSTALL.md             # Guia de instalação
├── QUICKSTART.md          # Início rápido
├── .env.example           # Variáveis de ambiente
└── test_api.py            # Script de teste
```

---

## 🚀 Como Usar

### 1️⃣ Instalar (1 minuto)
```bash
cd "VIX Fin"
pip install -r requirements.txt
```

### 2️⃣ Executar (30 segundos)
```bash
cd backend
python app.py
```

### 3️⃣ Acessar
Abra: **http://localhost:5000**

---

## 🎓 Funcionalidades

### 📚 Educação Financeira
- 5 conceitos fundamentais
- 5 tipos de investimento detalhados
- Perfis de risco com alocações
- Dicas para iniciantes
- Fórmulas de cálculo

### 📊 Cotações em Tempo Real
- Buscar cotação de qualquer ativo
- Abertura, máxima, mínima, volume
- Histórico de preços
- Ativos recomendados

### 🎯 Simulador
- Cálculo com juros compostos
- Aportes mensais automáticos
- Relatórios anuais
- Comparação de cenários

### ✨ Recomendações Personalizadas
- Alocação customizada por risco
- Ativos sugeridos
- Aporte recomendado
- Próximos passos

---

## 🔗 Endpoints da API

| Método | Endpoint | Função |
|--------|----------|---------|
| GET | `/api/educacao/conceitos` | Carrega conceitos |
| GET | `/api/educacao/tipos` | Carrega tipos de investimento |
| GET | `/api/cotacoes/<ticker>` | Busca cotação atual |
| GET | `/api/historico/<ticker>` | Busca histórico de preços |
| POST | `/api/simulador/simular` | Simula investimento |
| POST | `/api/recomendacoes` | Gera recomendações |
| GET | `/api/health` | Verifica saúde da API |

---

## 💡 Exemplos de Uso

### Buscar Cotação
```bash
curl http://localhost:5000/api/cotacoes/PETR4.SA
```

### Simular Investimento
```bash
curl -X POST http://localhost:5000/api/simulador/simular \
  -H "Content-Type: application/json" \
  -d '{
    "valor_inicial": 1000,
    "aporte_mensal": 200,
    "taxa_anual": 10,
    "anos": 10
  }'
```

### Obter Recomendações
```bash
curl -X POST http://localhost:5000/api/recomendacoes \
  -H "Content-Type: application/json" \
  -d '{
    "renda": 5000,
    "objetivo": "acumular",
    "horizonte_tempo": 10,
    "aversao_risco": "moderada"
  }'
```

---

## 🧪 Testar a API

```bash
# Em outro terminal:
pip install requests
python test_api.py
```

Este script testa:
- ✅ Health check
- ✅ Endpoints de educação
- ✅ Busca de cotações
- ✅ Simulador
- ✅ Recomendações

---

## 📱 Interface Web

### Seções Principais

1. **Início** - Bem-vindo e features
2. **Educação** - Conceitos e tipos de investimento
3. **Cotações** - Busca e acompanhamento de preços
4. **Simulador** - Simule seus investimentos
5. **Recomendações** - Perfil personalizado

### Design
- ✨ Moderno e limpo
- 📱 Responsivo (funciona em celular)
- ⚡ Rápido e intuitivo
- 🎨 Paleta de cores profissional

---

## 🎯 Ativos Suportados

**Ações Brasileiras:**
- PETR4.SA (Petrobras)
- VALE3.SA (Vale)
- WEGE3.SA (WEG)
- BBDC4.SA (Bradesco)
- Mais de 500 outras

**ETFs e Fundos:**
- VGIR11.SA (Vanguard Índice)
- IVVB11.SA (iShares S&P 500)
- BRDT11.SA (Brasil Renda Fixa)

**Índices:**
- ^BVSP (Ibovespa)
- ^GSPC (S&P 500)

---

## 🔒 Segurança & Avisos

⚠️ **Apenas para fins educacionais**
⚠️ **Não é um serviço financeiro oficial**
⚠️ **Não execute trades reais aqui**
⚠️ **Consulte profissional antes de investir**

---

## 🚀 Próximas Features Sugeridas

- [ ] Autenticação de usuários
- [ ] Salvar simulações favoritas
- [ ] Análise técnica avançada
- [ ] Notificações de preços
- [ ] Integração com corretoras
- [ ] Dashboard com gráficos
- [ ] API de histórico pessoal
- [ ] Relatórios em PDF

---

## 📚 Documentação

- **[README.md](README.md)** - Documentação completa
- **[INSTALL.md](INSTALL.md)** - Guia passo a passo
- **[QUICKSTART.md](QUICKSTART.md)** - Início rápido

---

## 🛠 Stack Técnico

**Backend:**
- Python 3.8+
- Flask 3.0
- yfinance (dados de mercado)
- pandas/numpy (cálculos)

**Frontend:**
- HTML5
- CSS3 (responsivo)
- JavaScript puro (sem dependências)

**Dados:**
- yfinance (API de dados)
- CORS habilitado

---

## 💾 Arquivos Principais

| Arquivo | Linhas | Função |
|---------|--------|--------|
| app.py | 100+ | Servidor e rotas |
| educacao.py | 150+ | Conceitos educacionais |
| cotacoes.py | 100+ | Integração yfinance |
| simulador.py | 90+ | Simulações |
| recomendacoes.py | 180+ | Engine de recomendações |
| index.html | 200+ | Interface |
| style.css | 500+ | Estilos |
| app.js | 400+ | Lógica frontend |

**Total: 1500+ linhas de código**

---

## 🎓 Conceitos Abordados

1. ✅ O que é Investimento
2. ✅ Rentabilidade e Cálculos
3. ✅ Gestão de Risco
4. ✅ Diversificação
5. ✅ Horizonte de Investimento
6. ✅ Tipos de Ativos
7. ✅ Perfis de Risco
8. ✅ Alocação de Ativos
9. ✅ Juros Compostos
10. ✅ Estratégias de Investimento

---

## 📞 Suporte

Se encontrar algum problema:

1. Verifique se Python 3.8+ está instalado
2. Rode: `pip install -r requirements.txt`
3. Certifique-se que porta 5000 está livre
4. Verifique sua conexão com internet

---

## 🎉 Pronto para Usar!

Seu assistente de investimentos está **100% funcional e pronto**. 

### Comece agora:
```bash
cd "VIX Fin"
pip install -r requirements.txt
cd backend
python app.py
```

Depois abra: **http://localhost:5000**

---

**Criado com ❤️ para educação financeira**
**Sucesso nos seus investimentos! 🚀💰**
