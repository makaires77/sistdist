import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

def calculate_availability(n, k, p):
    if n <= 0 or k <= 0 or k > n or p < 0 or p > 1:
        raise ValueError("Valores inválidos para os parâmetros.")
    
    def calculate_probability(x):
        return np.math.comb(n, x) * p**x * (1 - p)**(n - x)
    
    probabilities = [calculate_probability(x) for x in range(k)]
    availability = 1 - sum(probabilities)
    return availability

def plot_availability_curve(n_values, k_values, p_values, unit_cost):
    sns.set(style="whitegrid", rc={"axes.grid.axis": "y", "axes.grid.which": "major"})

    # Definir uma paleta de cores para atribuir cores diferentes às curvas de acordo com k
    colors = sns.color_palette("husl", len(k_values))

    fig, ax1 = plt.subplots(figsize=(12, 11))
    ax2 = ax1.twinx()

    lines = []  # Armazenar as linhas da legenda adicional

    for p in p_values:
        for i, k in enumerate(k_values):
            availabilities = []
            total_costs = []
            try:
                for n_val in n_values:
                    availability = calculate_availability(n_val, k, p)
                    availabilities.append(availability * 100)  # Exibindo em formato percentual
                    total_costs.append(n_val * unit_cost / 1000)  # Exibindo em k$
            except ValueError as e:
                print(f"Erro: {str(e)}")
                availabilities.append(float('nan'))
                total_costs.append(float('nan'))
            
            line = ax2.plot(n_values, availabilities, label=f'p = {p}, k = {k}', color=colors[i])
            lines.append(line[0])  # Adicionar a linha à lista de linhas da legenda adicional
            
            # Adicionar rótulos dos pontos de dados nas curvas
            for x, y in zip(n_values, availabilities):
                ax2.annotate(f"({k}, {x})", (x, y), xytext=(0, -10), textcoords="offset points",
                             ha='center', va='top', fontsize=8)

        # Adicionar rótulos nas bases internas das colunas
        for x, y in zip(n_values, total_costs):
            ax1.annotate(f"${y:.1f}k", (x, y), xytext=(0, -30), textcoords="offset points",
                         ha='center', va='top', fontsize=14)

        ax1.bar(n_values, total_costs, width=0.8, alpha=0.3, label='Custo (k$)', color='cyan', zorder=0)

    ax1.set_ylabel('Custo total com servidores (Unidade: 1.000 USD/mês)')
    ax2.set_xlabel('Número total de servidores (n)')
    ax2.set_ylabel('Disponibilidade do Serviço (%)')  # Exibindo em formato percentual
    
    ax2.set_title('Curva de Disponibilidade e Custo Total')

    # Configurar escala logarítmica inversa no eixo vertical
    ax2.set_ylim(10, 102)

    # Formatar rótulos do eixo vertical
    def percent_formatter(x, pos):
        return f"{int(x)}%"
    ax2.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

    # Criar legenda original
    legend1 = ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.9))

    # Adicionar a legenda adicional
    legend_labels = [f'k = {k}' for k in k_values]
    legend2 = ax2.legend(lines, legend_labels, loc='upper left', bbox_to_anchor=(0, 1))

    # Adicionar as duas legendas ao mesmo tempo
    ax2.add_artist(legend1)
    ax2.add_artist(legend2)

    # Ajustar o layout do gráfico para evitar sobreposição de elementos
    plt.subplots_adjust(left=0, right=0.95, top=0.98, bottom=0.1)

    # Adicionar espaço para as legendas antes do eixo esquerdo
    ax1.set_xlim(min(n_values)-2, max(n_values)+1)

    plt.show()