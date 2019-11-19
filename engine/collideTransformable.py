import numpy as np
from transform import Transform
from vector import Vector
from transformable import Transformable
from hitbox import Hitbox
from polygone import *

class CollideTransformable(Transformable):
    def __init__(self):
        super().__init__()
        #-----------------------------
        #         Collisions
        #-----------------------------
        self.__rigid_body = False
        self.__collide = False
        self.__collide_hit_box = Polygon([Vector(0,0)])
        self.__rigid_hit_box = Polygon([Vector(0,0)])

    def copy(self):
        t = CollideTransformable()
        super().__init__(t)
        t.set_collide(self.get_collide())
        t.set_rigid_body(self.get_rigid_body())
        Hb = self.get_hit_box().copy()
        t.set_hit_box(Hb)
        return t

    def set_rigid_body(self,val):
        """ Sets whether it's a rigid body or not """
        self.__rigid_body = val
        if val:
            self.__collide = True #A rigid body collides

    def get_rigid_body(self):
        """ Returns if it's a rigid body """
        return self.__rigid_body

    def set_collide(self,val):
        """ Sets whether this can collide """
        self.__collide = val

    def get_collide(self):
        """ Returns if this collides """
        return self.__collide

    def set_hit_box(self,val):
        """ Set the collide hit box of this """
        self.__collide_hit_box = val
        self.__collide_hit_box.link(self)
        rigidhb = val.copy()
        rigidhb.rescale(0.999)
        self.set_rigid_hit_box(rigidhb)

    def get_hit_box(self):
        """ Compute the hit box according to the position / rotation / scale """
        return self.__collide_hit_box

    def set_rigid_hit_box(self,val):
        """ Set the rigid body hit box -- Don't use it if you don't know what you're doing """
        self.__rigid_hit_box = val
        self.__rigid_hit_box.link(self)

    def get_rigid_hit_box(self):
        """ Returns the rigid hit box """
        return self.__rigid_hit_box
