import numpy as np 

class node():
    def __init__(self, name, connection = None):
        self.name  = name
        self.dist  = float('inf')
        self.via   = None
        self.q_pos = -1
        self.connection = connection
        self.not_visited = True
        self.dest = False

class shortest_path():
    def __init__(self, no_nodes, node_names, gph = None, target_idx = -1):
        self.n = no_nodes
        self.node_names = node_names
        self.map = gph
        self.target_idx = target_idx
        self.order = np.array([])
        self.create_nodes()
        self.queue = np.array([self.nodes[0]])
        self.find_path()
        # print('\nfinal data:')
        self.show()
        self.path()

    def create_nodes(self):
        self.nodes = [node(name = self.node_names[i], connection = self.map[i]) for i in range(self.n)]
        self.nodes[0].dist  = 0
        self.nodes[self.target_idx].dest = True
        self.order = np.append(self.order, self.nodes[0].dist)

    def find_path(self):
        while len(self.queue):
            Node = self.queue[0]
            self.queue = np.delete(self.queue, 0)
            self.order = np.delete(self.order, 0)
            Node.not_visited = False

            #stop condition i.e target reaches top of queue
            if Node.dest:
                return
            # print("current node:", Node.name)
            for i, weight in enumerate(Node.connection):
                if (weight > 0) and self.nodes[i].not_visited:
                    if (Node.dist + weight < self.nodes[i].dist):
                        self.nodes[i].via  = Node
                        self.nodes[i].dist = Node.dist + weight
                        if self.nodes[i].q_pos == -1:
                            self.queue = np.append(self.queue, self.nodes[i])
                            self.order = np.append(self.order, self.nodes[i].dist)
                        else:
                            self.order[self.nodes[i].q_pos] = self.nodes[i].dist

            # self.show()
            self.prioritise()


    def prioritise(self):
        index = np.argsort(self.order)
        self.order = self.order[index]
        self.queue = self.queue[index]
        for i, Node in enumerate(self.queue):
            Node.q_pos = i - 1

    def show(self):
        for node in self.nodes:
            print("node:", node.name, "via:", node.via.name if node.via != None else '-', "dist:", node.dist)

    def path(self):
        Node = self.nodes[self.target_idx]
        print("\npath:", end = ' ')
        while Node != None:
            print(Node.name, '-', end = ' ')
            Node = Node.via
        Node = self.nodes[self.target_idx]
        print("\ndist:", end = ' ')
        while Node != None:
            print(Node.dist, '-', end = ' ')
            Node = Node.via
        print("\n\n")



def main():
    sp = shortest_path(6, 'ABCDEF', gph = [[-1,  2,  4, -1, -1, 10],
                                           [ 2, -1,  1,  5,  2, -1],
                                           [ 4,  1, -1, -1,  3,  6],
                                           [-1,  5, -1, -1,  3,  2],
                                           [-1,  2,  3,  3, -1,  2],
                                           [-1, -1, -1,  2,  2, -1]])




if __name__ == '__main__':
    main()

