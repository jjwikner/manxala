#!/usr/bin/python3
# ================
import matplotlib.pyplot as plt
import argparse
import numpy as np
 
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica"
})


class objDraw():
 
    def __init__(self, xy=(0,0)):
        x,y = xy        
        self.lw = 2
        self.xx = []
        self.yy = []
        self.x0 = x
        self.y0 = y
        self.p = {}
        self.l = []        
        self.angle = 0
        self.direction = None
        self.circlek = 14
        self.put(xy)
        
    def circle(self,xy=(0,0),r=0):
        xx  = []
        yy  = []
        x,y = xy
        for m in range(self.circlek):
            # This is a oneliner in numpy, but for sake of
            # potential revertion to lists...
            xx.append(x+r*np.cos(np.pi*2*m/self.circlek))
            yy.append(y+r*np.sin(np.pi*2*m/self.circlek))
        xx.append(xx[0])
        yy.append(yy[0])
        
        return (xx,yy)
            
            
    def bbox(self):
        xmax = -1e13
        ymax = -1e13
        xmin = 1e13
        ymin = 1e13
 
        for pt_no,pts in enumerate(self.xx):
            if max(pts) > xmax:
                xmax = max(pts)
            if min(pts) < xmin:
                xmin = min(pts)
 
            if max(self.yy[pt_no]) > ymax:
                ymax = max(self.yy[pt_no])
 
            if min(self.yy[pt_no]) < ymin:
                ymin = min(self.yy[pt_no])
 
        return (xmin,ymin,xmax,ymax)
 
 
    def plot(self):
        # ---
        for pt_no,pts in enumerate(self.xx):
            plt.plot(pts, self.yy[pt_no],'-k',
                     linewidth=self.lw)
      
    def flip(self, direction=None):
        self.direction=direction
        mmx = []
        mmy = []
        # This can be done so much neater...
        # Consider using numpy instead.
        if direction == "x":
            for pt_no,x_pts in enumerate(self.x):
                y_pts = self.y[pt_no]           
                lx = []
                ly = []
                for pt_nox,x_pt in enumerate(x_pts):
                    y_pt = y_pts[pt_nox]               
                    lx.append(-x_pt)
                    ly.append(y_pt)
                   
                mmx = mmx + [lx]
                mmy = mmy + [ly]
            self.x = mmx
            self.y = mmy
            for port in self.p:
                self.p[port] = (-self.p[port][0],self.p[port][1])

            labels = []
            for label in self.l:
                label["pos"]  = (-label["pos"][0], label["pos"][1])
                labels.append( label )
            self.l = labels
            
        if direction == "y":
            for pt_no,x_pts in enumerate(self.x):
                y_pts = self.y[pt_no]           
                lx = []
                ly = []
                for pt_nox,x_pt in enumerate(x_pts):
                    y_pt = y_pts[pt_nox]               
                    lx.append(x_pt)
                    ly.append(-y_pt)
 
                mmx = mmx + [lx]
                mmy = mmy + [ly]
 
            self.x = mmx
            self.y = mmy
            for port in self.p:
                self.p[port] = (self.p[port][0],-self.p[port][1])
 
            labels = []
            for label in self.l:
                label["pos"]  = (label["pos"][0], -label["pos"][1])
                labels.append( label )
            self.l = labels
 
        self.move((self.x0,self.y0))
 
    def rot(self, theta=0):
        self.angle = theta
        # x and y directions
        rott = np.array([[np.cos(theta), -np.sin(theta)],
                         [np.sin(theta), np.cos(theta)]])       
        mmx = []
        mmy = []
        for pt_no,x_pts in enumerate(self.x):
            y_pts = self.y[pt_no]           
            lx = []
            ly = []
            for pt_nox,x_pt in enumerate(x_pts):
                y_pt = y_pts[pt_nox]               
                new = np.dot(rott, np.array([x_pt,y_pt]))
                lx.append(new[0])
                ly.append(new[1])
 
            mmx = mmx + [lx]
            mmy = mmy + [ly]
 
        self.x = mmx
        self.y = mmy
        
        for port in self.p:
            self.p[port] = np.dot(rott, np.array(self.p[port])).tolist()

        # Use a label class instead...
        
        labels = []        
        for label in self.l:
            label["pos"] = np.dot(rott, np.array(label["pos"])).tolist()
            labels.append(label)
        self.l = labels
        
        # Places the devices
        self.move((self.x0, self.y0))
 
    def move(self, xy=(0,0)):
        x,y=xy
        self.xx = []
        self.yy = []
        self.x0 = x
        self.y0 = y
       
        for pt_no,pts in enumerate(self.x):           
            self.xx = self.xx + [[self.x0+xx for xx in pts]]
            self.yy = self.yy + [[self.y0+yy for yy in self.y[pt_no]]]

        for port in self.p:
            xx,yy = self.p[port]
            setattr(self, port, (self.x0+xx,self.y0+yy))
        
    def ports(self):
        for port in self.p:
            x,y = self.p[port]
            plt.text(x+self.x0,y+self.y0," "+port,rotation=self.angle*180/np.pi)
            plt.plot(x+self.x0,y+self.y0,'ko')

        for label in self.l:
            print(label)
            try:
                x,y = label["pos"]
                plt.text(x+self.x0,y+self.y0," " + label["label"],
                         rotation=self.angle*180/np.pi)
            except:
                pass # undefined
            # plt.plot(x+self.x0,y+self.y0,'ko')
            
class op_(objDraw):
    def put(self, xy=(0,0)):
        x,y = xy
        self.x = [ [0, 0, 0.75, 0], [-0.25, 0], [-0.25, 0], [0.75, 1]]
        self.y = [ [0, 1, 0.5, 0], [0.75, 0.75], [0.25, 0.25], [0.5,0.5] ]
        self.p = {'vp': (-0.25, 0.75),
                  'vn': (-0.25, 0.25),
                  'vo': (1, 0.5)}
        self.l = [{"label": "OP1", "pos": (0.125,0.5)}]
        self.move(xy)
                  
class op(objDraw):
    def put(self, xy=(0,0)):
        x,y = xy
        self.x = [ [0, 0, 0.75, 0], [-0.25, 0], [-0.25, 0], [0.75, 1]]
        self.y = [ [0, 1, 0.5, 0], [0.75, 0.75], [0.25, 0.25], [0.5,0.5] ]
        self.p = {'vp': (-0.25, 0.75),
                  'vn': (-0.25, 0.25),
                  'vo': (1, 0.5)}
        self.l = [{"label": "OP1", "pos": (0.125,0.5)}]
        self.move(xy)

class vgnd(objDraw):
    def put(self, xy=(0,0)):
        x,y = xy
        self.x = [[0,0,0.125,0,-0.125,0]]
        self.y = [[0,-0.25,-0.25, -0.3,-0.25, -0.25]]
        self.p = {'gnd': (0,0) }
        self.move(xy)
        
class vsrc(objDraw):
    def put(self, xy=(0,0)):
        x,y = xy
        r = 0.15
        xx,yy = self.circle((0,0),r=r)
        self.x = [xx, [0,0],[0,0] ]
        self.y = [yy, [-r,-0.5],[r,0.5]]
        self.p = {'vn': (0,-0.5),
                  'vp': (0,0.5) }
        self.move(xy)

class wire(objDraw):
    # Change this to contain segments further down the road.
    def put(self, xy=(0,0)):
        x,y = xy
        self.x = [ [0, 1] ]
        self.y = [ [0, 0] ]
        self.p = {}
        self.move(xy)
 
class resistor(objDraw):
    def put(self, xy=(0,0)):
        x,y = xy
        self.x = [ [0.25, 0.25, 0.75, 0.75, 0.25], [0, 0.25], [0.75, 1] ]
        self.y = [ [-0.05, 0.05, 0.05, -0.05, -0.05], [0, 0], [0, 0] ]
        self.p = {} # {'p': (-0.25,0), 'n': (0.75,0) }
        self.move(xy)

class connector(objDraw):
    def put(self, xy=(0,0), direction="in"):
        x,y = xy
        if direction == "out":            
            self.x = [ [0, 0.25, 0.25, 0.3, 0.35, 0.3, 0.25, 0.25] ]
            self.y = [ [0, 0, 0.05, 0.05, 0, -0.05, -0.05, 0] ]
        if direction == "in":            
            self.x = [ [0, -0.25, -0.3, -0.35, -0.35, -0.3, -0.25] ]
            self.y = [ [0, 0, 0.05, 0.05, -0.05, -0.05, 0] ]
        
        self.p = {} # {'p': (-0.25,0), 'n': (0.75,0) }
        self.move(xy)
    
class capacitor(objDraw):
    def put(self, xy=(0,0)):
        x,y = xy
        self.x = [ [0.45, 0.45], [0.55, 0.55], [0, 0.45], [0.55, 1] ]
        self.y = [ [-0.1, 0.1],[-0.1, 0.1],  [0, 0], [0, 0] ]
        self.p = {} # {'p': (-0.25,0), 'n': (0.75,0) }
        self.move(xy)

class label(objDraw):
    ###
    def put(self, xy=(0,0), label="Hej"):
        x,y = xy
        self.x = [ [x] ]
        self.y = [ [y] ]
        setattr(self, p, {'label': (x, y) } )
        setattr(self, 'label', (x,y))
        self.move(xy)
        
    
# Then a bundle-class for circuits
class circuit():
    def define(self):
        pass
   
# Get points of ports and find way to connect them.
 
 
class canvas():
 
    def __init__(self, figure=1):
        self.figure = figure
        self.objects = []
        self.title = r'Figure 1: \textbf{Operational amplifiers and a resistor.}'
 
    def bbox(self):
        xmax = -1e13
        ymax = -1e13
 
        xmin = 1e13
        ymin = 1e13
 
        for obj in self.objects:
            xxmin,yymin,xxmax,yymax = obj.bbox()
            if xxmin < xmin:
                xmin = xxmin
            if yymin < ymin:
                ymin = yymin
 
            if xxmax > xmax:
                xmax = xxmax
 
            if yymax > ymax:
                ymax = yymax
        return (xmin,ymin,xmax,ymax)
               
 
    def show(self):
        plt.figure(self.figure)
        for obj in self.objects:
            # print(obj)
            obj.ports()
            obj.plot()
 
        xmin,ymin,xmax,ymax = self.bbox()
        plt.xlim([min([xmin,ymin]),max([xmax,ymax])])
        plt.ylim([min([xmin,ymin]),max([xmax,ymax])])
        plt.title(self.title,fontsize=16)
        plt.axis('off')
        #plt.grid(True)
        plt.show()
       
    def save(self):
        plt.figure(self.figure)
        plt.savefig("hej.png")
       
    def example(self):
        # ----
        opx1 = op()
        # print(opx1)
        opx1.put()
        opx1.rot(theta=np.pi)
 
        opx2 = op()
        opx2.put((2,0))
        opx2.flip(direction="x")
 
        opx3 = op()
        opx3.put((0,2))
        opx3.flip(direction="y")
 
        res1 = resistor()
        res1.put((-1,2))
        res1.rot(theta = np.pi/2.0)
       
        wire1 = wire()
        wire1.put()
        wire1.x = [[0,1,2,3]]
        wire1.y = [[0,0,-1,2]]
        wire1.move((2,1.5))
 
        # This is perhaps not what we want to do ? Objects are objects and canvas a set of object sets.
        # Revise this
        self.objects = self.objects + [opx1, opx2, opx3, res1, wire1]
   
    def rot_objects(self, objects=None, theta = 30):
 
        rott = np.array([[np.cos(theta), -np.sin(theta)],
                         [np.sin(theta), np.cos(theta)]])       
 
        if objects is None:
            objects = self.objects
 
        for obj in objects:
            obj.rot(theta=theta)
            #obj.ports()
            new = np.dot(rott, [obj.x0, obj.y0])
            obj.move((new[0],new[1]))
 
    def inverting_op(self):

        opx = op_((0,0))
        opx.flip(direction="y")
        
        R0 = resistor((-0.25,0.25))

        R1 = resistor((-0.25,0.25))
        R1.flip(direction='x')

        w1 = wire()
        w1.x = [[-0.25,-0.25]] # <-- something new here.
        w1.y = [[0.25,-0.25]]
        w1.move() # This is also dodgy
 
        w2 = wire()
        w2.x = [[0.75,1,1]]
        w2.y = [[0.25,0.25,-0.5]]
        w2.move()

        src = vsrc((-1.25,-0.25))

        cap = capacitor((0.5,0.5))
        cap.rot(np.pi/2.0)

        conn1 = connector() # Fix to init
        conn1.put(opx.vo, direction="out")
        
        conn2 = connector()
        conn2.put(src.vp, direction="in")

        gnd1 = vgnd(opx.vp)
        gnd2 = vgnd(src.vn)
        
        self.objects = self.objects + [opx, R0, R1, w1, w2,
                                       src, gnd1, gnd2, cap, conn1 , conn2]
  
       
# ================       
 
def main(args=None):
    cv = canvas()
    cv.inverting_op()
    print("===")
    cv.show()
    cv.rot_objects(theta = np.pi/3)
    cv.show()
   
 
# ================
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_known_args()[0]   
    main(args=args)
    exit
 
# ================
