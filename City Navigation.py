import math
import heapq
import time

# Data kota dan koordinat
cities = {
    "A": (0, 0),
    "B": (2, 1),
    "C": (4, 2),
    "D": (5, 5),
    "E": (1, 4)
}

# Data jalan antar kota
roads = {
    "A": ["B", "E"],
    "B": ["A", "C"],
    "C": ["B", "D"],
    "D": ["C"],
    "E": ["A", "D"]
}

# Heuristik Euclidean Distance
def euclidean(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

# Algoritma A*
def a_star(start, goal, cities, roads):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {city: float('inf') for city in cities}
    g_score[start] = 0
    visited_nodes = set()

    while open_list:
        _, current = heapq.heappop(open_list)
        visited_nodes.add(current)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], visited_nodes

        for neighbor in roads[current]:
            tentative_g = g_score[current] + euclidean(cities[current], cities[neighbor])
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean(cities[neighbor], cities[goal])
                heapq.heappush(open_list, (f_score, neighbor))

    return None, visited_nodes

# Algoritma Greedy Best-First Search (GBFS)
def gbfs(start, goal, cities, roads):
    open_list = []
    heapq.heappush(open_list, (euclidean(cities[start], cities[goal]), start))
    came_from = {}
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)
        visited.add(current)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], visited

        for neighbor in roads[current]:
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(open_list, (euclidean(cities[neighbor], cities[goal]), neighbor))

    return None, visited

# Jalankan dan bandingkan hasil
start = "A"
goal = "D"

# A* Execution
start_time_a = time.time()
path_a, visited_a = a_star(start, goal, cities, roads)
end_time_a = time.time()
time_a = (end_time_a - start_time_a) * 1000  # ms

# GBFS Execution
start_time_g = time.time()
path_g, visited_g = gbfs(start, goal, cities, roads)
end_time_g = time.time()
time_g = (end_time_g - start_time_g) * 1000  # ms

# Output
print("=== Hasil Pencarian A* ===")
print("Rute :", " -> ".join(path_a))
print("Waktu:", f"{time_a:.2f} ms")
print("Node yang dikunjungi:", len(visited_a))

print("\n=== Hasil Pencarian GBFS ===")
print("Rute :", " -> ".join(path_g))
print("Waktu:", f"{time_g:.2f} ms")
print("Node yang dikunjungi:", len(visited_g))

# Tabel Perbandingan (Text)
print("\n=== Perbandingan ===")
print(f"{'Algoritma':<10} | {'Waktu (ms)':<12} | {'Jumlah Node'}")
print("-" * 40)
print(f"{'GBFS':<10} | {time_g:<12.2f} | {len(visited_g)}")
print(f"{'A*':<10} | {time_a:<12.2f} | {len(visited_a)}")
