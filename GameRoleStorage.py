import GameRole
from GameRole import UniqueGameRole
import Player
import random

class GameRoleStorage:
    __list = []

    def __init__(self, rolesList: []):
        self.__list = rolesList

    async def assignRoles(self, playerList: []):
        random.shuffle(playerList)
        playersCount = len(playerList)

        availableRoles = [role for role in self.__list if role.minPlayersToAllowThisRole <= playersCount]

        for i, role in enumerate(availableRoles):
            playerList[i].role = role
            await playerList[i].notifyRole()

        for ply in playerList:
            if ply.role == None:
                ply.role = GameRole.CiviliansRole()
            print(ply)