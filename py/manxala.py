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
    # Maybe see the home as a hole instead.
    
    def __init__(self, verbose=False):
        # ---
        self.homes = [home(), home()]
        self.holes = []
        for m in range(12):
            self.holes.append(hole())
        self.verbose = verbose

    def hoho(self, player=0):
        if player == 0:
            return (self.holes[0].nop,self.holes[1].nop, self.holes[2].nop)
        return (self.holes[6].nop,self.holes[7].nop, self.holes[8].nop)

    def clean(self, player=0):
        if (player == 0):
            if self.hoho(player=player) == [0,0,0]:
                print("Clear!")
                return True

        if self.hoho(player=player) == [0,0,0]:
            print("Clear!")
            return True

        return False
    
    def sum(self):
        the_sum = 0
        for home in self.homes:
            the_sum += home.nop
        for hole in self.holes:
            the_sum += hole.nop
        return the_sum
    
    def rst(self):
        for home in self.homes:
            home.rst()
        for hole in self.holes:
            hole.rst()

    def show(self):
        print( '+-------------------------+')
        subrow = int( self.homes[0].nop / 23)
        for k in range(subrow+1):
            print(f'| {self.homes[0].show()[(k*23):(k+1)*23]:^23} |')
        print( '+------------+------------+')

        for row in range(6):
            subrow = max([ int( (-1+self.holes[row].nop) / 10),
                           int( (-1+self.holes[11-row].nop) / 10) ] )
            for k in range(subrow+1):
                print(f'| {self.holes[row].show()[(k*10):(k+1)*10]:^10} | {self.holes[11-row].show()[(k*10):(k+1)*10]:^10} |')
            print( '+------------+------------+')
                    
        subrow = int( self.homes[1].nop / 23)
        for k in range(subrow+1):
            print(f'| {self.homes[1].show()[(k*23):(k+1)*23]:^23} |')
        print( '+-------------------------+')

    def push(self, player=0, hole=0):
        # if player, then rotate with 6.
        
        pearls = self.holes[hole].flush()
        hole_position = hole
        for m in range(pearls):
            hole_position = hole_position + 1  #  + m + 1
            at_base = False
            if (player == 0):
                if (hole_position==12):
                    self.homes[player].add()
                    at_base = True
                    continue
                if (hole_position > 12):
                    hole_position = hole_position-13 
            else: # (player == 1):
                if (hole_position > 11):
                    hole_position = hole_position-12 
                if (hole_position == 6):
                    self.homes[player].add() # handle this
                    at_base = True
                    
                    continue
            #print(f"------------> {hole_position}")
            self.holes[hole_position].add()
            
        return hole_position,at_base
        
    def iter(self, player=0, hole=0, rounds=10):
        # ===
        gogo = True
        ctr = 0
        while gogo:
            hole,base = self.push(player=player, hole=hole)
            ctr = ctr + 1
            self.show()
            print(f"{ctr}: {hole} // {self.sum()}")
            # if self.clean
            
            if (player == 0) and base: # hole == 12):
                # Then ended in home, pick random along three home holes
                if not self.clean(player=player):
                    mm = self.hoho(player=player)
                    print(mm)
                    hole = mm.index(max(mm))
                else:
                    print("Game ended!")
                    gogo = False
                    
                
            elif (player == 1) and base: # (hole == 6):
                # Then ended in home, pick random along three home holes
                if not self.clean(player=player):
                    mm = self.hoho(player=player)
                    print("Argabarag")
                    hole = 6+mm.index(max(mm))
                else:
                    print("Game ended!")
                    gogo = False

            else:
                if self.holes[hole].nop == 1:
                    print("Take the L! Ended on a singularity!")
                    gogo = False
            if ctr >= rounds:
                gogo = False
                
    
def main(args=None):
    manxala = board(verbose=True)
    manxala.show()
    hole = 6
    player = 1
    manxala.iter(player=player, hole=hole, rounds=args.rounds)
    
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--plot",
                        help="Plotting of graphs",
                        action="store_true")

    parser.add_argument("--rounds",
                        help="Number of test runs", 
                        default=3, type=int)
    
    args = parser.parse_args()
    
    main(args=args)
