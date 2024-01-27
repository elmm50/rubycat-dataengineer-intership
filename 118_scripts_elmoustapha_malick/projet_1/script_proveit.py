#!/usr/bin/env python
#
# Copyright Rubycat
"""
#@author elmoustapha.malick@rubycat.eu
"""
from proveitadmin.audit.service import Service
from proveitadmin.audit.event.user.userserviceconnectionsummaryevent import UserServiceConnectionSummaryEvent
from proveitadmin.audit.auditdatabase import AuditDatabase
from rccore.utils.dateutils import createLocalDateTime, getUtcTimestamp,convertDateToString,createLocalDateTime, createLocalDateTime
import proveitadmin.audit.event.types as EventTypes
from proveitadmin.audit.hbsource import HbSource
from proveitadmin.audit.event.user.userevent import UserEvent
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime,timedelta, timezone
import pytz
from math import floor

                           #### Database : PROVEIT
   
   
#### Configuration of PROVIT
# for connecting with database(db) of PROVEIT                          
proveit_conf = [
        "127.0.0.1",
        33333,
        "rubydbuser",
        "ctuMycEZ9vnachl2S0kxJNi5wzZCtepDQKJFwZdwl9O9UjfKrl",
        False
]
                    
#### Connection to the database
def database_connection():
    return AuditDatabase(
        *proveit_conf
    )
   

#### Creation of a event
def create_event(begin_time,end_time,name_user):
     return UserServiceConnectionSummaryEvent(
                              service=Service('service1', host='ip1'),
                              connectionCtx={},
                              timestamp=end_time,
                              beginDate=begin_time,
                              endDate=end_time, 
                              source=HbSource(userName=name_user))

#### Plot function
def plot_graph(axis_x_list,list_axis_y,name_title):
    # Plotting
    fig,ax =plt.subplots(figsize=(16,8))
    ax.plot(axis_x_list,list_axis_y,marker="o")
    ax.set(title = "Graphe d'évolution du nombre de sessions",
           xlabel = "Date",
           ylabel = "Nombre de sessions")
    plt.setp(ax.get_xticklabels(), rotation =30)
    plt.axis(ymin=0)
    plt.grid()
    plt.savefig(name_title)
    
    return 0
  

####################################################################################
####################################################################################
####################################################################################
                             
                           ####
                           ####
                           ####

####################################################################################
################# number of overlap sessions Per delta_x    ########################
####################################################################################


# For finding the number of iteration
# ie the length of my window (N)
def x_max_numb(date_start,date_finish,delta_x):
    
    # Initialisation
    x_max=0
    is_hour=None
    
    # If we want only days
    if (delta_x >= 24*60*60):
        x_max=abs(int(date_start.strftime('%d'))-int(date_finish.strftime('%d')))+1
        is_hour=False
    
    # If we want only hours
    elif(delta_x < 24*60*60):
        x_max=abs(int(date_start.strftime('%H'))-int(date_finish.strftime('%H')))+1
        is_hour=True
        
    # We could also do it for minutes,secondes,..

    return x_max,is_hour  

####

def max_session_simultany(date_start,date_finish,delta_x,queryevent):
    
    # Converting queryevent to have two lists one for timestamp(x) 
    # and maximum of simultaneous sessions (y)
    list_timestamp,list_session=timestamp_session_list(queryevent)
    
    # Bornes of my iterable intervals associated with delta_x
    start_borne=date_start.timestamp()
    finish_borne=start_borne+delta_x
    
    # take note that we take the maximum of simaltaneous sessions in [star_borne,finish_borne[ window 

    # List of max session per delta_x and correponding date
    max_session=[]
    date=[]
    
    # Nomber of iteration with x_max_numb function    
    x_max,is_hour=x_max_numb(date_start,date_finish,delta_x)
    
    
    # Variable for checking if a interval is empty ie does not have a timestamp in it 
    # variable for stocking the last numb_max to compare with the numb_max of the current interval: [start_borne,finish_borne]
    last_numb_max=0
    last_event=False
    
    # delta_x_division
    delta_x_division=24*60*60
    if (is_hour==True):
        delta_x_division=60*60

    for i in range(0,x_max,int(delta_x/(delta_x_division))):  # step depending on delta_x
        print(i)
        print(x_max)
        print(int(delta_x/3600))
        # Initialisation of locale variables
        interval_empty=True
        numb_max=0
        list_max=[0]
        
        for timestamp in list_timestamp:
            
            if (start_borne<=timestamp and finish_borne>timestamp):
                timestamp_index=list_timestamp.index(timestamp)
                list_max.append(list_session[timestamp_index])
     
                interval_empty=False

        # If we are in a empty interval
        if (interval_empty==True ):
            numb_max=max(last_numb_max,max(list_max))

        # If we are in not empty interval
        elif(interval_empty==False ):
            numb_max=max(last_numb_max,max(list_max))
            last_numb_max=list_max[-1] 
   
        # Adding
        max_session.append(numb_max)
        if(is_hour==True ):
            date.append(datetime.fromtimestamp(start_borne).strftime('%d/%m/%y %H:%M'))
        
        if(is_hour==False):
            date.append(datetime.fromtimestamp(start_borne).strftime('%d/%m/%y'))
            

        # Going to the next interval  
        start_borne=finish_borne
        finish_borne=finish_borne+delta_x  

    return date,max_session

# So this function return us two lists of the same length,the list max_session give us the 
# the maximum of simultaneous sessions and the list date give us the corresonding date
# if the delta_x is =< 24*60*60 (24 hours) we plot it in this format (day/month/year)
# if the delta_x is > 24*60*60 we plot it in this format (day/month/year Hours:Minutes)
    

                                
####################################################################################
############################ Per start/end time in timestamp funtion ###############
####################################################################################
# Number of sesssions per start/end timestamp of a session

def timestamp_session_list(queryevent):  
    if (queryevent!=[]):
            list_tuple=[]

            for list_k in queryevent:
                    list_tuple.append(((list_k.beginDate.timestamp()),1))  
                    list_tuple.append(((list_k.endDate.timestamp()),-1))    

            list_tuple.sort(key=lambda a: a[0])
            list_session=accumulator_list([lt[1] for lt in list_tuple])
            list_timestamp=[lt[0] for lt in list_tuple]

            return list_timestamp,list_session
    else:
        return [],[]
# this function return us two lists of the same length and that means that the first element of the list : list_session
# is the number of sessions(max) with it corresponding timestamp witch is the first element of the list : list_timestamp    
    
# accumulator_list fonction :
#             for exemple  :  list1= [1,1,-1,1,-,1]
#                             accumulator_list(list1)=[1,2,1,2,1]
def accumulator_list(list1):
     t_ini=[]
     for t1 in list1 :
        if len(t_ini)==0 :
            t_ini.append(t1)
            continue
        t=t_ini[-1]
        t_ini.append(t+t1)
     return t_ini
             
######################################################################################
######################################################################################
######################################################################################


                               
                            
##################################   START   ##########################################

def main():
    
     db = database_connection()
     with db.session_scope():


         queryevent = db.session.query(UserServiceConnectionSummaryEvent).all()
         
         for i in queryevent : 
             print("begindate : ",i.beginDate,"enddate : ",i.endDate)
             # Be careful the time that is pop up in this for loop is (+1 hour) 
             
         date_start=datetime(2023,1,1,0,0,tzinfo=None)
         date_finish=datetime(2023,1,10,23,0,tzinfo=None)
         
         l1,l2=max_session_simultany(date_start,date_finish,24*60*60,queryevent)
         print(l1)
         print(l2)  
                
         # reset the db
         reponse=input("Voulez vous reset la db (o/n) ? :")
         if(reponse =='o'):
            db.deleteTables()

if __name__ == '__main__':
    main()
    