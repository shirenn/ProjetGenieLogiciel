from node import Node
import pygame
from vector import Vector
from spriteScheduler import SpriteScheduler

class SpriteNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.__state = 's' #stay,move,damaged,collision,
        self.__sps = None #
        self.animation_speed = 3
        self.animation_step = 0

        self.mapping = "Flat" #Flat : étiré // Repeatx : Repeted along x

    def copy(self):
        sn = SpriteNode()
        self.paste_in(sn)
        return sn

    def paste_in(self,sn):
        Node.paste_in(self,sn)
        sn.set_state(self.get_state())
        if self.get_sps() is not None:
            sn.set_sps(self.get_sps().copy())
        else:
            sn.set_sps(None)

    def set_sps(self,sche):
        self.__sps = sche

    def create_sps(self,name):
        """
        creates the SpriteScheduler associated with the name "name"
        to add/modify such a SpriteScheduler,
        feel free to change the corresponding json.
        """
        sche = SpriteScheduler(name)
        sche.load_automaton()
        sche.load_sprites()
        self.set_sps(sche)

    def get_sps(self):
        """ returns the spriteScheduler associated with the spriteNode"""
        return self.__sps

    def send_char(self,char):
        """ Sends some character of information to the SpriteScheduler """
        self.__sps.step(char)


    def set_state(self,state):
        self.__state = state

    def get_state(self):
        return self.__state

    def get_pos_camera(self,distorsion,box):
        scale,trans = distorsion
        transform = box.get_transform()
        world_pos = box.get_self_poly()
        world_rot = transform.cut_translate()
        world_tr = transform.get_translate()
        pos_vect_rot = world_pos.apply_transform(world_rot)
        pos_vect_rot_scal = pos_vect_rot
        pos_vect = pos_vect_rot_scal.apply_transform(world_tr).apply_transform(trans).apply_transform(scale)
        return pos_vect

    def aff(self,fen,distorsion):
        """ Aff this node on the camera"""
        scale,trans = distorsion
        if  self.__sps is not None:
            if self.__sps.loaded:
                if self.animation_step >= self.animation_speed:
                    self.__sps.step(self.__state)
                    self.animation_step = 0
                self.animation_step += 1
                img = self.__sps.get_sprite()
            else:
                print("Images should never be imported on-the-fly!")
                exit(0)
                s = self.__sps.get_sprite()
                img = pygame.image.load(s).convert_alpha()
            #image_dim = Vector(img.get_width(),img.get_height())
            #dist = scale.transform_vect(image_dim)
            #x,y = dist.to_tuple()
            #(bx,by,bw,bh) = self.get_hit_box().get_rect().get_coord()
            #print(" ",bw,bh)
            #print("xy",int(x),int(y))
            (px,py,pw,ph),a = self.get_pos_camera(distorsion,self.get_hit_box()).to_rect()
            if self.mapping == "Flat":
                img = pygame.transform.smoothscale(img,(int(pw),int(ph)))
                fen.blit(img,(int(px) ,int(py) ))
            elif self.mapping == "Repeatx":
                dx = px
                while dx < px+pw and ph != 0:
                    (w,h) = img.get_width(),img.get_height()
                    ratio = (ph/h)
                    img2 = pygame.transform.smoothscale(img,(int(ratio*w),int(ratio*h)))
                    fen.blit(img2,(int(dx),int(py)),(0,0,px+pw-dx,ph))
                    dx += w*ratio
                
        else:
            coll_box = self.get_pos_camera(distorsion,self.get_hit_box())
            rigid_box = self.get_pos_camera(distorsion,self.get_rigid_hit_box())
            pygame.draw.polygon(fen,(0,255,0),coll_box.to_tuples())
            pygame.draw.polygon(fen,(188,0,0),rigid_box.to_tuples())
