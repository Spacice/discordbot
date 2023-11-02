import discord
from discord.ext import tasks
from config import gameChannels
from config import gameVars

import GameRole
import GameRoleStorage
import Timer
from DayTime import *


class Game:
    inGamePlayers = []
    gameRoles: GameRoleStorage.GameRoleStorage
    timeOfDay = Day

    isStarted = False

    timer: Timer
    playerStep = 0
    night = 0
    def __init__(self, bot, minPlayers = 1):
        self.bot = bot
        self.minPlayers = minPlayers

    async def gameCycle(self):
        if (self.timer.seconds % gameVars.timeNotifyEvery == 0) and not self.timer.isStopped:
            await self.messagesChannel.send(f"Осталось {self.timer.seconds} секунд.")

        if self.timer.isStopped:
            if await self.timeOfDay.handle(self.messagesChannel, self.inGamePlayers):
                if self.timeOfDay == Night:
                    self.timeOfDay = Day
                else:
                    self.timeOfDay = Night
                    self.timer.reset(gameVars.discussionTime)
            else:
                self.timer.reset(gameVars.chooseTime)
        self.timer.update()

    @tasks.loop(seconds=1)
    async def startedGameLoop(self):
        if len(self.cityChannel.members) < len(self.inGamePlayers):
            toLobbyMembers = self.cityChannel.members
            for ply in self.inGamePlayers:
                if ply not in toLobbyMembers:
                    await self.messagesChannel.send(f'Игра остановлена. {ply.nick} покинул городок.')
                await ply.moveToLobby()
            self.inGamePlayers.clear()

            self.isStarted = False
            self.startedGameLoop.stop()
            return
        await self.gameCycle()

    @tasks.loop(seconds=10)
    async def checkLobbyLoop(self):
        #voice channels
        self.lobbyChannel = self.bot.get_channel(gameChannels['lobbyVoiceChannelID'])
        self.cityChannel = self.bot.get_channel(gameChannels['cityVoiceChannelID'])

        #text channels
        self.messagesChannel = self.bot.get_channel(gameChannels['messagesTextChannelID'])

        lobbyCount = len(self.lobbyChannel.members)
        if self.isStarted == False:
            if lobbyCount >= self.minPlayers:
                await self.messagesChannel.send(f'Начинаем игру!')
                self.inCityRole = discord.utils.get(self.bot.guilds[0].roles, name="In city")
                self.inGamePlayers = [Player.Player(self.lobbyChannel, self.cityChannel, self.inCityRole, member) for member in self.lobbyChannel.members]
                for ply in self.inGamePlayers:
                    await ply.unmute()
                    await ply.moveToCity()
                self.gameRoles = GameRoleStorage.GameRoleStorage([GameRole.MafiaRole(), GameRole.SheriffRole(), GameRole.ProstituteRole(), GameRole.ManiacRole(), GameRole.DoctorRole(), GameRole.DonRole()])
                await self.gameRoles.assignRoles(self.inGamePlayers)

                self.timer = Timer.Timer(gameVars.chooseTime)
                self.timeOfDay = Night
                await self.messagesChannel.send(f"{self.timer.seconds} секунд до ночи, приготовьтесь!")

                self.isStarted = True
                self.startedGameLoop.start()

if __name__ == "__main__":
    print("Please run this script from external file")