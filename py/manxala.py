#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
from os import system
import time

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
        # Returns the list of gems in the first three home holes
        if player == 0:
            return [self.holes[0].nop,self.holes[1].nop, self.holes[2].nop]
        return [self.holes[6].nop,self.holes[7].nop, self.holes[8].nop]

    def clean(self, player=0):
        if (player == 0):
            if self.hoho(player=player) == [0,0,0]:
                return True

        if self.hoho(player=player) == [0,0,0]:
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
        #system('clear')
        #time.sleep(1)
        
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
        # The function that pushes the gems forward through the system.
        # if player==1, then rotate with 6.        

        pearls = self.holes[hole].flush()
        hole_position = hole + 6*player 
        at_base = False

        m = 0
        while m < pearls:
            m = m + 1
            hole_position = hole_position + 1 
            at_base = False

            if (player==0) and (hole_position == 12):
                # First hit on the place.
                at_base = True
                self.homes[player].add() # Add one gem to the home.
                if (m < pearls):
                    # There are pearls lefts                    
                    hole_position = -1                    
                else:
                    # No pearls left and thus leave the while loop
                    break 

            elif (player==1) and (hole_position == 12):
                # First hit on the place.
                at_base = True
                self.homes[player].add() # Add one gem to the home.
                if (m < pearls):
                    # There are pearls lefts                    
                    hole_position = -1                    
                else:
                    # No pearls left and thus leave the while loop
                    break 

            else:
                if hole_position > 12:
                    hole_position = hole_position - 12
                    
                self.holes[hole_position-6*player].add()
                
        #print(f" ----> {hole_position} <---- ")
        #print(f" ----> {hole_position-6*player} <---- ")
        return hole_position-6*player,at_base
    
    def iter(self, player=0, hole=0, rounds=10):
        # ===
        gogo = True
        ctr = 0
        base = False
        cleaned = False
        # rounds is for testing purposes only, to avoid deadlock in loop
        # print(hole)
        if hole is None:
            pearls_in_holes = self.hoho(player=player)
            print(f"From home, starting condition { pearls_in_holes }")
            # One of many algorithms... to be added here
            hole = player*6 + pearls_in_holes.index(max(pearls_in_holes))
            
        if self.sweep(): # clean(player=0) or self.clean(player=1):
            # Clean in home
            # This must be done when iteration is over.
            print(f"-------------------> Game ended! Player {player} gets the gems!")
            gogo = False
            cleaned = True
            pass
        
        while gogo:
            hole,base = self.push(player=player, hole=hole)
            
            ctr = ctr + 1
            self.show()
            #print(f"{ctr}: {hole} // {self.sum()}")
            
            if base: # Ended at home base, break the loop and reiterate
                gogo = False
            else: # On the normal enchilada.
                if self.holes[hole].nop == 1:                    
                    self.holes[hole].flush()
                    self.homes[player].add()
                    print("Take the L! Ended on a singularity!")
                    if (player == 0) and (hole in [0,1,2]):
                        gems = self.holes[hole+6].nop
                        self.holes[hole+6].flush()
                        self.homes[player].add(nop=gems)
                        pass
                    if (player == 1) and (hole in [6,7,8]):
                        gems = self.holes[hole-6].nop
                        self.holes[hole-6].flush()
                        self.homes[player].add(nop=gems)
                        pass
                    # if in home, snatch them other bitches. Wait with that.
                    gogo = False
                    
                # else continue as usual
                # why is it continuing
            if ctr >= rounds: # break check
                gogo = False

                
        return base,cleaned # status vector, we need to add for stop here too

    def sweep(self):
        status = False
        
        if self.clean(player=0):
            clean = True
            self.homes[0].add(nop=self.holes[6].nop+self.holes[7].nop+self.holes[8].nop)
            self.holes[6].flush()
            self.holes[7].flush()
            self.holes[8].flush()
            status = True
        if self.clean(player=1):
            clean = True
            self.homes[1].add(nop=self.holes[0].nop+self.holes[1].nop+self.holes[2].nop)
            self.holes[0].flush()
            self.holes[1].flush()
            self.holes[2].flush()
            status = True

        return status
        
    
def main(args=None):
    manxala = board(verbose=True)
    
    print("==========================================================================")
    manxala.show()

    if args.hole > 11:
        args.hole = None

    assert args.player in [0,1] 
    active_player = args.player
    active_hole = args.hole

    clean = False
    while not clean:
        print(f"Player {active_player} makes heris round.")
        base,clean = manxala.iter(player=active_player, 
                              hole=active_hole, 
                              rounds=args.rounds)
        active_hole = None

        manxala.sweep()
        
        if base:
            active_player = active_player
        else:
            active_player = 1-active_player



    manxala.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--plot",
                        help="Plotting of graphs",
                        action="store_true")

    parser.add_argument("--rounds",
                        help="Number of test runs", 
                        default=3, type=int)

    parser.add_argument("--player",
                        help="Player to start", 
                        default=0, type=int)

    parser.add_argument("--hole", help="Hole to start in", default = 0, type =  int)

    args = parser.parse_args()
    
    main(args=args)
