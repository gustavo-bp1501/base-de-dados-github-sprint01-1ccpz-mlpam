# =============================================================================
# FIAP - Modelagem Linear Para Aprendizado de Máquina (MLPAM)
# Challenge Sprint 1 - 1º Semestre
# Empresa Parceira: GoodWe (Energia)
# Base de Dados: Capacidade Instalada de Geração por UF - ANEEL
# ↓ Autores ↓
# Ana Beatriz Berbel Marini - RM 574176
# Gustavo Bonamico Piccoli - RM 569984
# Marcelo Francisco Josafá Ribeiro Martins - RM 573905
# Maria Eduarda Medeiros Lemos - RM 574094
# Pietro Lorande da SIlva - RM 569125
# =============================================================================

import pandas as pd
import numpy as np

# =============================================================================
# ITEM 01 - CARREGAMENTO E DESCRIÇÃO DA BASE DE DADOS
# =============================================================================

# Carrega o arquivo XLSX disponibilizado pela ANEEL
df = pd.read_excel('Planilha-Capacidade-Geracao-Energetica-Por-UF.xlsx')

print("=" * 65)
print("ITEM 01 - DESCRIÇÃO DA BASE DE DADOS")
print("=" * 65)

print(f"\nTotal de observações: {len(df)}")
print(f"Total de variáveis:   {len(df.columns)}")
print(f"\nPrimeiras linhas:")
print(df.head())
print(f"\nTipos de dados:\n{df.dtypes}")

# -----------------------------------------------------------------------------
# DERIVANDO UMA SEGUNDA VARIÁVEL CONTÍNUA: Participação Percentual por Período
# Para cada par (AnoReferencia, MesReferencia), calcula a participação
# percentual de cada UF em relação à potência total instalada no período.
# -----------------------------------------------------------------------------
totais_periodo = df.groupby(['AnoReferencia', 'MesReferencia'])['MdaPotenciaInstaladakW'].transform('sum')
df['Participacao_Percentual'] = (df['MdaPotenciaInstaladakW'] / totais_periodo) * 100

# =============================================================================
# CLASSIFICAÇÃO DAS VARIÁVEIS
# =============================================================================

print("\n" + "=" * 65)
print("CLASSIFICAÇÃO DAS VARIÁVEIS")
print("=" * 65)

print("""
VARIÁVEIS QUALITATIVAS NOMINAIS (categorias sem ordem natural):
  1. NomUF  → Nome completo da Unidade da Federação
             Ex: 'BAHIA', 'SÃO PAULO', 'AMAZONAS'
  2. SigUF  → Sigla da Unidade da Federação (2 letras)
             Ex: 'BA', 'SP', 'AM'

VARIÁVEIS QUALITATIVAS ORDINAIS (categorias com ordem natural):
  1. MesReferencia  → Mês da coleta (1=Jan, ..., 12=Dez)
                     Existe hierarquia temporal de janeiro a dezembro
  2. AnoReferencia  → Ano da coleta (2006, 2007, ..., 2026)
                     Existe hierarquia temporal crescente entre os anos

VARIÁVEIS QUANTITATIVAS DISCRETAS (valores inteiros contáveis):
  1. AnoReferencia   → Número inteiro representando o ano de referência
  2. MesReferencia   → Número inteiro de 1 a 12 representando o mês

VARIÁVEIS QUANTITATIVAS CONTÍNUAS (valores numéricos reais):
  1. MdaPotenciaInstaladakW   → Potência instalada total em kW (quilowatt)
                                Pode assumir qualquer valor real positivo
  2. Participacao_Percentual  → Participação percentual (%) de cada UF
                                na potência total do período (derivada)
""")

# Estatísticas descritivas das variáveis quantitativas contínuas
print("Estatísticas Descritivas - Variáveis Contínuas:")
print(df[['MdaPotenciaInstaladakW', 'Participacao_Percentual']].describe().round(2))

# =============================================================================
# ITEM 02a - TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS
#            Variável Quantitativa DISCRETA: AnoReferencia
# =============================================================================

print("\n" + "=" * 65)
print("ITEM 02a - TDF: Variável Discreta → AnoReferencia")
print("=" * 65)

# Frequência absoluta por ano
freq_abs = df['AnoReferencia'].value_counts().sort_index()

# Frequência relativa (proporção)
freq_rel = freq_abs / freq_abs.sum()

# Frequência percentual
freq_perc = freq_rel * 100

# Frequência acumulada absoluta
freq_ac = freq_abs.cumsum()

# Frequência acumulada relativa
freq_rel_ac = freq_rel.cumsum()

# Montando a tabela de distribuição de frequências
tdf_discreta = pd.DataFrame({
    'Ano':              freq_abs.index,
    'Fi (Freq. Abs.)':  freq_abs.values,
    'Fr (Freq. Rel.)':  freq_rel.values.round(4),
    'F% (Freq. %)':     freq_perc.values.round(2),
    'Fac (Acum. Abs.)': freq_ac.values,
    'Frac (Acum. Rel.)':freq_rel_ac.values.round(4)
})

print("\nTabela de Distribuição de Frequências - AnoReferencia:")
print(tdf_discreta.to_string(index=False))

# -----------------------------------------------------------------------
# INSIGHTS - Variável Discreta: AnoReferencia
# -----------------------------------------------------------------------

# Insight 1: Verificando se há anos com mais registros que outros
ano_mais_frequente = freq_abs.idxmax()
ano_menos_frequente = freq_abs.idxmin()
print(f"\n# INSIGHT 1: O ano com maior número de registros é {ano_mais_frequente}"
      f" ({freq_abs[ano_mais_frequente]} obs.), enquanto {ano_menos_frequente}"
      f" tem apenas {freq_abs[ano_menos_frequente]} obs.")
# Isso revela que o dataset cobre uma série histórica de ~20 anos (2006–2026),
# e anos mais recentes ou mais antigos podem ter menos meses registrados.

# Insight 2: Evolução temporal - quantos registros existem para os anos recentes
ultimos_3_anos = df[df['AnoReferencia'] >= 2024]
perc_recentes = (len(ultimos_3_anos) / len(df)) * 100
print(f"\n# INSIGHT 2: Os anos de 2024 em diante correspondem a"
      f" {perc_recentes:.1f}% das observações ({len(ultimos_3_anos)} registros).")
# Isso indica que a série histórica é densa nos anos passados e ainda sendo
# construída para o período mais recente, o que é esperado em dados trimestrais.

# Insight 3: Cobertura da série histórica
anos_unicos = df['AnoReferencia'].nunique()
print(f"\n# INSIGHT 3: A base cobre {anos_unicos} anos distintos, o que permite"
      f" análises de tendência de longo prazo para o setor de energia elétrica.")
# Para uma empresa como a GoodWe (energia renovável), entender a evolução
# histórica da capacidade instalada ao longo de duas décadas é estratégico.

# =============================================================================
# ITEM 02b - TABELA DE DISTRIBUIÇÃO DE FREQUÊNCIAS
#            Variável Quantitativa CONTÍNUA: MdaPotenciaInstaladakW
# =============================================================================

print("\n" + "=" * 65)
print("ITEM 02b - TDF: Variável Contínua → MdaPotenciaInstaladakW")
print("=" * 65)

# Usando a Regra de Sturges para definir o número de classes
n = len(df)
k = int(np.ceil(1 + 3.322 * np.log10(n)))  # Regra de Sturges
print(f"\nNúmero de classes pela Regra de Sturges: k = 1 + 3,322 * log10({n}) ≈ {k}")

# Limites do intervalo
vmin = df['MdaPotenciaInstaladakW'].min()
vmax = df['MdaPotenciaInstaladakW'].max()
amplitude_total = vmax - vmin
h = amplitude_total / k  # Amplitude de cada classe

print(f"Valor mínimo:         {vmin:,.2f} kW")
print(f"Valor máximo:         {vmax:,.2f} kW")
print(f"Amplitude total:      {amplitude_total:,.2f} kW")
print(f"Amplitude de classe:  {h:,.2f} kW")

# Criando os intervalos de classe
bins = [vmin + i * h for i in range(k + 1)]
bins[-1] = vmax + 0.01  # Garante que o valor máximo seja incluído

# Rótulos dos intervalos
labels = [
    f"[{bins[i]:,.0f} – {bins[i+1]:,.0f})"
    for i in range(k)
]

# Aplicando o corte nos dados
df['Classe'] = pd.cut(
    df['MdaPotenciaInstaladakW'],
    bins=bins,
    labels=labels,
    right=False,
    include_lowest=True
)

# Frequência absoluta por classe
freq_abs_c  = df['Classe'].value_counts().sort_index()
freq_rel_c  = freq_abs_c / freq_abs_c.sum()
freq_perc_c = freq_rel_c * 100
freq_ac_c   = freq_abs_c.cumsum()
freq_rac_c  = freq_rel_c.cumsum()

# Ponto médio de cada classe
midpoints = [(bins[i] + bins[i+1]) / 2 for i in range(k)]

# Montando a tabela de distribuição de frequências contínua
tdf_continua = pd.DataFrame({
    'Classe (kW)':        labels,
    'Ponto Médio':        [f"{m:,.0f}" for m in midpoints],
    'Fi (Freq. Abs.)':    freq_abs_c.values,
    'Fr (Freq. Rel.)':    freq_rel_c.values.round(4),
    'F% (Freq. %)':       freq_perc_c.values.round(2),
    'Fac (Acum. Abs.)':   freq_ac_c.values,
    'Frac (Acum. Rel.)':  freq_rac_c.values.round(4)
})

print("\nTabela de Distribuição de Frequências - MdaPotenciaInstaladakW:")
print(tdf_continua.to_string(index=False))

# -----------------------------------------------------------------------
# INSIGHTS - Variável Contínua: MdaPotenciaInstaladakW
# -----------------------------------------------------------------------

# Insight 1: Concentração na 1ª classe - assimetria positiva acentuada
primeira_classe_perc = freq_perc_c.values[0]
print(f"\n# INSIGHT 1: A 1ª classe (menor potência) concentra"
      f" {primeira_classe_perc:.1f}% das observações.")
# Isso indica forte assimetria à direita: a maioria dos estados/períodos
# registra baixa potência instalada, enquanto poucos estados (como SP, MG, BA)
# dominam com valores muito elevados. Para a GoodWe, isso sinaliza que há
# grande heterogeneidade regional — estados de baixa potência são oportunidades
# de expansão de energia renovável.

# Insight 2: Mediana vs Média - detectando outliers de alta potência
mediana = df['MdaPotenciaInstaladakW'].median()
media = df['MdaPotenciaInstaladakW'].mean()
print(f"\n# INSIGHT 2: Mediana = {mediana:,.0f} kW | Média = {media:,.0f} kW")
print(f"#            A média é {((media/mediana)-1)*100:.1f}% maior que a mediana.")
# A média consideravelmente superior à mediana confirma a assimetria positiva.
# Grandes estados (como São Paulo e Minas Gerais) "puxam" a média para cima.
# A GoodWe deve considerar estratégias diferenciadas: escala para grandes mercados
# e capilaridade para estados emergentes de energia renovável.

# Insight 3: Porcentagem acumulada até a metade das classes
metade_k = k // 2
perc_metade = freq_rac_c.values[metade_k - 1] * 100
print(f"\n# INSIGHT 3: As primeiras {metade_k} classes (de {k} no total)"
      f" acumulam {perc_metade:.1f}% das observações.")
# Isso reforça que a distribuição é extremamente concentrada nos valores mais
# baixos de potência instalada, típico de mercados de energia em desenvolvimento
# com poucos grandes geradores e muitos estados de menor porte.

print("\n" + "=" * 65)
print("Análise concluída com sucesso.")
print("=" * 65)