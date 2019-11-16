from vector import Vector
from node import Node
from spriteNode import SpriteNode
from polygone import *
from transform import Transform

import pygame

DEBUG = False

class MovableNode(SpriteNode):
    """ A node that can move with more powerful functions"""
    def __init__(self):
        super().__init__()
        self.__speed = Vector(0,0)
        self.__acc = Vector(0,0)
        self.__ang_speed = 0
        self.__ang_acc = 0
        self.__force_effect = {}
        self.__mass = 1 #kg
        self.__ang_inertia = 1 #SI

    def set_mass(self,val):
        self.__mass = val
    def get_mass(self):
        return self.__mass
    def set_ang_inertia(self,val):
        self.__ang_inertia = val
    def get_ang_inertia(self):
        return self.__ang_inertia
    def set_acc(self,val):
        self.__acc = val
    def get_acc(self):
        return self.__acc
    def set_ang_acc(self,val):
        self.__ang_acc = val
    def get_ang_acc(self):
        return self.__ang_acc
    def set_speed(self,speed):
        self.__speed = speed
    def get_speed(self):
        return self.__speed
    def set_ang_speed(self,speed):
        self.__ang_speed = speed
    def get_ang_speed(self):
        return self.__ang_speed
    
    def add_force(self,force):
        self.__force_effect[force] = None
    def affected_by_force(self,force):
        try:
            self.__force_effect[force]
            return True
        except KeyError:
            return False
    def list_forces(self):
        return list(self.__force_effect.keys())
    def move(self):
        self.translate(self.get_speed())
        self.rotate(self.get_ang_speed())
    def reverse_move(self):
        self.translate(-self.get_speed())
        self.rotate(-self.get_ang_speed())
    def compute_speed(self,dt):
        #Compute acc
        self.compute_effect_forces()
        #Compute speed
        self.set_speed(self.get_speed() + self.get_acc()*dt)
        self.set_ang_speed(self.get_ang_speed() + self.get_ang_acc()*dt)
    def compute_effect_forces(self):
        forces = self.list_forces()
        acc = Vector(0,0)
        ang_acc = 0
        for f in forces:
            (accf,ang_accf) = f.get_acc(self)
            acc += accf
            ang_acc += ang_accf
        self.set_acc(acc/self.get_mass())
        self.set_ang_acc(ang_acc/self.get_ang_inertia())

    def get_direction_rigid_collide(self,p):
        """ Returns either the point or the segment that first created a collision between self (moving) and p (not moving) """
        speed = -self.get_speed().copy()
        ang_speed = -self.get_ang_speed()
        factor_max = 1
        factor_min = 0
        timeout = 0
        while 1: #Proceeds by dichotomia assuming last pos wasn't creating a collision but the new one is
            factor = (factor_max+factor_min)/2
            self_cpy = self.get_hit_box().copy()
            assert self_cpy.collide(p)
            self_cpy.translate(speed*factor)
            self_cpy.rotate(ang_speed*factor)
            points_in = p.points_in(self_cpy)
            segments_collide = p.segments_collide_with(self_cpy)
            print("p",p)
            print("self cpy",self_cpy)
            print("factor",factor,points_in,segments_collide)
            if len(points_in) == 1:
                return points_in[0]
            if len(segments_collide) == 1:
                return segments_collide[0]
            if len(points_in) == 2 and len(segments_collide) == 0:
                return Segment(points_in[0],points_in[1])
            if len(points_in) < 1 and len(segments_collide) <1:
                factor_max = factor
            else:
                factor_min = factor
            timeout += 1
            if timeout > 100:
                assert False #Timeout in get_object_collide

    def get_segment_collide(self,p):
        obj = self.get_direction_rigid_collide(p)
        if isinstance(obj,Vector):
            p_points = p.get_points()
            assert len(p_points) > 1 #Rigid bodies can't be reduced to 1 point
            index = p_points.index(obj)
            p1 = p_points[(index-1)%len(p_points)]
            p2 = p_points[(index+1)%len(p_points)]
            s1 = Segment(p1,obj)
            s2 = Segment(obj,p2)
            s1_collide = self.get_hit_box().segments_collide_with(Polygon([s1.p1,s1.p2]))
            s2_collide = self.get_hit_box().segments_collide_with(Polygon([s2.p1,s2.p2]))
            """
            print("self",self)
            print("p",p)
            print("obj",obj)
            print("p_points",p_points)
            print("index",index)
            print("p1",p1)
            print("p2",p2)
            print("s1",s1)
            print("s2",s2)
            print("s1_collide",s1_collide)
            print("s2_collide",s2_collide)
            """
            
            assert s1_collide == s2_collide
            #s_collide = s1_collide + s2_collide
            return (s1_collide[0],-1)
        else:
            return (obj,1)

    def get_resistance_support(self,support):
        (seg,sg) = self.get_segment_collide(support.get_hit_box())
        (p1,p2) = (seg.p1,seg.p2)
        v = p2 + (-p1)
        v_orthn = v.orthogonal().normalise()
        if DEBUG:
            print("sg",sg)
            print("seg",seg)
            print("v",v)
            print("orth",v_orthn)
        return v_orthn*(self.get_speed().len())*sg

    def apply_reaction(self,support):
        
        #Get how to remove the collision
        correction = self.correct_collide_rigid_body(support)
        #Get how to correct the speed
        speed = self.get_resistance_support(support)
        #Correct position and speed
        self.translate(correction)
        self.set_speed(self.get_speed()+speed)
        if DEBUG:
            print("final self box",self.get_hit_box())
            print("final support box",support.get_hit_box())
            print("final collide",self.get_hit_box().collide(support.get_hit_box()))
            print("final rigid",self.get_rigid_hit_box().collide(support.get_rigid_hit_box()))

    def correct_collide_rigid_body(self,support):
        speed = -self.get_speed().copy()
        ang_speed = -self.get_ang_speed()
        factor_max = 1
        factor_min = 0
        timeout = 0
        while 1: #Proceeds by dichotomia assuming last pos wasn't creating a collision but the new one is
            factor = (factor_max+factor_min)/2
            self_cpy = self.get_hit_box().copy()
            self_cpy_rigid = self.get_rigid_hit_box().copy()
            assert self_cpy.collide(support.get_hit_box())
            self_cpy.translate(speed*factor)
            self_cpy.rotate(ang_speed*factor)
            self_cpy_rigid.translate(speed*factor)
            self_cpy_rigid.rotate(ang_speed*factor)
            if DEBUG:
                print("factor",factor)
            if self_cpy.collide(support.get_hit_box()):
                if self_cpy_rigid.collide(support.get_rigid_hit_box()):
                    factor_min = factor
                else:
                    if DEBUG:
                        print("resulting move",speed*factor)
                    return speed*factor
            else:
                factor_max = factor
            
            timeout += 1
            if timeout > 100:
                if DEBUG:
                    print("timeout speed",self.get_speed())
                    print("timeout self",self.get_hit_box())
                    print("timeout support",support.get_hit_box())
                    print("timeout rigid self",self.get_rigid_hit_box())
                    print("timeout rigid supppot",support.get_rigid_hit_box())
                assert False #Timeout in get_object_collide (rigid)
