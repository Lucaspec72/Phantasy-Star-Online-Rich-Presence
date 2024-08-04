#Developped by Lucaspec72
#Special thanks and credits :
#Thanks to Nova_Plus for helping mapping the Memory ID for the Maps.
#The good folks at the dolphin discord for answering my questions.
#Location Images contributors :

import dolphin_memory_engine as dme
from discordrp import Presence
import time
import argparse

client_id = "1269030453172637801"
start_time = int(time.time())


memory_eur_rev0_dict = {
    "teamName"                  : 2152256794,
    "location"                  : 2153031046,
    "globalUsername"            : 2163134352,
    "onlineUsername"            : 2161796186,
    "offlineUsername"           : 2161782076,
    "localMultiplayerUsername"  : 2162964080,
    "playerCount"               : 2153585324
}
memory_usa_rev2_dict = {
    "teamName"                  : 2152256010,
    "location"                  : 2153026918,
    "globalUsername"            : 2164107416,
    "onlineUsername"            : 2161811994,
    "offlineUsername"           : 2161797884,
    "localMultiplayerUsername"  : 2161797884,
    "playerCount"               : 2153601132
}

supported_pso_versions = {
    "eur_rev0" : memory_eur_rev0_dict,
    "usa_rev2" : memory_usa_rev2_dict
}

location_dict = {
    #Episode 1 maps
    "bossOld"               : "Under the Dome",
    "boss02d"               : "Underground Channel",
    "boss03d"               : "Electrical Tower",
    "boss04d"               : "The Final Area",
    "city00"                : "Pioneer 2 City",
    "forest01s"             : "Forest 1",
    "forest02s"             : "Forest 2",
    "cave01"                : "Cave 1",
    "cave02"                : "Cave 2",
    "cave03"                : "Cave 3",
    "machine01"             : "Mine 1",
    "machine02"             : "Mine 2",
    "ancient01"             : "Ruins 1",
    "ancient02"             : "Ruins 2",
    "ancient03"             : "Ruins 3",
    #Lobby Maps
    "Lobby_Old"             : "Lobby Menu",
    "lobby_01e"             : "Lobby 1",
    "lobby_02e"             : "Lobby 2",
    "lobby_03e"             : "Lobby 3",
    "lobby_04e"             : "Lobby 4",
    "lobby_05e"             : "Lobby 5",
    "lobby_06e"             : "Lobby 6",
    "lobby_07e"             : "Lobby 7",
    "lobby_08e"             : "Lobby 8",
    "lobby_09e"             : "Lobby 9",
    "lobby_10e"             : "Lobby 10",
    "lobby_red_be00e"       : "Lobby 11",
    "lobby_yellow_be00e"    : "Lobby 12",
    "lobby_green_be00e"     : "Lobby 13",
    "lobby_soccer01e"       : "Lobby 14",
    "lobby_soccer02e"       : "Lobby 15",
    #Episode 2 maps
    "labo00"                : "Pioneer 2 Labo",
    "ruins01"               : "VR Temple Alpha",
    "ruins02"               : "VR Temple Beta",
    "boss07s"               : "Barba Ray's Lair",
    "space01"               : "VR Space Ship Alpha",
    "space02"               : "VR Space Ship Beta",
    "boss08d"               : "Gol Dragon's Lair",
    "jungle01"              : "Central Control Area",
    "jungle02"              : "Jungle Area North",
    "jungle03"              : "Jungle Area East",
    "jungle04"              : "Mountain Area",
    "jungle05"              : "Seaside Area",
    "boss05i"               : "Gal Gryphon's Lair",
    "seabed01"              : "SeaBed Upper Levels",
    "seabed02"              : "SeaBed Lower Levels",
    "boss06d"               : "Olga Flow's Lair"
}   
assets_dict = {
    "Lobby 1": "lobby_1",
    "Pioneer 2 City" : "city",
    "Pioneer 2 Labo" : "labo",
    "Forest 1" : "forest_1",
    "VR Temple Alpha" : "ruins_1",
    "VR Temple Beta" : "ruins_2"
}

#parse argument

def parseArguments():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('-version', help="Specify the version.", required=False)

    args = parser.parse_args()

    return args

#=====================================================#
#SETTINGS (will eventually be in a configuration file)
#=====================================================#
memory_dict = supported_pso_versions.get(parseArguments().version, memory_usa_rev2_dict)

print("=============================================================")
print("Phantasy Star Online Rich Presence v0.5.1-prototype")
print("by Lucaspec72")
print("")
print("=============================================================")

dme.hook()

if dme.is_hooked():
    print("Dolphin Hooked")
    
    def is_dolphin_running():
        try:
            # Try reading memory, which will throw an error if Dolphin is not running
            if dme.read_word(memory_dict.get("playerCount")) > 30:
                print("Warning, Incorrect Memory Map")
                return False
            else:
                return True
        except Exception as e:
            # If an error occurs, Dolphin is probably not running
            return False

    def get_team(isOnline,location):
        #Current team value (remains assigned even after leaving, need to check for room and online status to prove we're actually online)
        temp1 = dme.read_bytes(memory_dict.get("teamName"), 14)
        # Decode the bytes into a string
        temp1 = temp1.decode('utf-8', errors='ignore').strip('\x00')
        if isOnline and location.split(' ')[0] != "lobby" and temp1:
            return temp1
        else:
            return
        
    def get_location(): #DEBUG one of the values is incorrect, find non-persistant data
        temp1 = dme.read_bytes(memory_dict.get("location"), 22) #EUR code
        #temp1 = dme.read_bytes(2153026918, 14) #USA code
        # Decode the bytes into a string
        temp1 = temp1.decode('utf-8', errors='ignore').strip('\x00')  # or 'ascii', depending on your data
        temp1 = temp1.split('.')[0]
        if temp1.split('_')[0] != "lobby":
            temp1 = temp1.split('_')[0]
        return location_dict.get(temp1, "Unknown Location")


    def get_username():
        #Global Username
        temp1 = dme.read_bytes(memory_dict.get("globalUsername"), 12)
        #Offline Username
        temp2 = dme.read_bytes(memory_dict.get("offlineUsername"), 12)
        #localmultiplayer Username (player 1)
        temp3 = dme.read_bytes(memory_dict.get("localMultiplayerUsername"), 12)
        #Online Username
        temp4 = dme.read_bytes(memory_dict.get("onlineUsername"), 12)

        temp1 = temp1.decode('utf-8', errors='ignore').strip('\x00')
        temp2 = temp2.decode('utf-8', errors='ignore').strip('\x00')
        temp3 = temp3.decode('utf-8', errors='ignore').strip('\x00')
        temp4 = temp4.decode('utf-8', errors='ignore').strip('\x00')
        #check for state of player, and returns both the username and it's isOnline state.
        if temp2 == temp3 and temp2:
            #Player is in local multiplayer, returns username of player 1
            return temp2,False
        elif temp4 == temp1 and temp4:
            #Player is online
            return temp1,True
        else:
            #Player is offline
            return temp1,False

    with Presence(client_id) as presence:
        print("Connected")
        presence.set(
            {
                "state": "Starting Game",
                "timestamps": {"start": int(time.time())}
            }
        )
        print("Presence Set Up") 




        
        while is_dolphin_running() :
            #Update Values from Dolphin
            player_count = dme.read_word(memory_dict.get("playerCount"))
            #player_ConnectionState = getPlayerState()
            username, isOnline = get_username()
            location = get_location()
            team = get_team(isOnline, location)
            #Debug value print
            #print("=============")
            #print("Player count : ")
            #print([player_count])
            #print("Username : ")
            #print([username])
            #print("isOnline : ")
            #print([isOnline])
            #print("location : ")
            #print([location])
            #print("team : ")
            #print([team])


            #Define Payload
            drp_payload = {

                "details": "In Game",
                "timestamps": {"start": start_time}
            }

            #handles the image displayed
            if player_count > 0:
                assetimage = assets_dict.get(location, "missing_asset")
            else:
                assetimage = "main_menu"
            drp_payload["assets"] = {
                "large_image": assetimage,
                "large_text": location,
                #"small_image": "small_image",  # If possible replace with server logo
                #"small_text": "small text hover",
            }

            
            #Location display
            if player_count == 0:
                drp_payload["state"] = "in Menu"
            else:
                drp_payload["state"] = "in " + location

            #State Conditions.
            if player_count == 1 and not isOnline:
                drp_payload["details"] = username + " is in Singleplayer"
                drp_payload["party"] = {
                    "size": [player_count,1], #make playercount take from value with logic
                }
            if player_count > 1 and not isOnline:
                drp_payload["details"] = username + " is in Local Multiplayer"
                drp_payload["party"] = {
                    "size": [player_count,4], #make playercount take from value with logic
                }
            if location.split(' ')[0] == "Lobby" and player_count > 0:
                drp_payload["details"] = username + " is in Lobby"
                drp_payload["party"] = {
                    "size": [player_count,30], #make playercount take from value with logic
                }
            if team:
                drp_payload["details"] = username + " is in Team " + team
                drp_payload["party"] = {
                    "size": [player_count,4], #make playercount take from value with logic
                }
            
            if player_count == 0:
                drp_payload["party"] = {}



            presence.set(drp_payload)
            time.sleep(7)
        print("Dolphin Closed")
else:
    print("Failed to hook into Dolphin")