from random import randint, sample
import itertools
import argparse
import sys


class EpidemicSimulator(object):
    def __init__(self):
        # min and max number of nodes
        self.NODES_MIN = 10
        self.NODES_MAX = 1000

        # min and max number of iterations
        self.IT_MIN = 10
        self.IT_MAX = 5000

        # number of random nodes to choose
        # on each iteration of protocol simulation
        self.X = 4

        self.get_args()


    # get optional arguments -n -i and validetae them
    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-n", "--nodes",
             help="number of nodes",
             type=int,
             required=True,
        )

        parser.add_argument(
            "-i", "--iterations",
            help="number of iteration",
            type=int,
            required=True
        )

        args = parser.parse_args()

        if self.validate_args(args.nodes, args.iterations):
            self.nodes_num = args.nodes
            self.iterations = args.iterations


    # check args values to be in specified range
    def validate_args(self, nodes_num, iterations):
        if nodes_num not in range(self.NODES_MIN, self.NODES_MAX):
            print(f"-n should be in range [{self.NODES_MIN}, {self.NODES_MAX}]")
            sys.exit(0)

        if iterations not in range(self.IT_MIN, self.IT_MAX):
            print(f"-i should be in range [{self.IT_MIN}, {self.IT_MAX}]")
            sys.exit(0)

        return True


    # basic implementation of epidemic protocol
    # return True if all nodes received a packet
    def epidemic_protocol(self):
        nodes = {n:0 for n in range(0, self.nodes_num)}
        queue = [randint(0, self.nodes_num)]
        nodes[0] = 1

        while queue:
            for node_sender in queue:
                for node_receiver in sample(range(self.nodes_num), self.X):
                    if nodes[node_receiver] != 1:
                        nodes[node_receiver] = 1
                        queue.append(node_receiver) # node_receiver -> node_sender
                queue.remove(node_sender)

        if sum(value is 1 for value in nodes.values()) == self.nodes_num:
            return True


    # run N(self.iterations) times epidemic_protocol()
    # and count how many times all nodes received a packet
    def simulate(self):
        full_coverage = 0

        for it in range(0, self.iterations):
            if self.epidemic_protocol():
                full_coverage += 1

        print(f"In {full_coverage*100/self.iterations}% cases all nodes received the packet")




if __name__ == "__main__":
    epidemic = EpidemicSimulator()
    epidemic.simulate()
