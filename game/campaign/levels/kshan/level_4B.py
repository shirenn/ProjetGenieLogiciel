from imports import *

class Level_4B_kshan(Level):
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_kshan4Bdv"].show(g)
            else:
                quit_all = g.dict_dial["dial_kshan4B"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_kshan4Bbf"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_kshan4Bgf"].show(g)
            if g.player.is_in_inventory(KeyItem("key_A")):
                quit_all = g.dict_dial["dial_kshan4f"].show(g)
                if not "Midden Pass" in g.save["accessible"]:
                    g.save["accessible"].append("Midden Pass")
        return quit_all
            
    def reward(self,g):
        g.player.set_inventory({KeyItem("key_B"):1})
        
    def check_victory(self,g,arg):
        return arg
        
        
    def launch(self,g):
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t * 100 #*8 to be faster (but it doesn't match the music anymore !
            
        #objects = self.init_objects(g)

        gl = GameLevel(self.objects,player_pos,name="level_4B_kshan",parallax=g.options["parallax"])
        
        #g.launch_music(text)
        
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
        deadly = DeadlyPotion(Hitbox(Rect(100,-2,10,10)))
        plat = []
        dist = -10
        h = 10
        for i in range(20):
            l = (i+1)*70%100 + 50
            plat.append(SolidPlatform(Hitbox(Rect(dist,h,l,16))))
            h += i*17%23 - 10
            dist += l+(i*9%13) +10
            if i == 8:
                plat.append(Antidote(Hitbox(Rect(dist,h-12,10,10))))
            else: 
                plat.append(Poison(Hitbox(Rect(dist,h-12,10,10))))
                
        flag = Flag(Hitbox(Rect(dist-20,-8,10,20)))
        
        return plat + [deadly,flag]
