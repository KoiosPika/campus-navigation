from flask import Flask, render_template, request, jsonify
import heapq
from collections import deque

app = Flask(__name__)

def create_graph():
    graph = {
        "AD" : {"LH": 1, "SGMH": 1, "CJ": 1, "GH": 1, "MC": 4},
        "B"  : {"KHS": 2, "PL": 5, "TSU": 2, "CPAC": 4, "SRC": 3},
        "CC" : {"TS": 5, "TTF": 6},
        "CPAC" : {"B": 4, "PL": 3, "H": 5, "MH": 2, "GC": 2, "NPS": 3, "TSU": 2, "VA": 2},
        "CS" : {"E": 1, "GAS": 3, "ENPS": 4},
        "E" : {"CS": 1, "RG": 4, "SHCC": 4, "EC": 6},
        "DBH" : {"MH": 1, "MC": 1, "LH": 1, "GC": 2},
        "EC" : {"PL": 2, "H": 3, "E": 6, "SHCC": 5},
        "ENPS" : {"CS": 4, "ESPS": 1},
        "ESPS" : {"ENPS": 1, "H": 7, "CJ": 4},
        "GAH" : {"UP": 1, "SCPS": 2, "TSU": 2},
        "GAS": {"CS": 3, "RG": 2, "RH": 1, "HRE": 1},
        "GC" : {"CPAC": 2, "DBH": 2, "MH": 2, "NPS": 2},
        "GF" : {"TS": 2, "AF": 1, "TSC": 2},
        "GH" : {"H": 2, "MH": 2, "AD": 1, "LH": 1, "CJ": 1},
        "H" : {"CPAC": 5, "EC": 3, "ESPS": 7, "GH": 2, "PL": 4, "MH": 3},
        "HRE": {"GAS": 1, "RH": 1},
        "KHS": {"B": 2, "SRC": 3, "TG": 1, "PL": 3},
        "LH" : {"AD": 1, "DBH": 1, "GH": 1, "MH": 1, "MC": 3},
        "MC" : {"DBH": 1, "LH": 3, "AD": 4, "SGMH": 4},
        "MH" : {"CPAC": 2, "DBH": 1, "GC": 2, "GH": 2, "H": 3, "LH": 1},
        "MS" : {"TSF": 4, "T": 2},
        "NPS" : {"GC": 2, "CPAC": 3, "VA": 6},
        "PL" : {"B": 5, "CPAC": 3, "EC": 2, "H": 3, "KHS": 3, "SHCC": 4},
        "RG" : {"E": 4, "GAS": 2, "SHCC": 3, "RH": 4},
        "RH" : {"GAS": 1, "HRE": 1, "RG": 4},
        "SCPS" : {"GAH": 2, "UP": 1, "SRC": 1, "TSU": 3, "CY": 5},
        "SGMH" : {"AD": 1, "MC": 4, "CJ": 2},
        "SHCC" : {"E": 4, "TG": 3, "PL": 4, "RG": 3, "EC": 5, "T": 2},
        "SRC" : {"KHS": 3, "SCPS": 1, "TG": 2, "B": 3, "TTC": 1},
        "T" : {"MS": 2, "SHCC": 2, "TG": 5},
        "TG" : {"KHS": 1, "SHCC": 3, "SRC": 2, "T": 5, "TTC": 2},
        "TH" : {"ASC": 1, "VA": 3, "TSU": 6},
        "TS" : {"CC": 5, "GF": 2, "TSC": 3, "TTF": 4, "AF": 4},
        "TSC" : {"GF": 2, "TS": 3, "AF": 1, "TTF": 1, "TSF": 3},
        "TSF" : {"MS": 4, "TSC": 3, "AF": 1, "TTF": 2},
        "TSU" : {"B": 2, "GAH": 2, "SCPS": 3, "TH": 6, "VA": 3, "CPAC": 2},
        "TTC" : {"TG": 2, "TTF": 1, "SRC": 1},
        "TTF": {"CC": 6, "TS": 4, "TSC": 1, "TSF": 2, "TTC": 1, "AF": 3},
        "UP" : {"GAH": 1, "SCPS": 1, "CY": 6},
        "VA" : {"TH": 3, "TSU": 3, "CPAC": 2, "NPS": 6},
        "AF" : {"GF": 1, "TS": 4, "TSC": 1, "TSF": 1, "TTF": 3},
        "ASC" : {"TH": 1},
        "CJ" : {"AD": 1, "GH": 1, "SGMH": 2, "ESPS":4},
        "CY" : {"SCPS": 5, "UP": 6},
        }
    return graph

def dijkstra(graph, source, destination):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    priority_queue = [(0, source)]
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node == destination:
            break
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    
    return distances[destination], path

# Implement Breadth First Search algorithm
def bfs(graph, start, destination):
    queue = deque([[start]]) #Queue for BFS paths to explore
    #set to track visited intersections
    visited = set()
    
    #continue BFS until all the paths a re explored
    while queue:
        path = queue.popleft()
        #Get the current intersection (last node in path)
        current_intersection = path[-1]
        
        #Check if we have reached the destination
        if current_intersection == destination:
            return path
        
        #check if we have reached the destination
        if current_intersection not in visited:
            visited.add(current_intersection)
            
            for neighbor in graph.get(current_intersection, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                
    return None

# Implement Depth First Search algorithm
def dfs(graph, start, destination, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
        
    visited.add(start)
    
    if start == destination:
        return path
        
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result_path = dfs(graph, neighbor, destination, path + [neighbor], visited)
            if result_path:
                return result_path
    return None

@app.route('/')
def home():
    return render_template('index.html')  # This will look in the 'templates' folder

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()  # Use request.get_json() to parse JSON data
    start = data['start']
    end = data['end']
    algorithm = data['algorithm']
    graph = create_graph()

    if algorithm == 'Dijkstra':
        _, path = dijkstra(graph, start, end)
    elif algorithm == 'BFS':
        path = bfs(graph, start, end)
    elif algorithm == 'DFS':
        path = dfs(graph, start, end)
    else:
        path = None

    distance = 20

    return jsonify({"distance": distance,"path": path if path else []})

if __name__ == '__main__':
    app.run(debug=True)
