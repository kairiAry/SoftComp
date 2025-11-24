from flask import Blueprint, render_template, request
import numpy as np
import random
import string

latihan3_bp = Blueprint('latihan3', __name__)

POP_SIZE = 100
GENERATIONS = 200
TOURNAMENT_K = 5
PC = 0.9
PM = 0.2
ELITE_SIZE = 1

def route_distance(route, dist_matrix):
    d = sum(dist_matrix[route[i], route[(i+1)%len(route)]] for i in range(len(route)))
    return d

def create_individual(n):
    ind = list(range(n))
    random.shuffle(ind)
    return ind

def initial_population(size, n):
    return [create_individual(n) for _ in range(size)]

def tournament_selection(pop, dist_matrix):
    k = random.sample(pop, TOURNAMENT_K)
    return min(k, key=lambda ind: route_distance(ind, dist_matrix))

def ordered_crossover(p1, p2):
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    child = [-1]*size
    child[a:b+1] = p1[a:b+1]
    p2_idx = 0
    for i in range(size):
        if child[i] == -1:
            while p2[p2_idx] in child:
                p2_idx += 1
            child[i] = p2[p2_idx]
    return child

def swap_mutation(ind):
    a, b = random.sample(range(len(ind)), 2)
    ind[a], ind[b] = ind[b], ind[a]

@latihan3_bp.route('/', methods=['GET', 'POST'])
def index():
    rute_hasil = None
    jarak_hasil = None
    history = []
    error_msg = None
    
    jumlah_kota = 0 

    if request.method == 'POST':
        try:
            jumlah_kota = int(request.form.get('jumlah_kota'))
            
            matrix_data = []
            for i in range(jumlah_kota):
                row = []
                for j in range(jumlah_kota):
                    input_name = f'dist_{i}_{j}'
                    val = request.form.get(input_name)
                    if val:
                        row.append(float(val))
                    else:
                        row.append(0.0)
                matrix_data.append(row)
            
            dist_matrix = np.array(matrix_data)
            
            cities = [string.ascii_uppercase[i] for i in range(jumlah_kota)]
            
            pop = initial_population(POP_SIZE, jumlah_kota)
            best = min(pop, key=lambda ind: route_distance(ind, dist_matrix))
            best_dist = route_distance(best, dist_matrix)
            
            for g in range(GENERATIONS):
                new_pop = []
                pop = sorted(pop, key=lambda ind: route_distance(ind, dist_matrix))
                
                if route_distance(pop[0], dist_matrix) < best_dist:
                    best = pop[0]
                    best_dist = route_distance(best, dist_matrix)
                
                new_pop.extend(pop[:ELITE_SIZE])
                
                while len(new_pop) < POP_SIZE:
                    p1 = tournament_selection(pop, dist_matrix)
                    p2 = tournament_selection(pop, dist_matrix)
                    child = ordered_crossover(p1, p2) if random.random() < PC else p1[:]
                    if random.random() < PM: swap_mutation(child)
                    new_pop.append(child)
                
                pop = new_pop
                history.append(best_dist)

            rute_hasil = [cities[i] for i in best]
            rute_hasil.append(rute_hasil[0])
            jarak_hasil = round(best_dist, 2)

        except Exception as e:
            error_msg = f"Terjadi kesalahan input: {e}"

    return render_template('halaman3.html', 
                           rute=rute_hasil, 
                           jarak=jarak_hasil, 
                           history=history,
                           error=error_msg)