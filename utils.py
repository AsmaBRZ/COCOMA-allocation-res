import numpy as np


bags=[]
positions_agents=[]

def distance(x1,x2,y1,y2):
    return abs(x1-x2) + abs(y1-y2)
   
   
def initbags(n):
    m=[]
    for i in range (n):
        m.append([])
    return m
  
  
def bid(grid,r,i,agent):
      global positions_agents
      pos_r_x=np.where(grid == r)[0][0]
      pos_r_y=np.where(grid == r)[1][0]
      #init the nearest target with the robot's position
      nearest_pos_target_x=positions_agents[i][0][0]
      nearest_pos_target_y=positions_agents[i][0][1]
      distance_nearest_target=distance(nearest_pos_target_x,pos_r_x,nearest_pos_target_y,pos_r_y)
      
      print("nearest_pos_target ",nearest_pos_target)
      for j in range(1,len(positions_agents[i])):
          pos_a_x=positions_agents[i][j][0]
          pos_a_y=positions_agents[i][j][1]
          d=distance(pos_a_x,pox_r_x,pos_a_y,pos_r_y)
          if(d<distance_nearest_target):
              nearest_pos_target_x=pos_a_x
              nearest_pos_target_y=pos_a_y
              distance_nearest_target=distance(nearest_pos_target_x,pos_r_x,nearest_pos_target_y,pos_r_y)
          
      return [distance_nearest_target,nearest_pos_target_x,nearest_pos_target_y]
         
def sii(grid,agents,resources):
    global bags
    bags=initbags(len(agents))
    global positions_agents
    positions_agents=initbags(len(agents))
    
    cp=0
    #init position of agents
    for a in agents:
        pos_a_x=np.where(grid == a)[0][0] 
        pos_a_y=np.where(grid == a)[1][0]
        positions_agents[cp].append([pos_a_x,pos_a_y])
        cp+=1
        
    for r in resources:         
         i=0
         for agent in positions_agents:
             print(i)
             
             
             
             
