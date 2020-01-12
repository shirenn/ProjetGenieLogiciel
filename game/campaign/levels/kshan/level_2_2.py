from game.campaign.levels.imports import *

class Level_2_2_kshan(Level):
    """ all functions are explained in the Level abstract class """
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_accessed():
                quit_all = g.dict_dial["dial_kshan2_2dv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan2_2"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan2_2bf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan2_2gf"].show(g)
        return quit_all
        
    def check_victory(self,g,arg):
        return arg
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100 #*8 to be faster (but it doesn't match the music anymore !

        gl = GameLevel(self.objects,player_pos,name=g.dict_str["Evil Coins"],parallax=g.options["parallax"],limgpar=get_cave_bg(g),music="Soliloquy.mp3")
        gl.load_inventory(g.player.get_inventory())
        
        success = self.check_victory(g, g.launch_level(gl,None))
        pygame.event.get()#to capture inputs made during the wait
        
        
        if success:
            self.fun_dialogue(g,"good_end")
            self.set_finished()
            self.reward(g)
        else:
            self.fun_dialogue(g,"bad_end")
        
        return success
    
    def create_objects(self,g):
        obj = []
        dist = -10
        for i in range(10):
            l = (i+1)*70%100 + 50
            obj.append(SolidPlatform(Hitbox(Rect(dist,(i*-8)+10,l,16))))
            dist += l+(i*9%13) +10
            if i > 0:
                coin = Coin(Hitbox(Rect(dist+2,(i*-8)-10,10,10)))
                obj.append(coin)
            
        for i in range(10,20):
            l = (i+1)*70%100 + 50
            obj.append(SolidPlatform(Hitbox(Rect(dist,((i-10)*12)-62,l,16))))
            dist += l+(i*9%13) +10
            coin = Coin(Hitbox(Rect(dist+l//2,((i-10)*12)-72,10,10)))
            obj.append(coin)
        obj.append(Flag(Hitbox(Rect(dist+l//4,43,10,20))))
        obj.append(SolidPlatform(Hitbox(Rect(dist+l//4,63,16,16))))
        
        return obj
