# Guia de Instalação e Execução - VIX Fin

## ✅ Checklist de Instalação

### 1️⃣ Pré-requisitos
- Python 3.8+ instalado
- pip atualizado

### 2️⃣ Instalação Rápida

```bash
# 1. Navegar para a pasta do projeto
cd "VIX Fin"

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar a chave do Gemini (necessária para o chat da Atena)
cp .env.example .env
# edite o .env e preencha GEMINI_API_KEY com uma chave gratuita de
# https://aistudio.google.com/app/apikey

# 4. Executar o servidor
cd backend
python app.py
```

### 3️⃣ Acessar a Aplicação

Abra seu navegador em: **http://localhost:5000**

## 🎯 Estrutura do Projeto

```
VIX Fin/
├── backend/                 # API Flask
│   ├── app.py              # Servidor principal
│   ├── educacao.py         # Conteúdo educacional
│   ├── cotacoes.py         # Dados de mercado
│   ├── simulador.py        # Simulador
│   └── recomendacoes.py    # Recomendações
├── frontend/               # Interface Web
│   ├── index.html
│   └── static/
│       ├── style.css
│       └── app.js
├── requirements.txt        # Dependências
├── README.md              # Documentação
└── INSTALL.md             # Este arquivo
```

## 🚀 Primeiro Uso

### Explorar Educação
1. Clique em **"Educação"** na navegação
2. Aprenda sobre conceitos básicos de investimento
3. Explore os diferentes tipos de investimento

### Verificar Cotações
1. Vá para **"Cotações"**
2. Digite um ticker (ex: PETR4.SA, VALE3.SA)
3. Veja preço, variação e histórico

### Usar o Simulador
1. Acesse **"Simulador"**
2. Configure:
   - Valor inicial
   - Aporte mensal
   - Taxa anual esperada
   - Horizonte em anos
3. Clique "Simular"

### Receber Recomendações
1. Vá para **"Recomendações"**
2. Preencha seu perfil:
   - Renda mensal
   - Objetivo (acumular, renda ou aposentadoria)
   - Horizonte de tempo
   - Perfil de risco
3. Clique "Gerar Recomendações"

## 🔧 Solução de Problemas

### Problema: Porta 5000 em uso
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Problema: Módulos não encontrados
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problema: Cotações não carregam
- Verifique sua conexão com internet
- Use tickers válidos (com .SA para Brasil)
- Exemplos: PETR4.SA, VALE3.SA, WEGE3.SA

## 📚 Exemplos de Tickers

**Ações Brasileiras:**
- PETR4.SA - Petrobras
- VALE3.SA - Vale
- WEGE3.SA - WEG
- BBDC4.SA - Bradesco

**ETFs:**
- VGIR11.SA - Vanguard Índice
- IVVB11.SA - iShares S&P 500
- BRDT11.SA - Brasil Renda Fixa

## 💡 Dicas

1. **Comece pequeno**: Simule com valores baixos antes de investir real
2. **Use o simulador**: Teste diferentes cenários
3. **Aprenda primeiro**: Leia a seção de educação
4. **Perfil realista**: Escolha um perfil de risco condizente com sua situação
5. **Diversifique**: Não coloque tudo em um ativo

## 🎓 Objetivos de Aprendizagem

Ao usar VIX Fin, você aprenderá:

- ✅ Conceitos fundamentais de investimento
- ✅ Como calcular rentabilidade
- ✅ Diferentes tipos de ativos
- ✅ Importância da diversificação
- ✅ Perfis de risco
- ✅ Estratégias de investimento

## 📊 Funcionalidades em Detalhes

### Educação
- 5+ conceitos fundamentais
- 5 tipos principais de investimento
- Dicas para iniciantes
- Perfis de risco com alocações

### Cotações
- Preço atual
- Abertura, máxima, mínima
- Variação do dia
- Volume negociado
- Histórico de preços

### Simulador
- Montante com juros compostos
- Aportes mensais automáticos
- Relatórios anuais
- Comparação de cenários

### Recomendações
- Alocação personalizada
- Ativos sugeridos
- Aporte recomendado
- Próximos passos

## 🔐 Segurança

- ⚠️ **Não é um serviço financeiro oficial**
- ⚠️ **Apenas para fins educacionais**
- ⚠️ **Não faça trades reais nesta plataforma**
- ⚠️ **Consulte um profissional antes de investir real**

## 📞 Suporte

Se encontrar problemas:

1. Verifique se Python 3.8+ está instalado: `python --version`
2. Verifique se Flask está instalado: `pip show flask`
3. Verifique a conexão com internet
4. Verifique se nenhuma outra app usa a porta 5000

## 🚀 Próximos Passos

Após familiarizar-se com VIX Fin:

1. Abra conta em uma corretora
2. Comece com pequenos investimentos
3. Estude análise fundamental
4. Construa sua estratégia própria
5. Acompanhe seus resultados

---

**Bom aprendizado e sucesso nos seus investimentos! 🎯💰**
