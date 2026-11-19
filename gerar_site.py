# -*- coding: utf-8 -*-
"""
Script gerador do index.html completo e interativo para hospedagem na Netlify.
Gera todas as 4 abas, estilização profissional, gráficos em alta resolução e scripts de interação.
"""

import base64
import json
from datetime import datetime
from app import (
    TEMPOS_ORIGINAIS, GRUPO, INTEGRANTES, UNIDADE,
    analisar, fmt, fnum, fpct, texto_moda, comparar_media_mediana,
    grafico_histograma, grafico_barras, grafico_ogiva, figura_para_png,
    PERGUNTAS, respostas_interpretacao
)

def gerar_site_completo():
    r = analisar(TEMPOS_ORIGINAIS)
    ini, m, t = r["ini"], r["med"], r["tabela"]

    # Gerar gráficos em base64
    hist_b64 = base64.b64encode(figura_para_png(grafico_histograma(r))).decode()
    fa_b64 = base64.b64encode(figura_para_png(grafico_barras(r, 'FA', 'Frequência Absoluta (FA) por Classe', 'Frequência Absoluta (nº de ligações)'))).decode()
    fr_b64 = base64.b64encode(figura_para_png(grafico_barras(r, 'FR (%)', 'Frequência Relativa (FR %) por Classe', 'Frequência Relativa (%)', True))).decode()
    ogiva_b64 = base64.b64encode(figura_para_png(grafico_ogiva(r))).decode()

    resp = respostas_interpretacao(r)
    dif, forma = comparar_media_mediana(r)

    # Montar linhas da tabela de frequência
    linhas_tabela = ""
    for i, row in t.iterrows():
        classe_css = ' class="destaque-classe"' if i in r["maiores"] else ""
        linhas_tabela += f"""<tr{classe_css}>
            <td>{i + 1}</td>
            <td><b>{row['Classe']}</b></td>
            <td>{fnum(row['Soma'])}</td>
            <td><b>{int(row['FA'])}</b></td>
            <td>{int(row['FAA'])}</td>
            <td><b>{fpct(row['FR (%)'])}</b></td>
            <td>{fpct(row['FRAA (%)'])}</td>
        </tr>"""

    # Linha total
    total_soma = fnum(t['Soma'].sum())
    total_fa = int(t['FA'].sum())
    linhas_tabela += f"""<tr class="linha-total">
        <td colspan="2">TOTAL</td>
        <td>{total_soma}</td>
        <td>{total_fa}</td>
        <td>—</td>
        <td>100,00%</td>
        <td>—</td>
    </tr>"""

    # Cards da equipe
    lista_equipe_html = "".join(
        f"<li><b>{item.split(' – ')[0]}</b> — <span class='curso-tag'>{item.split(' – ')[1]}</span></li>"
        for item in INTEGRANTES
    )

    # Cards de Perguntas e Respostas
    qa_html = "".join(
        f"""<div class="qa-card">
            <div class="qa-pergunta">
                <span class="qa-badge">Questão {i}</span>
                <span>{PERGUNTAS[k]}</span>
            </div>
            <div class="qa-resposta">{resp[k]}</div>
        </div>"""
        for i, k in enumerate(PERGUNTAS, 1)
    )

    # Rol ordenado
    rol_html = "".join(
        f"<span class='rol-item{' central' if idx in m['posicoes'] else ''}'><small>{idx}º</small>{fnum(v)} s</span>"
        for idx, v in enumerate(r['serie'], 1)
    )

    # HTML completo
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Call Center Analytics – Painel Estatístico</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --azul-escuro: #0B2545;
            --azul-medio: #13315C;
            --azul: #1F6FB2;
            --azul-claro: #8DB8E0;
            --azul-gelo: #EAF2FB;
            --cinza: #6B7785;
            --cinza-claro: #E4E8EE;
            --cinza-bg: #F7F9FC;
            --branco: #FFFFFF;
            --texto: #1D2733;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: var(--texto);
            background: #F4F6F9;
            line-height: 1.5;
            padding: 24px 16px 50px 16px;
        }}
        .app-container {{
            max-width: 1240px;
            margin: 0 auto;
        }}
        /* Cabeçalho */
        .cabecalho {{
            background: linear-gradient(120deg, var(--azul-escuro) 0%, var(--azul-medio) 55%, var(--azul) 100%);
            border-radius: 16px;
            padding: 26px 32px;
            color: var(--branco);
            margin-bottom: 22px;
            box-shadow: 0 4px 18px rgba(11, 37, 69, 0.14);
        }}
        .cabecalho h1 {{
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: .05em;
            margin-bottom: 4px;
        }}
        .cabecalho p {{
            color: var(--azul-claro);
            font-size: 1.05rem;
            font-weight: 500;
            margin-bottom: 14px;
        }}
        .tags-cabecalho {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .tag {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.16);
            color: var(--branco);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 999px;
            padding: 5px 14px;
            font-size: 0.82rem;
            font-weight: 500;
        }}

        /* Card da Equipe */
        .equipe-card {{
            background: var(--branco);
            border: 1px solid var(--cinza-claro);
            border-left: 5px solid var(--azul);
            border-radius: 12px;
            padding: 18px 24px;
            margin-bottom: 22px;
            box-shadow: 0 2px 8px rgba(11, 37, 69, 0.04);
        }}
        .equipe-card h3 {{
            color: var(--azul-escuro);
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .lista-equipe {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 8px 20px;
            list-style: none;
            padding-left: 0;
        }}
        .lista-equipe li {{
            font-size: 0.92rem;
            color: #2D3748;
            display: flex;
            align-items: baseline;
            gap: 6px;
        }}
        .lista-equipe li::before {{
            content: "•";
            color: var(--azul);
            font-weight: bold;
            font-size: 1.1rem;
        }}
        .curso-tag {{
            color: var(--cinza);
            font-size: 0.85rem;
        }}

        /* Abas de Navegação */
        .tabs-nav {{
            display: flex;
            gap: 8px;
            border-bottom: 2px solid var(--cinza-claro);
            margin-bottom: 24px;
            overflow-x: auto;
            padding-bottom: 2px;
        }}
        .tab-btn {{
            background: var(--branco);
            border: 1px solid var(--cinza-claro);
            border-bottom: none;
            border-radius: 10px 10px 0 0;
            padding: 12px 20px;
            font-family: inherit;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--cinza);
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}
        .tab-btn:hover {{
            color: var(--azul);
            background: var(--azul-gelo);
        }}
        .tab-btn.active {{
            background: var(--azul-escuro);
            color: var(--branco);
            border-color: var(--azul-escuro);
        }}

        /* Conteúdo das Abas */
        .tab-content {{
            display: none;
            animation: fadeIn 0.25s ease-in-out;
        }}
        .tab-content.active {{
            display: block;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(4px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Cards de KPIs */
        .grid-kpis {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--branco);
            border: 1px solid var(--cinza-claro);
            border-radius: 14px;
            padding: 16px 18px;
            box-shadow: 0 1px 4px rgba(11, 37, 69, 0.05);
            border-top: 4px solid var(--azul);
        }}
        .kpi-card.destaque {{
            border-top-color: var(--azul-escuro);
            background: var(--azul-gelo);
        }}
        .kpi-rotulo {{
            color: var(--cinza);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: .05em;
            font-weight: 600;
        }}
        .kpi-valor {{
            color: var(--azul-escuro);
            font-size: 1.7rem;
            font-weight: 800;
            margin-top: 4px;
            line-height: 1.15;
        }}
        .kpi-valor small {{
            font-size: 0.95rem;
            color: var(--cinza);
            font-weight: 600;
        }}
        .kpi-nota {{
            color: var(--cinza);
            font-size: 0.78rem;
            margin-top: 4px;
        }}

        /* Seções e Caixas */
        .secao-bloco {{
            background: var(--branco);
            border-radius: 14px;
            border: 1px solid var(--cinza-claro);
            padding: 24px 28px;
            margin-bottom: 22px;
            box-shadow: 0 1px 4px rgba(11, 37, 69, 0.04);
        }}
        .secao-titulo {{
            color: var(--azul-escuro);
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .caixa {{
            background: var(--azul-gelo);
            border-left: 5px solid var(--azul);
            border-radius: 8px;
            padding: 14px 18px;
            margin: 12px 0 18px 0;
            color: var(--azul-escuro);
            font-size: 0.95rem;
        }}
        .caixa b {{ color: var(--azul-escuro); }}
        .etapa-badge {{
            display: inline-block;
            background: var(--azul-escuro);
            color: var(--branco);
            font-size: 0.72rem;
            font-weight: 700;
            border-radius: 6px;
            padding: 3px 8px;
            margin-bottom: 8px;
            letter-spacing: .04em;
            text-transform: uppercase;
        }}

        /* Tabelas */
        .tabela-wrap {{
            overflow-x: auto;
            border-radius: 10px;
            border: 1px solid var(--cinza-claro);
            margin: 14px 0;
        }}
        table.freq {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
            background: var(--branco);
            text-align: center;
        }}
        table.freq th {{
            background: var(--azul-escuro);
            color: var(--branco);
            padding: 12px 10px;
            font-weight: 600;
        }}
        table.freq td {{
            padding: 10px;
            border-bottom: 1px solid var(--cinza-claro);
            color: #1D2733;
        }}
        table.freq tr:nth-child(even) td {{
            background: var(--cinza-bg);
        }}
        table.freq tr.destaque-classe td {{
            background: var(--azul-gelo);
            font-weight: 700;
            color: var(--azul-escuro);
        }}
        table.freq tr.linha-total td {{
            background: var(--azul-medio);
            color: var(--branco);
            font-weight: 700;
        }}

        /* Q&A Cards */
        .qa-card {{
            background: #F8FAFD;
            border: 1px solid #DFE6EE;
            border-left: 5px solid var(--azul);
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 14px;
        }}
        .qa-pergunta {{
            color: var(--azul-escuro);
            font-size: 0.98rem;
            font-weight: 700;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .qa-badge {{
            background: var(--azul);
            color: var(--branco);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
            text-transform: uppercase;
            white-space: nowrap;
        }}
        .qa-resposta {{
            color: #2D3748;
            font-size: 0.94rem;
            line-height: 1.6;
        }}

        /* Rol */
        .rol-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin: 10px 0;
        }}
        .rol-item {{
            background: #F1F4F8;
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 0.85rem;
            color: #1D2733;
        }}
        .rol-item small {{
            color: var(--cinza);
            font-size: 0.68rem;
            margin-right: 4px;
        }}
        .rol-item.central {{
            background: var(--azul-escuro);
            color: var(--branco);
            font-weight: 700;
        }}
        .rol-item.central small {{
            color: var(--azul-claro);
        }}

        /* Gráficos */
        .grid-graficos {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 20px;
        }}
        .grafico-card {{
            background: var(--branco);
            border: 1px solid var(--cinza-claro);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 1px 4px rgba(11, 37, 69, 0.04);
        }}
        .grafico-card img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        .grafico-legenda {{
            color: var(--cinza);
            font-size: 0.85rem;
            margin-top: 10px;
        }}

        /* Grade de Cards Interativos (Aba 4) */
        .grid-editor-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 12px;
            margin-top: 16px;
        }}
        .card-atendimento {{
            background: var(--branco);
            border: 1px solid var(--cinza-claro);
            border-radius: 10px;
            padding: 10px 12px;
            box-shadow: 0 1px 3px rgba(11, 37, 69, 0.04);
            display: flex;
            flex-direction: column;
            gap: 6px;
            transition: all 0.2s ease;
        }}
        .card-atendimento:hover {{
            border-color: var(--azul);
            box-shadow: 0 3px 8px rgba(31, 111, 178, 0.12);
        }}
        .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .card-num {{
            background: var(--azul-gelo);
            color: var(--azul-escuro);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
            border: 1px solid #C8DCF0;
        }}
        .card-del {{
            background: none;
            border: none;
            color: var(--cinza);
            cursor: pointer;
            font-size: 0.85rem;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .card-del:hover {{
            color: #D32F2F;
            background: #FFEBEE;
        }}
        .card-input {{
            width: 100%;
            padding: 6px 8px;
            font-size: 1rem;
            font-weight: 600;
            color: var(--azul-escuro);
            border: 1px solid var(--cinza-claro);
            border-radius: 6px;
            text-align: center;
        }}
        .card-input:focus {{
            outline: none;
            border-color: var(--azul);
        }}
        .card-min {{
            color: var(--cinza);
            font-size: 0.75rem;
            text-align: right;
        }}

        /* Barra de Ferramentas */
        .toolbar {{
            background: var(--branco);
            border: 1px solid var(--cinza-claro);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 16px;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
        }}
        .tool-group {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .btn {{
            font-family: inherit;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }}
        .btn-primary {{
            background: var(--azul);
            color: var(--branco);
        }}
        .btn-primary:hover {{
            background: var(--azul-medio);
        }}
        .btn-secondary {{
            background: #F1F4F8;
            color: var(--texto);
            border-color: var(--cinza-claro);
        }}
        .btn-secondary:hover {{
            background: var(--cinza-claro);
        }}
        .btn-danger {{
            background: #FFF0F0;
            color: #D32F2F;
            border-color: #FFCDD2;
        }}
        .btn-danger:hover {{
            background: #D32F2F;
            color: var(--branco);
        }}

        /* Rodapé */
        .footer {{
            text-align: center;
            color: var(--cinza);
            font-size: 0.85rem;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--cinza-claro);
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Cabeçalho -->
        <header class="cabecalho">
            <h1>CALL CENTER ANALYTICS</h1>
            <p>Análise Estatística de Desempenho Operacional</p>
            <div class="tags-cabecalho">
                <span class="tag">⏱️ Tempos em segundos</span>
                <span class="tag">📊 Trabalho Avaliativo 3 – Estatística Descritiva</span>
                <span class="tag">🐍 Python · Pandas · Matplotlib · Streamlit</span>
            </div>
        </header>

        <!-- Card da Equipe -->
        <section class="equipe-card">
            <h3>👥 {GRUPO} – Integrantes:</h3>
            <ul class="lista-equipe">
                {lista_equipe_html}
            </ul>
        </section>

        <!-- Navegação em Abas -->
        <nav class="tabs-nav">
            <button class="tab-btn active" onclick="abrirAba(event, 'aba-dashboard')">📊 Dashboard</button>
            <button class="tab-btn" onclick="abrirAba(event, 'aba-distribuicao')">📋 Distribuição de Frequência</button>
            <button class="tab-btn" onclick="abrirAba(event, 'aba-graficos')">📈 Gráficos e Análise Visual</button>
            <button class="tab-btn" onclick="abrirAba(event, 'aba-editor')">✏️ Editar Dados ao Vivo</button>
        </nav>

        <!-- ABA 1: DASHBOARD -->
        <div id="aba-dashboard" class="tab-content active">
            <span class="etapa-badge">Etapa 1 — Indicadores Globais</span>
            <div class="grid-kpis">
                <div class="kpi-card">
                    <div class="kpi-rotulo">Total de Atendimentos</div>
                    <div class="kpi-valor">{ini['n']} <small>ligações</small></div>
                    <div class="kpi-nota">Amostra do estudo</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-rotulo">Menor / Maior Tempo</div>
                    <div class="kpi-valor">{fnum(ini['menor'])} / {fnum(ini['maior'])} <small>s</small></div>
                    <div class="kpi-nota">Extremos observados</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-rotulo">Amplitude Total</div>
                    <div class="kpi-valor">{fnum(ini['amplitude'])} <small>s</small></div>
                    <div class="kpi-nota">Maior − Menor</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-rotulo">Número de Classes</div>
                    <div class="kpi-valor">{r['k']} <small>classes</small></div>
                    <div class="kpi-nota">√{ini['n']} = {fmt(r['raiz'])} → {r['k']}</div>
                </div>
                <div class="kpi-card destaque">
                    <div class="kpi-rotulo">Média Aritmética</div>
                    <div class="kpi-valor">{fmt(m['media'])} <small>s</small></div>
                    <div class="kpi-nota">Σx ÷ n = {fmt(m['soma'])} ÷ {m['n']}</div>
                </div>
                <div class="kpi-card destaque">
                    <div class="kpi-rotulo">Mediana (Md)</div>
                    <div class="kpi-valor">{fmt(m['mediana'])} <small>s</small></div>
                    <div class="kpi-nota">(100 + 102) ÷ 2</div>
                </div>
                <div class="kpi-card destaque">
                    <div class="kpi-rotulo">Moda (Mo)</div>
                    <div class="kpi-valor" style="font-size: 1.35rem;">{texto_moda(m)}</div>
                    <div class="kpi-nota">Nenhum tempo se repete</div>
                </div>
            </div>

            <div class="secao-bloco">
                <h2 class="secao-titulo">🎯 Objetivo da Análise e Resumo Operacional</h2>
                <div class="caixa">
                    Avaliar o <b>Tempo Médio de Atendimento (TMA)</b> de <b>40 ligações</b> de um call center, identificando o tempo típico, a dispersão dos dados e os atendimentos que fogem ao padrão operacional.
                </div>
                <p style="margin-bottom: 8px;"><b>Forma da Distribuição:</b> A diferença entre média ({fmt(m['media'])} s) e mediana ({fmt(m['mediana'])} s) é de <b>{fmt(dif)} s</b>, indicando uma distribuição <b>{forma}</b>.</p>
                <p><b>Tempo típico:</b> Fica em torno de <b>{fnum(round(m['mediana']))} a {fnum(round(m['media']))} s</b> (cerca de 1,7 minuto por ligação).</p>
            </div>

            <div class="secao-bloco">
                <span class="etapa-badge">Etapa 5 — Questões de Interpretação</span>
                <h2 class="secao-titulo">💡 Respostas Oficiais da Interpretação</h2>
                <div class="qa-container">
                    {qa_html}
                </div>
            </div>
        </div>

        <!-- ABA 2: DISTRIBUIÇÃO DE FREQUÊNCIA -->
        <div id="aba-distribuicao" class="tab-content">
            <div class="secao-bloco">
                <span class="etapa-badge">Etapa 2 e 3 — Tabela de Frequência</span>
                <h2 class="secao-titulo">📋 Tabela de Distribuição de Frequências (k = 6 classes)</h2>
                <div class="caixa">
                    <b>Regras aplicadas:</b> k = √40 = 6,32 → <b>6 classes</b> (arredondamento clássico).<br>
                    <b>Amplitude de classe:</b> h = 148 ÷ 6 = 24,67 → arredondada para cima = <b>25 s</b>.<br>
                    O limite inferior pertence à classe e o superior não (notação <code>40 |— 65</code>).
                </div>

                <div class="tabela-wrap">
                    <table class="freq">
                        <thead>
                            <tr>
                                <th>Nº</th>
                                <th>Classe (s)</th>
                                <th>Soma dos dados (s)</th>
                                <th>Frequência Absoluta (FA)</th>
                                <th>Frequência Acumulada (FAA)</th>
                                <th>Frequência Relativa (FR)</th>
                                <th>Frequência Relativa Acum. (FRAA)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {linhas_tabela}
                        </tbody>
                    </table>
                </div>
                <p class="grafico-legenda">A classe em azul claro (90 |— 115 s) representa a classe modal, concentrando 27,50% de todos os atendimentos.</p>
            </div>

            <div class="secao-bloco">
                <h2 class="secao-titulo">🔢 Dados em Ordem Crescente (Rol de 40 Valores)</h2>
                <p style="font-size: 0.9rem; color: var(--cinza); margin-bottom: 10px;">Os dois valores centrais (20º e 21º) destacados em azul-escuro determinam a mediana:</p>
                <div class="rol-container">
                    {rol_html}
                </div>
            </div>
        </div>

        <!-- ABA 3: GRÁFICOS -->
        <div id="aba-graficos" class="tab-content">
            <span class="etapa-badge">Etapa 4 — Visualização Gráfica</span>
            <div class="grid-graficos">
                <div class="grafico-card">
                    <h3 style="color: var(--azul-escuro); margin-bottom: 8px;">Histograma de Frequência</h3>
                    <img src="data:image/png;base64,{hist_b64}" alt="Histograma de Atendimento">
                    <p class="grafico-legenda">Barras contíguas indicando a distribuição contínua dos tempos.</p>
                </div>
                <div class="grafico-card">
                    <h3 style="color: var(--azul-escuro); margin-bottom: 8px;">Frequência Absoluta (FA)</h3>
                    <img src="data:image/png;base64,{fa_b64}" alt="Frequência Absoluta">
                    <p class="grafico-legenda">Número absoluto de atendimentos em cada classe.</p>
                </div>
                <div class="grafico-card">
                    <h3 style="color: var(--azul-escuro); margin-bottom: 8px;">Frequência Relativa (FR %)</h3>
                    <img src="data:image/png;base64,{fr_b64}" alt="Frequência Relativa">
                    <p class="grafico-legenda">Representatividade percentual de cada classe no total.</p>
                </div>
                <div class="grafico-card">
                    <h3 style="color: var(--azul-escuro); margin-bottom: 8px;">Ogiva de Galton (FAA Acumulada)</h3>
                    <img src="data:image/png;base64,{ogiva_b64}" alt="Ogiva de Galton">
                    <p class="grafico-legenda">Curva ascendente demonstrando a evolução acumulada dos atendimentos.</p>
                </div>
            </div>
        </div>

        <!-- ABA 4: EDITAR DADOS AO VIVO -->
        <div id="aba-editor" class="tab-content">
            <span class="etapa-badge">Demonstração Interativa</span>
            <div class="secao-bloco">
                <h2 class="secao-titulo">✏️ Grade de Cards Interativa</h2>
                <div class="caixa">
                    Cada atendimento possui seu <b>próprio espaço e quadrado</b>. Você pode alterar qualquer valor diretamente no card, excluir atendimentos ou adicionar novas ligações.
                </div>

                <div class="toolbar">
                    <div class="tool-group">
                        <input type="number" id="novo-tempo-input" placeholder="Tempo (s)" value="100" min="1" max="999" style="width: 110px; padding: 7px 10px; border: 1px solid var(--cinza-claro); border-radius: 6px; font-size: 0.95rem;">
                        <button class="btn btn-primary" onclick="adicionarLigacao()">➕ Adicionar Ligação</button>
                    </div>
                    <div class="tool-group">
                        <button class="btn btn-secondary" onclick="restaurarValores()">↩️ Restaurar Originais (40)</button>
                        <button class="btn btn-danger" onclick="limparValores()">🗑️ Limpar Todos</button>
                    </div>
                </div>

                <div id="grid-cards-container" class="grid-editor-cards">
                    <!-- Cards dinâmicos inseridos via JS -->
                </div>
            </div>
        </div>

        <footer class="footer">
            <p>Trabalho Avaliativo em Grupo 3 – Estatística Descritiva · UNICA</p>
            <p>Desenvolvido em Python com Pandas, Matplotlib e Streamlit.</p>
        </footer>
    </div>

    <!-- Script de Interatividade das Abas e dos Cards -->
    <script>
        const DADOS_ORIGINAIS = {json.dumps(TEMPOS_ORIGINAIS)};
        let dadosAtuais = [...DADOS_ORIGINAIS];

        function abrirAba(evt, idAba) {{
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(c => c.classList.remove('active'));

            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(b => b.classList.remove('active'));

            document.getElementById(idAba).classList.add('active');
            evt.currentTarget.classList.add('active');
        }}

        function formatarMinutos(segundos) {{
            const min = Math.floor(segundos / 60);
            const seg = Math.floor(segundos % 60);
            return min > 0 ? `${{min}}m ${{String(seg).padStart(2, '0')}}s` : `${{seg}}s`;
        }}

        function renderizarCards() {{
            const container = document.getElementById('grid-cards-container');
            if (!container) return;
            container.innerHTML = '';

            dadosAtuais.forEach((val, idx) => {{
                const card = document.createElement('div');
                card.className = 'card-atendimento';
                card.innerHTML = `
                    <div class="card-top">
                        <span class="card-num">#${{String(idx + 1).padStart(2, '0')}}</span>
                        <button class="card-del" title="Excluir ligação" onclick="removerLigacao(${{idx}})">✕</button>
                    </div>
                    <input type="number" class="card-input" value="${{val}}" min="1" max="9999" onchange="atualizarLigacao(${{idx}}, this.value)">
                    <div class="card-min">⏱️ ${{formatarMinutos(val)}}</div>
                `;
                container.appendChild(card);
            }});
        }}

        function atualizarLigacao(idx, novoValor) {{
            const num = parseFloat(novoValor);
            if (num && num > 0) {{
                dadosAtuais[idx] = num;
                renderizarCards();
            }}
        }}

        function removerLigacao(idx) {{
            dadosAtuais.splice(idx, 1);
            renderizarCards();
        }}

        function adicionarLigacao() {{
            const input = document.getElementById('novo-tempo-input');
            const val = parseFloat(input.value);
            if (val && val > 0) {{
                dadosAtuais.push(val);
                renderizarCards();
                input.value = '100';
            }}
        }}

        function restaurarValores() {{
            dadosAtuais = [...DADOS_ORIGINAIS];
            renderizarCards();
        }}

        function limparValores() {{
            if (confirm('Tem certeza de que deseja apagar todos os atendimentos?')) {{
                dadosAtuais = [];
                renderizarCards();
            }}
        }}

        // Inicializar os cards
        document.addEventListener('DOMContentLoaded', () => {{
            renderizarCards();
        }});
    </script>
</body>
</html>
"""
    return html

if __name__ == "__main__":
    conteudo = gerar_site_completo()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("index.html gerado com sucesso!")
