import random
from flask import Blueprint, render_template, request

latihan2_bp = Blueprint('latihan2', __name__)

items = {
    'A': {'weight': 7, 'value': 5},
    'B': {'weight': 2, 'value': 4},
    'C': {'weight': 1, 'value': 7},
    'D': {'weight': 9, 'value': 2},
}
item_list = list(items.keys())
n_items = len(item_list)

def decode(chromosome):
    total_weight = 0
    total_value = 0
    chosen_items = []
    for gene, name in zip(chromosome, item_list):
        if gene == 1:
            total_weight += items[name]['weight']
            total_value += items[name]['value']
            chosen_items.append(name)
    return chosen_items, total_weight, total_value

def fitness(chromosome, capacity):
    _, total_weight, total_value = decode(chromosome)
    if total_weight <= capacity:
        return total_value
    else:
        return 0

def roulette_selection(population, fitnesses):
    total_fit = sum(fitnesses)
    if total_fit == 0:
        return random.choice(population)
    pick = random.uniform(0, total_fit)
    current = 0
    for chrom, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return chrom
    return population[-1]

def crossover(p1, p2):
    if len(p1) < 2: return p1, p2
    point = random.randint(1, len(p1) - 1)
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate):
    return [1 - g if random.random() < mutation_rate else g for g in chromosome]

def solve_knapsack(capacity, pop_size, generations, mutation_rate):
    population = [[random.randint(0, 1) for _ in range(n_items)] for _ in range(pop_size)]
    history = []

    for gen in range(generations):
        fitnesses = [fitness(ch, capacity) for ch in population]
        
        best_idx = fitnesses.index(max(fitnesses))
        best_chrom = population[best_idx]
        best_fit = fitnesses[best_idx]
        best_items, w, v = decode(best_chrom)

        history.append({
            'gen': gen + 1,
            'chrom': str(best_chrom),
            'items': ", ".join(best_items) if best_items else "-",
            'weight': w,
            'value': v,
            'fitness': best_fit
        })

        new_population = [best_chrom]
        while len(new_population) < pop_size:
            p1 = roulette_selection(population, fitnesses)
            p2 = roulette_selection(population, fitnesses)
            c1, c2 = (crossover(p1, p2) if random.random() < 0.8 else (p1[:], p2[:]))
            new_population.extend([mutate(c1, mutation_rate), mutate(c2, mutation_rate)])
            
        population = new_population[:pop_size]

    fitnesses = [fitness(ch, capacity) for ch in population]
    final_best_idx = fitnesses.index(max(fitnesses))
    final_chrom = population[final_best_idx]
    final_items, final_w, final_v = decode(final_chrom)

    return {
        'history': history,
        'final_items': final_items,
        'final_weight': final_w,
        'final_value': final_v,
        'final_chrom': final_chrom
    }

@latihan2_bp.route('/', methods=['GET', 'POST'])
def index():
    result = None
    params = {
        'capacity': 15,
        'pop_size': 10,
        'generations': 10,
        'mutation_rate': 0.1
    }

    if request.method == 'POST':
        params['capacity'] = int(request.form.get('capacity', 15))
        params['pop_size'] = int(request.form.get('pop_size', 10))
        params['generations'] = int(request.form.get('generations', 10))
        params['mutation_rate'] = float(request.form.get('mutation_rate', 0.1))

        result = solve_knapsack(
            params['capacity'], 
            params['pop_size'], 
            params['generations'], 
            params['mutation_rate']
        )

    return render_template('halaman2.html', result=result, params=params)