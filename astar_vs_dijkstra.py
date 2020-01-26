import numpy as np 
import cv2
import A_star_graphics as ag
import dijkstra_graphics as dg


def main():

    bs = 10
    size = 750
    start = [np.random.randint(size // bs), np.random.randint(size // bs)]
    end = [np.random.randint(size // bs), np.random.randint(size // bs)]
    
    dsp = dg.shortest_path(start_idx = start, 
                          target_idx =   end,
                            blk_size = bs, size = size, blockage = 0)
    asp = ag.shortest_path(start_idx = start, 
                          target_idx =   end,
                            blk_size = bs, size = size, blockage = 0)

    dsp.find_path()
    asp.find_path()


    dsp.show_path()
    asp.show_path()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

