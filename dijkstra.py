import numpy as np 
import cv2

class node():
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]
        self.dist  = float('inf')
        self.via   = None
        self.q_pos = -1
        self.dest  = False
        self.not_visited = True


class shortest_path():
    def __init__(self, start_idx = [0, 0], target_idx = [5, 5], blk_size = 50, size = 750, blockage = 10):
        self.h, self.w  = size, size
        self.start_idx  = start_idx
        self.target_idx = target_idx
        self.size = size
        self.block_size = blk_size
        self.h = self.h // self.block_size
        self.w = self.w // self.block_size
        self.blockageclr = [255, 255, 255]
        self.targetclr   = [0  , 0  , 255]
        self.startclr    = [255, 0  , 0  ]
        self.pathclr     = [0  , 175, 255]
        self.qclr        = [255, 0  , 255]
        self.curclr      = [100, 100, 0  ]
        self.visitclr    = [0  , 255, 0  ]
        self.nodes = []
        self.map = np.zeros((size, size, 3), np.uint8)
        self.order = np.array([])
        self.create_nodes()
        self.block(blockage)
        self.queue = np.array([self.nodes[self.start_idx[0], self.start_idx[1]]])

    def create_nodes(self):
        for row in range(self.h):
            self.nodes.append([])
            for col in range(self.w):
                self.nodes[row].append(node([row, col]))
        self.nodes = np.array(self.nodes)
        self.nodes[self.start_idx[0], self.start_idx[1]].dist  = 0
        self.map = self.fill(self.map, self.start_idx, color = self.startclr)
        self.nodes[self.target_idx[0], self.target_idx[1]].dest = True
        self.map = self.fill(self.map, self.target_idx, color = self.targetclr)
        self.order = np.append(self.order, self.nodes[self.start_idx[0], self.start_idx[1]].dist)

    def find_path(self):
        weight = 1
        while len(self.queue):
            Node = self.queue[0]
            self.show()
            self.map = self.fill(self.map, self.start_idx, color = self.startclr)
            self.queue = np.delete(self.queue, 0)
            self.order = np.delete(self.order, 0)
            Node.not_visited = False

            #stop condition i.e target reaches top of queue
            if Node.dest:
                self.map = self.fill(self.map, self.target_idx, color = self.targetclr)
                return

            for i, j  in [[-1, 0], [1, 0], [0, -1], [0, 1]]:#, [-1, -1], [-1, 1], [1, -1], [1, 1]
                x, y = Node.x + i, Node.y + j
                if x >= 0 and y >= 0 and x < self.h and y < self.w: 
                    if self.nodes[x, y].not_visited :
                        if (Node.dist + weight < self.nodes[x, y].dist):
                            self.nodes[x, y].via  = Node
                            self.nodes[x, y].dist = Node.dist + weight
                            if self.nodes[x, y].q_pos == -1:
                                self.map = self.fill(self.map, [x, y], color = self.qclr)
                                self.queue = np.append(self.queue, self.nodes[x, y])
                                self.order = np.append(self.order, self.nodes[x, y].dist)
                            else:
                                self.order[self.nodes[x, y].q_pos] = self.nodes[x, y].dist
            self.map = self.fill(self.map, [Node.x, Node.y], color = self.visitclr)

            self.prioritise()


    def prioritise(self):
        index = np.argsort(self.order)
        self.order = self.order[index]
        self.queue = self.queue[index]
        for i, Node in enumerate(self.queue):
            Node.q_pos = i - 1

    def block(self, per = 30):
        for i in range(((self.size // self.block_size) ** 2) * per // 100):
            randx = np.random.randint(self.size // self.block_size)
            randy = np.random.randint(self.size // self.block_size)
            self.map = self.fill(self.map, [randx, randy], self.blockageclr)
            self.nodes[randx, randy].not_visited = False
        self.map = self.fill(self.map, [self.target_idx[0], self.target_idx[1]], self.targetclr)
        self.map = self.fill(self.map, [self.start_idx[0], self.start_idx[1]], self.startclr)
        self.nodes[self.target_idx[0], self.target_idx[1]].not_visited = True
        cv2.imshow("dijkstra", self.map)
        cv2.waitKey(100)
        cv2.destroyAllWindows()


    def show(self):
        cv2.imshow("dijkstra", self.map)
        k = cv2.waitKey(1)
        if k == 27:
            cv2.destroyAllWindows()

    def show_path(self):
        cost = 0
        Node = self.nodes[self.target_idx[0], self.target_idx[1]].via
        while Node.via != None:
            cost += 1
            self.map = self.fill(self.map, [Node.x, Node.y], color = self.pathclr)
            cv2.imshow("dijkstra", self.map)
            k = cv2.waitKey(10)
            if k == 27:
                return
            Node = Node.via
        print("distance :", cost, "pixel")
        self.map = cv2.putText(self.map, str(cost) , (10,20), cv2.FONT_HERSHEY_SIMPLEX , .75, [255, 250, 250], 2)
        cv2.imshow("dijkstra", self.map)
        cv2.waitKey(0)

    def fill(self,img, block, color = [0, 0, 255], pad = 1):
        block_size = self.block_size
        h, w, *_ = img.shape
        img[h - (block[1] * block_size + block_size - pad) : h - (block[1] * block_size) - pad, pad + block[0] * block_size : block[0] * block_size + block_size - pad ] = color
        return img


def main():

    bs = 10
    size = 750
    sp = shortest_path(start_idx = [np.random.randint(size // bs), np.random.randint(size // bs)], 
                      target_idx = [np.random.randint(size // bs), np.random.randint(size // bs)],
                        blk_size = bs, size = size, blockage = 30)
    sp.find_path()
    sp.show_path()
    cv2.destroyAllWindows()





if __name__ == '__main__':
        main()

