from functions import import_database_credentials
from pymongo import MongoClient

username, password = import_database_credentials()

cluster =MongoClient("mongodb+srv://"+username+":"+password+
                     "@cluster0.d8xlm.mongodb.net/<dbname>?retryWrites=true&w=majority")


def team_dbinstance():
    team_collection = cluster['fpl_transfer_advisor']['team_data']
    return team_collection


def player_type_dbinstance():
    type_collection = cluster['fpl_transfer_advisor']['type_details']
    return type_collection


def player_details_dbinstance():
    player_collection = cluster['fpl_transfer_advisor']['player_data']
    return player_collection
