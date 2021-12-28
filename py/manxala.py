#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt

class hole():

    def __init__(self, nop = 4, verbose=False):
        self.nop = nop
        self.verbose = verbose

    def add(self):
        self.nop = self.nop + 1

    def sub(self):
        # assert 0
        self.nop = self.nop - 1

    def flush(self):
        nop = self.nop
        self.nop = 0
        return nop
    
    def show(self):
        if self.verbose:
            print("O"*self.nop)
        return "O"*self.nop
        
    def rst(self, nop = 4):
        self.nop = nop

class home():
    def __init__(self ,verbose =False):
        self.nop = 0
        self.verbose = verbose

    def rst(self, nop=0):
        self.nop = nop

    def add(self, nop =1): # since we can steal
        self.nop = self.nop + nop

    def show(self):
        if self.verbose:
            print("O"*self.nop)
        return "O"*self.nop
        

class board():
    
    def __init__(self, verbose=False):
        self.homes = [home(), home()]
        self.holes = []
        for m in range(12):
            self.holes.append(hole())
        self.verbose = verbose

    def rst(self):
        for home in self.homes:
            home.rst()
        for hole in self.holes:
            hole.rst()

    def show(self):
        print( '+-------------------------+')
        print(f'|{self.homes[0].show():^25}|')
        print( '+------------+------------+')

        for row in range(6):
            print(f'| {self.holes[row].show():^10} | {self.holes[11-row].show():^10} |')
            print( '+------------+------------+')
                    
        print(f'|{self.homes[1].show():^25}|')
        print( '+-------------------------+')

    def push(self, player=0, hole=0):
        pearls = self.holes[hole].flush()
        for m in range(pearls):
            self.holes[hole+m+1].add()
        self.show()
        
        
def main(args=None):
    manxala = board(verbose=True)
    manxala.show()
    manxala.push()
    
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--plot",
                        help="Plotting of graphs",
                        action="store_true")
    
    args = parser.parse_args()
    
    main(args=args)
