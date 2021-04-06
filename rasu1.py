import numpy as np
from copy import deepcopy
from functools import reduce
from operator import add

HashArr=["C","N","E","S","W"]
HashArr1=["R","D"]

NewUtil=np.NINF
BestAction="NULL"
HEALTH_RANGE = 5
ARROWS_RANGE = 4
MATERIALS_RANGE=3
POSITION_RANGE=5
MONSTER_STATES_RANGE=2 
ACTION_RANGE=10

HEALTH_VALUES = tuple(range(HEALTH_RANGE))
ARROWS_VALUES = tuple(range(ARROWS_RANGE))
MATERIALS_VALUES = tuple(range(MATERIALS_RANGE))
POSITION_VALUES = tuple(range(POSITION_RANGE))
MONSTER_STATE_VALUES=tuple(range(MONSTER_STATES_RANGE))
ACTION_VALUES=tuple(range(ACTION_RANGE))
#print(ACTION_VALUES)

HEALTH_FACTOR = 25 # 0, 25, 50, 75, 100
ARROWS_FACTOR = 1 # 0, 1, 2, 3
MATERIALS_FACTOR = 1 # 0, 1, 2
POSITION_FACTOR=1 # 0, 1, 2, 3, 4
MONSTER_STATES_FACTOR=1 #0: Ready, 1: Dormant
ACTION_FACTOR=1 

ACTION_SHOOT = 0
ACTION_HIT = 1
ACTION_UP=2
ACTION_DOWN=3
ACTION_RIGHT=4
ACTION_LEFT=5
ACTION_STAY=6
ACTION_GATHER=7
ACTION_CRAFT=8
ACTION_STAY=9

TEAM = 34
Y = [1/2, 1,2]
PRIZE = 50
COST = -10/Y[TEAM%3]
#COST=-10

GAMMA = 0.999
DELTA = 0.001

# Center=0, North=1, East=2, South=3, West=4

utilities = np.zeros((HEALTH_RANGE, ARROWS_RANGE, MATERIALS_RANGE, POSITION_RANGE,MONSTER_STATES_RANGE))
policies = np.full((HEALTH_RANGE, ARROWS_RANGE, MATERIALS_RANGE, POSITION_RANGE, MONSTER_STATES_RANGE), -1, dtype='int')
temp=np.zeros(utilities.shape)

def value_iteration():
    global utilities
    index = 1
    while True: # one iteration of value iteration
        delta = 0
        # temp=np.zeros(utilities.shape)
        for l in range(0,5):
            for k in range(0,3):
                for j in range(0,4):
                    for m in range(0,2):
                        for i in range (0,5):
                            stt=State(i,j,k,l,m)
                            ANS=action(stt)
                            temp[stt.show()],policies[stt.show()]=action(stt)
                            delta=max(delta, abs(temp[stt.show()]-utilities[stt.show()]))

        utilities=deepcopy(temp)
        trace(index, utilities, policies)
        
        index +=1
        if delta <= DELTA:
            break
class State:
other

    def __init__(self, enemy_health, num_arrows,num_materials,num_position,monster_state):
        if (enemy_health not in HEALTH_VALUES) or (num_arrows not in ARROWS_VALUES) or (num_materials not in MATERIALS_VALUES) or (num_position not in POSITION_VALUES) or (monster_state not in MONSTER_STATE_VALUES) :
            print(enemy_health,num_arrows,num_materials,num_position,monster_state)
other

            raise ValueError
        
        self.health = enemy_health 
        self.arrows = num_arrows 
        self.materials = num_materials 
        self.position = num_position
        self.monsterState = monster_state

    def show(self):
        return (self.health, self.arrows, self.materials, self.position, self.monsterState)

    def __str__(self):
        return f'({self.health},{self.arrows},{self.materials},{self.position},{self.monsterState})'

REWARD = np.zeros((HEALTH_RANGE, ARROWS_RANGE, MATERIALS_RANGE, POSITION_RANGE, MONSTER_STATES_RANGE))
REWARD[0, :, :, :, :] = PRIZE

def action(state):
    # returns cost, array of tuple of (probability, state)
    # state = State(*state)

    NewUtil=np.NINF
    BestAction=-2
    DownCost=np.NINF
    UpCost=np.NINF
    LeftCost=np.NINF
    RightCost=np.NINF
    StayCost=np.NINF
    CraftCost=np.NINF
    HitCost=np.NINF
    ShootCost=np.NINF
    GatherCost=np.NINF
    if(state.health==0):
        return 0, -1 #"NONE"

    if(state.position==0):   #Pos::center #Availaible actions : Up, Down, Right, Left, None, shoot, stay, hit
        
        #Move Down
        if(state.monsterState==1):  #Dormant state
            state1= State( state.health , state.arrows, state.materials,3,1) #MM stays dormant : Success of Action
            state2= State( state.health , state.arrows, state.materials,3,0) #MM becomes ready : Success of Action
            state3= State( state.health , state.arrows, state.materials,2,1) #MM stays dormant : Failure of Action
            state4= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Failure of Action

            DownCost=( 0.85 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.15 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                    
            

        elif(state.monsterState==0):  #Ready state
            state1= State( state.health , state.arrows, state.materials,3,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL
            state3= State( state.health , state.arrows, state.materials,2,0) #MM stays ready  : Failure of Action
            state4= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL

            DownCost= (0.85 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
            + 0.15 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))
                     

        #Move Up
        if(state.monsterState==1):  #Dormant state
            state1= State( state.health , state.arrows, state.materials,1,1) #MM stays dormant : Success of Action
            state2= State( state.health , state.arrows, state.materials,1,0) #MM becomes ready : Success of Action
            state3= State( state.health , state.arrows, state.materials,2,1) #MM stays dormant : Failure of Action
            state4= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Failure of Action

            UpCost= (0.85 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.15 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                    

        elif(state.monsterState==0):  #Ready state
            state1= State( state.health , state.arrows, state.materials,1,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL
            state3= State( state.health , state.arrows, state.materials,2,0) #MM stays ready  : Failure of Action
            state4= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL

            UpCost=( 0.85 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
            + 0.15 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))
        

        #Move Right
        if(state.monsterState==1):  #Dormant state
            state1= State( state.health , state.arrows, state.materials,2,1) #MM stays dormant : Success of Action
            state2= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Success of Action
            state3= State( state.health , state.arrows, state.materials,2,1) #MM stays dormant : Failure of Action
            state4= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Failure of Action

            RightCost= (0.85 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.15 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                    

        elif(state.monsterState==0):  #Ready state
            state1= State( state.health , state.arrows, state.materials,2,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL
            state3= State( state.health , state.arrows, state.materials,2,0) #MM stays ready  : Failure of Action
            state4= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL

            RightCost= (0.85 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
            + 0.15 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))

        
        #Move Left
        if(state.monsterState==1):  #Dormant state
            state1= State( state.health , state.arrows, state.materials,4,1) #MM stays dormant : Success of Action
            state2= State( state.health , state.arrows, state.materials,4,0) #MM becomes ready : Success of Action
            state3= State( state.health , state.arrows, state.materials,2,1) #MM stays dormant : Failure of Action
            state4= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Failure of Action

            LeftCost= (0.85 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.15 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                    

        elif(state.monsterState==0):  #Ready state
            state1= State( state.health , state.arrows, state.materials,4,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL
            state3= State( state.health , state.arrows, state.materials,2,0) #MM stays ready  : Failure of Action
            state4= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL

            LeftCost= (0.85 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
            + 0.15 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))

        #STAY
        if(state.monsterState==1):  #Dormant state
            state1= State( state.health , state.arrows, state.materials,0,1) #MM stays dormant : Success of Action
            state2= State( state.health , state.arrows, state.materials,0,0) #MM becomes ready : Success of Action
            state3= State( state.health , state.arrows, state.materials,2,1) #MM stays dormant : Failure of Action
            state4= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Failure of Action

            StayCost= (0.85 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.15 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                    

        elif(state.monsterState==0):  #Ready state
            state1= State( state.health , state.arrows, state.materials,0,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL
            state3= State( state.health , state.arrows, state.materials,2,0) #MM stays ready  : Failure of Action
            state4= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL

            StayCost= (0.85 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.85 * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
            + 0.15 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15 * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))


        #SHOOT
        if(state.arrows>=1):
            if(state.monsterState==1):  #Dormant state
                state1= State( max(state.health-1,0) , state.arrows-1, state.materials,0,1) #MM stays dormant : Success of Action
                state2= State( max(state.health-1,0) , state.arrows-1, state.materials,0,0) #MM becomes ready : Success of Action
                state3= State( state.health, state.arrows-1, state.materials,0,1) #MM stays dormant : Failure of Action
                state4= State( state.health , state.arrows-1, state.materials,0,0) #MM becomes ready : Failure of Action

                ShootCost= (0.5 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.5 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
                + 0.5 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
                + 0.5 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                        

            elif(state.monsterState==0):  #Ready state
                state1= State( max(state.health-1,0) , state.arrows-1, state.materials,0,0) #MM stays ready : Success of Action
                state2= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL
                state3= State( state.health , state.arrows-1, state.materials,0,0) #MM stays ready  : Failure of Action
                state4= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL

                ShootCost= (0.5 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.5 * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
                + 0.5 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
                + 0.5 * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))

        #HIT  
        if(state.monsterState==1):  #Dormant state
            state1= State( max(state.health-2,0) , state.arrows, state.materials,0,1) #MM stays dormant : Success of Action
            state2= State( max(state.health-2,0) , state.arrows, state.materials,0,0) #MM becomes ready : Success of Action
            state3= State( state.health, state.arrows, state.materials,0,1) #MM stays dormant : Failure of Action
            state4= State( state.health , state.arrows, state.materials,0,0) #MM becomes ready : Failure of Action

            HitCost= (0.1 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.1 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.9 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.9 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                    

        elif(state.monsterState==0):  #Ready state
            state1= State( max(state.health-2,0) , state.arrows, state.materials,0,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL
            state3= State( state.health , max(state.arrows-1,0), state.materials,0,0) #MM stays ready  : Failure of Action
            state4= State( min(state.health+1,4) , 0, state.materials,0,1) #MM attacks and become dormant : UNSUCCESSFUL

            HitCost= (0.1 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + ( 0.1 ) * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
            + 0.9 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + ( 0.9 ) * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))


            
    elif(state.position==1):   #Pos::North #Availaible actions : Down, None, Craft, stay
        
        #Move Down
        if(state.monsterState==1): #Dormant
            state1= State( state.health , state.arrows, state.materials,0,1) #Success of Action : Stays in Dormant
            state2= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Stays in Dormant
            state3= State( state.health , state.arrows, state.materials,0,0) #Success of Action : Becomes ready
            state4= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Becomes ready

            DownCost=(0.85*0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.8*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.2*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15*0.2*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        elif(state.monsterState==0): #Ready
            state1= State( state.health , state.arrows, state.materials,0,0) #Success of Action : Stays Ready
            state2= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Stays Ready
            state3= State( state.health , state.arrows, state.materials,0,1) #Success of Action : Attack
            state4= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Attack

            DownCost=(0.85*0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.5*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
other

            + 0.15*0.5*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        #STAY
        if(state.monsterState==1): #Dormant
            state1= State( state.health , state.arrows, state.materials,1,1) #Success of Action : Stays in Dormant
            state2= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Stays in Dormant
            state3= State( state.health , state.arrows, state.materials,1,0) #Success of Action : Becomes ready
            state4= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Becomes ready

            StayCost= (0.85*0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.8*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.2*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15*0.2*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        elif(state.monsterState==0): #Ready
            state1= State( state.health , state.arrows, state.materials,1,0) #Success of Action : Stays Ready
            state2= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Stays Ready
            state3= State( state.health , state.arrows, state.materials,1,1) #Success of Action : Attack
            state4= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Attack

            StayCost= (0.85*0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.5*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15*0.5*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
        
        #Craft
        if(state.materials>=1):
            if(state.monsterState==1): #Dormant
                state1= State( state.health , min(3,state.arrows+1), state.materials-1,1,1)
                state2= State( state.health , min(3,state.arrows+2), state.materials-1,1,1) 
                state3= State( state.health , min(3,state.arrows+3), state.materials-1,1,1)
                state4= State( state.health , min(3,state.arrows+1), state.materials-1,1,0)
                state5= State( state.health , min(3,state.arrows+2), state.materials-1,1,0) 
                state6= State( state.health , min(3,state.arrows+3), state.materials-1,1,0)
                CraftCost= (0.5*0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.35 *0.8 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
                + 0.15 *0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
                + 0.5 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()])
                + 0.35 *0.2*(COST + REWARD[state5.show()] + GAMMA*utilities[state5.show()])
                + 0.15 *0.2*(COST + REWARD[state6.show()] + GAMMA*utilities[state6.show()]))

            elif(state.monsterState==0): #Ready
                state1= State( state.health , min(3,state.arrows+1), state.materials-1,1,0)
                state2= State( state.health , min(3,state.arrows+2), state.materials-1,1,0) 
                state3= State( state.health , min(3,state.arrows+3), state.materials-1,1,0)
                state4= State( state.health , min(3,state.arrows+1), state.materials-1,1,1)
                state5= State( state.health , min(3,state.arrows+2), state.materials-1,1,1) 
                state6= State( state.health , min(3,state.arrows+3), state.materials-1,1,1)
                CraftCost= (0.5*0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.35 *0.5 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
                + 0.15 *0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
                + 0.5 * 0.5 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()])
                + 0.35 *0.5*(COST + REWARD[state5.show()] + GAMMA*utilities[state5.show()])
other

                + 0.15 *0.5*(COST + REWARD[state6.show()] + GAMMA*utilities[state6.show()]))

    
    elif(state.position==2):   #Pos::East #Availaible actions : Left, None, shoot, stay, hit
        
        #Move Left
        if(state.monsterState==1):  #Dormant state
            state1= State( state.health , state.arrows, state.materials,0,1) #MM stays dormant : Success of Action
            state2= State( state.health , state.arrows, state.materials,0,0) #MM becomes ready : Success of Action

other

            LeftCost= (0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()]))
            
                    

        elif(state.monsterState==0):  #Ready state
            state1= State( state.health , state.arrows, state.materials,0,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,2,1) #MM attacks and become dormant : UNSUCCESSFUL

            LeftCost= (0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()]))
        

        #STAY
        if(state.monsterState==1):  #Dormant state
            state1= State( state.health , state.arrows, state.materials,2,1) #MM stays dormant : Success of Action
            state2= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Success of Action

other

            StayCost= (0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            +0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()]))
                    

        elif(state.monsterState==0):  #Ready state
            state1= State( state.health , state.arrows, state.materials,2,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,2,1)  #MM attacks and become dormant : UNSUCCESSFUL

            StayCost= (0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()]))


        #SHOOT
        if(state.arrows>=1):
            if(state.monsterState==1):  #Dormant state
                state1= State( max(state.health-1,0) , state.arrows-1, state.materials,2,1) #MM stays dormant : Success of Action
                state2= State( max(state.health-1,0) , state.arrows-1, state.materials,2,0) #MM becomes ready : Success of Action
                state3= State( state.health, state.arrows-1, state.materials,2,1) #MM stays dormant : Failure of Action
                state4= State( state.health , state.arrows-1, state.materials,2,0) #MM becomes ready : Failure of Action

                ShootCost= (0.9 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.9 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
                + 0.1 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
                + 0.1 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
                        

            elif(state.monsterState==0):  #Ready state
                state1= State( max(state.health-1,0) , state.arrows-1, state.materials,2,0) #MM stays ready : Success of Action
                state2= State( min(state.health+1,4) , 0, state.materials,2,1) #MM attacks and become dormant : UNSUCCESSFUL
                state3= State( state.health , state.arrows-1, state.materials,2,0) #MM stays ready  : Failure of Action
                state4= State( min(state.health+1,4) , 0, state.materials,2,1) #MM attacks and become dormant : UNSUCCESSFUL

                ShootCost= (0.9 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.9* 0.5 *(COST + REWARD[state2.show()] - 40 + GAMMA*utilities[state2.show()])
                + 0.1 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
                + 0.1 * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))

        #HIT  
        if(state.monsterState==1):  #Dormant state
            state1= State( max(state.health-2,0) , state.arrows, state.materials,2,1) #MM stays dormant : Success of Action
            state2= State( max(state.health-2,0) , state.arrows, state.materials,2,0) #MM becomes ready : Success of Action
            state3= State( state.health, state.arrows, state.materials,2,1) #MM stays dormant : Failure of Action
            state4= State( state.health , state.arrows, state.materials,2,0) #MM becomes ready : Failure of Action

            HitCost= (0.2 * 0.8 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.2 * 0.2 *(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.8 * 0.8 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.8 * 0.2 *(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))
            

        elif(state.monsterState==0):  #Ready state
            state1= State( max(state.health-2,0) , state.arrows, state.materials,2,0) #MM stays ready : Success of Action
            state2= State( min(state.health+1,4) , 0, state.materials,2,1) #MM attacks and become dormant : UNSUCCESSFUL
            state3= State( state.health , max(state.arrows-1,0), state.materials,2,0) #MM stays ready  : Failure of Action
            state4= State( min(state.health+1,4) , 0, state.materials,2,1) #MM attacks and become dormant : UNSUCCESSFUL

            HitCost= (0.2 * 0.5 *(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + (0.2) * 0.5 *(COST + REWARD[state2.show()] - 40+ GAMMA*utilities[state2.show()])
            + 0.8 * 0.5 *(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + (0.8) * 0.5 *(COST + REWARD[state4.show()] -40 + GAMMA*utilities[state4.show()]))

                    

    elif(state.position==3):   #Pos::South #Availaible actions : Up, None, Gather, stay
        
        #Move Up
        if(state.monsterState==1): #Dormant
            state1= State( state.health , state.arrows, state.materials,0,1) #Success of Action : Stays in Dormant
            state2= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Stays in Dormant
            state3= State( state.health , state.arrows, state.materials,0,0) #Success of Action : Becomes ready
            state4= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Becomes ready

            UpCost=(0.85*0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.8*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.2*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15*0.2*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        elif(state.monsterState==0): #Ready
            state1= State( state.health , state.arrows, state.materials,0,0) #Success of Action : Stays Ready
            state2= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Stays Ready
            state3= State( state.health , state.arrows, state.materials,0,1) #Success of Action : Attack
            state4= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Attack

            UpCost=(0.85*0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.5*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15*0.5*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        #STAY
        if(state.monsterState==1): #Dormant
            state1= State( state.health , state.arrows, state.materials,3,1) #Success of Action : Stays in Dormant
            state2= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Stays in Dormant
            state3= State( state.health , state.arrows, state.materials,3,0) #Success of Action : Becomes ready
            state4= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Becomes ready

            StayCost= (0.85*0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.8*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.2*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15*0.2*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        elif(state.monsterState==0): #Ready
            state1= State( state.health , state.arrows, state.materials,3,0) #Success of Action : Stays Ready
            state2= State( state.health , state.arrows, state.materials,2,0) #Failure of Action : Stays Ready
            state3= State( state.health , state.arrows, state.materials,3,1) #Success of Action : Attack
            state4= State( state.health , state.arrows, state.materials,2,1) #Failure of Action : Attack

            StayCost= (0.85*0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.15*0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.85*0.5*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.15*0.5*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        
        #Gather
        if(state.monsterState==1): #Dormant
            state1= State( state.health , state.arrows, min(state.materials+1,2),3,1)
            state2= State( state.health , state.arrows, state.materials,3,1) 
            state3= State( state.health , state.arrows, min(state.materials+1,2),3,0)
            state4= State( state.health , state.arrows, state.materials,3,0) 
        
            GatherCost = (0.75*0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.25 *0.8*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.75*0.2*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
            + 0.25 *0.2*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        elif(state.monsterState==0):# Ready
            state1= State( state.health , state.arrows, min(state.materials+1,2),3,0)
            state2= State( state.health , state.arrows, state.materials,3,0) 
            state4= State( state.health , state.arrows, min(state.materials+1,2),3,1)
            state3= State( state.health , state.arrows, state.materials,3,1) 
        
            GatherCost = (0.75*0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
            + 0.25 *0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
            + 0.75*0.5*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
other

            + 0.25 *0.5*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))



    elif(state.position==4):   #Pos::West #Availaible actions : Right, None, shoot, stay
        
        #Move Right
        if(state.monsterState==1): #Dormant
            state1= State( state.health , state.arrows, state.materials,0,1) # Success of Action
            state2= State( state.health , state.arrows, state.materials,0,0) # Success of Action
            RightCost= (0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                         + 0.2*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()]))
        
        elif(state.monsterState==0): #Ready
            state1= State( state.health , state.arrows, state.materials,0,0) # Success of Action
            state2= State( state.health , state.arrows, state.materials,0,1) # Success of Action
other

            RightCost= (0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                         + 0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()]))


        # #STAY
        
        # state1= State( state.health , state.arrows, state.materials,4,state.monsterState) # Success of Action
        # StayCost= (COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                
        #STAY
        if(state.monsterState==1): #Dormant
            state1= State( state.health , state.arrows, state.materials,4,1) # Success of Action
            state2= State( state.health , state.arrows, state.materials,4,0) # Success of Action
            StayCost= (0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                         + 0.2*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()]))
        
        elif(state.monsterState==0): #Ready
            state1= State( state.health , state.arrows, state.materials,4,0) # Success of Action
            state2= State( state.health , state.arrows, state.materials,4,1) # Success of Action
other

            StayCost= (0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                         + 0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()]))

        #SHOOT
        if(state.arrows>=1):
            if(state.monsterState==1): #Dormant
                state1= State( max(state.health-1,0) , state.arrows-1, state.materials,4,1)# Success of Action
                state2= State( state.health, state.arrows-1, state.materials,4,1) # Failure of Action
                state3= State( max(state.health-1,0) , state.arrows-1, state.materials,4,0)# Success of Action
                state4= State( state.health, state.arrows-1, state.materials,4,0) # Failure of Action
            
                ShootCost= (0.25*0.8*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.75*0.8*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
                + 0.25*0.2*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
                + 0.75*0.2*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

            elif(state.monsterState==0): #Ready
                state1= State( max(state.health-1,0) , state.arrows-1, state.materials,4,0)# Success of Action
                state2= State( state.health, state.arrows-1, state.materials,4,0) # Failure of Action
                state3= State( max(state.health-1,0) , state.arrows-1, state.materials,4,1)# Success of Action
                state4= State( state.health, state.arrows-1, state.materials,4,1) # Failure of Action
            
                ShootCost= (0.25*0.5*(COST + REWARD[state1.show()] + GAMMA*utilities[state1.show()])
                + 0.75*0.5*(COST + REWARD[state2.show()] + GAMMA*utilities[state2.show()])
                + 0.25*0.5*(COST + REWARD[state3.show()] + GAMMA*utilities[state3.show()])
other

                + 0.75*0.5*(COST + REWARD[state4.show()] + GAMMA*utilities[state4.show()]))

        

    if(NewUtil<=DownCost):
        NewUtil=DownCost
        BestAction=0 #DOWN

    if(NewUtil<=UpCost):
        NewUtil=UpCost
        BestAction=1#"Up"
        
    if(NewUtil<=RightCost):
        NewUtil=RightCost
        BestAction=2#"Right"
    
    if(NewUtil<=LeftCost):
        NewUtil=LeftCost
        BestAction=3#"Left"
    
    if(NewUtil<=GatherCost):
        NewUtil=GatherCost
        BestAction=4#"Gather"

    if(NewUtil<=StayCost):
        NewUtil=StayCost
        BestAction=5#"Stay"

    if(NewUtil<=HitCost):
        NewUtil=HitCost
        BestAction=6#"Hit"

    if(NewUtil<=CraftCost):
        NewUtil=CraftCost
        BestAction=7#"Craft"

    if(NewUtil<=ShootCost):
        NewUtil=ShootCost
        BestAction=8  #"Shoot"
    

    # if(state.health==1 and state.arrows==0 and state.materials==0 and state.position==1 and state.monsterState==1):
    #     print(DownCost)
    #     print(UpCost)
    #     print(LeftCost)
    #     print(RightCost)
    #     print(ShootCost)
    #     print(StayCost)
    #     print(HitCost)

    return NewUtil,BestAction




def trace(iteration, utilities, policies):
    print(f'iteration={iteration}')

    utilities=np.around(utilities,4)
    for state, util in np.ndenumerate(utilities):
        # util=np.around(util)
        util_str = '{:.3f}'.format(util)
        
        # if state[0] == 0:
        #     print(f'{state}:{-1}=[{util_str}]')
        #     continue 
        
        if policies[state] == -1:
            act_str = 'NONE'
        elif policies[state] == 0:
            act_str = 'DOWN'
        elif policies[state] == 1:
            act_str = 'UP'
        elif policies[state] == 2:
            act_str = 'RIGHT'
        elif policies[state] == 3:
            act_str = 'LEFT'
        elif policies[state] == 4:
            act_str = 'GATHER'
        elif policies[state] == 5:
            act_str = 'STAY'
        elif policies[state] == 6:
            act_str = 'HIT'
        elif policies[state] == 7:
            act_str = 'CRAFT'
        elif policies[state] == 8:
            act_str = 'SHOOT'
        
        print(f'( {HashArr[state[3]]}, {state[2]}, {state[1]}, {HashArr1[state[4]]}, {state[0] * 25}):{act_str}=[{util_str}]')

    print("\n\n")
# SSS=State(1,0,0,0,1)
# print(action(SSS))



value_iteration()