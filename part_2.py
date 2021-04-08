import sys
import numpy as np
from copy import deepcopy
from functools import reduce
from operator import add

GAMMA = 0.999
DELTA = 0.001
COST=-10
POINTS = 50

Positions=["C","N","E","S","W"]
States=["R","D"]
Health = [0,25,50,75,100]
States_monster=[0,1]
arrow_range = [0,1,2,3]
Material_ct = [0,1,2]
Health_mon= [0,1,2,3,4]
Sqaure_pos = [0,1,2,3,4]


utilities = np.zeros((5, 4, 3, 5,2))
a= "ABC"
policies = np.full((5, 4, 3, 5,2),a , dtype='object')
temp=np.zeros(utilities.shape)

REWARD = np.zeros((5, 4, 3, 5,2))
REWARD[0, :, :, :, :] = POINTS


class State:
 

    def __init__(self, enemy_health, num_arrows,num_materials,num_position,monster_state):
        if (enemy_health not in Health_mon) or (num_arrows not in arrow_range) or (num_materials not in Material_ct) or (num_position not in Sqaure_pos) or (monster_state not in States_monster) :
            raise ValueError

        self.position = num_position
        self.monsterState = monster_state
        self.health = enemy_health 
        self.arrows = num_arrows 
        self.materials = num_materials 
        
    def get(self):
        return (self.health, self.arrows, self.materials, self.position, self.monsterState)

    



def center(s):
        arr = [-1000,-1000,-1000,-1000,-1000,-1000,-1000]
        Move_Center=-1000
        if(s.monsterState==1):  
            s1= State( s.health , s.arrows, s.materials,3,1) 
            s2= State( s.health , s.arrows, s.materials,3,0) 
            s3= State( s.health , s.arrows, s.materials,2,1) 
            s4= State( s.health , s.arrows, s.materials,2,0) 

            Move_Center=( 0.85 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.15 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
                    
            

        else:  
            s1= State( s.health , s.arrows, s.materials,3,0) 
            health=min(s.health+1,4) 
            s2= State(health , 0, s.materials,0,1) 
            s3= State( s.health , s.arrows, s.materials,2,0) 
            health=min(s.health+1,4) 
            s4= State(health , 0, s.materials,0,1) 

            Move_Center= (0.85 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.15 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))

        arr[0]=Move_Center          

        #Move Up
        MoveUp=-1000
        if(s.monsterState==1):  
            s1= State( s.health , s.arrows, s.materials,1,1) 
            s2= State( s.health , s.arrows, s.materials,1,0)
            s3= State( s.health , s.arrows, s.materials,2,1)
            s4= State( s.health , s.arrows, s.materials,2,0) 
            MoveUp= (0.85 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.15 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
                    

        else:  
            s1= State( s.health , s.arrows, s.materials,1,0) 
            health=min(s.health+1,4) 
            s2= State( health , 0, s.materials,0,1)
            s3= State( s.health , s.arrows, s.materials,2,0) 
            s4= State(health , 0, s.materials,0,1) 

            MoveUp=( 0.85 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.15 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))
        
        arr[1]=MoveUp
        
        Move_Right=-1000
        if(s.monsterState==1):  
            s1= State( s.health , s.arrows, s.materials,2,1) 
            s2= State( s.health , s.arrows, s.materials,2,0) 
            s3= State( s.health , s.arrows, s.materials,2,1) 
            s4= State( s.health , s.arrows, s.materials,2,0) 

            Move_Right= (0.85 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.15 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
                    

        else:  
            s1= State( s.health , s.arrows, s.materials,2,0) 
            health=min(s.health+1,4) 
            s2= State( health , 0, s.materials,0,1) 
            s3= State( s.health , s.arrows, s.materials,2,0) 
            health=min(s.health+1,4) 
            s4= State( health , 0, s.materials,0,1) 

            Move_Right= (0.85 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.15 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))

        arr[2]=Move_Right
     
        MoveLeft=-1000
        if(s.monsterState==1):  
            s1= State( s.health , s.arrows, s.materials,4,1) 
            s2= State( s.health , s.arrows, s.materials,4,0)
            s3= State( s.health , s.arrows, s.materials,2,1) 
            s4= State( s.health , s.arrows, s.materials,2,0) 

            MoveLeft= (0.85 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.15 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
                    

        else: 
            s1= State( s.health , s.arrows, s.materials,4,0) 
            health=min(s.health+1,4) 
            s2= State( health , 0, s.materials,0,1)
            s3= State( s.health , s.arrows, s.materials,2,0) 
            s4= State( health , 0, s.materials,0,1)

            MoveLeft= (0.85 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.15 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))
        arr[3]=MoveLeft
      
        Donotmove=-1000
        if(s.monsterState==1):  
            s1= State( s.health , s.arrows, s.materials,0,1) 
            s2= State( s.health , s.arrows, s.materials,0,0)
            s3= State( s.health , s.arrows, s.materials,2,1) 
            s4= State( s.health , s.arrows, s.materials,2,0) 
            Donotmove= (0.85 * 0.8 *( COST+REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.2 *( COST+REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.15 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
                    

        else: 
            s1= State( s.health , s.arrows, s.materials,0,0) 
            health=min(s.health+1,4) 
            s2= State(health , 0, s.materials,0,1) 
            s3= State( s.health , s.arrows, s.materials,2,0)
            s4= State( health , 0, s.materials,0,1) 

            Donotmove= (0.85 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.85 * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.15 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15 * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))

        arr[4]=Donotmove

        Use_arrow=-1000
        
        if(s.monsterState==1):  
            if(s.arrows>=1):
                health=max(s.health-1,0)
                s1= State( health , s.arrows-1, s.materials,0,1) 
                s2= State( health , s.arrows-1, s.materials,0,0) 
                s3= State( s.health, s.arrows-1, s.materials,0,1) 
                s4= State( s.health , s.arrows-1, s.materials,0,0) 

                Use_arrow= (0.5 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.5 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.5 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.5 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
                        

        else:  
            if(s.arrows>=1):
                health=max(s.health-1,0)
                s1= State( health , s.arrows-1, s.materials,0,0) 
                health=min(s.health+1,4)
                s2= State( health , 0, s.materials,0,1) 
                s3= State( s.health , s.arrows-1, s.materials,0,0) 
                s4= State( health , 0, s.materials,0,1)

                Use_arrow= (0.5 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.5 * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.5 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.5 * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))
        arr[5]=Use_arrow
    
        Use_blade=-1000
        if(s.monsterState==1):  
            health=max(s.health-2,0)
            s1= State( health , s.arrows, s.materials,0,1) 
            s2= State( health , s.arrows, s.materials,0,0)
            s3= State( s.health, s.arrows, s.materials,0,1) 
            s4= State( s.health , s.arrows, s.materials,0,0) 

            Use_blade= (0.1 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.1 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.9 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.9 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
                    

        else:
            health=max(s.health-2,0)
            s1= State( health , s.arrows, s.materials,0,0)
            health= min(s.health+1,4)
            s2= State( health, 0, s.materials,0,1) 
            arrow_no=max(s.arrows-1,0)
            s3= State( s.health , arrow_no, s.materials,0,0) 
            s4= State( health , 0, s.materials,0,1) 

            Use_blade= (0.1 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ ( 0.1 ) * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.9 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ ( 0.9 ) * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))
        arr[6]=Use_blade
        mx = -10000
        ind = 0
        actions = ['DOWN','UP','RIGHT','LEFT','STAY','SHOOT','HIT']
        for i in range(7):
            # print(arr[i])
            if arr[i]>=mx:
                ind= i
                mx=arr[i]
        
        return max(arr),actions[ind]
def north(s):
        arr   = [-1000,-1000,-1000]
        Move_Center=-1000
        if(s.monsterState==1): 
            s1= State( s.health , s.arrows, s.materials,0,1) 
            s2= State( s.health , s.arrows, s.materials,2,1) 
            s3= State( s.health , s.arrows, s.materials,0,0) 
            s4= State( s.health , s.arrows, s.materials,2,0) 

            Move_Center=(0.85*0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.8*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.2*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.2*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))

        else: 
            s1= State( s.health , s.arrows, s.materials,0,0) 
            s2= State( s.health , s.arrows, s.materials,2,0) 
            s3= State( s.health , s.arrows, s.materials,0,1) 
            s4= State( s.health , s.arrows, s.materials,2,1) 
            Move_Center=(0.85*0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.5*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.5*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
        arr[0]=Move_Center
           
        Donotmove=-1000
        if(s.monsterState==1):     
            s1= State( s.health , s.arrows, s.materials,1,1)      
            s2= State( s.health , s.arrows, s.materials,2,1)      
            s3= State( s.health , s.arrows, s.materials,1,0)       
            s4= State( s.health , s.arrows, s.materials,2,0)        

            Donotmove= (0.85*0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.8*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.2*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.2*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))

        else:     
            s1= State( s.health , s.arrows, s.materials,1,0)        
            s2= State( s.health , s.arrows, s.materials,2,0) 
            s3= State( s.health , s.arrows, s.materials,1,1) 
            s4= State( s.health , s.arrows, s.materials,2,1) 

            Donotmove= (0.85*0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.5*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.5*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
        arr[1]=Donotmove
            
        Make_Arrow=-1000
        if(s.materials>=1):
            if(s.monsterState==1):     
                s1= State( s.health , min(3,s.arrows+1), s.materials-1,1,1)
                s2= State( s.health , min(3,s.arrows+2), s.materials-1,1,1) 
                s3= State( s.health , min(3,s.arrows+3), s.materials-1,1,1)
                s4= State( s.health , min(3,s.arrows+1), s.materials-1,1,0)
                s5= State( s.health , min(3,s.arrows+2), s.materials-1,1,0) 
                s6= State( s.health , min(3,s.arrows+3), s.materials-1,1,0)
                Make_Arrow= (0.5*0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.35 *0.8 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.15 *0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.5 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()])+ 0.35 *0.2*(COST + REWARD[s5.get()] + GAMMA*utilities[s5.get()])+ 0.15 *0.2*(COST + REWARD[s6.get()] + GAMMA*utilities[s6.get()]))

            else:     
                s1= State( s.health , min(3,s.arrows+1), s.materials-1,1,0)
                s2= State( s.health , min(3,s.arrows+2), s.materials-1,1,0) 
                s3= State( s.health , min(3,s.arrows+3), s.materials-1,1,0)
                s4= State( s.health , min(3,s.arrows+1), s.materials-1,1,1)
                s5= State( s.health , min(3,s.arrows+2), s.materials-1,1,1) 
                s6= State( s.health , min(3,s.arrows+3), s.materials-1,1,1)
                Make_Arrow= (0.5*0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.35 *0.5 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.15 *0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.5 * 0.5 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()])+ 0.35 *0.5*(COST + REWARD[s5.get()] + GAMMA*utilities[s5.get()])+ 0.15 *0.5*(COST + REWARD[s6.get()] + GAMMA*utilities[s6.get()]))
        arr[2]=Make_Arrow
        actions = ['DOWN','STAY','CRAFT']
        ind =0 
        mx = -10000
        for i in range(3):
            if arr[i]>=mx:
                ind= i
                mx=arr[i]
        return max(arr),actions[ind]
def west(s):
        arr =[-1000,-1000,-1000]
        if(s.monsterState==1):     
            s1= State( s.health , s.arrows, s.materials,0,1)         
            s2= State( s.health , s.arrows, s.materials,0,0)         
            Move_Right= (0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.2*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()]))
            arr[0]=Move_Right
        else:     
            s1= State( s.health , s.arrows, s.materials,0,0)         
            s2= State( s.health , s.arrows, s.materials,0,1)         
 

            Move_Right= (0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()]))

            arr[0]=Move_Right
    
                
           
        Donotmove=-1000
        if(s.monsterState==1):     
            s1= State( s.health , s.arrows, s.materials,4,1)         
            s2= State( s.health , s.arrows, s.materials,4,0)         
            Donotmove= (0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.2*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()]))
        
        else:     
            s1= State( s.health , s.arrows, s.materials,4,0)         
            s2= State( s.health , s.arrows, s.materials,4,1)         
 

            Donotmove=   (0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()]))
        arr[1]=Donotmove
        #SHOOT
        Use_arrow=-1000
        
        if(s.monsterState==1):     
            if(s.arrows>=1):
                s1= State( max(s.health-1,0) , s.arrows-1, s.materials,4,1)        
                s2= State( s.health, s.arrows-1, s.materials,4,1)         
                s3= State( max(s.health-1,0) , s.arrows-1, s.materials,4,0)        
                s4= State( s.health, s.arrows-1, s.materials,4,0)         
            
                Use_arrow= (0.25*0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.75*0.8*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.25*0.2*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.75*0.2*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))

        else:     
            if(s.arrows>=1):
                s1= State( max(s.health-1,0) , s.arrows-1, s.materials,4,0)        
                s2= State( s.health, s.arrows-1, s.materials,4,0)         
                s3= State( max(s.health-1,0) , s.arrows-1, s.materials,4,1)        
                s4= State( s.health, s.arrows-1, s.materials,4,1)         
            
                Use_arrow= (0.25*0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.75*0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.25*0.5*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()]) + 0.75*0.5*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
        arr[2]=Use_arrow
        mx = -10000
        ind = 0
        actions = ['RIGHT','STAY','SHOOT']
        for i in range(3):
            if arr[i]>=mx:
                ind= i
                mx=arr[i]
        return max(arr),actions[ind]
def south(s):
        arr = [0,0,0]
        MoveUp=Donotmove=Collect_mat=-1000
        if(s.monsterState==1):     
            s1= State( s.health , s.arrows, s.materials,0,1)      
            s2= State( s.health , s.arrows, s.materials,2,1)      
            s3= State( s.health , s.arrows, s.materials,0,0)       
            s4= State( s.health , s.arrows, s.materials,2,0)        

            MoveUp=(0.85*0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.8*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.2*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.2*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))

        else:     
            s1= State( s.health , s.arrows, s.materials,0,0) 
            s2= State( s.health , s.arrows, s.materials,2,0) 
            s3= State( s.health , s.arrows, s.materials,0,1) 
            s4= State( s.health , s.arrows, s.materials,2,1) 

            MoveUp=(0.85*0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.5*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.5*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
        arr[0]=MoveUp
           
        if(s.monsterState==1):     
            s1= State( s.health , s.arrows, s.materials,3,1)      
            s2= State( s.health , s.arrows, s.materials,2,1)      
            s3= State( s.health , s.arrows, s.materials,3,0)       
            s4= State( s.health , s.arrows, s.materials,2,0)        

            Donotmove= (0.85*0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.8*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.2*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.2*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))

        else:     
            s1= State( s.health , s.arrows, s.materials,3,0)        
            s2= State( s.health , s.arrows, s.materials,2,0) 
            s3= State( s.health , s.arrows, s.materials,3,1) 
            s4= State( s.health , s.arrows, s.materials,2,1) 

            Donotmove= (0.85*0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.15*0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.85*0.5*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.15*0.5*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))

        arr[1]=Donotmove
     
        if(s.monsterState==1):     
            s1= State( s.health , s.arrows, min(s.materials+1,2),3,1)
            s2= State( s.health , s.arrows, s.materials,3,1) 
            s3= State( s.health , s.arrows, min(s.materials+1,2),3,0)
            s4= State( s.health , s.arrows, s.materials,3,0) 
        
            Collect_mat = (0.75*0.8*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.25 *0.8*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.75*0.2*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.25 *0.2*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))

        else:
            s1= State( s.health , s.arrows, min(s.materials+1,2),3,0)
            s2= State( s.health , s.arrows, s.materials,3,0) 
            s4= State( s.health , s.arrows, min(s.materials+1,2),3,1)
            s3= State( s.health , s.arrows, s.materials,3,1) 
        
            Collect_mat = (0.75*0.5*(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.25 *0.5*(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.75*0.5*(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.25 *0.5*(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
        arr[2]=Collect_mat
        mx = -10000
        ind = 0
        actions = ['UP','STAY','GATHER']
        for i in range(3):
            if arr[i]>=mx:
                ind= i
                mx=arr[i]
        return max(arr),actions[ind]
def east(s):
        arr = [0,0,0,0]
        MoveLeft=Donotmove=Use_arrow=Use_blade=-1000
        if(s.monsterState==1):       
            s1= State( s.health , s.arrows, s.materials,0,1)         
            s2= State( s.health , s.arrows, s.materials,0,0)        
            MoveLeft= (0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()]) + 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()]))
            
                    

        else:       
            s1= State( s.health , s.arrows, s.materials,0,0)         
            s2= State( min(s.health+1,4) , 0, s.materials,2,1)         

            MoveLeft= (0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()]) + 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()]))
        arr[0]=MoveLeft

           
        if(s.monsterState==1):       
            s1= State( s.health , s.arrows, s.materials,2,1)         
            s2= State( s.health , s.arrows, s.materials,2,0)        

 

            Donotmove= (0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()]))
                    

        else:       
            s1= State( s.health , s.arrows, s.materials,2,0)         
            s2= State( min(s.health+1,4) , 0, s.materials,2,1)          

            Donotmove= (0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()]))

        arr[1]=Donotmove
        
        if(s.monsterState==1):       
            if(s.arrows>=1):
                s1= State( max(s.health-1,0) , s.arrows-1, s.materials,2,1)         
                s2= State( max(s.health-1,0) , s.arrows-1, s.materials,2,0)        
                s3= State( s.health, s.arrows-1, s.materials,2,1)         
                s4= State( s.health , s.arrows-1, s.materials,2,0)        

                Use_arrow= (0.9 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.9 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.1 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.1 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
        else:       
            if(s.arrows>=1):
                s1= State( max(s.health-1,0) , s.arrows-1, s.materials,2,0)         
                s2= State( min(s.health+1,4) , 0, s.materials,2,1)         
                s3= State( s.health , s.arrows-1, s.materials,2,0)         
                s4= State( min(s.health+1,4) , 0, s.materials,2,1)         

                Use_arrow= (0.9 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.9* 0.5 *(COST + REWARD[s2.get()] - 40 + GAMMA*utilities[s2.get()])+ 0.1 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.1 * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))
        arr[2]=Use_arrow
  
        if(s.monsterState==1):       
            s1= State( max(s.health-2,0) , s.arrows, s.materials,2,1)         
            s2= State( max(s.health-2,0) , s.arrows, s.materials,2,0)        
            s3= State( s.health, s.arrows, s.materials,2,1)         
            s4= State( s.health , s.arrows, s.materials,2,0)        
            Use_blade= (0.2 * 0.8 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ 0.2 * 0.2 *(COST + REWARD[s2.get()] + GAMMA*utilities[s2.get()])+ 0.8 * 0.8 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ 0.8 * 0.2 *(COST + REWARD[s4.get()] + GAMMA*utilities[s4.get()]))
        else:       
            s1= State( max(s.health-2,0) , s.arrows, s.materials,2,0)         
            s2= State( min(s.health+1,4) , 0, s.materials,2,1)         
            s3= State( s.health , max(s.arrows-1,0), s.materials,2,0)         
            s4= State( min(s.health+1,4) , 0, s.materials,2,1)         

            Use_blade= (0.2 * 0.5 *(COST + REWARD[s1.get()] + GAMMA*utilities[s1.get()])+ (0.2) * 0.5 *(COST + REWARD[s2.get()] - 40+ GAMMA*utilities[s2.get()])+ 0.8 * 0.5 *(COST + REWARD[s3.get()] + GAMMA*utilities[s3.get()])+ (0.8) * 0.5 *(COST + REWARD[s4.get()] -40 + GAMMA*utilities[s4.get()]))
        arr[3]=Use_blade
        mx = -10000
        ind = 0
        actions = ['LEFT','STAY','SHOOT','HIT']
        for i in range(4):
            if arr[i]>=mx:
                ind= i
                mx=arr[i]
        return max(arr), actions[ind]       
def update(s):
    action = 'NONE'
    utility= 0
    if(s.health==0):
        return 0, action
    if s.position==1:
        utility,action=north(s)
    elif s.position==4:
        utility,action=west(s)
    elif s.position==3:
        utility,action=south(s)
    elif s.position==2:
        utility,action=east(s)
    elif s.position==0:
        utility,action=center(s)
    return utility,action





def display(utilities, policies):
    utilities=np.around(utilities,4)
    for state, util in np.ndenumerate(utilities):
        utility_value = '{:.3f}'.format(util)        
        print(f'({Positions[state[3]]},{state[2]},{state[1]},{States[state[4]]},{Health[state[0]]}):{policies[state]}=[{utility_value}]')


orig_stdout = sys.stdout
f = open("./outputs/part_2_trace.txt", "w")
sys.stdout = f

ct = 1
value = True 
delta = 0
while value: 
    
    i=0
    while (i <5):
        k=0
        while (k <3):
            j=0
            while (j <4):
                m=0
                while (m <2):
                    l=0
                    while (l <5):
                        s=State(l,j,k,i,m)
                        temp[s.get()],policies[s.get()]=update(s)
                        diff = abs(temp[s.get()]-utilities[s.get()])
                        # utilities[s.get()]=temp[s.get()]
                        delta=max(delta, diff)
                        l+=1
                    m+=1
                j+=1
            k+=1
        i+=1
    utilities=deepcopy(temp)
    print(f'iteration={ct-1}')
    display( utilities, policies)
    
    if delta <= DELTA:
        value = False
    ct+=1
    delta = 0

sys.stdout = orig_stdout
f.close()