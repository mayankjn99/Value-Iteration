PART - 2 

Value Iteration Algorithm
Task 1 
Interations needed to converge = 118
Observations -
- Indiana Jones is not a rash decision-maker. Due to the high value of gamma, it puts more weight on the long-term goals.
 This can be inferred from the fact that IJ prefers to move away from/dodge MM i whenever it is in its ready state i.e if Indiana Jones is in north sqaure 'STAY' action is choosen instead of 'DOWN' action which will lead him to center square .
 Being a risk-averse person IJ does not prefers to shoot whenever the possibility of hitting MM is low  that's why 'SHOOT' and 'HIT'  action is performed in east square and avoided in center square .
 Also it is noticed that 'CRAFT' and 'GATHER' actions are performed whenever MM is in Ready State  . 
 Indiana Jones  prefers to use his blade from the eastern box due to the high amount of damage possible, especially when mm's health fully recharges.
Whenever in the central box and MM is in the dormant state,IJ prefers to move right and then shoot MM with his arrows/blade so as to get a higher probability of hitting him.


1. (W, 0, 0, D, 100) 
	States in transitions and actions taken  = >
	1. Right = (C,0,0,D,100)
	2. Right = (E,0,0,D,100)
	3. Hit = (E,0,0,D,50)
	4. Hit = (E,0,0,D,0)
	Stops when MM Health is zero and  HIT action is performed in East square 

2. (C, 2, 0, R, 100)
	States in transitions and actions taken  = >  
	1. Up =  (N,2,0,R,100) 
	2. Craft = (N,1,1,R,100) 
	3. Craft = (N,0,2,R,100)
	4. Stay = (N,0,2,R,100) 
	5. Down = (C,0,2,D,100)
	6. Right = (E,0,2,D,100)
	7. Shoot =(E,0,1,D,75)
	8. Shoot = (E,0,0,D,50)
	9. Hit = (E,0,0,D,0)
	Stops when MM Health is zero , Indiana Jones wait until MM is in ready state and till then make arrow and use these arrows and blade  in the east square as probability of hitting the MM is higher there . 

Task 2 

Case 1:

Left action in east sqaure moves indiana jones to West Square (Change from task1)
Interations needed to converge = 120 
No significant changes as compared to general policy 



Case 2:
Step cost =0 for Stay action  (Change from task1)
Interations needed to converge = 57 

West Square observes very prominent changes and  the most prefered action is 'STAY' .

Case 3:

Gamma = 0.25 (Change from task1)
Interations needed to converge  = 8 
Due to small discount factor (Gamma) as compared to previous cases leads to convergence faster ( 8 iterations)

