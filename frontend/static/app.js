// ========================================
// INICIALIZAÇÃO
// ========================================

const API_BASE_URL = '/api';

// URL base do backend Flask
const BACKEND_URL = "";

// Variáveis globais
let educacaoCarregada = false;
let tiposCarregados = false;
let chatHistorico = [];
let lastFetchDebug = null;

// Verifica se a API está respondendo
async function checkApiHealth() {
    try {
        const res = await fetch(`${API_BASE_URL}/health`);
        if (!res.ok) throw new Error('API indisponível');
        const data = await res.json();
        console.log('API health:', data);
        return true;
    } catch (err) {
        console.warn('API health check failed:', err);
        const banner = document.createElement('div');
        banner.className = 'api-warning';
        banner.textContent = '⚠️ Backend inacessível — algumas funcionalidades podem não funcionar.';
        banner.style.cssText = 'background:#fff3cd;color:#856404;padding:0.75rem;text-align:center;';
        document.body.insertBefore(banner, document.body.firstChild);
        return false;
    }
}

// Inicialização quando a página carregar
document.addEventListener('DOMContentLoaded', async function () {
    console.log('✅ VIX Fin carregado com sucesso');

    showSection('home');

    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            return false;
        });
    });

    document.getElementById('ticker-input')?.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') buscarCotacao();
    });

    await checkApiHealth();

    // Primeira busca de cotações + atualização a cada 15 segundos
    buscarMoedas();
    buscarAcoesEIndices();
    setInterval(() => {
        buscarMoedas();
        buscarAcoesEIndices();
    }, 15000);
});

// ========================================
// NAVEGAÇÃO
// ========================================

function showSection(sectionId) {
    console.log(`Navegando para: ${sectionId}`);

    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));

    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
        if (sectionId === 'educacao' && !educacaoCarregada) {
            carregarEducacao();
        }
    } else {
        console.warn(`❌ Seção "${sectionId}" não encontrada no DOM`);
    }
    return false;
}

function switchTab(tabName, event) {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));

    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    } else {
        document.querySelector(`button[onclick*="switchTab('${tabName}')"]`)?.classList.add('active');
    }

    const tabContent = document.getElementById(tabName);
    if (tabContent) {
        tabContent.classList.add('active');
    }

    if (tabName === 'conceitos' && !educacaoCarregada) {
        carregarEducacao();
    } else if (tabName === 'tipos' && !tiposCarregados) {
        carregarTiposInvestimento();
    }
}

// Evita XSS ao injetar texto da API no innerHTML
function escapeHtml(texto) {
    if (texto === null || texto === undefined) return '';
    return String(texto)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ========================================
// EDUCAÇÃO
// ========================================

async function carregarEducacao() {
    const conceitosList = document.getElementById('conceitos-list');
    try {
        const response = await fetch(`${API_BASE_URL}/educacao/conceitos`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        conceitosList.innerHTML = data.conceitos.map(conceito => `
            <div class="card-item">
                <h4>${escapeHtml(conceito.titulo)}</h4>
                <p>${escapeHtml(conceito.descricao)}</p>
                ${conceito.formula ? `
                    <div style="margin-top: 1rem; padding: 1rem; background: #F5F5F5; border-radius: 4px; color: #8D0004;">
                        <strong>Fórmula:</strong> ${escapeHtml(conceito.formula)}
                    </div>` : ''}
                ${conceito.exemplos ? `
                    <div style="margin-top: 0.5rem;">
                        <strong>Exemplos:</strong> ${conceito.exemplos.map(escapeHtml).join(', ')}
                    </div>` : ''}
            </div>
        `).join('');

        educacaoCarregada = true;
    } catch (error) {
        console.error('Erro ao carregar educação:', error);
        conceitosList.innerHTML = '<div class="error">Erro ao carregar dados.</div>';
    }
}

async function carregarTiposInvestimento() {
    const tiposList = document.getElementById('tipos-list');
    try {
        const response = await fetch(`${API_BASE_URL}/educacao/tipos`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        tiposList.innerHTML = data.tipos.map(tipo => `
            <div class="card-item" style="border-left-color: var(--accent-color);">
                <h4>${escapeHtml(tipo.nome)}</h4>
                <div style="margin: 1rem 0;">
                    <strong>Risco:</strong> ${escapeHtml(tipo.risco)}<br>
                    <strong>Rentabilidade:</strong> ${escapeHtml(tipo.rentabilidade)}<br>
                    <strong>Liquidez:</strong> ${escapeHtml(tipo.liquidez)}
                </div>
                <p><strong>Descrição:</strong> ${escapeHtml(tipo.descricao)}</p>
                <div style="margin-top: 1rem;">
                    <strong>✅ Vantagens:</strong>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        ${tipo.vantagens.map(v => `<li>${escapeHtml(v)}</li>`).join('')}
                    </ul>
                </div>
                <div style="margin-top: 1rem;">
                    <strong>⚠️ Desvantagens:</strong>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        ${tipo.desvantagens.map(d => `<li>${escapeHtml(d)}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `).join('');

        tiposCarregados = true;
    } catch (error) {
        console.error('Erro ao carregar tipos:', error);
        tiposList.innerHTML = '<div class="error">Erro ao carregar dados.</div>';
    }
}

// ========================================
// COTAÇÕES
// ========================================

// Alternar visualmente as abas do painel
function alternarAba(tipo, botaoClicado) {
    const painelMoedas = document.getElementById("painel-moedas");
    const painelBr = document.getElementById("painel-acoes-br");
    const painelGlobal = document.getElementById("painel-acoes-global");

    if (painelMoedas) painelMoedas.style.display = "none";
    if (painelBr) painelBr.style.display = "none";
    if (painelGlobal) painelGlobal.style.display = "none";

    if (tipo === 'moedas' && painelMoedas) painelMoedas.style.display = "block";
    if (tipo === 'acoes-br' && painelBr) painelBr.style.display = "block";
    if (tipo === 'acoes-global' && painelGlobal) painelGlobal.style.display = "block";

    document.querySelectorAll(".aba-btn").forEach(btn => btn.classList.remove("ativa"));
    if (botaoClicado) botaoClicado.classList.add("ativa");
}

// Buscar moedas e cripto via backend
async function buscarMoedas() {
    const url = `${BACKEND_URL}/api/moedas?t=${Date.now()}`;
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        if (data.erro) throw new Error(data.erro);

        if (data.dolar) atualizarCardLayout("usd-value", "usd-pct",
            data.dolar.valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
            data.dolar.variacao
        );
        if (data.euro) atualizarCardLayout("eur-value", "eur-pct",
            data.euro.valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
            data.euro.variacao
        );
        if (data.bitcoin) atualizarCardLayout("btc-value", "btc-pct",
            data.bitcoin.valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }),
            data.bitcoin.variacao
        );
        if (data.ethereum) atualizarCardLayout("eth-value", "eth-pct",
            data.ethereum.valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }),
            data.ethereum.variacao
        );
    } catch (e) {
        console.error("Erro ao carregar moedas:", e);
    }
}

// Buscar ações brasileiras e internacionais via backend
async function buscarAcoesEIndices() {
    const ativos = [
        "^BVSP", "PETR4", "VALE3", "ITUB4", "WEGE3", "TAEE11",
        "ITSA4", "ABEV3", "SBSP3", "ENEV3", "BBDC3", "BBAS3",
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META"
    ];

    for (const ticker of ativos) {
        try {
            const response = await fetch(`${BACKEND_URL}/api/cotacoes/${encodeURIComponent(ticker)}?t=${Date.now()}`);
            if (!response.ok) continue;

            const data = await response.json();
            if (data.erro) continue;

            const preco = data.preco;
            const variacao = data.variacao;
            const idPrefixo = ticker.toLowerCase().replace("^", "").replace(".sa", "");
            let precoFormatado;

            if (idPrefixo === "bvsp") {
                precoFormatado = `${preco.toLocaleString('pt-BR', { maximumFractionDigits: 0 })} pts`;
            } else {
                const ehEstrangeira = ["aapl", "msft", "nvda", "amzn", "googl", "meta", "brk-b"].includes(idPrefixo);
                precoFormatado = preco.toLocaleString(ehEstrangeira ? 'en-US' : 'pt-BR', {
                    style: 'currency',
                    currency: ehEstrangeira ? 'USD' : 'BRL'
                });
            }

            atualizarCardLayout(`${idPrefixo}-value`, `${idPrefixo}-pct`, precoFormatado, variacao);
        } catch (e) {
            console.error(`Erro no ativo ${ticker}:`, e);
        }
    }
}

// Atualiza o card no HTML com o valor e aplica o efeito de brilho se o valor mudou
function atualizarCardLayout(idValor, idPorcentagem, valorFormatado, variacao) {
    const elValor = document.getElementById(idValor);
    const elPct = document.getElementById(idPorcentagem);

    if (elValor && elPct) {
        const idCard = idValor.replace("-value", "");
        const cardContainer = document.getElementById(`card-${idCard}`);

        if (cardContainer && elValor.innerText !== valorFormatado && elValor.innerText !== "Carregando...") {
            cardContainer.classList.add("card-atualizado");
            setTimeout(() => { cardContainer.classList.remove("card-atualizado"); }, 800);
        }

        elValor.classList.remove("valor-carregando");
        elValor.innerText = valorFormatado;

        const sinal = variacao > 0 ? "+" : "";
        elPct.innerText = `${sinal}${variacao.toFixed(2)}%`;
        elPct.className = variacao >= 0 ? "porcentagem alta" : "porcentagem baixa";
    }
}

// ========================================
// SIMULADOR
// ========================================

async function simularInvestimento() {
    const valorInicial = parseFloat(document.getElementById('valor-inicial').value);
    const aporteMensal = parseFloat(document.getElementById('aporte-mensal').value);
    const taxaAnual = parseFloat(document.getElementById('taxa-anual').value);
    const horizonte = parseInt(document.getElementById('horizonte').value);

    if (isNaN(valorInicial) || valorInicial <= 0) {
        alert('Valor inicial deve ser um número maior que 0');
        return;
    }
    if (isNaN(aporteMensal) || aporteMensal < 0) {
        alert('Aporte mensal deve ser um número maior ou igual a 0');
        return;
    }
    if (isNaN(taxaAnual) || taxaAnual <= 0 || taxaAnual > 100) {
        alert('Taxa anual deve ser um número entre 0 e 100');
        return;
    }
    if (isNaN(horizonte) || horizonte <= 0 || horizonte > 100) {
        alert('Horizonte deve ser um número entre 1 e 100 anos');
        return;
    }

    const resultado = document.getElementById('simulacao-resultado');
    resultado.innerHTML = '<div class="loading"></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/simulador/simular`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                valor_inicial: valorInicial,
                aporte_mensal: aporteMensal,
                taxa_anual: taxaAnual,
                anos: horizonte
            })
        });

        if (!response.ok) {
            const text = await response.text().catch(() => '');
            reportFetchError(resultado, `HTTP ${response.status}: ${response.statusText}`, text);
            return;
        }

        const data = await response.json().catch(err => {
            reportFetchError(resultado, 'Erro ao parsear JSON da resposta', err.message);
            return null;
        });

        if (!data) return;

        if (data.erro) {
            reportFetchError(resultado, `Erro retornado pela API: ${data.erro}`);
            return;
        }

        if (!data.simulacao) {
            resultado.innerHTML = '<div class="error">❌ Erro: Resposta inválida do servidor</div>';
            return;
        }

        const sim = data.simulacao;

        resultado.innerHTML = `
            <div class="simulacao-resultado">
                <h3>Resultado da Simulação</h3>
                <div class="resultado-destaque">
                    <div class="resultado-item">
                        <div class="resultado-label">Total Investido</div>
                        <div class="resultado-valor">R$ ${sim.total_investido.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</div>
                    </div>
                    <div class="resultado-item">
                        <div class="resultado-label">Valor Final</div>
                        <div class="resultado-valor">R$ ${sim.valor_final.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</div>
                    </div>
                    <div class="resultado-item">
                        <div class="resultado-label">Ganho Total</div>
                        <div class="resultado-valor">R$ ${sim.ganho.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</div>
                    </div>
                    <div class="resultado-item">
                        <div class="resultado-label">Rentabilidade</div>
                        <div class="resultado-valor">${sim.rentabilidade_percentual}%</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <h3>Evolução do Patrimônio</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Ano</th>
                            <th>Patrimônio (R$)</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${sim.historico_anual.map(h => `
                            <tr>
                                <td><strong>Ano ${h.ano}</strong></td>
                                <td>R$ ${h.saldo.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } catch (error) {
        console.error('Erro na simulação:', error);
        reportFetchError(resultado, 'Erro ao simular investimento', error.message || error);
    }
}

// Exibe erros de fetch com detalhes no elemento UI e salva no debug global
function reportFetchError(container, message, details = '') {
    lastFetchDebug = { message, details, timestamp: new Date().toISOString() };
    console.warn('Fetch debug:', lastFetchDebug);
    container.innerHTML = `
        <div class="error">❌ ${escapeHtml(message)}</div>
        <details style="margin-top:0.5rem;color:var(--text-light);">
            <summary>Ver detalhes</summary>
            <pre style="white-space:pre-wrap;max-height:200px;overflow:auto">${escapeHtml(typeof details === 'string' ? details : JSON.stringify(details, null, 2))}</pre>
        </details>
        <div style="margin-top:0.5rem;font-size:0.9rem;color:var(--text-light);">
            Se o problema persistir, abra o Console do navegador para mais informações.
        </div>
    `;
}

// Exibe o último erro de fetch no console (pode ser chamada manualmente)
function showLastFetchDebug() {
    if (!lastFetchDebug) return alert('Nenhum erro de fetch registrado ainda.');
    alert(JSON.stringify(lastFetchDebug, null, 2));
}

// ========================================
// RECOMENDAÇÕES
// ========================================

async function obterRecomendacoes() {
    const renda = parseFloat(document.getElementById('renda').value);
    const objetivo = document.getElementById('objetivo').value;
    const horizonte = parseInt(document.getElementById('horizonte-recom').value);
    const aversaoRisco = document.getElementById('aversao-risco').value;

    if (isNaN(renda) || renda <= 0) {
        alert('Renda mensal deve ser um número maior que 0');
        return;
    }
    if (!objetivo) {
        alert('Selecione um objetivo');
        return;
    }
    if (isNaN(horizonte) || horizonte <= 0 || horizonte > 100) {
        alert('Horizonte deve ser um número entre 1 e 100 anos');
        return;
    }
    if (!aversaoRisco) {
        alert('Selecione sua aversão ao risco');
        return;
    }

    const resultado = document.getElementById('recomendacoes-resultado');
    resultado.innerHTML = '<div class="loading"></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/recomendacoes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                renda: renda,
                objetivo: objetivo,
                horizonte_tempo: horizonte,
                aversao_risco: aversaoRisco
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.erro) {
            resultado.innerHTML = `<div class="error">❌ Erro: ${escapeHtml(data.erro)}</div>`;
            return;
        }

        if (!data.recomendacao) {
            resultado.innerHTML = '<div class="error">❌ Erro: Resposta inválida do servidor</div>';
            return;
        }

        const rec = data.recomendacao;

        resultado.innerHTML = `
            <div class="recomendacao-box">
                <h3>Seu Perfil de Investidor</h3>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 1.5rem 0;">
                    <div><strong>Renda Mensal:</strong> R$ ${rec.perfil.renda_mensal.toLocaleString('pt-BR')}</div>
                    <div><strong>Objetivo:</strong> ${getObjetivoLabel(rec.perfil.objetivo)}</div>
                    <div><strong>Horizonte:</strong> ${rec.perfil.horizonte_tempo} anos</div>
                    <div><strong>Perfil de Risco:</strong> ${getRiscoLabel(rec.perfil.aversao_risco)}</div>
                </div>
            </div>
            <div class="card">
                <h3>💰 Aporte Recomendado</h3>
                <div style="font-size: 1.2rem; margin: 1rem 0;">
                    <div>Mínimo: <strong>R$ ${rec.aporte_recomendado.minimo.toLocaleString('pt-BR')}</strong></div>
                    <div>Ideal: <strong>R$ ${rec.aporte_recomendado.ideal.toLocaleString('pt-BR')}</strong></div>
                    <div>Máximo: <strong>R$ ${rec.aporte_recomendado.maximo.toLocaleString('pt-BR')}</strong></div>
                </div>
                <p style="color: var(--text-light); margin-top: 1rem;">${escapeHtml(rec.aporte_recomendado.mensagem)}</p>
            </div>
            <div class="card">
                <h3>📊 Alocação Sugerida</h3>
                <div class="alocacao-bars">
                    ${Object.entries(rec.alocacao_sugerida).map(([chave, valor]) => `
                        <div class="alocacao-bar">
                            <div class="alocacao-label">
                                <span>${getAlocacaoLabel(chave)}</span>
                                <span>${valor}%</span>
                            </div>
                            <div class="alocacao-progress">
                                <div class="alocacao-fill" style="width: ${valor}%">
                                    ${valor > 10 ? valor + '%' : ''}
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="card">
                <h3>🎯 Ativos Recomendados</h3>
                <div class="cards-grid">
                    ${rec.ativos_sugeridos.map(ativo => `
                        <div class="card-item" style="border-left-color: var(--accent-color);">
                            <h4>${escapeHtml(ativo.nome)}</h4>
                            <div style="margin: 1rem 0;">
                                <strong>Percentual:</strong> ${ativo.percentual}%<br>
                                <strong>Razão:</strong> ${escapeHtml(ativo.razao)}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="card">
                <h3>📋 Estratégia: ${escapeHtml(rec.estrategia.nome)}</h3>
                <p><strong>Descrição:</strong> ${escapeHtml(rec.estrategia.descricao)}</p>
                <p><strong>Rebalanceamento:</strong> ${escapeHtml(rec.estrategia.rebalanceamento)}</p>
                <h4 style="margin-top: 1.5rem;">Dicas:</h4>
                <ul>
                    ${rec.estrategia.dicas.map(dica => `<li>${escapeHtml(dica)}</li>`).join('')}
                </ul>
            </div>
            <div class="card" style="background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white;">
                <h3>🚀 Próximos Passos</h3>
                <ol style="margin-left: 1.5rem;">
                    ${rec.proximos_passos.map(passo => `<li style="padding: 0.5rem 0;">${escapeHtml(passo)}</li>`).join('')}
                </ol>
            </div>
        `;
    } catch (error) {
        console.error('Erro na geração de recomendações:', error);
        resultado.innerHTML = `<div class="error">❌ Erro ao gerar recomendações: ${escapeHtml(error.message)}</div>`;
    }
}

// Traduz o valor do campo "objetivo" para exibição
function getObjetivoLabel(objetivo) {
    const labels = {
        'acumular': 'Acumular Patrimônio',
        'gerar_renda': 'Gerar Renda',
        'aposentadoria': 'Preparar Aposentadoria'
    };
    return labels[objetivo] || objetivo;
}

// Traduz o valor do campo "aversão ao risco" para exibição
function getRiscoLabel(risco) {
    const labels = {
        'baixa': 'Baixa (Conservador)',
        'moderada': 'Moderada (Equilibrado)',
        'alta': 'Alta (Agressivo)'
    };
    return labels[risco] || risco;
}

// Traduz as chaves da alocação para nomes legíveis
function getAlocacaoLabel(chave) {
    const labels = {
        'renda_fixa': 'Renda Fixa',
        'acoes': 'Ações',
        'tesouro_direto': 'Tesouro Direto',
        'fundos': 'Fundos',
        'etfs': 'ETFs'
    };
    return labels[chave] || chave;
}

// ========================================
// CHAT (Atena — assistente do VIX Fin)
// ========================================

// Abre e fecha a janela do chat
function alternarChat() {
    const janela = document.getElementById("chat-janela");
    if (!janela) return;
    janela.classList.toggle("chat-escondido");

    if (!janela.classList.contains("chat-escondido")) {
        document.getElementById("chat-input")?.focus();
    }
}

// Adiciona uma mensagem na janela do chat
// tipo: 'user' | 'bot' | 'erro'
function adicionarMensagemChat(texto, tipo) {
    const container = document.getElementById("chat-mensagens");
    if (!container) return;

    const div = document.createElement("div");
    div.className = `chat-msg chat-msg-${tipo === 'user' ? 'user' : (tipo === 'erro' ? 'erro' : 'bot')}`;
    div.textContent = texto;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// Envia a mensagem do usuário para a API e exibe a resposta da Atena
async function enviarMensagemChat(event) {
    event.preventDefault();

    const input = document.getElementById("chat-input");
    const digitando = document.getElementById("chat-digitando");
    if (!input) return;

    const mensagem = input.value.trim();
    if (!mensagem) return;

    adicionarMensagemChat(mensagem, "user");
    chatHistorico.push({ role: "user", text: mensagem });
    input.value = "";
    input.disabled = true;
    if (digitando) digitando.style.display = "block";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensagem, historico: chatHistorico })
        });

        const data = await response.json();

        if (!response.ok || data.erro) {
            adicionarMensagemChat(data.erro || "Erro ao conversar com o assistente.", "erro");
        } else {
            adicionarMensagemChat(data.resposta, "bot");
            chatHistorico.push({ role: "model", text: data.resposta });
        }
    } catch (e) {
        console.error("Erro no chat:", e);
        adicionarMensagemChat("Não consegui me conectar ao assistente agora. Tente de novo em breve.", "erro");
    } finally {
        input.disabled = false;
        input.focus();
        if (digitando) digitando.style.display = "none";
    }
}