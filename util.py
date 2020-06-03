class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent
    
    def get_action(self):
        return self.action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    def __len__(self):
        return len(self.frontier)
    
    def get_states(self):
        result = []
        for node in self.frontier:
            result.append(node.get_state())
        return result



class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# n0 = Node(0, None, None)

# n1 = Node(1, n0, 'a')

# n2 = Node(2, n1, 'b')

# explored_nodes = [n0, n1, n2]

# print(n1 in explored_nodes)

# frontier = StackFrontier()
# print(len(frontier))

# frontier.add(n0)
# frontier.add(n1)
# frontier.add(n2)
# print('frontier states:', frontier.get_states())

# print(frontier.contains_state(1))
# print(not frontier.contains_state(5))
