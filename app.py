# -*- coding: utf-8 -*-
"""
=====================================================================
 CALL CENTER ANALYTICS
 Análise Estatística de Desempenho Operacional
---------------------------------------------------------------------
 Tema: Análise do tempo médio de atendimento (TMA) de um call center

 Bibliotecas utilizadas:
   - Pandas     -> organizar os dados e construir a tabela de frequências
   - Matplotlib -> elaborar o histograma e os demais gráficos
   - NumPy      -> apoio em cálculos numéricos
   - Streamlit  -> interface web (dashboard) do projeto

 Siglas usadas na tabela de distribuição de frequência:
   Σx   = soma dos dados que pertencem a cada classe
   FA   = Frequência Absoluta
   FAA  = Frequência Absoluta Acumulada
   FR   = Frequência Relativa (%)
   FRAA = Frequência Relativa Acumulada (%)

 Para executar:  streamlit run app.py
=====================================================================
"""

# ---------------------------------------------------------------------
# 0. IMPORTAÇÃO DAS BIBLIOTECAS
# ---------------------------------------------------------------------
import base64
import io
import math
from datetime import datetime

import matplotlib

matplotlib.use("Agg")  # backend sem janela (necessário para rodar dentro do Streamlit)
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------
# 1. CONFIGURAÇÕES GERAIS
# ---------------------------------------------------------------------

# Dados originais do trabalho: 40 tempos de atendimento, em SEGUNDOS.
TEMPOS_ORIGINAIS = [
    40, 44, 49, 55, 62,
    65, 68, 71, 74, 77, 80, 83, 86, 89, 90, 92, 94,
    96, 98, 100, 102, 104, 106, 108, 110, 115, 118,
    121, 124, 127, 130, 133, 136,
    139, 142, 148, 155,
    163, 171, 188,
]

# Identificação do grupo (aparece no relatório gerado)
GRUPO = "Trabalho Avaliativo – Grupo 3"
INTEGRANTES = [
    "Riann Matheus Dias da Costa – Sistemas de Informação",
    "Carlos Rafael Pagung Silva – Sistemas de Informação",
    "Gabriel Lima Souza – Sistemas de Informação",
    "Marcos Antônio Silva Sena – Ciência da Computação",
    "Gabrielle Fernanda Carvalho Ventura – Ciência da Computação",
    "Victor Augusto Ferreira – Ciência da Computação",
    "Kauã Pedro Ferreira Araújo – Ciência da Computação",
    "João Pedro Alves Sampaio – Ciência da Computação",
    "Maria Eduarda Martins Santos – Ciência da Computação",
    "João Victor Alves Nascimento – Sistemas de Informação",
]

UNIDADE = "s"               # unidade de medida dos tempos (segundos)
COLUNA = "Tempo (s)"        # nome da coluna na tabela editável

# Paleta de cores da identidade visual (azul-escuro, azul-claro, branco e cinza)
AZUL_ESCURO = "#0B2545"
AZUL_MEDIO = "#13315C"
AZUL = "#1F6FB2"
AZUL_CLARO = "#8DB8E0"
AZUL_GELO = "#EAF2FB"
CINZA = "#6B7785"
CINZA_CLARO = "#E4E8EE"
BRANCO = "#FFFFFF"

# Configuração da página do Streamlit (título da aba do navegador e layout largo)
st.set_page_config(
    page_title="Call Center Analytics",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------
# 2. ESTILO VISUAL (CSS)
#    Define fontes, cores, cartões de indicadores e tabelas.
# ---------------------------------------------------------------------
def aplicar_estilo():
    """Injeta o CSS que dá a aparência de dashboard profissional."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"], .stMarkdown, .stText, button, input {{
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{ padding-top: 3.5rem; padding-bottom: 3rem; max-width: 1300px; }}

        /* Menu lateral */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {AZUL_ESCURO} 0%, {AZUL_MEDIO} 100%);
        }}
        section[data-testid="stSidebar"] * {{ color: {BRANCO} !important; }}
        section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,.18); }}

        /* Cabeçalho */
        .cabecalho {{
            background: linear-gradient(120deg, {AZUL_ESCURO} 0%, {AZUL_MEDIO} 55%, {AZUL} 100%);
            border-radius: 16px;
            padding: 24px 28px;
            color: {BRANCO};
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(11,37,69, 0.12);
        }}
        .cabecalho h1 {{
            color: {BRANCO} !important;
            font-size: 1.95rem;
            font-weight: 800;
            letter-spacing: .05em;
            margin: 0;
            padding: 0;
            line-height: 1.25;
        }}
        .cabecalho p {{
            color: {AZUL_CLARO};
            margin: 6px 0 14px 0;
            font-size: 1.05rem;
            font-weight: 500;
        }}
        .tags-cabecalho {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}
        .cabecalho .tag {{
            display: inline-flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.16);
            color: {BRANCO};
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 999px;
            padding: 5px 14px;
            font-size: 0.82rem;
            font-weight: 500;
        }}

        /* Cartões de indicadores (KPIs) */
        .grade-kpi {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(165px, 1fr)); gap: 14px; margin: 6px 0 18px 0; }}
        .kpi {{
            background:{BRANCO}; border:1px solid {CINZA_CLARO}; border-radius: 14px;
            padding: 16px 18px; box-shadow: 0 1px 3px rgba(11,37,69,.06); border-top: 4px solid {AZUL};
        }}
        .kpi.destaque {{ border-top-color: {AZUL_ESCURO}; background: {AZUL_GELO}; }}
        .kpi .rotulo {{ color:{CINZA}; font-size:.78rem; text-transform: uppercase; letter-spacing:.05em; font-weight:600; }}
        .kpi .valor {{ color:{AZUL_ESCURO}; font-size:1.65rem; font-weight:800; margin-top: 4px; line-height:1.15; }}
        .kpi .valor small {{ font-size: .9rem; color:{CINZA}; font-weight:600; }}
        .kpi .nota {{ color:{CINZA}; font-size:.78rem; margin-top: 4px; }}

        /* Caixas de texto explicativo */
        .caixa {{
            background:{AZUL_GELO}; border-left: 5px solid {AZUL}; border-radius: 10px;
            padding: 14px 18px; margin: 10px 0 16px 0; color:{AZUL_ESCURO};
        }}
        .caixa.cinza {{ background:#F4F6F9; border-left-color:{CINZA}; }}
        .caixa b {{ color:{AZUL_ESCURO}; }}
        .etapa {{
            display:inline-block; background:{AZUL_ESCURO}; color:{BRANCO}; font-size:.72rem;
            font-weight:700; border-radius: 6px; padding: 2px 8px; margin-bottom: 6px; letter-spacing:.04em;
        }}

        /* Tabela de distribuição de frequência */
        table.freq {{ width:100%; border-collapse: collapse; font-size: .95rem; background:{BRANCO};
                      border-radius: 12px; overflow:hidden; box-shadow: 0 1px 3px rgba(11,37,69,.08); }}
        table.freq th {{ background:{AZUL_ESCURO}; color:{BRANCO}; padding: 11px 10px; text-align:center; font-weight:600; }}
        table.freq td {{ padding: 9px 10px; text-align:center; border-bottom: 1px solid {CINZA_CLARO}; color:#1d2733; }}
        table.freq tr:nth-child(even) td {{ background: #F7F9FC; }}
        table.freq tr.maior td {{ background: {AZUL_GELO}; font-weight:700; color:{AZUL_ESCURO}; }}
        table.freq tr.total td {{ background:{AZUL_MEDIO}; color:{BRANCO}; font-weight:700; }}
        .tabela-wrap {{ overflow-x:auto; }}

        /* Dados em ordem crescente (rol) - usado na explicação da mediana */
        .rol {{ display:flex; flex-wrap:wrap; gap:6px; margin: 8px 0 6px 0; }}
        .rol span {{ background:#F1F4F8; border-radius:6px; padding:4px 8px; font-size:.85rem; color:#1d2733; }}
        .rol span small {{ color:{CINZA}; font-size:.68rem; margin-right:3px; }}
        .rol span.central {{ background:{AZUL_ESCURO}; color:{BRANCO}; font-weight:700; }}
        .rol span.central small {{ color:{AZUL_CLARO}; }}

        /* Abas (role="tab" funciona em versões novas e antigas do Streamlit) */
        .stTabs [role="tablist"] {{ gap: 6px; flex-wrap: wrap; }}
        .stTabs [role="tab"] {{
            background: #F1F4F8; border-radius: 10px 10px 0 0; padding: 10px 18px; font-weight: 600;
        }}
        .stTabs [role="tab"][aria-selected="true"] {{ background: {AZUL_ESCURO} !important; color: {BRANCO} !important; }}
        .stTabs [role="tab"][aria-selected="true"] p {{ color: {BRANCO} !important; }}

        h2, h3 {{ color: {AZUL_ESCURO}; }}

        /* Cards da Grade de Atendimentos (Aba Editar Dados) */
        .badge-card {{
            background: {AZUL_GELO};
            color: {AZUL_ESCURO};
            font-size: 0.78rem;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
            border: 1px solid #C8DCF0;
            display: inline-block;
        }}
        .tempo-conversao {{
            color: {CINZA};
            font-size: 0.75rem;
            font-weight: 500;
            margin-top: 3px;
            text-align: right;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# 3. FUNÇÕES DE FORMATAÇÃO (padrão brasileiro: vírgula como decimal)
# ---------------------------------------------------------------------
def fmt(valor, casas=2):
    """Formata um número no padrão brasileiro. Ex.: 1234.5 -> '1.234,50'."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def fnum(valor):
    """Mostra inteiros sem casas decimais e decimais com até 2 casas."""
    valor = float(valor)
    if valor.is_integer():
        return fmt(valor, 0)
    return fmt(valor, 2).rstrip("0").rstrip(",")


def ltx(valor, casas=2):
    """Número formatado para uso dentro de fórmulas LaTeX (vírgula decimal sem espaçamento)."""
    return fmt(valor, casas).replace(",", "{,}")


def fpct(valor):
    """Formata percentual. Ex.: 27.5 -> '27,50%'."""
    return f"{fmt(valor, 2)}%"


# ---------------------------------------------------------------------
# 4. VALIDAÇÃO DOS DADOS
#    Aceita somente números positivos e ignora células vazias.
# ---------------------------------------------------------------------
def validar_dados(df):
    """
    Recebe o DataFrame da tabela editável e devolve:
      - lista com os tempos válidos (números > 0)
      - lista de mensagens de aviso sobre valores descartados
    """
    avisos = []
    if df is None or df.empty or COLUNA not in df.columns:
        return [], avisos

    # Converte para número; textos ou valores inválidos viram NaN
    serie = pd.to_numeric(df[COLUNA], errors="coerce")

    vazios = int(serie.isna().sum())
    nao_positivos = int((serie <= 0).sum())

    if vazios:
        avisos.append(f"{vazios} linha(s) vazia(s) ou inválida(s) foram ignoradas.")
    if nao_positivos:
        avisos.append(f"{nao_positivos} valor(es) menor(es) ou igual(is) a zero foram ignorados "
                      "(o tempo de atendimento precisa ser positivo).")

    validos = serie[serie > 0].dropna().astype(float).tolist()
    return validos, avisos


# ---------------------------------------------------------------------
# 5. CÁLCULOS ESTATÍSTICOS
# ---------------------------------------------------------------------

# 5.1 ETAPA 1 - organização e análise inicial dos dados
def medidas_iniciais(serie):
    """Calcula total, menor valor, maior valor e amplitude total usando Pandas."""
    menor = serie.min()                  # menor valor do conjunto
    maior = serie.max()                  # maior valor do conjunto
    amplitude = maior - menor            # Amplitude total = Maior valor - Menor valor
    return {"n": int(serie.count()), "menor": float(menor),
            "maior": float(maior), "amplitude": float(amplitude)}


# 5.2 ETAPA 3 - média, mediana e moda SIMPLES (calculadas com os 40 valores)
def medidas_simples(serie):
    """
    Média aritmética simples : soma de todos os valores ÷ quantidade de valores
    Mediana simples          : valor central dos dados em ordem crescente
                               (quantidade par -> média dos dois valores centrais)
    Moda simples             : valor que mais se repete (pode não existir)
    """
    n = int(serie.count())
    dados = serie.sort_values().reset_index(drop=True)   # rol: dados em ordem crescente

    # ---- Média aritmética simples ----
    soma = float(dados.sum())
    media = soma / n

    # ---- Mediana simples ----
    if n % 2 == 0:
        # Quantidade PAR: posições n/2 e n/2 + 1 (contando a partir de 1)
        posicoes = [n // 2, n // 2 + 1]
        centrais = [float(dados.iloc[p - 1]) for p in posicoes]
        mediana = sum(centrais) / 2
    else:
        # Quantidade ÍMPAR: posição (n + 1) / 2
        posicoes = [(n + 1) // 2]
        centrais = [float(dados.iloc[posicoes[0] - 1])]
        mediana = centrais[0]

    # ---- Moda simples ----
    contagem = dados.value_counts()                      # quantas vezes cada valor aparece
    maior_rep = int(contagem.max())
    if maior_rep == 1 and n > 1:
        modas = []                                       # nenhum valor se repete -> amodal
    else:
        modas = sorted(contagem[contagem == maior_rep].index.tolist())

    # Desvio padrão: usado apenas para comparar média e mediana na interpretação
    desvio = float(dados.std(ddof=1)) if n > 1 else 0.0

    return {"n": n, "soma": soma, "media": media,
            "posicoes": posicoes, "centrais": centrais, "mediana": mediana,
            "modas": modas, "rep_moda": maior_rep, "desvio": desvio}


# 5.3 ETAPA 2 - definição das classes (amplitude de classe e limites)
def passo_dos_dados(serie):
    """Descobre a 'precisão' dos dados: 1 para inteiros, 0,1 ou 0,01 para decimais."""
    if all(float(v).is_integer() for v in serie):
        return 1.0
    if all(float(round(v, 1)) == float(v) for v in serie):
        return 0.1
    return 0.01


def definir_classes(serie, k):
    """
    Calcula a amplitude de classe (h) e os limites de cada classe.
      h = Amplitude total / número de classes, arredondado PARA CIMA
      A primeira classe começa no menor valor (40 nos dados originais).
    Como o limite superior NÃO pertence à classe ( 40 |— 65 ),
    garantimos que o maior valor fique dentro da última classe.
    """
    menor, maior = float(serie.min()), float(serie.max())
    amplitude = maior - menor
    passo = passo_dos_dados(serie)

    h_bruto = amplitude / k if k else 0
    h = math.ceil(round(h_bruto / passo, 6)) * passo if amplitude > 0 else passo
    # Se o maior valor cair exatamente no limite superior da última classe,
    # ele ficaria de fora (limite superior aberto). Por isso aumentamos h.
    if menor + k * h <= maior:
        h += passo
    h = round(h, 2)

    limites = [round(menor + i * h, 2) for i in range(k + 1)]
    return h_bruto, h, limites


# 5.4 ETAPA 2 - tabela de distribuição de frequência (Pandas)
def tabela_frequencia(serie, k):
    """
    Monta a distribuição de frequência com Pandas:
      Soma  = soma dos dados que pertencem à classe (o total é a soma de todos os dados)
      FA    = frequência absoluta (quantidade de valores na classe)
      FAA   = frequência absoluta acumulada
      FR    = frequência relativa (%) = FA / N x 100
      FRAA  = frequência relativa acumulada (%)
    """
    h_bruto, h, limites = definir_classes(serie, k)
    n = len(serie)

    # pd.cut distribui cada valor em sua classe.
    # right=False -> intervalo fechado à esquerda e aberto à direita: [40, 65)  =  40 |— 65
    categorias = pd.cut(serie, bins=limites, right=False)
    fa = categorias.value_counts(sort=False).values
    # groupby soma os valores que caíram em cada classe
    soma_classe = serie.groupby(categorias, observed=False).sum().values

    tabela = pd.DataFrame({
        "Li": limites[:-1],                       # limite inferior
        "Ls": limites[1:],                        # limite superior
    })
    tabela["Classe"] = [f"{fnum(a)} |— {fnum(b)}" for a, b in zip(tabela["Li"], tabela["Ls"])]
    tabela["Soma"] = soma_classe                          # soma dos dados de cada classe
    tabela["FA"] = fa.astype(int)                         # frequência absoluta
    tabela["FAA"] = tabela["FA"].cumsum()                 # frequência absoluta acumulada
    tabela["FR (%)"] = tabela["FA"] / n * 100             # frequência relativa
    tabela["FRAA (%)"] = tabela["FR (%)"].cumsum()        # frequência relativa acumulada

    return tabela, h_bruto, h, limites


# 5.5 ETAPA 2 - número de classes (obrigatório): k = √n com arredondamento CLÁSSICO
def numero_de_classes(n):
    """
    Calcula o número de classes pela regra da raiz quadrada:
      k = √n, arredondado pela regra clássica:
        parte decimal menor que 0,5 -> arredonda para baixo
        parte decimal 0,5 ou maior  -> arredonda para cima
      Ex.: n = 40 -> √40 = 6,32 -> k = 6 classes.
    """
    raiz = math.sqrt(n)            # raiz quadrada do total de observações
    # Arredondamento clássico. (A função round() do Python usa o "arredondamento do banqueiro",
    # que leva 6,5 para 6; por isso usamos floor(x + 0,5), que leva 6,5 para 7.)
    k = math.floor(round(raiz, 9) + 0.5)
    return raiz, max(1, k)


# 5.6 Função principal: executa TODA a análise para um conjunto de dados
def analisar(tempos):
    """Recebe a lista de tempos e devolve todos os resultados da análise."""
    if len(tempos) == 0:
        return None
    serie = pd.Series(sorted(tempos), name=COLUNA, dtype=float)   # dados em ordem crescente
    raiz, k = numero_de_classes(len(serie))                       # k = √n (arredondamento clássico)
    ini = medidas_iniciais(serie)
    medidas = medidas_simples(serie)
    tabela, h_bruto, h, limites = tabela_frequencia(serie, k)

    # Classe(s) com a maior frequência absoluta (pode haver empate)
    maior_fa = int(tabela["FA"].max())
    maiores = [i for i, f in enumerate(tabela["FA"]) if f == maior_fa]

    return {"serie": serie, "k": k, "raiz": raiz, "ini": ini, "med": medidas, "tabela": tabela,
            "h_bruto": h_bruto, "h": h, "limites": limites, "maiores": maiores}


# ---------------------------------------------------------------------
# 6. INTERPRETAÇÃO AUTOMÁTICA DOS RESULTADOS
#    Gera textos que mudam de acordo com os dados analisados.
# ---------------------------------------------------------------------
def texto_moda(m):
    """Descreve a moda simples (pode ser amodal, unimodal ou com várias modas)."""
    if not m["modas"]:
        return "Amodal"
    return " e ".join(f"{fnum(v)} {UNIDADE}" for v in m["modas"])


def comparar_media_mediana(r):
    """Compara média e mediana para descrever a forma (simetria) da distribuição."""
    m = r["med"]
    dif = m["media"] - m["mediana"]
    rel = dif / m["desvio"] if m["desvio"] else 0
    if abs(rel) < 0.1:
        forma = "praticamente simétrica"
        if dif > 0:
            forma += ", com leve tendência à direita (alguns atendimentos mais longos puxam a média para cima)"
        elif dif < 0:
            forma += ", com leve tendência à esquerda"
    elif dif > 0:
        forma = ("assimétrica à direita: existem atendimentos bem mais demorados que "
                 "elevam a média acima da mediana")
    else:
        forma = ("assimétrica à esquerda: existem atendimentos bem mais rápidos que "
                 "reduzem a média abaixo da mediana")
    return dif, forma


# Perguntas da Etapa 5 (as chaves são só identificadores internos, não aparecem na tela)
PERGUNTAS = {
    "11": "Qual intervalo apresentou a maior quantidade de atendimentos?",
    "12": "Qual foi o percentual de atendimentos nessa classe?",
    "13": "O que a frequência acumulada permite identificar sobre os tempos de atendimento?",
    "14": "O que a média, a mediana e a moda indicam sobre o comportamento dos tempos analisados?",
    "15": "Com base na tabela e no histograma, qual conclusão você apresenta sobre a distribuição?",
}


def respostas_interpretacao(r):
    """Respostas automáticas para as questões da Etapa 5 do roteiro (11 a 15)."""
    t, m, ini = r["tabela"], r["med"], r["ini"]
    i_mx = r["maiores"][0]
    classe_mx = t["Classe"].iloc[i_mx]
    fa_mx = int(t["FA"].iloc[i_mx])
    fr_mx = float(t["FR (%)"].iloc[i_mx])
    outras = [t["Classe"].iloc[i] for i in r["maiores"][1:]]
    extra = (f" (empatada com {', '.join(outras)})" if outras else "")

    # Questão 13: primeira classe em que a FAA alcança pelo menos metade dos atendimentos
    i_meio = int(np.argmax(t["FAA"].values >= ini["n"] / 2))
    lim_meio = t["Ls"].iloc[i_meio]
    faa_meio = int(t["FAA"].iloc[i_meio])
    fraa_meio = float(t["FRAA (%)"].iloc[i_meio])

    dif, forma = comparar_media_mediana(r)
    if m["modas"]:
        txt_moda = (f"a moda é <b>{texto_moda(m)}</b> (aparece {m['rep_moda']} vezes), "
                    "indicando o tempo mais recorrente")
    else:
        txt_moda = ("<b>não há moda</b> (conjunto amodal), pois nenhum tempo se repete; "
                    f"a maior concentração aparece na classe <b>{classe_mx} {UNIDADE}</b>")

    ult_li = t["Li"].iloc[-2] if len(t) > 1 else ini["menor"]
    acima = int((r["serie"] >= ult_li).sum())

    q11 = (f"A classe <b>{classe_mx} {UNIDADE}</b> apresentou a maior quantidade de atendimentos: "
           f"<b>{fa_mx}</b> ligações{extra}.")
    q12 = (f"Essa classe concentra <b>{fpct(fr_mx)}</b> dos atendimentos "
           f"(FR = {fa_mx} ÷ {ini['n']} × 100).")
    q13 = (f"A frequência acumulada mostra <b>quantos atendimentos terminaram até determinado tempo</b>. "
           f"Por exemplo, <b>{faa_meio} atendimentos ({fpct(fraa_meio)})</b> duraram menos de "
           f"<b>{fnum(lim_meio)} {UNIDADE}</b>, ou seja, mais da metade das ligações termina antes desse "
           f"tempo. Com ela a empresa sabe que percentual das ligações foi resolvido abaixo de um tempo-limite.")
    q14 = (f"A média é <b>{fmt(m['media'])} {UNIDADE}</b> e a mediana é <b>{fmt(m['mediana'])} {UNIDADE}</b>; "
           f"{txt_moda}. A diferença entre média e mediana é de {fmt(dif)} {UNIDADE}, o que indica uma "
           f"distribuição <b>{forma}</b>. O tempo típico de atendimento fica em torno de "
           f"<b>{fnum(round(m['mediana']))} a {fnum(round(m['media']))} {UNIDADE}</b>.")
    q15 = (f"Os tempos variam de {fnum(ini['menor'])} a {fnum(ini['maior'])} {UNIDADE} "
           f"(amplitude de {fnum(ini['amplitude'])} {UNIDADE}). A maior concentração está na classe "
           f"<b>{classe_mx} {UNIDADE}</b>, perto da média e da mediana. As classes finais têm poucas ligações "
           f"({acima} atendimento(s) a partir de {fnum(ult_li)} {UNIDADE}), que merecem atenção da gestão "
           f"por elevarem o TMA. Em geral, a operação mostra um padrão de atendimento consistente, com a "
           f"maioria das ligações próxima do tempo médio.")
    return {"11": q11, "12": q12, "13": q13, "14": q14, "15": q15}


# ---------------------------------------------------------------------
# 7. COMPONENTES VISUAIS (cartões, tabelas, caixas de texto)
# ---------------------------------------------------------------------
def cartao(rotulo, valor, nota="", destaque=False):
    """Gera o HTML de um cartão de indicador (KPI)."""
    classe = "kpi destaque" if destaque else "kpi"
    return (f'<div class="{classe}"><div class="rotulo">{rotulo}</div>'
            f'<div class="valor">{valor}</div><div class="nota">{nota}</div></div>')


def grade_cartoes(cartoes):
    """Agrupa vários cartões em uma grade responsiva."""
    st.markdown(f'<div class="grade-kpi">{"".join(cartoes)}</div>', unsafe_allow_html=True)


def caixa(html, tipo=""):
    """Caixa de texto explicativo."""
    st.markdown(f'<div class="caixa {tipo}">{html}</div>', unsafe_allow_html=True)


def tabela_html(r):
    """Converte a tabela de frequência do Pandas em HTML formatado, com linha de TOTAL."""
    t = r["tabela"]
    linhas = []
    for i, row in t.iterrows():
        css = ' class="maior"' if i in r["maiores"] else ""
        linhas.append(
            f"<tr{css}><td>{i + 1}</td><td>{row['Classe']}</td>"
            f"<td>{fnum(row['Soma'])}</td><td>{int(row['FA'])}</td><td>{int(row['FAA'])}</td>"
            f"<td>{fpct(row['FR (%)'])}</td><td>{fpct(row['FRAA (%)'])}</td></tr>"
        )
    # Linha de total (Σ dados = soma de todas as observações, Σ FA = N e Σ FR = 100%)
    linhas.append(
        f'<tr class="total"><td colspan="2">TOTAL</td><td>{fnum(t["Soma"].sum())}</td>'
        f'<td>{int(t["FA"].sum())}</td><td>—</td><td>{fpct(t["FR (%)"].sum())}</td><td>—</td></tr>'
    )
    cab = ("<tr><th>Nº</th><th>Classe (s)</th><th>Soma dos dados (s)</th><th>FA</th>"
           "<th>FAA</th><th>FR (%)</th><th>FRAA (%)</th></tr>")
    return f'<div class="tabela-wrap"><table class="freq">{cab}{"".join(linhas)}</table></div>'


def rol_html(r):
    """Mostra os dados em ordem crescente (rol), destacando o(s) valor(es) central(is) da mediana."""
    pos = r["med"]["posicoes"]
    itens = []
    for i, v in enumerate(r["serie"], start=1):
        css = ' class="central"' if i in pos else ""
        itens.append(f"<span{css}><small>{i}º</small>{fnum(v)}</span>")
    return f'<div class="rol">{"".join(itens)}</div>'


def tabela_exportacao(r):
    """Versão da tabela para exportar em CSV (com linha de total)."""
    t = r["tabela"]
    exp = t[["Classe", "Soma", "FA", "FAA", "FR (%)", "FRAA (%)"]].copy()
    exp = exp.rename(columns={"Classe": "Classe (s)", "Soma": "Soma dos dados (s)"})
    total = pd.DataFrame([{"Classe (s)": "TOTAL", "Soma dos dados (s)": exp["Soma dos dados (s)"].sum(),
                           "FA": exp["FA"].sum(), "FAA": None, "FR (%)": exp["FR (%)"].sum(),
                           "FRAA (%)": None}])
    return pd.concat([exp, total], ignore_index=True).round(2)


def para_csv(df):
    """Converte DataFrame em CSV compatível com o Excel em português (';' e vírgula decimal)."""
    return df.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")


# ---------------------------------------------------------------------
# 8. GRÁFICOS COM MATPLOTLIB
# ---------------------------------------------------------------------
def estilo_eixos(ax, titulo, xlabel, ylabel):
    """Padroniza título, rótulos, grade e bordas dos gráficos."""
    ax.set_title(titulo, fontsize=13, fontweight="bold", color=AZUL_ESCURO, pad=14)
    ax.set_xlabel(xlabel, fontsize=10.5, color=CINZA)
    ax.set_ylabel(ylabel, fontsize=10.5, color=CINZA)
    ax.grid(axis="y", color=CINZA_CLARO, linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#B8C2CE")
    ax.tick_params(colors="#3A4654", labelsize=9.5)


def grafico_histograma(r):
    """
    ETAPA 4 - Histograma: barras encostadas, uma para cada classe.
    Eixo X = intervalos de classe | Eixo Y = frequência absoluta (FA).
    """
    t, h = r["tabela"], r["h"]
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=110)
    cores = [AZUL_ESCURO if i in r["maiores"] else AZUL for i in range(len(t))]
    barras = ax.bar(t["Li"], t["FA"], width=h, align="edge", color=cores,
                    edgecolor=BRANCO, linewidth=1.6, label="Frequência absoluta (FA)")
    # Valores identificados em cima de cada barra
    for barra, fa in zip(barras, t["FA"]):
        ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.15, str(int(fa)),
                ha="center", va="bottom", fontsize=11, fontweight="bold", color=AZUL_ESCURO)
    # Eixo X com os limites das classes
    ax.set_xticks(r["limites"])
    ax.set_xticklabels([fnum(v) for v in r["limites"]])
    ax.set_ylim(0, max(t["FA"]) * 1.2 + 0.5)
    estilo_eixos(ax, "Histograma — Distribuição dos tempos de atendimento",
                 "Tempo de atendimento (segundos) — intervalos de classe",
                 "Quantidade de atendimentos (FA)")
    alcas, _ = ax.get_legend_handles_labels()
    alcas.append(Patch(color=AZUL_ESCURO, label="Classe com maior FA"))
    ax.legend(handles=alcas, frameon=False, fontsize=9, loc="upper right")
    fig.tight_layout()
    return fig


def grafico_barras(r, coluna, titulo, ylabel, percentual=False):
    """Gráfico de barras separadas por classe (frequência absoluta ou relativa)."""
    t = r["tabela"]
    fig, ax = plt.subplots(figsize=(7, 4.6), dpi=110)
    cores = [AZUL_ESCURO if i in r["maiores"] else AZUL_CLARO for i in range(len(t))]
    barras = ax.bar(t["Classe"], t[coluna], color=cores, edgecolor=AZUL_MEDIO, linewidth=0.8, width=0.65)
    for barra, v in zip(barras, t[coluna]):
        texto = fpct(v) if percentual else str(int(v))
        ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height(), texto,
                ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=AZUL_ESCURO)
    ax.set_ylim(0, max(t[coluna]) * 1.2 + (1 if percentual else 0.5))
    estilo_eixos(ax, titulo, "Intervalo de classe (segundos)", ylabel)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    return fig


def grafico_ogiva(r):
    """Ogiva: curva da frequência relativa acumulada (FRAA) nos limites superiores."""
    t = r["tabela"]
    x = [t["Li"].iloc[0]] + t["Ls"].tolist()
    y = [0] + t["FRAA (%)"].tolist()
    fig, ax = plt.subplots(figsize=(10, 4.4), dpi=110)
    ax.plot(x, y, marker="o", color=AZUL_ESCURO, linewidth=2.2, markerfacecolor=AZUL_CLARO,
            label="Frequência relativa acumulada (FRAA)")
    ax.fill_between(x, y, color=AZUL_CLARO, alpha=0.25)
    for xi, yi in zip(x[1:], y[1:]):
        ax.annotate(fpct(yi), (xi, yi), textcoords="offset points", xytext=(0, 8),
                    ha="center", fontsize=9, color=AZUL_ESCURO)
    ax.axhline(50, color=CINZA, linestyle=":", linewidth=1.2, label="50% dos atendimentos")
    ax.set_xticks(x)
    ax.set_xticklabels([fnum(v) for v in x])
    ax.set_ylim(0, 112)
    estilo_eixos(ax, "Ogiva — Frequência relativa acumulada (FRAA)",
                 "Tempo de atendimento (segundos)", "Atendimentos acumulados (%)")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.tight_layout()
    return fig


def figura_para_png(fig):
    """Converte uma figura do Matplotlib em bytes PNG (para download e relatório)."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    return buf.getvalue()


def mostrar_figura(fig):
    """Exibe a figura no Streamlit e libera a memória."""
    st.pyplot(fig, width="stretch")
    plt.close(fig)


# ---------------------------------------------------------------------
# 9. RELATÓRIO RESUMIDO (arquivo HTML para download)
# ---------------------------------------------------------------------
def texto_mediana(m):
    """Texto da conta da mediana com os valores substituídos."""
    if len(m["posicoes"]) == 2:
        p1, p2 = m["posicoes"]
        v1, v2 = m["centrais"]
        return (f"n = {m['n']} (par) → Md = ({p1}º valor + {p2}º valor) ÷ 2 = "
                f"({fnum(v1)} + {fnum(v2)}) ÷ 2 = <b>{fmt(m['mediana'])} s</b>")
    return f"n = {m['n']} (ímpar) → Md = {m['posicoes'][0]}º valor = <b>{fmt(m['mediana'])} s</b>"


def gerar_relatorio(r):
    """Cria um relatório HTML completo com dados, tabela, medidas, histograma e interpretação."""
    ini, m = r["ini"], r["med"]
    fig = grafico_histograma(r)
    png = base64.b64encode(figura_para_png(fig)).decode()
    plt.close(fig)
    resp = respostas_interpretacao(r)
    dados_txt = ", ".join(fnum(v) for v in r["serie"])
    moda_txt = (f"<b>{texto_moda(m)}</b> (aparece {m['rep_moda']} vezes)" if m["modas"]
                else "<b>Amodal</b>: nenhum tempo se repete")
    itens_qa = "".join(
        f'<div class="qa-card">'
        f'<div class="qa-pergunta"><span class="qa-badge">Questão {i}</span><span>{PERGUNTAS[k]}</span></div>'
        f'<div class="qa-resposta">{resp[k]}</div>'
        f'</div>'
        for i, k in enumerate(PERGUNTAS, 1)
    )
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Relatório - Call Center Analytics</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;color:#1d2733;max-width:900px;margin:30px auto;padding:0 18px;line-height:1.5}}
h1{{color:{AZUL_ESCURO};margin-bottom:0}}
h2{{color:{AZUL_MEDIO};border-bottom:2px solid {AZUL_CLARO};padding-bottom:6px;margin-top:32px;margin-bottom:14px}}
table{{border-collapse:collapse;width:100%;margin:12px 0}}
th{{background:{AZUL_ESCURO};color:#fff;padding:8px}}
td{{padding:7px;text-align:center;border-bottom:1px solid #ddd}}
tr.maior td{{background:{AZUL_GELO};font-weight:bold}}
tr.total td{{background:{AZUL_MEDIO};color:#fff;font-weight:bold}}
.sub{{color:{CINZA}}}
img{{max-width:100%;border-radius:4px;box-shadow:0 1px 4px rgba(0,0,0,0.08)}}

/* Formatação da seção de interpretação (perguntas e respostas) */
.qa-card {{
    background: #F8FAFD;
    border: 1px solid #DFE6EE;
    border-left: 5px solid {AZUL};
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 16px;
    page-break-inside: avoid;
}}
.qa-pergunta {{
    color: {AZUL_ESCURO};
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.qa-badge {{
    background: {AZUL};
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 12px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
}}
.qa-resposta {{
    color: #2D3748;
    font-size: 14.5px;
    line-height: 1.65;
    padding-left: 2px;
}}

/* Identificação da equipe */
.equipe-card {{
    background: #F8FAFD;
    border: 1px solid #DFE6EE;
    border-left: 5px solid {AZUL};
    border-radius: 6px;
    padding: 14px 18px;
    margin: 16px 0 24px 0;
}}
.equipe-card h3 {{
    color: {AZUL_ESCURO};
    font-size: 15px;
    margin: 0 0 8px 0;
}}
.lista-integrantes {{
    margin: 0;
    padding-left: 20px;
    color: #2D3748;
    font-size: 13.5px;
    line-height: 1.6;
}}
</style></head><body>
<h1>CALL CENTER ANALYTICS</h1><p class="sub">Análise Estatística de Desempenho Operacional —
gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
<div class="equipe-card">
    <h3>👥 {GRUPO} – Integrantes:</h3>
    <ol class="lista-integrantes">
        {"".join(f"<li><b>{item.split(' – ')[0]}</b> — <span style='color:{CINZA}'>{item.split(' – ')[1]}</span></li>" for item in INTEGRANTES)}
    </ol>
</div>
<h2>1. Dados utilizados ({ini['n']} atendimentos, em segundos)</h2><p>{dados_txt}</p>
<h2>2. Organização inicial</h2>
<p>Menor valor: <b>{fnum(ini['menor'])} s</b> · Maior valor: <b>{fnum(ini['maior'])} s</b> ·
Amplitude total: {fnum(ini['maior'])} − {fnum(ini['menor'])} = <b>{fnum(ini['amplitude'])} s</b></p>
<p>Número de classes: √{ini['n']} = {fmt(r['raiz'])} → <b>{r['k']}</b> · Amplitude de classe: {fnum(ini['amplitude'])} ÷ {r['k']} =
{fmt(r['h_bruto'])} → <b>{fnum(r['h'])} s</b></p>
<h2>3. Distribuição de frequência</h2>{tabela_html(r).replace('class="freq"', '')}
<p>FA = frequência absoluta · FAA = frequência absoluta acumulada · FR = frequência relativa ·
FRAA = frequência relativa acumulada</p>
<h2>4. Medidas estatísticas</h2>
<p><b>Média aritmética:</b> x̄ = Σx ÷ n = {fmt(m['soma'])} ÷ {m['n']} = <b>{fmt(m['media'])} s</b></p>
<p><b>Mediana:</b> {texto_mediana(m)}</p>
<p><b>Moda:</b> {moda_txt}</p>
<h2>5. Histograma</h2><img src="data:image/png;base64,{png}" alt="Histograma">
<h2>6. Interpretação dos resultados</h2>
<div class="qa-container">
{itens_qa}
</div>
</body></html>""".encode("utf-8")


# ---------------------------------------------------------------------
# 10. ESTADO DA APLICAÇÃO (st.session_state)
#     Guarda os dados editados para que não se percam ao trocar de aba.
# ---------------------------------------------------------------------
def df_original():
    """DataFrame com os 40 tempos originais (usado na tabela editável)."""
    return pd.DataFrame({COLUNA: [float(v) for v in TEMPOS_ORIGINAIS]})


def iniciar_estado():
    """Cria as variáveis de estado apenas na primeira execução."""
    padrao = {
        "dados": list(map(float, TEMPOS_ORIGINAIS)),   # dados APLICADOS na análise
        "base_editor": df_original(),                   # dados exibidos na tabela editável
        "versao_editor": 0,                             # muda para recriar a tabela editável
        "confirmar_limpeza": False,                     # controla a confirmação do botão Limpar
        "auto": True,                                   # atualização automática ligada
        "mensagem": None,
    }
    for chave, valor in padrao.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


# Funções chamadas pelos botões (callbacks)
def restaurar_originais():
    """Botão 'Restaurar': volta para os 40 valores originais."""
    st.session_state.base_editor = df_original()
    st.session_state.versao_editor += 1
    st.session_state.dados = list(map(float, TEMPOS_ORIGINAIS))
    st.session_state.confirmar_limpeza = False
    st.session_state.mensagem = ("success", "Os 40 valores originais foram restaurados com sucesso.")


def pedir_limpeza():
    st.session_state.confirmar_limpeza = True


def cancelar_limpeza():
    st.session_state.confirmar_limpeza = False


def confirmar_limpeza():
    """Limpa todos os dados após a confirmação do usuário."""
    st.session_state.base_editor = pd.DataFrame({COLUNA: pd.Series([], dtype=float)})
    st.session_state.versao_editor += 1
    st.session_state.dados = []
    st.session_state.confirmar_limpeza = False
    st.session_state.mensagem = ("warning", "Todos os dados foram apagados. "
                                 "Adicione novos atendimentos ou restaure os originais.")


def excluir_atendimento(idx):
    """Exclui um atendimento específico pelo índice."""
    if 0 <= idx < len(st.session_state.dados):
        removido = st.session_state.dados.pop(idx)
        st.session_state.base_editor = pd.DataFrame({COLUNA: st.session_state.dados})
        st.session_state.versao_editor += 1
        st.session_state.mensagem = ("info", f"Ligação #{idx + 1} ({removido:.0f} s) excluída.")


def adicionar_atendimento():
    """Adiciona um novo tempo de atendimento à lista."""
    val = st.session_state.get("input_novo_tempo", 0)
    if val and val > 0:
        st.session_state.dados.append(float(val))
        st.session_state.base_editor = pd.DataFrame({COLUNA: st.session_state.dados})
        st.session_state.versao_editor += 1
        st.session_state.mensagem = ("success", f"Atendimento #{len(st.session_state.dados)} ({val} s) adicionado!")


def adicionar_lote_tempos():
    """Adiciona múltiplos tempos extraídos de um texto."""
    import re
    texto = st.session_state.get("input_lote_texto", "")
    nums = [float(x) for x in re.findall(r"\b\d+(?:\.\d+)?\b", texto) if float(x) > 0]
    if nums:
        st.session_state.dados.extend(nums)
        st.session_state.base_editor = pd.DataFrame({COLUNA: st.session_state.dados})
        st.session_state.versao_editor += 1
        st.session_state.mensagem = ("success", f"{len(nums)} novos atendimentos adicionados com sucesso!")
        st.session_state.input_lote_texto = ""
    else:
        st.session_state.mensagem = ("warning", "Nenhum número válido foi encontrado no texto digitado.")


# ---------------------------------------------------------------------
# 11. MENU LATERAL
# ---------------------------------------------------------------------
def menu_lateral():
    with st.sidebar:
        st.markdown("## 📞 CALL CENTER ANALYTICS")
        st.caption("Análise Estatística de Desempenho Operacional")
        st.markdown("---")
        n = len(st.session_state.dados)
        original = sorted(st.session_state.dados) == sorted(map(float, TEMPOS_ORIGINAIS))
        st.markdown(f"**Atendimentos na análise:** {n}")
        if n:
            # Número de classes calculado automaticamente: k = √n (arredondamento clássico)
            raiz, k = numero_de_classes(n)
            st.markdown(f"**Número de classes:** {k}  \n(√{n} = {fmt(raiz)} → {k})")
        st.markdown(f"**Situação dos dados:** {'✅ originais' if original else '✏️ modificados'}")
        st.markdown("---")
        with st.expander("👥 Integrantes do Grupo", expanded=False):
            for item in INTEGRANTES:
                nome, curso = item.split(" – ")
                st.markdown(f"• **{nome}**  \n  <small style='color:{AZUL_CLARO}'>{curso}</small>", unsafe_allow_html=True)
        st.markdown("---")
        st.caption("Ferramentas: Python · Pandas · Matplotlib · Streamlit")


# ---------------------------------------------------------------------
# 12. ABA 4 - DEMONSTRAÇÃO INTERATIVA / EDITAR DADOS (parte 1: editor)
#     É desenhada ANTES das outras abas para que qualquer alteração
#     seja aplicada e todas as abas já mostrem os resultados novos.
# ---------------------------------------------------------------------
def aba_editor():
    st.markdown('<span class="etapa">DEMONSTRAÇÃO AO VIVO</span>', unsafe_allow_html=True)
    st.subheader("✏️ Visualização e Edição dos Tempos de Atendimento")
    caixa(
        "Visualize e personalize os dados de forma individual nos <b>cards da grade</b>. "
        "Cada atendimento possui seu <b>próprio espaço</b> para alteração imediata de valor ou exclusão no <b>✕</b>. "
        "Adicione novos registros na barra de ferramentas ou alterne para o modo planilha quando preferir."
    )

    # Mensagem de retorno dos botões (restaurar / limpar)
    if st.session_state.mensagem:
        tipo, texto = st.session_state.mensagem
        getattr(st, tipo)(texto)
        st.session_state.mensagem = None

    # Confirmação antes de limpar tudo
    if st.session_state.confirmar_limpeza:
        st.warning("⚠️ Tem certeza de que deseja apagar **todos** os tempos de atendimento?")
        c_conf1, c_conf2 = st.columns(2)
        c_conf1.button("Sim, apagar tudo", on_click=confirmar_limpeza, type="primary", width="stretch")
        c_conf2.button("Cancelar", on_click=cancelar_limpeza, width="stretch")
        st.markdown("")

    # Mini KPIs resumidos do conjunto atual
    n_total = len(st.session_state.dados)
    if n_total > 0:
        menor = min(st.session_state.dados)
        maior = max(st.session_state.dados)
        media = sum(st.session_state.dados) / n_total
        k_classes = int(round(math.sqrt(n_total) + 1e-9))

        col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)
        col_k1.metric("Atendimentos (n)", f"{n_total}")
        col_k2.metric("Menor Tempo", f"{fnum(menor)} s")
        col_k3.metric("Maior Tempo", f"{fnum(maior)} s")
        col_k4.metric("Média Atual", f"{fmt(media)} s")
        col_k5.metric("Nº de Classes (k)", f"{k_classes}")
        st.markdown("")

    # Barra de Ferramentas / Controles
    with st.container(border=True):
        f_col1, f_col2, f_col3 = st.columns([1.6, 1.4, 1.2], gap="medium")

        with f_col1:
            st.markdown("**➕ Adicionar Atendimento**")
            add_c1, add_c2 = st.columns([1.5, 1.2])
            add_c1.number_input(
                "Novo tempo (s)",
                min_value=1,
                max_value=9999,
                value=st.session_state.get("input_novo_tempo", 100),
                step=1,
                key="input_novo_tempo",
                label_visibility="collapsed",
            )
            add_c2.button("Adicionar", on_click=adicionar_atendimento, type="primary", width="stretch")

        with f_col2:
            st.markdown("**⚡ Ações Rápidas**")
            btn_c1, btn_c2 = st.columns(2)
            btn_c1.button("↩️ Restaurar (40)", on_click=restaurar_originais, width="stretch", help="Restaura os 40 valores originais do estudo")
            btn_c2.button("🗑️ Limpar Tudo", on_click=pedir_limpeza, width="stretch", help="Apaga todos os dados")

        with f_col3:
            st.markdown("**⚙️ Sincronização**")
            st.toggle("Atualização automática", key="auto", help="Recalcula todas as abas e gráficos a cada modificação.")
            if not st.session_state.auto:
                aplicar = st.button("🔄 Aplicar alterações", type="primary", width="stretch")
            else:
                aplicar = False

    # Inserção em lote (expansível)
    with st.expander("📥 Inserir múltiplos atendimentos de uma vez (em lote)", expanded=False):
        st.caption("Digite ou cole números separados por vírgula, espaço ou linhas (exemplo: `45, 52, 68, 75, 82, 90, 115`):")
        st.text_area("Valores em segundos", key="input_lote_texto", placeholder="Ex: 45, 50, 72, 88, 95, 102, 110, 125, 140", height=80)
        st.button("➕ Inserir lote nos dados", on_click=adicionar_lote_tempos, type="primary")

    # Seletor de visualização (Cards vs Tabela)
    st.markdown("")
    modo_c1, modo_c2 = st.columns([2, 1])
    with modo_c1:
        st.markdown("#### 📦 Dados Cadastrados")
    with modo_c2:
        modo_visao = st.radio(
            "Modo de visualização:",
            ["🗂️ Grade de Cards (Visual)", "📋 Tabela Planilha"],
            horizontal=True,
            label_visibility="collapsed",
        )

    versao = st.session_state.versao_editor
    n_dados = len(st.session_state.dados)

    if modo_visao == "🗂️ Grade de Cards (Visual)":
        if n_dados == 0:
            st.info("Nenhum atendimento cadastrado. Adicione tempos acima ou clique em '↩️ Restaurar (40)' para começar.")
        else:
            # Sincronização dos valores digitados nos inputs
            valores_cards = []
            mudou = False
            for i in range(n_dados):
                chave_card = f"c_{i}_{versao}"
                if chave_card in st.session_state:
                    val_atual = float(st.session_state[chave_card])
                    valores_cards.append(val_atual)
                    if val_atual != st.session_state.dados[i]:
                        mudou = True
                else:
                    valores_cards.append(st.session_state.dados[i])

            if mudou and st.session_state.auto:
                st.session_state.dados = valores_cards
                st.session_state.base_editor = pd.DataFrame({COLUNA: valores_cards})
            elif aplicar and valores_cards != st.session_state.dados:
                st.session_state.dados = valores_cards
                st.session_state.base_editor = pd.DataFrame({COLUNA: valores_cards})
                st.success("Alterações aplicadas com sucesso!")

            # Renderização da grade em 5 colunas
            NUM_COLS = 5
            for i in range(0, n_dados, NUM_COLS):
                cols = st.columns(NUM_COLS)
                for j in range(NUM_COLS):
                    idx = i + j
                    if idx < n_dados:
                        valor = st.session_state.dados[idx]
                        minutos = int(valor // 60)
                        segundos = int(valor % 60)
                        txt_min = f"{minutos}m {segundos:02d}s" if minutos > 0 else f"{segundos}s"

                        with cols[j]:
                            with st.container(border=True):
                                c_top1, c_top2 = st.columns([2.5, 1])
                                c_top1.markdown(f"<span class='badge-card'>#{idx + 1:02d}</span>", unsafe_allow_html=True)
                                c_top2.button("✕", key=f"del_{idx}_{versao}", on_click=excluir_atendimento, args=(idx,), help=f"Excluir ligação #{idx + 1}")

                                st.number_input(
                                    f"Tempo #{idx + 1}",
                                    value=int(valor),
                                    min_value=1,
                                    max_value=9999,
                                    step=1,
                                    key=f"c_{idx}_{versao}",
                                    label_visibility="collapsed",
                                    help=f"Tempo da ligação #{idx + 1} em segundos",
                                )
                                st.markdown(f"<div class='tempo-conversao'>⏱️ {txt_min}</div>", unsafe_allow_html=True)

    else:
        # Modo Tabela Planilha (st.data_editor)
        editado = st.data_editor(
            st.session_state.base_editor,
            key=f"editor_{st.session_state.versao_editor}",
            num_rows="dynamic",
            width="stretch",
            height=430,
            column_config={
                COLUNA: st.column_config.NumberColumn(
                    "Tempo de atendimento (s)", min_value=1, step=1, format="%d",
                    help="Somente números positivos, em segundos."),
            },
        )
        validos, avisos = validar_dados(editado)
        for aviso in avisos:
            st.warning(aviso)
        if st.session_state.auto or aplicar:
            st.session_state.dados = validos
        elif sorted(validos) != sorted(st.session_state.dados):
            st.info("Há alterações não aplicadas. Clique em 'Aplicar alterações'.")

    # Exportar dados
    st.markdown("")
    with st.expander("⬇️ Exportar dados utilizados em CSV", expanded=False):
        dados_df = pd.DataFrame({"Atendimento": range(1, len(st.session_state.dados) + 1),
                                 COLUNA: st.session_state.dados})
        st.download_button("⬇️ Baixar dados em CSV", para_csv(dados_df),
                           "dados_tempos_atendimento.csv", "text/csv", width="stretch")


# 12.1 ABA 4 (parte 2): resumo atualizado logo abaixo do editor
def aba_editor_resumo(r):
    st.markdown("---")
    st.markdown("#### 📊 Resultado atualizado em tempo real")
    if r is None:
        st.info("Nenhum dado válido. Adicione tempos de atendimento para ver a análise.")
        return
    ini, m = r["ini"], r["med"]
    grade_cartoes([
        cartao("Atendimentos", ini["n"]),
        cartao("Menor / Maior", f"{fnum(ini['menor'])} / {fnum(ini['maior'])} <small>{UNIDADE}</small>"),
        cartao("Amplitude total", f"{fnum(ini['amplitude'])} <small>{UNIDADE}</small>"),
        cartao("Nº de classes", r["k"], f"√{ini['n']} = {fmt(r['raiz'])} → {r['k']}"),
        cartao("Intervalo de classe (h)", f"{fnum(r['h'])} <small>{UNIDADE}</small>",
               f"{fnum(ini['amplitude'])} ÷ {r['k']} = {fmt(r['h_bruto'])} ↑"),
        cartao("Média", f"{fmt(m['media'])} <small>{UNIDADE}</small>", destaque=True),
        cartao("Mediana", f"{fmt(m['mediana'])} <small>{UNIDADE}</small>", destaque=True),
        cartao("Moda", texto_moda(m),
               "nenhum tempo se repete" if not m["modas"] else f"aparece {m['rep_moda']} vezes",
               destaque=True),
    ])
    c1, c2 = st.columns([1.15, 1], gap="large")
    with c1:
        st.markdown(tabela_html(r), unsafe_allow_html=True)
    with c2:
        mostrar_figura(grafico_histograma(r))


# ---------------------------------------------------------------------
# 13. ABA 1 - DASHBOARD
# ---------------------------------------------------------------------
def aba_dashboard(r):
    if r is None:
        st.info("Sem dados para analisar. Vá até a aba **Editar Dados** e adicione atendimentos "
                "ou restaure os valores originais.")
        return
    ini, m, t = r["ini"], r["med"], r["tabela"]
    i_mx = r["maiores"][0]

    # ETAPA 1 - Organização e análise inicial
    st.markdown('<span class="etapa">ETAPA 1 — ORGANIZAÇÃO E ANÁLISE INICIAL</span>', unsafe_allow_html=True)
    grade_cartoes([
        cartao("Total de atendimentos", ini["n"], "ligações analisadas"),
        cartao("Menor tempo", f"{fnum(ini['menor'])} <small>{UNIDADE}</small>", "atendimento mais rápido"),
        cartao("Maior tempo", f"{fnum(ini['maior'])} <small>{UNIDADE}</small>", "atendimento mais demorado"),
        cartao("Amplitude total", f"{fnum(ini['amplitude'])} <small>{UNIDADE}</small>",
               f"{fnum(ini['maior'])} − {fnum(ini['menor'])}"),
    ])

    # Medidas de tendência central (média, mediana e moda simples)
    st.markdown('<span class="etapa">MEDIDAS DE TENDÊNCIA CENTRAL</span>', unsafe_allow_html=True)
    grade_cartoes([
        cartao("Média aritmética (TMA)", f"{fmt(m['media'])} <small>{UNIDADE}</small>",
               f"≈ {fmt(m['media'] / 60)} min", destaque=True),
        cartao("Mediana", f"{fmt(m['mediana'])} <small>{UNIDADE}</small>", "valor central", destaque=True),
        cartao("Moda", texto_moda(m),
               "nenhum tempo se repete" if not m["modas"] else f"aparece {m['rep_moda']} vezes",
               destaque=True),
        cartao("Classe com maior frequência", f"{t['Classe'].iloc[i_mx]}",
               f"{int(t['FA'].iloc[i_mx])} atendimentos · {fpct(t['FR (%)'].iloc[i_mx])}"),
    ])

    # Comparação entre média e mediana
    dif, forma = comparar_media_mediana(r)
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("#### 🎯 Objetivo da análise")
        caixa(f"A equipe de operações registrou o tempo de <b>{ini['n']} atendimentos</b>, em segundos. "
              "Usando a <b>Estatística Descritiva</b>, os dados foram organizados em classes, "
              "resumidos em uma distribuição de frequência e representados graficamente para "
              "avaliar o <b>tempo médio de atendimento (TMA)</b> e o comportamento da equipe.")
        st.markdown("#### ⚖️ Comparação entre média e mediana")
        caixa(f"Média <b>{fmt(m['media'])} {UNIDADE}</b> × mediana <b>{fmt(m['mediana'])} {UNIDADE}</b> "
              f"→ diferença de <b>{fmt(dif)} {UNIDADE}</b>. A distribuição é <b>{forma}</b>.", "cinza")
    with c2:
        st.markdown("#### 💡 Principais resultados")
        linha_moda = ("• <b>Não há moda</b>: nenhum tempo de atendimento se repete." if not m["modas"]
                      else f"• O tempo mais recorrente (moda) é <b>{texto_moda(m)}</b>.")
        caixa(
            f"• Os atendimentos variam de <b>{fnum(ini['menor'])}</b> a <b>{fnum(ini['maior'])} {UNIDADE}</b>.<br>"
            f"• A maior concentração está na classe <b>{t['Classe'].iloc[i_mx]} {UNIDADE}</b>, com "
            f"<b>{int(t['FA'].iloc[i_mx])}</b> ligações ({fpct(t['FR (%)'].iloc[i_mx])}).<br>"
            f"• Em média, cada cliente é atendido em <b>{fmt(m['media'])} {UNIDADE}</b> "
            f"(cerca de {fmt(m['media'] / 60, 1)} minutos).<br>"
            f"• Metade dos atendimentos dura até <b>{fmt(m['mediana'])} {UNIDADE}</b> (mediana).<br>"
            f"{linha_moda}"
        )

    # ETAPA 5 - Respostas às questões de interpretação
    st.markdown("---")
    st.markdown('<span class="etapa">ETAPA 5 — INTERPRETAÇÃO DOS RESULTADOS</span>', unsafe_allow_html=True)
    resp = respostas_interpretacao(r)
    # Cada pergunta aparece como um tópico (•), sem numeração
    for num, pergunta in PERGUNTAS.items():
        with st.expander(f"• {pergunta}", expanded=(num in ("11", "12"))):
            st.markdown(resp[num], unsafe_allow_html=True)

    # Relatório resumido para download
    st.markdown("---")
    st.download_button("📄 Gerar relatório resumido da análise (HTML)", gerar_relatorio(r),
                       "relatorio_call_center_analytics.html", "text/html", type="primary")
    st.caption("O relatório abre em qualquer navegador e pode ser impresso ou salvo em PDF (Ctrl+P).")


# ---------------------------------------------------------------------
# 14. ABA 2 - DISTRIBUIÇÃO DE FREQUÊNCIA
# ---------------------------------------------------------------------
def aba_distribuicao(r):
    if r is None:
        st.info("Sem dados para montar a distribuição de frequência.")
        return
    ini, m, t = r["ini"], r["med"], r["tabela"]
    h = r["h"]

    # Passo a passo da construção das classes
    st.markdown('<span class="etapa">ETAPA 2 — CONSTRUÇÃO DA DISTRIBUIÇÃO DE FREQUÊNCIA</span>',
                unsafe_allow_html=True)
    c0, c1 = st.columns(2)
    with c0:
        st.markdown("**1) Número de classes (k)**")
        st.latex(rf"k = \sqrt{{n}} = \sqrt{{{ini['n']}}} = {ltx(r['raiz'])} \Rightarrow {r['k']}")
    with c1:
        st.markdown("**2) Amplitude total (AT)**")
        st.latex(rf"AT = {fnum(ini['maior'])} - {fnum(ini['menor'])} = {fnum(ini['amplitude'])}\ s")
    c2, c3 = st.columns(2)
    with c2:
        st.markdown("**3) Amplitude de classe (h)**")
        st.latex(rf"h = \frac{{AT}}{{k}} = \frac{{{fnum(ini['amplitude'])}}}{{{r['k']}}} "
                 rf"= {ltx(r['h_bruto'])} \Rightarrow {fnum(h)}\ s")
    with c3:
        st.markdown("**4) Primeira classe**")
        st.latex(rf"{fnum(r['limites'][0])} \vdash {fnum(r['limites'][1])}")
    st.caption(f"O número de classes é a raiz quadrada do total de observações, com arredondamento "
               f"clássico (abaixo de 0,5 desce; a partir de 0,5 sobe). O valor de h também é arredondado para cima para que todas as {ini['n']} observações caibam nas "
               f"{r['k']} classes. A primeira classe começa no menor valor ({fnum(ini['menor'])}). "
               f"O limite inferior pertence à classe e o superior não (ex.: {r['tabela']['Classe'].iloc[0]} inclui "
               f"de {fnum(r['limites'][0])} até valores menores que {fnum(r['limites'][1])}).")

    # Tabela de frequência
    st.markdown("#### 📋 Tabela de distribuição de frequência")
    st.markdown(tabela_html(r), unsafe_allow_html=True)

    # Conferências pedidas nas orientações finais do roteiro
    soma_fa, soma_fr = int(t["FA"].sum()), float(t["FR (%)"].sum())
    ok_fa = soma_fa == ini["n"]
    ok_soma = abs(float(t["Soma"].sum()) - m["soma"]) < 1e-9   # soma das classes = soma de todos os dados
    ok_fr = abs(soma_fr - 100) < 1e-9
    continuas = all(t["Ls"].iloc[i] == t["Li"].iloc[i + 1] for i in range(len(t) - 1))
    st.markdown(
        f"{'✅' if ok_soma else '❌'} Σ soma dos dados = **{fnum(t['Soma'].sum())}** "
        f"(soma de todas as observações: {fnum(m['soma'])}) &nbsp;&nbsp; "
        f"{'✅' if ok_fa else '❌'} Σ FA = **{soma_fa}** (total de observações: {ini['n']}) &nbsp;&nbsp; "
        f"{'✅' if ok_fr else '❌'} Σ FR = **{fpct(soma_fr)}** &nbsp;&nbsp; "
        f"{'✅' if continuas else '❌'} Classes contínuas, sem sobreposição &nbsp;&nbsp; "
        f"🔷 Linha destacada = classe com maior FA"
    )

    # Botão de exportação da tabela
    st.download_button("⬇️ Exportar tabela de frequência (CSV)", para_csv(tabela_exportacao(r)),
                       "tabela_frequencia.csv", "text/csv")

    # Significado de cada coluna
    st.markdown("#### 📖 O que significa cada coluna?")
    caixa(
        f"<b>Classe:</b> intervalo de tempo de atendimento (ex.: {t['Classe'].iloc[0]} = de "
        f"{fnum(r['limites'][0])} s até menos de {fnum(r['limites'][1])} s).<br>"
        "<b>Soma dos dados:</b> soma dos tempos de atendimento que pertencem à classe. O total é a soma "
        "de todos os dados observados (o mesmo valor usado no cálculo da média).<br>"
        "<b>FA – Frequência Absoluta:</b> quantidade de clientes atendidos naquele intervalo.<br>"
        "<b>FAA – Frequência Absoluta Acumulada:</b> quantidade de clientes atendidos <i>até</i> aquele "
        "intervalo (soma das FA até a classe).<br>"
        "<b>FR – Frequência Relativa:</b> porcentagem de clientes em cada intervalo, (FA ÷ N) × 100.<br>"
        "<b>FRAA – Frequência Relativa Acumulada:</b> porcentagem de clientes atendidos até aquele intervalo."
    )
    caixa("<b>Por que agrupar os valores em classes?</b><br>"
          "Analisar 40 valores um a um dificulta enxergar padrões. Agrupando em classes, os dados ficam "
          "resumidos em poucas faixas, o que mostra rapidamente <b>onde os atendimentos se concentram</b>, "
          "como eles se distribuem e permite construir o histograma. Isso facilita a comunicação dos "
          "resultados para a gestão.", "cinza")

    # ETAPA 3 - Média, mediana e moda simples com fórmulas e valores substituídos
    st.markdown("---")
    st.markdown('<span class="etapa">ETAPA 3 — CÁLCULO DAS MEDIDAS ESTATÍSTICAS</span>',
                unsafe_allow_html=True)
    st.caption(f"Média, mediana e moda calculadas com os {m['n']} tempos de atendimento.")

    m1, m2, m3 = st.columns(3, gap="large")
    with m1:
        st.markdown("##### Média aritmética")
        st.latex(r"\bar{x} = \frac{\sum x}{n}")
        st.latex(rf"\bar{{x}} = \frac{{{ltx(m['soma'])}}}{{{m['n']}}} = {ltx(m['media'])}\ s")
        st.caption("Soma de todos os tempos dividida pela quantidade de atendimentos. "
                   "É o tempo médio gasto para atender um cliente.")
    with m2:
        st.markdown("##### Mediana")
        if len(m["posicoes"]) == 2:
            p1, p2 = m["posicoes"]
            v1, v2 = m["centrais"]
            st.latex(rf"Md = \frac{{{p1}^{{\circ}}\text{{ valor}} + {p2}^{{\circ}}\text{{ valor}}}}{{2}}")
            st.latex(rf"Md = \frac{{{fnum(v1)} + {fnum(v2)}}}{{2}} = {ltx(m['mediana'])}\ s")
            st.caption(f"Com n = {m['n']} (par), a mediana é a média dos dois valores centrais "
                       f"({p1}º e {p2}º) dos dados em ordem crescente.")
        else:
            p = m["posicoes"][0]
            st.latex(rf"Md = {p}^{{\circ}}\text{{ valor}}")
            st.latex(rf"Md = {ltx(m['mediana'])}\ s")
            st.caption(f"Com n = {m['n']} (ímpar), a mediana é o valor central ({p}º) dos dados "
                       "em ordem crescente.")
    with m3:
        st.markdown("##### Moda")
        st.latex(r"Mo = \text{valor que mais se repete}")
        if m["modas"]:
            modas_ltx = r" \text{ e } ".join(fnum(v).replace(",", "{,}") for v in m["modas"])
            st.latex(rf"Mo = {modas_ltx}\ s")
            st.caption(f"Aparece {m['rep_moda']} vezes nos dados. É o tempo de atendimento mais recorrente.")
        else:
            st.latex(r"Mo = \text{Amodal}")
            st.caption("Nenhum tempo de atendimento se repete (cada valor aparece uma única vez), "
                       "por isso o conjunto não tem moda.")

    # Dados em ordem crescente com os valores centrais destacados
    st.markdown("##### 🔢 Dados em ordem crescente (rol)")
    st.markdown(rol_html(r), unsafe_allow_html=True)
    st.caption("Os valores destacados são os centrais, usados no cálculo da mediana.")


# ---------------------------------------------------------------------
# 15. ABA 3 - GRÁFICOS E ANÁLISE VISUAL
# ---------------------------------------------------------------------
def aba_graficos(r):
    if r is None:
        st.info("Sem dados para gerar os gráficos.")
        return
    t = r["tabela"]
    i_mx = r["maiores"][0]

    st.markdown('<span class="etapa">ETAPA 4 — CONSTRUÇÃO DO HISTOGRAMA</span>', unsafe_allow_html=True)
    fig = grafico_histograma(r)
    png = figura_para_png(fig)
    mostrar_figura(fig)
    st.download_button("⬇️ Baixar histograma (PNG)", png, "histograma.png", "image/png")
    caixa(f"O histograma mostra os <b>{len(t)} intervalos de classe</b> no eixo horizontal e a "
          f"<b>quantidade de atendimentos (FA)</b> no vertical. A barra mais alta (azul-escuro) é a classe "
          f"<b>{t['Classe'].iloc[i_mx]} {UNIDADE}</b>, onde estão {int(t['FA'].iloc[i_mx])} atendimentos.")

    st.markdown("---")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        mostrar_figura(grafico_barras(r, "FA", "Frequência absoluta (FA) por classe", "Atendimentos (FA)"))
        st.caption("Quantos clientes foram atendidos em cada faixa de tempo.")
    with c2:
        mostrar_figura(grafico_barras(r, "FR (%)", "Frequência relativa (FR) por classe",
                                      "Percentual de atendimentos (%)", percentual=True))
        st.caption("Percentual de clientes em cada faixa de tempo (soma = 100%).")

    st.markdown("---")
    mostrar_figura(grafico_ogiva(r))
    caixa("A <b>ogiva</b> mostra a frequência relativa acumulada (FRAA): lendo o gráfico, é possível saber "
          "que percentual dos atendimentos terminou até cada tempo.", "cinza")


# ---------------------------------------------------------------------
# 16. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------
def main():
    aplicar_estilo()
    iniciar_estado()
    menu_lateral()

    # Cabeçalho do sistema
    st.markdown(
        """<div class="cabecalho">
            <h1>CALL CENTER ANALYTICS</h1>
            <p>Análise Estatística de Desempenho Operacional</p>
            <div class="tags-cabecalho">
                <span class="tag">⏱️ Tempos em segundos</span>
                <span class="tag">🐍 Python · Pandas · Matplotlib</span>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # Criação das quatro abas
    aba1, aba2, aba3, aba4 = st.tabs([
        "📊 Dashboard", "📋 Distribuição de Frequência", "📈 Gráficos e Análise Visual", "✏️ Editar Dados",
    ])

    # 1º) Desenha o editor (aba 4) para capturar as alterações ANTES dos cálculos
    with aba4:
        aba_editor()

    # 2º) Executa a análise completa com os dados atuais
    resultado = analisar(st.session_state.dados)

    # 3º) Preenche as abas com os resultados recalculados
    with aba1:
        aba_dashboard(resultado)
    with aba2:
        aba_distribuicao(resultado)
    with aba3:
        aba_graficos(resultado)
    with aba4:
        aba_editor_resumo(resultado)


if __name__ == "__main__":
    main()
