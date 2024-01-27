
#!/usr/bin/env python
#
# Copyright Rubycat
"""
#@author elmoustapha.malick@rubycat.eu
"""
from proveitadmin.admin.admindatabase import AdminDatabase
from proveitadmin.authorization.role.role import RoleUser
from proveitadmin.authorization.role.role import RolesUserAssociation 
from proveitadmin.authorization.accesspolicy.useraccesspolicy import UserRoleUserAccessPolicyAssociation
from proveitadmin.authorization.accesspolicy.useraccesspolicy import ServiceGroupUserAccessPolicyAssociation
from proveitadmin.service.service import Service
from proveitadmin.authorization.role.role import Role
from proveitadmin.authorization.filter.filter import Filter
from proveitadmin.authorization.accesspolicy.accesspolicy import FilterAccessPolicyAssociation
from proveitadmin.service import AUTHENTICATION_CREDENTIALS
from proveitadmin.globals.constants import AUTHENTICATION_MODE
from proveitadmin.authentication.realm import Realm
from sqlalchemy import func
import numpy as np
import csv

                                 # Make sure to be connected to the db of proveit (ssh tunnel)

#### Database : PROVEIT
#### Configuration of PROVIT
# for connecting with database(db) of PROVEIT 
proveit_conf = [
        "127.0.0.1",
        33333,
        "rubydbuser",
        "9KVIIUrsPsY9fNOndenzxobsK74dTy4gfRTsNF3ZT0AIkSlz1l",
        False
]
#### Connection to the database
def database_connection():
        return AdminDatabase(
            *proveit_conf
)

################################### Functions ####################################

# A rapid debug to give the corresponding string of a variable
# using AUTHENTICATION_CREDENTIALS = enum('NONE','PRIMARY_CREDENTIALS','SECONDARY_CREDENTIALS')
# but we could change in rccore the function enum so it could do the following
list_authen_mode=['UNKNOWN','PASSWORD','SSHKEY','X509CERT','SECRET']
list_authen_creden=['NONE','PRIMARY_CREDENTIALS','SECONDARY_CREDENTIALS']

def enum_string(a,enum):
    for x in enum:
        if (a==enum.index(x)):
            return x

# Give us all existing services
def all_services(db):
    list_service=[] 
    with db.session_scope():
        queryservice = db.session.query(Service.name).order_by(func.lower(Service.name)).all()
        for i in queryservice:
             list_service.append(i.name) 
    return  list_service    

  
# Give us all existing realms
def all_royaumes(db):
    list_royaume=[] 
    with db.session_scope():
        queryroyaume = db.session.query(Realm).order_by(func.lower(Realm.name)).all()
        for i in queryroyaume:
             list_royaume.append([i.name,i.id])  
    return  list_royaume  


# Give us all existing users for a corresponding realm 
def all_users(db,id_realm):
    list_user=[]  
    with db.session_scope():
        queryuser = db.session.query(RoleUser.name).\
            filter(RoleUser.realmId==id_realm).order_by(func.lower(RoleUser.name)).distinct()        
        for i in queryuser:
             list_user.append(i[0])  
    return  list_user  

# Give us all services for a user in a realm the ouput is a list  
def all_services_for_user_realm(user_name,realm_name,db):
        
        data=[]
        
        try:
                # We have a 'problem' in RoleUser table it give us for a user two different id 
                # because of the role : PROVEIT-ADMINISTRATOR-PROFILE
                # so we ignore it to give us a unique id for a user
                table_joined_user_id=db.session.query(RoleUser.id).\
                join(RolesUserAssociation, RoleUser.id==RolesUserAssociation.userId).\
                join(Role,RolesUserAssociation.roleId==Role.id).\
                filter(Role.name!='PROVEIT-ADMINISTRATOR-PROFILE').\
                filter(RoleUser.name==user_name).all()
                
                # Give us the id of our realm so we take only the users in this realm
                table_realm=db.session.query(Realm.id).\
                        filter(Realm.name==realm_name)
                
                # Test : used id or realm id is existing 
                table_joined_user_id[0][0]
                table_realm[0][0]

                for m in table_joined_user_id:
                        
                        # We are going to join the tables : RolesUserAssociation,ServiceGroupUserAccessPolicyAssociation and 
                        # ServiceGroupUserAccessPolicyAssociation to give us the corresponding id of a service group
                        # beacause every service have to be in only one group service
                        # class RolesUserAssociation for table users
                        # class ServiceGroupUserAccessPolicyAssociation for table role
                        # class UserRoleUserAccessPolicyAssociation for table plicy
                        table_joined_policy_role=db.session.query(RolesUserAssociation,ServiceGroupUserAccessPolicyAssociation).\
                                join(UserRoleUserAccessPolicyAssociation, RolesUserAssociation.roleId==UserRoleUserAccessPolicyAssociation.roleId).\
                                join(ServiceGroupUserAccessPolicyAssociation,UserRoleUserAccessPolicyAssociation.accesspolicyId==ServiceGroupUserAccessPolicyAssociation.accesspolicyId).\
                                filter(RolesUserAssociation.userId==m.id).\
                                filter(RolesUserAssociation.realmId==table_realm[0][0]).all()
                        
                        for i,j in table_joined_policy_role:
                                
                                # To take all services
                                table_service=db.session.query(Service).filter(Service.groupId==j.groupId)
        
                                for l in table_service:
                                        temporer_tuple_info=[realm_name,user_name]
                                        
                                        # To take all available filtres
                                        table_joined_filtre=db.session.query(Filter).\
                                        join(FilterAccessPolicyAssociation,Filter.id==FilterAccessPolicyAssociation.filterId).\
                                        filter(FilterAccessPolicyAssociation.accesspolicyId==j.accesspolicyId).all()
                                        temporer_tuple_info.append(l.name)
                                        temporer_tuple_info.append(enum_string(l.authenticationMode,list_authen_mode))
                                        temporer_tuple_info.append(enum_string(l.authenticationCredentials,list_authen_creden))
                                        
                                        if (table_joined_filtre==[]):
                                                        temporer_tuple_info.append('NONE')
                                                        
                                        filtres_list=[]
                                        if (table_joined_filtre!=[]):
                                                for p in table_joined_filtre:
                                                        filtres_list.append(p.name)
                                                temporer_tuple_info.append(filtres_list)
                                        data.append(temporer_tuple_info) 
                return data 
        except:
                return "Veuillez saisir un utilisateur et/ou royaume valide !"
        
# Give us all users and his realm for a service the ouput is a list  
def all_users_from_service_realm(service_name,db): 
        
        data=[]
        
        try:
                
                # To take the id of a service
                table_service=db.session.query(Service).filter(Service.name==service_name).first()

                # Here we join tables : RolesUserAssociation,ServiceGroupUserAccessPolicyAssociation and UserRoleUserAccessPolicyAssociation
                # to take the id of group service
                table_joined_policy_role=db.session.query(RolesUserAssociation,ServiceGroupUserAccessPolicyAssociation).\
                join(UserRoleUserAccessPolicyAssociation, RolesUserAssociation.roleId==UserRoleUserAccessPolicyAssociation.roleId).\
                join(ServiceGroupUserAccessPolicyAssociation,UserRoleUserAccessPolicyAssociation.accesspolicyId==ServiceGroupUserAccessPolicyAssociation.accesspolicyId).\
                filter(ServiceGroupUserAccessPolicyAssociation.groupId==table_service.groupId).all()

                for i,j in table_joined_policy_role:
                        
                        # To take the available filtres
                        table_joined_filtre=db.session.query(Filter).\
                                        join(FilterAccessPolicyAssociation,Filter.id==FilterAccessPolicyAssociation.filterId).\
                                        filter(FilterAccessPolicyAssociation.accesspolicyId==j.accesspolicyId).all()                      
                                
                        # To take all users for this service       
                        table_user=db.session.query(RoleUser).filter(RoleUser.id==i.userId).all() 
                        
                        temporer_tuple_info=[service_name]
                        for l in table_user:
                                table_realm=db.session.query(Realm.name).\
                                filter(Realm.id==l.realmId).all()
                                temporer_tuple_info.append(table_realm[0][0])
                                temporer_tuple_info.append(l.name)
                                data.append(temporer_tuple_info) 
                                 
                return data 
        except :
                return "Veuillez saisir un service et/ou royaume valide !"
        
        
# Functions to export the information to a csv file
def table_realm_user_serviceINFO_to_csv(database,csv_name_string):
    # In this function we are going to create a csv file where the information are presented this way:
    # Realm, User, Service, Authentification, Filters
    all_realm=all_royaumes(database)
    with open(csv_name_string, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Realm', 'User', 'Service','Authentication Mode', 'Authentication credentials','Filters'])
        for i in all_realm :
              all_user_for_realm=all_users(database, i[1])
              with database.session_scope():  
                for j in all_user_for_realm:
                        data=all_services_for_user_realm(j,i[0], database)
                        for row in data:
                            writer.writerow(row)

def table_service_realm_user_to_csv(database,csv_name_string):
    # In this function we are going to create a csv file where the information are presented this way:
    # Service, Realm, User 
    all_realm=all_royaumes(database)
    with open(csv_name_string, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Service', 'Realm', 'User'])
        all_service_for_realm=all_services(database)
        with database.session_scope():
                for j in all_service_for_realm:
                        data=all_users_from_service_realm(j, database)
                        for row in data:
                            writer.writerow(row)
    




################################## START ##########################################

def main():
        db = database_connection()

        table_realm_user_serviceINFO_to_csv(db,'realm_user_serviceINFO.csv')
        table_service_realm_user_to_csv(db,'service_realm_user.csv')


if __name__ == '__main__':
        main()






