import discord
from GameRole import GameRole
from discord import state
class Player:
    __botNumber: int = 0
    __nick: str
    __role: GameRole = None
    __isBot: bool = True
    __discordMember: discord.Member

    __savedByDoctorOrProstituteFlag: bool = False
    __killedByMafiaOrManiacFlag: bool = False
    __isAlive: bool = True

    def __init__(self, lobbyChannel, cityChannel, inCityDiscordRole, discordMember = None, isBot = False):
        self.__isBot = isBot
        self.__discordMember = discordMember
        if isBot:
            self.__nick = f'Bot {self.__botNumber}'
            Player.__botNumber += 1
        else:
            self.__nick = discordMember.global_name

        self._inCityDiscordRole = inCityDiscordRole
        self._cityChannel = cityChannel
        self._lobbyChannel = lobbyChannel


    def __repr__(self):
        return f'{self.__nick}: {self.__role}'

    def __str__(self):
        return str(self.__repr__())

    def __eq__(self, other):
        return (isinstance(other, Player) and self.__discordMember == other.__discordMember
            or isinstance(other, discord.Member) and self.__discordMember == other)

    async def sendPersonalMesssage(self, text: str):
        await self.__discordMember.send(text)

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role: GameRole):
        self.__role = role

    async def notifyRole(self):
        await self.__discordMember.send(f'Ваша роль {self.__role}')

    @property
    def isAlive(self):
        return self.__isAlive

    @property
    def nick(self):
        return self.__nick

    def save(self, isSaved=True):
        self.__savedByDoctorOrProstituteFlag = isSaved

    def kill(self, wasKilled=True):
        self.__killedByMafiaOrManiacFlag = wasKilled

    async def mute(self):
        await self.__discordMember.edit(mute=True)

    async def unmute(self):
        await self.__discordMember.edit(mute=False)

    async def moveToChannel(self, channel):
        if self.__discordMember.voice is not None:
            await self.__discordMember.move_to(channel)

    async def moveToLobby(self):
        if self.__discordMember in self._cityChannel.members:
            await self.moveToChannel(self._lobbyChannel)
        await self.__discordMember.remove_roles(self._inCityDiscordRole)

    async def moveToCity(self):
        if self.__discordMember in self._lobbyChannel.members:
            await self.moveToChannel(self._cityChannel)
        await self.__discordMember.add_roles(self._inCityDiscordRole)

    async def wakeup(self, playerList: []):
        if self.__isAlive:
            if self.__isBot:
                pass
            else:
                message = f'{self.__nick}, Вы {self.role}. Выберите из списка игрока, над которым вы хотите выполнить действие {self.role.action}:\n'
                for i, ply in enumerate(playerList):
                    message += f'{i + 1}. {self.__discordMember.global_name}\n'
                await self.__discordMember.send(message)

    def applyActions(self):
        if self.__isAlive:
            if self.__killedByMafiaOrManiacFlag:
                if self.__savedByDoctorOrProstituteFlag:
                    return f'{self.__nick} спасли от смерти'
                else:
                    self.__isAlive = False
                    return  f'{self.__nick} был убит этой ночью'
        return ''

    def resetFlags(self):
        self.__killedByMafiaOrManiacFlag = False;
        self.__savedByDoctorOrProstituteFlag = False;