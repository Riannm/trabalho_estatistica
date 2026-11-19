# CALL CENTER ANALYTICS
### Análise Estatística de Desempenho Operacional

Trabalho Avaliativo em Grupo 3 – Estatística Descritiva
Tema: análise do tempo médio de atendimento (TMA) de um call center com 40 ligações (tempos em **segundos**).

Painel web feito em **Python** com:
- **Pandas**: organiza os dados e constrói a tabela de frequências (FA/Fi, FAA/Fac, FR/Fr);
- **Matplotlib**: gera o histograma e os demais gráficos;
- **Streamlit**: monta a interface (dashboard).

---

## 1. Instalação (Windows)

1. Instale o **Python 3.10 ou mais recente** em https://www.python.org/downloads/
   e marque a opção **"Add Python to PATH"** durante a instalação.
2. Abra o **Prompt de Comando** (ou PowerShell) dentro da pasta do projeto
   (no Explorador de Arquivos, digite `cmd` na barra de endereço da pasta e pressione Enter).
3. Instale as bibliotecas:

```bash
pip install streamlit pandas matplotlib numpy
```

ou, de forma equivalente:

```bash
pip install -r requirements.txt
```

> Se o comando `pip` não for reconhecido, use `py -m pip install streamlit pandas matplotlib numpy`.

## 2. Execução

```bash
streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`.
Para encerrar, pressione `Ctrl + C` no Prompt de Comando.

> Se `streamlit` não for reconhecido, use `py -m streamlit run app.py`.

---

## 3. Estrutura do projeto

```
call_center_analytics/
├── app.py                  # sistema completo (cálculos, tabelas, gráficos e interface)
├── requirements.txt        # bibliotecas necessárias
├── README.md               # este arquivo
└── .streamlit/config.toml  # tema visual (azul, branco e cinza)
```

**Identificação do grupo (Trabalho Avaliativo – Grupo 3):**
1. **Riann Matheus Dias da Costa** – Sistemas de Informação
2. **Carlos Rafael Pagung Silva** – Sistemas de Informação
3. **Gabriel Lima Souza** – Sistemas de Informação
4. **Marcos Antônio Silva Sena** – Ciência da Computação
5. **Gabrielle Fernanda Carvalho Ventura** – Ciência da Computação
6. **Victor Augusto Ferreira** – Ciência da Computação
7. **Kauã Pedro Ferreira Araújo** – Ciência da Computação
8. **João Pedro Alves Sampaio** – Ciência da Computação
9. **Maria Eduarda Martins Santos** – Ciência da Computação
10. **João Victor Alves Nascimento** – Sistemas de Informação

## 4. As quatro abas

| Aba | Conteúdo | Etapa do roteiro |
|---|---|---|
| 📊 **Dashboard** | Cartões com total, menor, maior, amplitude, média, mediana, moda e classe com maior frequência; objetivo da análise; comparação média × mediana; respostas automáticas das questões de interpretação; botão de relatório | Etapas 1 e 5 |
| 📋 **Distribuição de Frequência** | Cálculo do número de classes e da amplitude de classe; tabela com Classe, Soma dos dados, FA, FAA, FR e FRAA (com TOTAL); conferências; explicação das colunas; fórmulas da média, mediana e moda com os valores substituídos; dados em ordem crescente (rol) | Etapas 2 e 3 |
| 📈 **Gráficos e Análise Visual** | Histograma (Matplotlib), gráfico de frequência absoluta, gráfico de frequência relativa e ogiva | Etapa 4 |
| ✏️ **Editar Dados** | Grade interativa de cards individuais por atendimento com inputs imediatos e remoção rápida, mais modo alternativo em planilha (`st.data_editor`); inserção rápida e em lote; resultado atualizado na hora | Demonstração em sala |

## 5. Como a análise é feita

Siglas: **FA** = Frequência Absoluta · **FAA** = Frequência Absoluta Acumulada ·
**FR** = Frequência Relativa · **FRAA** = Frequência Relativa Acumulada

- **Amplitude total:** `AT = maior valor − menor valor = 188 − 40 = 148 s`
- **Número de classes (obrigatório):** `k = √n` com arredondamento clássico (abaixo de 0,5 desce; a partir de 0,5 sobe): `√40 = 6,32` → **6 classes**.
  O número de classes não pode ser alterado manualmente; se a quantidade de dados mudar, ele é recalculado.
- **Amplitude de classe:** `h = AT ÷ k = 148 ÷ 6 = 24,67`, arredondada para cima: **25 s**
- **Classes:** começam no menor valor (40); o limite inferior pertence à classe e o superior não
  (`40 |— 65` inclui de 40 até valores menores que 65).
- **FR** = (FA ÷ N) × 100 · **FAA** = soma acumulada das FA · **FRAA** = soma acumulada das FR

Média, mediana e moda são **simples**, calculadas com os 40 valores:

- **Média aritmética:** `x̄ = Σx ÷ n = 4.153 ÷ 40 = 103,83 s`
- **Mediana:** n = 40 é par, então é a média dos dois valores centrais (20º e 21º) em ordem crescente:
  `Md = (100 + 102) ÷ 2 = 101 s`
- **Moda:** valor que mais se repete. Nos dados originais nenhum tempo se repete, então o conjunto é **amodal**.

### Resultados com os 40 dados originais (6 classes)

| Classe (s) | Soma dos dados | FA | FAA | FR | FRAA |
|---|---|---|---|---|---|
| 40 \|— 65 | 250 | 5 | 5 | 12,5% | 12,5% |
| 65 \|— 90 | 693 | 9 | 14 | 22,5% | 35,0% |
| **90 \|— 115** | **1.100** | **11** | **25** | **27,5%** | **62,5%** |
| 115 \|— 140 | 1.143 | 9 | 34 | 22,5% | 85,0% |
| 140 \|— 165 | 608 | 4 | 38 | 10,0% | 95,0% |
| 165 \|— 190 | 359 | 2 | 40 | 5,0% | 100,0% |
| **Total** | **4.153** | **40** | | **100%** | |

A coluna **Soma dos dados** soma os tempos que pertencem a cada classe; o total (4.153) é a soma de todos os dados observados.

| Medida | Resultado |
|---|---|
| Média | 103,83 s |
| Mediana | 101,00 s |
| Moda | Amodal (nenhum valor se repete) |

## 6. Demonstração ao vivo (aba ✏️ Editar Dados)

1. **Grade de Cards (Padrão):** Cada atendimento possui seu próprio card com badge de identificação (`#01`, `#02`...), campo de tempo em segundos, conversão automática para minutos e botão rápido de exclusão (`✕`).
2. **Adicionar novos tempos:** Digite o tempo na barra superior de ferramentas e clique em **Adicionar**, ou use o painel retrátil **Inserir em lote** para colar múltiplos números separados por vírgula.
3. **Modo alternativo:** Você pode alternar a qualquer momento entre **Grade de Cards (Visual)** e **Tabela Planilha**.
4. Com **Atualização automática** ligada, todas as abas e gráficos recalculam na hora. Se estiver desligada, use o botão **Aplicar alterações**.
5. **Restaurar os 40 valores originais** volta ao conjunto inicial; **Limpar dados** pede confirmação antes de apagar.
6. O **número de classes** é sempre `√n` com arredondamento clássico e é recalculado automaticamente quando a quantidade de dados muda.

Somente números positivos são aceitos. Linhas vazias ou valores inválidos são ignorados e o sistema avisa.

## 7. Exportações

- Tabela de frequência em CSV (abre no Excel em português);
- Dados utilizados em CSV;
- Histograma em PNG;
- **Relatório resumido em HTML**: dados, tabela, cálculos, histograma e interpretação. Abra no navegador e use `Ctrl + P` para salvar em PDF.
