# Anak Agung Rai Gayatri 2313231040
# I Gusti Ayu Nirmala Dewi 2313231019

import heapq
from collections import deque

class Problem():
    def __init__(self, knowledge, start_node, end_node):
        self.knowledge = knowledge
        self.start_node = start_node
        self.end_node = end_node

    def get_map(self):
        return self.knowledge

    def get_startNode(self):
        return self.start_node

    def get_endNode(self):
        return self.end_node
    
    def actionFunc(self, node, actiontype):
        if node in self.knowledge:
            ch_nodes = self.knowledge[node]
            if actiontype == "turnLeft":
                return ch_nodes[0][0]
            elif actiontype == "goStraight":
                return ch_nodes[1][0]
            elif len(ch_nodes) > 2:
                return ch_nodes[2][0]
        return None

    def DFS(self, node, reached=None, result=None):
        if reached is None:
            reached = set()
        if result is None:
            result = []
        
        reached.add(node)
        result.append(node)
        
        if node == self.get_endNode():
            return result, True
        
        if node.get_action():
            for action in node.get_action():
                leafnode = self.actionFunc(node, action)
                if leafnode and leafnode not in reached:
                    leafnode.set_parent(node)
                    result_path, found = self.DFS(leafnode, reached, result)
                    if found:
                        return result_path, True
        
        return result, False
    
    def BFS(self, node):
        reached = set()
        result = []
        queue = deque()
        
        reached.add(node)
        result.append(node)
        queue.append(node)
        
        while queue:
            node = queue.popleft()
            if node == self.get_endNode():
                return result, True
            
            if node.get_action():
                for action in node.get_action():
                    leafnode = self.actionFunc(node, action)
                    if leafnode and leafnode not in reached:
                        reached.add(leafnode)
                        queue.append(leafnode)
                        result.append(leafnode)
                    if leafnode == self.get_endNode():
                        return result, True
        
        return result, False
    
    def Dijkstra(self):
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.start_node))
        distances = {node: float('inf') for node in self.knowledge}
        distances[self.start_node] = 0
        predecessors = {node: None for node in self.knowledge}
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_node == self.end_node:
                break
            
            for neighbor, cost in self.get_map().get(current_node, []):
                distance = current_distance + cost
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        path = []
        node = self.end_node
        while node:
            path.append(node)
            node = predecessors[node]
        
        return path[::-1] if distances[self.end_node] != float('inf') else None
    
    def get_ChildNodes(self, method):
        start_node = self.get_startNode()
        if method == "DFS":
            return self.DFS(start_node)
        elif method == "BFS":
            return self.BFS(start_node)
        else:
            result = self.Dijkstra()
            return result, result is not None

class Node():
    def __init__(self, state, action):
        self.state = state
        self.action = action
        self.parent = None
    
    def __hash__(self):
        return hash(self.state)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
    
    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent
    
    def set_parent(self, node):
        self.parent = node
    
    def get_action(self):
        return self.action

def main():
    node_A = Node("A", ["turnLeft", "goStraight"])
    node_B = Node("B", ["turnLeft", "goStraight", "turnRight"])
    node_C = Node("C", ["turnLeft", "goStraight"])
    node_D = Node("D", None)
    node_E = Node("E", None)
    node_F = Node("F", None)
    node_G = Node("G", None)
    
    knowledge = {
        node_A: [(node_B, 1), (node_C, 4)],
        node_B: [(node_D, 2), (node_E, 5), (node_F, 1)],
        node_C: [(node_F, 3), (node_G, 2)],
        node_D: [],
        node_E: [],
        node_F: [],
        node_G: []
    }
    
    problem = Problem(knowledge, start_node=node_A, end_node=node_F)
    path, status = problem.get_ChildNodes(method="Dijkstra")
    
    if status:
        print(" -> ".join(node.get_state() for node in path))
    else:
        print("No path found")

if __name__ == "__main__":
    main()
