from queue import PriorityQueue

class BranchAndBound:
    def __init__(self, distances):
        self.distances = distances
        self.num_cities = len(distances)
        self.min_path = None
        self.min_distance = float('inf')

    def tsp_branch_and_bound(self):
        start_city = 0  # Assuming the starting city is always index 0

        def cost(vertex, path):
            return self.distances[path[-1]][vertex]

        def bound(path):
            last_vertex = path[-1]
            return sum(
                min(self.distances[last_vertex][j] for j in range(self.num_cities) if j not in path)
                for _ in range(self.num_cities - len(path))
            )

        def backtrack(path):
            if len(path) == self.num_cities:
                distance = sum(self.distances[path[i]][path[i+1]] for i in range(self.num_cities - 1))
                distance += self.distances[path[-1]][path[0]]
                if distance < self.min_distance:
                    self.min_distance = distance
                    self.min_path = path[:]
            else:
                priority_queue = PriorityQueue()
                for next_vertex in range(self.num_cities):
                    if next_vertex not in path:
                        new_path = path[:]
                        new_path.append(next_vertex)
                        new_bound = bound(new_path)
                        if new_bound < self.min_distance:
                            priority_queue.put((new_bound, new_path))

                while not priority_queue.empty():
                    _, next_path = priority_queue.get()
                    backtrack(next_path)

        backtrack([start_city])
        # Append the starting city to the end of the path
        self.min_path.append(start_city)
        return self.min_path, self.min_distance
