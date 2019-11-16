import os,sys

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from vector import Vector
from transform import Transform
import random

class Line:
    """ Represents a line : y = ax+b """
    def __init__(self,a,b,vert=False,x=0):
        self.a = a
        self.b = b
        self.vert = vert
        self.x = x

    def is_point_up(self,p):
        """ Returns true if the point p is in the up side of the line """
        if self.vert:
            return p.x == self.x
        return p.y >= self.a*p.x+self.b

    def is_on_line(self,p):
        return p.y == self.a*p.x+self.b

    def intersect_point(self,l2):
        """ Returns the intersect point between two given lines """
        if self.vert:
            return Vector(self.x,l2.a*self.x+l2.b)
        if l2.vert:
            return Vector(l2.x,self.a*l2.x+self.b)
        if self.a-l2.a == 0:
            if self.b == l2.b:
                return Line(self.a,self.b) #Superposed lines
            return None #Parallel lines
        x = (l2.b-self.b)/(self.a-l2.a)
        y = self.a*x+self.b
        return Vector(x,y)

    def __eq__(self,l2):
        if self.vert and l2.vert:
            return self.x and l2.x
        if not(self.vert) and not(l2.vert):
            return self.a == l2.a and self.b == l2.b

    def __repr__(self):
        if self.vert:
            return "Line(vert,"+str(self.x)+")"
        return "Line("+str(self.a)+"x+"+str(self.b)+")"

class Segment:
    """ Represents a segment from vector p1 to vector p2 """
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

    def collide_line(self,l):
        """ Returns true if it collides a specific line """
        if l.is_on_line(self.p1) or l.is_on_line(self.p2):
            return True
        b1 = int(l.is_point_up(self.p1))
        b2 = int(l.is_point_up(self.p2))
        return (b1+b2) == 1

    def get_inter_segment(self,s):
        ls = s.get_line()
        l = self.get_line()
        inter_p = l.intersect_point(ls)
        if inter_p is None:
            return None #They don't collide
        else:
            if isinstance(inter_p,Line):
                #To check if collinear segments intersect (only check x coordinate is enough)
                sfsp1x = self.is_in_interval_x(s.p1.x)
                sfsp2x = self.is_in_interval_x(s.p2.x)
                ssfp1x = s.is_in_interval_x(self.p1.x)
                ssfp2x = s.is_in_interval_x(self.p2.x)
                if sfsp1x or sfsp2x or ssfp1x or ssfp2x:
                    return inter_p
                else:
                    return None
            else:
                #To check if a non collinear segments intersect (must check x and y)
                sfpx = self.is_in_interval_x(inter_p.x)
                spx = s.is_in_interval_x(inter_p.x)
                sfpy = self.is_in_interval_y(inter_p.y)
                spy = s.is_in_interval_y(inter_p.y)
                if sfpx and spx and sfpy and spy:
                    return inter_p
                else:
                    return None

    def collide_segment(self,s):
        return bool(self.get_inter_segment(s))
            

    def is_in_interval_x(self,x):
        """ Returns if x in the interval of this segment """
        minx = min(self.p1.x,self.p2.x)
        maxx = max(self.p1.x,self.p2.x)
        return minx <= x and x <= maxx

    def is_in_interval_y(self,y):
        """ Returns if x in the interval of this segment """
        miny = min(self.p1.y,self.p2.y)
        maxy = max(self.p1.y,self.p2.y)
        return miny <= y and y <= maxy
    
    def length(self):
        return ((self.p1.x-self.p2.x)**2+(self.p1.y-self.p2.y)**2)**0.5
        
    def get_line(self):
        if self.p1.x-self.p2.x == 0:
            return Line(0,0,True,self.p1.x)
        a = (self.p1.y-self.p2.y)/(self.p1.x-self.p2.x)
        b = self.p1.y - a*self.p1.x
        return Line(a,b)

    def __eq__(self,s):
        return self.p1 == s.p1 and self.p2 == s.p2

    def __repr__(self):
        return "Segment("+repr(self.p1)+","+repr(self.p2)+")"
        
class Polygon:
    """ Polygon made of a list of vector points"""
    def __init__(self,points):
        self.__points = points
        self.compute_segments()
        self.compute_max_min()

    def compute_segments(self):
        """ Computes segments from points """
        self.__segments = []
        for i in range(len(self.get_points())):
            p1 = self.get_points()[i%len(self.get_points())]
            p2 = self.get_points()[(i+1)%len(self.get_points())]
            self.__segments.append(Segment(p1,p2))

    def get_points(self):
        return self.__points

    def get_segments(self):
        return self.__segments
    
    def translate(self,vector):
        """ Translates the polygon """
        for p in self.get_points():
            p.x += vector.x
            p.y += vector.y

    def rotate(self,angle):
        t = Transform()
        t.rotate(angle)
        p = self.apply_transform(t)
        self.__init__(p.get_points())

    def point_in(self,point):
        """ Returns true if the vector point is in the polygon """
        epsilon = 10**-5
        if point in self.get_points():
            return True
        count = 0
        for s in self.get_segments():
            line = Line(0,point.y)
            while line.b == s.p1.y or line.b == s.p2.y:
                line.b += epsilon*random.random()
            ls = s.get_line()
            inter_p = line.intersect_point(ls)
            if not(inter_p is None) and inter_p.x <= point.x:
                if s.collide_line(line):
                    count += 1
        return count%2 == 1


    def intersect_segment(self,s):
        for si in self.get_segments():
            if s.collide_segment(si):
                return True
        return False

    def points_in(self,poly):
        """ Returns points of self that are in p """
        l = []
        for p in self.get_points():
            if poly.point_in(p):
                l.append(p)
        return l

    def segments_collide_with(self,poly):
        """ Returns segments of self that are in poly """
        l = []
        for s in self.get_segments():
            if poly.intersect_segment(s):
                l.append(s)
        return l

    def collide(self,poly):
        """ Returns True if the polygon collides with poly """
        if poly.points_in(self) != [] or poly.segments_collide_with(self) != []:
            return True
        return False

    def apply_transform(self,transform):
        li = []
        for p in self.get_points():
            v = transform.transform_vect(p)
            li.append(Vector(v[0][0],v[1][0]))
        poly = Polygon(li)
        return poly

    def compute_max_min(self):
        max_x = None
        min_x = None
        max_y = None
        min_y = None
        for p in self.get_points():
            if max_x is None or p.x > max_x:
                max_x = p.x
            if min_x is None or p.x < min_x:
                min_x = p.x
            if max_y is None or p.y > max_y:
                max_y = p.y
            if min_y is None or p.y < min_y:
                min_y = p.y
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y

    def get_max_x(self):
        return self.max_x

    def get_max_y(self):
        return self.max_y

    def get_min_x(self):
        return self.min_x

    def get_min_y(self):
        return self.min_y

    def copy(self):
        l = []
        for p in self.get_points():
            l.append(p.copy())
        return Polygon(l)

    def to_tuples(self):
        l= []
        for p in self.get_points():
            l.append((p.x,p.y))
        return l

    def __mul__(self,vect):
        l = []
        for p in self.get_points():
            l.append(p.copy()*vect)
        return Polygon(l)

    def __eq__(self,p):
        return self.get_points() == p.get_points()

    def __repr__(self):
        return "Poly("+str(self.get_points())+")"
