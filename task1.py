import numpy as np
import os
import sys
from copy import deepcopy
from functools import reduce
from operator import add
positions = [ 'N','S','W','E','C']
positions_no = [0,1,2,3,4]
materials = [0,1,2]
arrows= [0,1,2,3]
states = ['D','R']
states_no = [0,1]
Health = [0,25,50,75,100]
Health_no = [0,1,2,3,4]
PRIZE = 50
Step_Cost = -10
Gamma = 0.999
Delta = 0.001
REWARD = np.zeros((5,3,4,2,5))
REWARD[:, :, :,:,0] = PRIZE
Utility = np.zeros((5,3,4,2,5))
# print(Utility[0][0][0][0][100])
class State:
    def __init__(self, position,material, num_arrows, state,health):
        if (position not in positions_no) or (num_arrows not in arrows) or (state not in states_no) or (material not in materials) or (health not in Health_no):
            raise ValueError
        
        self.pos = position
        self.mat = material
        self.arrow = num_arrows 
        self.state = state
        self.health= health

    def show(self):
        return (self.pos,self.mat,self.arrow,self.state,self.health)


s=State(4,0,0,0,4)


def north():
    if s.health==0:
        print('<',positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],'>',"None:[",0,"]")
    else :
        # 3 actions 
        # 1. Stay 
        s1= State(s.pos,s.mat,s.arrow,s.state,s.health)
        s2=State(3,s.mat,s.arrow,s.state,s.health)
        # s3=State(3,s.mat,s.arrow,1,s.health)
        # s4=State(s.pos,s.mat,s.arrow,1,s.health)

        Action_stay = 0.85*(Step_Cost + REWARD[s1.show()]+ Gamma*Utility[s1.show()]) +0.15*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])
        # print(Action_stay)
        # 2. Craft 
        Making_arrow=-10000
        if (s.mat>=1): 
            s1= State(s.pos,s.mat-1,min(s.arrow+1,3),s.state,s.health)
            s2= State(s.pos,s.mat-1,min(s.arrow+2,3),s.state,s.health)
            s3= State(s.pos,s.mat-1,min(s.arrow+3,3),s.state,s.health)

            Making_arrow = 0.5*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.35*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()]) +0.15*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])

        # 3. Move to Center
        s1= State(4,s.mat,s.arrow,s.state,s.health)
        s2=State(3,s.mat,s.arrow,s.state,s.health)

        Move_center  = 0.85*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.15*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])

        # print()
        if(Action_stay >= Making_arrow and Action_stay >= Move_center):
            print('<',positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],'>',"Stay:[",Action_stay,"]")
        elif (Making_arrow >= Action_stay and Making_arrow >= Move_center):
            print(positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],"Craft:[",Making_arrow,"]")
        else :
            print(positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],"Down:[",Move_center,"]")
        # print(max(Action_stay,max(Making_arrow,Move_center)))
        # Utility[s.show]= max(Action_stay,max(Making_arrow,Move_center))
        # print(Utility[s.show])


def east():
    if s.health==0:
        print('<',positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],'>',"None:[",0,"]")
    else :
        # 4 actions 
        arr = [0,0,0,0]
        # 1.Shooting arrow 
        Dormat_Shoot =-10000 
        Ready_Shoot = -10000
        if (s.state == 0):
            if s.arrow >=1:
                s1 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,max(s.health-1,0))
                s2 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,s.health)
                s3 =State(s.pos,s.mat,max(s.arrow-1,0),1,max(s.health-1,0))
                s4 =State(s.pos,s.mat,max(s.arrow-1,0),1,s.health)
            # print(s2.show())

                Dormat_Shoot= 0.9*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.1*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.9*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])+0.1*0.2*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])

        elif (s.state==1):
            if s.arrow>=1:
                s1= State(s.pos,s.mat,0,0,min(s.health+1,4))
                s2 = State(s.pos,s.mat,max(s.arrow-1,0),1,max(s.health-1,0))
                s3= State(s.pos,s.mat,max(s.arrow-1,0),1,s.health)

                Ready_Shoot = 0.5*(Step_Cost + REWARD[s1.show()] - 40  +Gamma*Utility[s1.show()]) +0.5*0.9*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.5*0.1*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])

        if (Dormat_Shoot > Ready_Shoot):
            arr[0]=Dormat_Shoot
        else : 
            arr[0]=Ready_Shoot

        # 2. Stays
        Dormat_Stay = -10000
        Ready_Stay = -10000
        if (s.state == 0):
            s1 =State(s.pos,s.mat,s.arrow,s.state,s.health)
            s1 =State(s.pos,s.mat,s.arrow,1,s.health)
            Dormat_Stay  =0.5*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.5*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])

        elif (s.state ==1):
            s1= State(s.pos,s.mat,0,0,min(s.health+1,4))
            s2 = State(s.pos,s.mat,s.arrow,1,s.health)
            # s3= State(s.pos,s.mat,s.arrow,1,s.health)
            Ready_Stay = 0.5*(Step_Cost + REWARD[s1.show()] -40 + Gamma*Utility[s1.show()])  +0.5*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])

        
        if (Dormat_Stay > Ready_Stay):
            arr[1]=Dormat_Stay
        else: 
            arr[1]= Ready_Stay

        # 3. moving to center 
        Dormat_center = -10000
        Ready_center = -10000
        if (s.state == 0):
            s1 =State(4,s.mat,s.arrow,s.state,s.health)
            s2 =State(4,s.mat,s.arrow,1,s.health)

            Dormat_center  =0.5*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()])  +0.5*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])

        elif (s.state ==1):
            s1= State(s.pos,s.mat,0,0,min(s.health+1,4))
            s2 = State(4,s.mat,s.arrow,1,s.health)

            Ready_center = 0.5*(Step_Cost + REWARD[s1.show()] -40 + Gamma*Utility[s1.show()])  +0.5*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])

        
        if (Dormat_center > Ready_center):
            arr[2]=Dormat_center
        else: 
            arr[2]= Ready_center
        # print(arr[2])
        # 4.  Shooting blade
        Dormat_blade = -10000
        Ready_blade = -10000
        if (s.state == 0):
            s1 =State(s.pos,s.mat,s.arrow,s.state,max(s.health-2,0))
            s2 =State(s.pos,s.mat,s.arrow,s.state,s.health)
            s3 =State(s.pos,s.mat,s.arrow,1,max(s.health-2,0))
            s4 =State(s.pos,s.mat,s.arrow,1,s.health)

            Dormat_blade= 0.2*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.8*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.2*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])+0.8*0.2*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])

        elif (s.state==1):
            s1= State(s.pos,s.mat,0,0,min(s.health+1,4))
            s2 = State(s.pos,s.mat,s.arrow,1,max(s.health-2,0))
            s3= State(s.pos,s.mat,s.arrow,1,s.health)

            Ready_blade = 0.5*(Step_Cost + REWARD[s1.show()] - 40  +Gamma*Utility[s1.show()]) +0.5*0.2*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.5*0.8*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])


        
        if (Dormat_blade > Ready_blade):
            arr[3]=Dormat_blade
        else: 
            arr[3]= Ready_blade
        # print(arr[3])
        mx = -10000
        ind = 0
        actions = ['SHOOT','STAY','LEFT','HIT']
        for i in range(4):
            if arr[i]>=mx:
                ind= i
                mx=arr[i]

        print(s.pos,s.mat,s.arrow,s.state,s.health,":",actions[ind],"[",max(arr),"]")

def south():
    if s.health==0:
        print('<',positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],'>',"None:[",0,"]")
    else :
        # 3 actions 
        arr = [0,0,0]
        # 1. Move to center 
        s1 =State(4,s.mat,s.arrow,s.state,s.health)
        s2 =State(3,s.mat,s.arrow,s.state,s.health)
        Move_center  = 0.85*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.15*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])
        arr[0]=Move_center
        # 2. Gather material 
        s1=State(s.pos,min(s.mat+1,2),s.arrow,s.state,s.health)
        s2=State(s.pos,s.mat,s.arrow,s.state,s.health)
        Gather= 0.75*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.25*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])
        arr[2]=Gather 
        # 3. Stays 
        s1 =State(s.pos,s.mat,s.arrow,s.state,s.health)
        s2 =State(3,s.mat,s.arrow,s.state,s.health)
        Stay_cost  = 0.85*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.15*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])
        arr[1]=Stay_cost

        mx = -10000
        ind = 0
        actions = ['UP','STAY','GATHER']
        for i in range(3):
            if arr[i]>=mx:
                ind= i
                mx=arr[i]
        
        print(positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],":",actions[ind],"[",max(arr),"]")
def west():
    if s.health==0:
        print('<',positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],'>',"None:[",0,"]")

    else :
        # 3 actions 
        arr = [-10000,0,0]
        # 1.Shooting arrow 
        if s.arrow>=1:
            s1 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,max(s.health-1,0))
            s2 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,s.health)
            Shoot= 0.25*(Step_Cost + REWARD[s1.show()]) + Gamma*Utility[s1.show()] +0.75*(Step_Cost + REWARD[s2.show()]) + Gamma*Utility[s2.show()]
            arr[0]=Shoot
        # 2. Stays
        s1 =State(s.pos,s.mat,s.arrow,s.state,s.health)
        Stay_cost  = (Step_Cost + REWARD[s1.show()]) + Gamma*Utility[s1.show()] 
        arr[1] =Stay_cost   
        # 3. moving to center 
        s1 =State(4,s.mat,s.arrow,s.state,s.health)
        Move_center  = (Step_Cost + REWARD[s1.show()]) + Gamma*Utility[s1.show()] 
        arr[2]=Move_center

        mx = -10000
        ind = 0
        actions = ['SHOOT','STAY','RIGHT']
        for i in range(3):
            if arr[i]>mx:
                ind= i
                mx=arr[i]
        
        print(positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],":",actions[ind],"[",max(arr),"]")

def center():
    if s.health==0:
        print('<',positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],'>',"None:[",0,"]")

    else :
        # 7 actions 
        arr = [0,0,0,0,0,0,0]
        # 1.Shooting arrow 
        # s1 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,s.health-25)
        # s2 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,s.health)
        # Shoot= 0.5*(Step_Cost + REWARD[s1.show()]) + Gamma*Utility[s1.show()] +
        #                 0.5*(Step_Cost + REWARD[s2.show()]) + Gamma*Utility[s2.show()]
        Dormat_Shoot =-10000 
        Ready_Shoot = -10000
        if (s.state == 0):
            if s.arrow>=1:
                s1 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,max(s.health-1,0))
                s2 =State(s.pos,s.mat,max(s.arrow-1,0),s.state,s.health)
                s3 =State(s.pos,s.mat,max(s.arrow-1,0),1,max(s.health-1,0))
                s4 =State(s.pos,s.mat,max(s.arrow-1,0),1,s.health)
                Dormat_Shoot= 0.9*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.1*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.9*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])+0.1*0.2*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])
        elif (s.state==1):
            if s.arrow>=1:
                s1= State(s.pos,s.mat,0,0,min(s.health+1,4))
                s2 = State(s.pos,s.mat,max(s.arrow-1,0),1,max(s.health-1,0))
                s3= State(s.pos,s.mat,max(s.arrow-1,0),1,s.health)
                Ready_Shoot = 0.5*(Step_Cost + REWARD[s1.show()] - 40  +Gamma*Utility[s1.show()]) +0.5*0.9*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.5*0.1*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])
        
        if (Dormat_Shoot > Ready_Shoot):
            arr[0]=Dormat_Shoot
        else : 
            arr[0]=Ready_Shoot
        # 2. Stays
        Dormant_Stay = -1000
        Ready_Stay = -1000
        if s.state==0:
            s1 =State(s.pos,s.mat,s.arrow,s.state,s.health)
            s2 =State(3,s.mat,s.arrow,s.state,s.health)
            s3=State(s.pos,s.mat,s.arrow,1,s.health)
            s4=State(3,s.mat,s.arrow,1,s.health)

            Dormant_Stay  = 0.85*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.15*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.85*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()]) + 0.15*0.2*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])
        if s.state ==1:
            s1 = State(s.pos,s.mat,0,0,min(s.health+1,4))
            s2=State(s.pos,s.mat,s.arrow,1,s.health)
            s3=State(3,s.mat,s.arrow,1,s.health)
            # s4=State(s.pos,s.mat,0,0,min(s.health+1,4))
            Ready_Stay  = 0.5*(Step_Cost + REWARD[s1.show()]-40 + Gamma*Utility[s1.show()]) +0.85*0.5*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.15*0.5*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()]) 
        
        if(Dormant_Stay > Ready_Stay):
            arr[1]=Dormant_Stay
        else:
            arr[1]=Ready_Stay

        # 3. moving to east

        Dormant_east =-1000
        Ready_east= -1000
        if (s.state==0):
            s1=State(3,s.mat,s.arrow,s.state,s.health)
            s2=State(3,s.mat,s.arrow,1,s.health)
            # s3=State(3,s.mat,s.arrow,s.state,s.health)
            # s4=State(3,s.mat,s.arrow,1,s.health)
            Dormant_east  = 0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.2*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])
        
        else : 
            s1=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s2=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s3=State(s.pos,s.mat,s.arrow,1,s.health)
            s2=State(s.pos,s.mat,s.arrow,1,s.health)
            # s3=State(3,s.mat,s.arrow,1,s.health)

            Ready_east = 0.5*(Step_Cost + REWARD[s1.show()]-40 + Gamma*Utility[s1.show()])+0.5*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])
        if (Dormant_east > Ready_east):
            arr[2]=Dormant_east
        else:
            arr[2]=Ready_east
        # 4. moving to west
        Dormant_west =-1000
        Ready_west= -1000
        if (s.state==0):
            s1=State(2,s.mat,s.arrow,s.state,s.health)
            s2=State(3,s.mat,s.arrow,s.state,s.health)
            s3=State(2,s.mat,s.arrow,1,s.health)
            s2=State(3,s.mat,s.arrow,1,s.health)
            # s3=State(3,s.mat,s.arrow,s.state,s.health)
            # s4=State(3,s.mat,s.arrow,1,s.health)
            Dormant_west  = 0.85*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.15*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.85*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()]) +0.15*0.2*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])
        
        else : 
            s1=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s2=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s3=State(s.pos,s.mat,s.arrow,1,s.health)
            s2=State(2,s.mat,s.arrow,1,s.health)
            s3=State(3,s.mat,s.arrow,1,s.health)

            Ready_west = 0.5*(Step_Cost + REWARD[s1.show()]-40 + Gamma*Utility[s1.show()])+0.5*0.85*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.5*0.15*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])
        if (Dormant_west > Ready_west):
            arr[3]=Dormant_west
        else:
            arr[3]=Ready_west

        # 5. moving to north
        Dormant_north =-1000
        Ready_north= -1000
        if (s.state==0):
            s1=State(0,s.mat,s.arrow,s.state,s.health)
            s2=State(3,s.mat,s.arrow,s.state,s.health)
            s3=State(0,s.mat,s.arrow,1,s.health)
            s2=State(3,s.mat,s.arrow,1,s.health)
            # s3=State(3,s.mat,s.arrow,s.state,s.health)
            # s4=State(3,s.mat,s.arrow,1,s.health)
            Dormant_north  = 0.85*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.15*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.85*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()]) +0.15*0.2*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])
        
        else : 
            s1=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s2=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s3=State(s.pos,s.mat,s.arrow,1,s.health)
            s2=State(0,s.mat,s.arrow,1,s.health)
            s3=State(3,s.mat,s.arrow,1,s.health)

            Ready_west = 0.5*(Step_Cost + REWARD[s1.show()]-40 + Gamma*Utility[s1.show()])+0.5*0.85*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.5*0.15*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])
        if (Dormant_north > Ready_north):
            arr[4]=Dormant_north
        else:
            arr[4]=Ready_north

        # 6. moving to south 
        Dormant_south =-1000
        Ready_south= -1000
        if (s.state==0):
            s1=State(1,s.mat,s.arrow,s.state,s.health)
            s2=State(3,s.mat,s.arrow,s.state,s.health)
            s3=State(1,s.mat,s.arrow,1,s.health)
            s2=State(3,s.mat,s.arrow,1,s.health)
            # s3=State(3,s.mat,s.arrow,s.state,s.health)
            # s4=State(3,s.mat,s.arrow,1,s.health)
            Dormant_south = 0.85*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.15*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.85*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()]) +0.15*0.2*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])
        
        else : 
            s1=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s2=State(s.pos,s.mat,0,0,min(s.health+1,4))
            # s3=State(s.pos,s.mat,s.arrow,1,s.health)
            s2=State(1,s.mat,s.arrow,1,s.health)
            s3=State(3,s.mat,s.arrow,1,s.health)

            Ready_south = 0.5*(Step_Cost + REWARD[s1.show()]-40 + Gamma*Utility[s1.show()])+0.5*0.85*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.5*0.15*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])
        if (Dormant_south > Ready_south):
            arr[5]=Dormant_south
        else:
            arr[5]=Ready_south


        #7. Shooting blade
      
        Dormat_blade = -10000
        Ready_blade = -10000
        if (s.state == 0):
            s1 =State(s.pos,s.mat,s.arrow,s.state,max(s.health-2,0))
            s2 =State(s.pos,s.mat,s.arrow,s.state,s.health)
            s3 =State(s.pos,s.mat,s.arrow,1,max(s.health-2,0))
            s4 =State(s.pos,s.mat,s.arrow,1,s.health)
            Dormat_blade= 0.1*0.8*(Step_Cost + REWARD[s1.show()] + Gamma*Utility[s1.show()]) +0.9*0.8*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.1*0.2*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])+0.2*0.9*(Step_Cost + REWARD[s4.show()] + Gamma*Utility[s4.show()])
        elif (s.state==1):
            s1= State(s.pos,s.mat,0,0,min(s.health+1,4))
            s2 = State(s.pos,s.mat,s.arrow,1,max(s.health-2,0))
            s3= State(s.pos,s.mat,s.arrow,1,s.health)
            Ready_blade = 0.5*(Step_Cost + REWARD[s1.show()] - 40  +Gamma*Utility[s1.show()]) +0.5*0.1*(Step_Cost + REWARD[s2.show()] + Gamma*Utility[s2.show()])+0.5*0.9*(Step_Cost + REWARD[s3.show()] + Gamma*Utility[s3.show()])
        
        if (Dormat_blade > Ready_blade):
            arr[6]=Dormat_blade
        else : 
            arr[6]=Ready_blade
        # print(arr[6])
        mx = -10000
        ind = 0
        actions = ['SHOOT','STAY','RIGHT','LEFT','UP','DOWN','HIT']
        for i in range(7):
            print(arr[i])
            if arr[i]>=mx:
                ind= i
                mx=arr[i]
        
        print(positions[s.pos],s.mat,s.arrow,states[s.state],Health[s.health],":",actions[ind],"[",max(arr),"]")




def update():
    if s.pos==0:
        north()
    elif s.pos==2:
        west()
    elif s.pos==1:
        south()
    elif s.pos==3:
        east()
    elif s.pos==4:
        center()

update()
            