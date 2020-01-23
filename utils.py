import numpy as np
import pandas as pd
import sys

def distance(x1,x2,y1,y2):
    return abs(x1-x2) + abs(y1-y2)


def initbags(n):
    m=[]
    for i in range (n):
        m.append([])
    return m

##################################################################
#########################SSI######################################
##################################################################     
def bid(grid,r,i,agent,positions_agents):
      pos_r_x=np.where(grid == r)[0][0]
      pos_r_y=np.where(grid == r)[1][0]
      #init the nearest target with the robot's position
      nearest_pos_target_x=positions_agents[i][0][0]
      nearest_pos_target_y=positions_agents[i][0][1]
      distance_nearest_target=distance(nearest_pos_target_x,pos_r_x,nearest_pos_target_y,pos_r_y)

      for j in range(1,len(positions_agents[i])):
          pos_a_x=positions_agents[i][j][0]
          pos_a_y=positions_agents[i][j][1]
          d=distance(pos_a_x,pos_r_x,pos_a_y,pos_r_y)
          if(d<distance_nearest_target):
              nearest_pos_target_x=pos_a_x
              nearest_pos_target_y=pos_a_y
              distance_nearest_target=distance(nearest_pos_target_x,pos_r_x,nearest_pos_target_y,pos_r_y)
      return [distance_nearest_target,i]
         
def ssi(grid,agents,resources):
    bags=initbags(len(agents))
    positions_agents=initbags(len(agents))
    
    cp=0
    #init position of agents
    for a in agents:
        pos_a_x=np.where(grid == a)[0][0] 
        pos_a_y=np.where(grid == a)[1][0]
        positions_agents[cp].append([pos_a_x,pos_a_y])
        cp+=1
        
    cp=0
    available_resources=np.array(resources.copy())
    for r in resources:
         print("Round:",cp)
         print("Available resources: ",available_resources[cp:len(resources)])
         i=0
         bids=[]
         for agent in agents:
             bids.append(bid(grid,r,i,agents[i],positions_agents))
             i+=1
         #print(bids)
         bids=np.array(bids)
         min_bid=min(bids[:,0])
         index_winner=np.where(bids[:,0] == min_bid)[0][0]
         agent_winner=agents[index_winner]
         #print("agent_winner ",agent_winner)
         pos_r_x=np.where(grid == r)[0][0]
         pos_r_y=np.where(grid == r)[1][0]
         positions_agents[index_winner].append([pos_r_x,pos_r_y])
         #print("positions_agents ",positions_agents)
         bags[index_winner].append(r)
         print("Resource: ",r," ==> Agent: ",agent_winner,"\n")
         cp+=1
    print("-- Solution --")
    df = pd.DataFrame()
    df['Agent'] = agents
    df['Resources'] = bags
    print(df.to_string(index=False))         

##################################################################
#########################SSI REGRET###############################
##################################################################        
def my_bids(grid,resources,i,agent,nodes_agent):
    bids=[]
    b=[]
    for r in resources:
        #calcul du cout
        g=gain(grid,r,i,agent,nodes_agent)
        bids.append(g)
        b.append(g[0])
    return bids,b
        
def gain(grid,r,i,agent,nodes_agent):
    cp = 0
    pos_a_x=np.where(grid == agent)[0][0] 
    pos_a_y=np.where(grid == agent)[1][0]
    pos_r_x=np.where(grid == r)[0][0]
    pos_r_y=np.where(grid == r)[1][0]
    min_cost=sys.maxsize
    cp_min=-1
    
    if(len(nodes_agent)==0):
        return (distance(pos_a_x,pos_r_x,pos_a_y,pos_r_y),cp)
    while(cp<len(nodes_agent)+1):
        if(cp==0):
            pos_node1_x=np.where(grid == nodes_agent[cp])[0][0]
            pos_node1_y=np.where(grid == nodes_agent[cp])[1][0]
            d=distance(pos_a_x,pos_r_x,pos_a_y,pos_r_y)+distance(pos_node1_x,pos_r_x,pos_node1_y,pos_r_y)-distance(pos_node1_x,pos_a_x,pos_node1_y,pos_a_y)
            if (d<min_cost):
                cp_min=cp
                min_cost=d
        elif(cp==len(nodes_agent)):
            pos_node1_x=np.where(grid == nodes_agent[cp-1])[0][0]
            pos_node1_y=np.where(grid == nodes_agent[cp-1])[1][0]
            d=distance(pos_node1_x,pos_r_x,pos_node1_y,pos_r_y)
            if(d<min_cost):
                cp_min=cp
                min_cost=d
        else:
            pos_node1_x=np.where(grid == nodes_agent[cp-1])[0][0]
            pos_node1_y=np.where(grid == nodes_agent[cp-1])[1][0]
            pos_node2_x=np.where(grid == nodes_agent[cp])[0][0]
            pos_node2_y=np.where(grid == nodes_agent[cp])[1][0]
            d=distance(pos_node1_x,pos_r_x,pos_node1_y,pos_r_y)+distance(pos_node2_x,pos_r_x,pos_node2_y,pos_r_y)-distance(pos_node1_x,pos_node2_x,pos_node1_y,pos_node2_y)
            if(d<min_cost):
                cp_min=cp
                min_cost=d
        cp+=1
    return (min_cost,cp)
        
    
def ssi_regret(grid,agents,resources):
    available_resources=resources.copy()    
    nodes_agents=initbags(len(agents))
    round_alloc=0
    while(len(available_resources)!=0):
        print("Round:",round_alloc)
        print("Available resources: ",available_resources)
        i=0
        regrets=[]
        tmp_bids=[]
        costs=[]
        for agent in agents:
            #each agent evaluates the available resources
            bids_cp,evaluation=my_bids(grid,available_resources,i,agent,nodes_agents[i])
            costs.append(evaluation)
            tmp_bids.append(bids_cp)
            i+=1
        #compute the item which has the max regret
        costs=np.array(costs)
        k=0
        while(k<len(costs[0])):
            col=np.array(costs)[:,k]
            tmp_c=np.flip(np.sort(col))
            first_max=tmp_c[0]
            second_max=tmp_c[1]
            regret=abs(second_max-first_max)
            regrets.append(regret)
            k+=1
        top_regret=max(regrets)

        #attribute the resource to the person having the min evaluation
        index_col_max_regret=np.where(regrets==top_regret)[0][0]
        col=costs[:,index_col_max_regret]
        min_bid=min(col)
        index_min_bid=np.where(col==min_bid)[0][0]
        agent_winner=agents[index_min_bid]
        res_won=available_resources[index_col_max_regret]
        print("Resource: ",res_won," ==> Agent: ",agent_winner,"\n")
        available_resources.remove(res_won)
        #insert the new node
        cp_insertion=tmp_bids[index_min_bid][index_col_max_regret][1]
        nodes_agents[index_min_bid].insert(cp_insertion,res_won)
        print("\n")
        round_alloc+=1
        
    print("-- Solution --")
    df = pd.DataFrame()
    df['Agent'] = agents
    df['Resources'] = nodes_agents
    print(df.to_string(index=False))    
        
        
        
##################################################################
###########################CBAA###################################
##################################################################
def choose_obj(i,agent,my_utilities,local_bid,objects):
    #each agent choose an object according to bids already set by the others
    y=local_bid.copy()
    my_utilities_sorted=np.flip(np.sort(my_utilities))
    cp=0
    while(cp<len(my_utilities_sorted)):
        index_res=np.where(my_utilities==my_utilities_sorted[cp])[0][0]
        if(cp==len(my_utilities_sorted)-1):
            my_bid=my_utilities_sorted[cp]
            return  my_bid,index_res
        my_bid=my_utilities_sorted[cp]-my_utilities_sorted[cp+1]
        if(my_bid>y[index_res]):
            return my_bid,index_res
        elif(my_bid==y[index_res]):
            owners=np.where(np.array(objects)[:,0]==index_res)
            for owner in owners[0]:
                if (owner!=i and i <owner):
                    return my_bid,index_res
        cp+=1
    
        
def cbaa(agents,resources,utilities,neighbours):
    #init robots have nothing
    objects=[]
    for p in range(len(agents)):
        objects.append([-1,-1])
    local_bids=np.zeros((len(agents),len(agents)))
    convergence=False
    roundd=0
    msgs=initbags(len(agents))
    while(not convergence):
        print("Round: ",roundd)
        #print("objects ",objects)
        i=0
        for obj in objects:
            if obj ==[-1,-1]:
                #the robot i hasnt an item ==> choose an object maximising its utility and make an offer
                my_utilities=utilities[i]
                my_bid,index_res=choose_obj(i,agents[i],utilities[i],local_bids[i],objects)
                local_bids[i][index_res]=my_bid
                objects[i]=[index_res,my_bid]
            i+=1
            #neighbours update their vectors
        j=0
        #send messages to neighbours
        for agent in agents:
            #print("My neighbours are: ",neighbours[j])
            for neighbour in neighbours[j]:
                n=int(neighbour[1])-1
                msg=local_bids[j].copy()
                #print("The message I send to my neighbours is: ",msg)
                msgs[n].append(msg)
            j+=1
        for q in range(len(agents)):
            print("Agent: ",agents[q]," : ","resource ",resources[objects[q][0]] )
            
        #update local bids with received msgs
        w=0
        new_objects=objects.copy()
        for agent in agents:
            my_messages=msgs[w].copy()
            l,o=update_local(w,my_messages,local_bids[w].copy(),objects[w].copy(),objects.copy())
            new_objects[w]=o
            local_bids[w]=l
            w+=1
        #clear msgs
        convergence=done(msgs.copy(),neighbours.copy(),objects.copy())
        msgs=None
        objects=new_objects.copy()
        msgs=initbags(len(agents)) 
        roundd+=1
        print("\n")
        
    print("----------- Solution ------------")
    i=0
    t=0
    
    res=[]
    b=[]
    ut=[]
    for o in objects:
        t+=utilities[i][o[0]]
        res.append(resources[objects[i][0]])
        ut.append(utilities[i][objects[i][0]])
        b.append(objects[i][1])
        i+=1     
        
    df = pd.DataFrame()
    df['Agent'] = agents
    df['Resource'] = res
    df['Utility'] = ut
    df['Bid'] = b
    print(df.to_string(index=False))
    print("Utilité totale : ",t)

def done(msgs,neighbours,objects):
    #when two agents sharing a link of neighborhood have different content of messages, the convergence is not yet reached
    j=0
    for my_neighbours in neighbours:
        msg=msgs[j]
        for my_neighbour in my_neighbours:
            index_neighbour=int(my_neighbour[1])-1
            m=msgs[index_neighbour]
            i=0
            while(i<len(msg)):
                if msg[0][i]!=m[0][i]:
                    return False
                i+=1
        j+=1
    q=np.array(objects)
    for o in objects:
        resource=o[0]
        if(len((np.where(q[:,0]==resource))[0])!=1):
            return False
    return True  
    
            
def update_local(i,msgs,local_bid,my_object,objects):  
    #each agent update its local vector according to the messages received from its neighbours  
    o=my_object[0]    
    l=local_bid.copy()
    for msg in msgs:
        k=0
        while(k<len(msg)):
                if(k==o):     
                    if(l[k]<msg[k]):
                        l[k]=msg[k].copy()
                        my_object=[-1,-1]
                   
                    elif(l[k]==msg[k]):  
                        owners=np.where(np.array(objects)[:,0]==o)
                        for owner in owners[0]:
                            if (owner!=i and i >owner and objects[owner][1]>=objects[i][1]):
                                my_object=[-1,-1]
                                break
                else:
                    l[k]=max(l[k].copy(),msg[k].copy())
                k+=1
    return l,my_object