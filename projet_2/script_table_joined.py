
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
import numpy as np

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

##### A rapid debug to give the corresponding string of a variable
# using AUTHENTICATION_CREDENTIALS = enum('NONE','PRIMARY_CREDENTIALS','SECONDARY_CREDENTIALS')
# but we could change in rccore the function enum so it could do the following
list_authen_mode=['UNKNOWN','PASSWORD','SSHKEY','X509CERT','SECRET']
list_authen_creden=['NONE','PRIMARY_CREDENTIALS','SECONDARY_CREDENTIALS']

def enum_string(a,enum):
    for x in enum:
        if (a==enum.index(x)):
            return x
######
   
def all_services_for_user_realm_demo(user_name,realm_name,db):
        set_service_with_info=set() # Only for testing can be commented
        list_info_user_realm={user_name,realm_name} # Only for testing can be commented

        try:
                # We have a 'problem' in RoleUser table it give us for un user two different id 
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

                print("===========================")
                print("L'utilisateur : ",user_name) 
                print("Royaume : ",realm_name)
                print("===========================")
                
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
                                        temporer_tuple_info=() # Only for testing can be commented
                                        
                                        # To take all available filtres
                                        table_joined_filtre=db.session.query(Filter).\
                                        join(FilterAccessPolicyAssociation,Filter.id==FilterAccessPolicyAssociation.filterId).\
                                        filter(FilterAccessPolicyAssociation.accesspolicyId==j.accesspolicyId).all()
                                
                                        print("Service : ",l.name)
                                        print("Authentication mode : ",enum_string(l.authenticationMode,list_authen_mode))
                                        print("Authentication credentials : ",enum_string(l.authenticationCredentials,list_authen_creden))
                                        
                                        temporer_tuple_info=temporer_tuple_info+(l.name,) # Only for testing can be commented
                                        temporer_tuple_info=temporer_tuple_info+(enum_string(l.authenticationMode,list_authen_mode),) # Only for testing can be commented
                                        temporer_tuple_info=temporer_tuple_info+(enum_string(l.authenticationCredentials,list_authen_creden),) # Only for testing can be commented

                                        if (table_joined_filtre==[]):
                                                        print("Filtre : NO FILTRE")
                                                        temporer_tuple_info=temporer_tuple_info+('NO FILTRE',) # Only for testing can be commented
                                        if (table_joined_filtre!=[]):
                                                for p in table_joined_filtre:
                                                        print("Filtre : ",p.name)
                                                        
                                                        temporer_tuple_info=temporer_tuple_info+(p.name,) # Only for testing can be commented

                                        print("------------------")
                                        
                                        set_service_with_info.add(temporer_tuple_info) # Only for testing can be commented

                print("===========================")
                return set_service_with_info,list_info_user_realm # Only for testing can be commented
        except:
                return "Veuillez saisir un utilisateur et/ou royaume valide !"
        

def all_users_from_service_realm_demo(service_name,realm_name,db): 
        set_user_with_info=set() # Only for testing can be commented
        set_info_service_realm=set() # Only for testing can be commented
        
        try:
                
                enter=True
                # To take the id of a service
                table_service=db.session.query(Service).filter(Service.name==service_name).first()
                table_realm=db.session.query(Realm.id).\
                        filter(Realm.name==realm_name)

                # Here we join tables : RolesUserAssociation,ServiceGroupUserAccessPolicyAssociation and UserRoleUserAccessPolicyAssociation
                # to take the id of group service
                table_joined_policy_role=db.session.query(RolesUserAssociation,ServiceGroupUserAccessPolicyAssociation).\
                join(UserRoleUserAccessPolicyAssociation, RolesUserAssociation.roleId==UserRoleUserAccessPolicyAssociation.roleId).\
                join(ServiceGroupUserAccessPolicyAssociation,UserRoleUserAccessPolicyAssociation.accesspolicyId==ServiceGroupUserAccessPolicyAssociation.accesspolicyId).\
                filter(ServiceGroupUserAccessPolicyAssociation.groupId==table_service.groupId).\
                filter(RolesUserAssociation.realmId==table_realm[0][0]).all()
                
                print("===========================")
                print("Le service : ",service_name)
                print("Authentication mode : ",enum_string(table_service.authenticationMode,list_authen_mode))
                print("Authentication credentials : ",enum_string(table_service.authenticationCredentials,list_authen_creden))


                set_info_service_realm.add(service_name) # Only for testing can be commented
                set_info_service_realm.add(enum_string(table_service.authenticationMode,list_authen_mode)) # Only for testing can be commented
                set_info_service_realm.add(enum_string(table_service.authenticationCredentials,list_authen_creden)) # Only for testing can be commented
                
                for i,j in table_joined_policy_role:
                        
                        # To take the available filtres
                        table_joined_filtre=db.session.query(Filter).\
                                        join(FilterAccessPolicyAssociation,Filter.id==FilterAccessPolicyAssociation.filterId).\
                                        filter(FilterAccessPolicyAssociation.accesspolicyId==j.accesspolicyId).all()
                                        
                        if (table_joined_filtre==[] and enter==True):
                                print("Filtre : NO FILTRE")
                                print("===========================")
                                enter=False
                                
                                set_info_service_realm.add('NO FILTRE') # Only for testing can be commented
                                
                        if (table_joined_filtre!=[] and enter==True):
                                enter=False
                                for p in table_joined_filtre:
                                        print("Filtre : ",p.name) 
                                        
                                        set_info_service_realm.add(p.name) # Only for testing can be commented           
                                print("===========================")
                                
                        # To take all users for this service       
                        table_user=db.session.query(RoleUser).filter(RoleUser.id==i.userId).all() 
                        for l in table_user:
                                print("User : ",l.name)
                                print("Royaume : ",realm_name)
                                print("------------------")
                                
                                
                                temporer_tuple_info=() # Only for testing can be commented
                                temporer_tuple_info=temporer_tuple_info+(l.name,) # Only for testing can be commented
                                temporer_tuple_info=temporer_tuple_info+(realm_name,) # Only for testing can be commented
                                set_user_with_info.add(temporer_tuple_info) # Only for testing can be commented

                print("===========================")
                return set_user_with_info,set_info_service_realm # Only for testing can be commented
        except :
                return "Veuillez saisir un service et/ou royaume valide !"
        
        
###################################################################################






################################## START ##########################################

def main():
        db = database_connection()
        with db.session_scope():
                
                #set_service_with_info,list_info_user_realm=all_services_for_user_realm_demo('user1','défaut', db)
                set_user_with_info,set_info_service_realm=all_users_from_service_realm_demo('service4','défaut',db)

            # reset the db
            #reponse=input("Voulez vous reset la db (o/n) ? :")
            #if(reponse =='o'):
            #db.deleteTables()

if __name__ == '__main__':
   main()