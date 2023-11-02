import discord
from discord.ext import tasks
import random

class Game:
    started = False
    inGamePlayers = []

    gameRoles = {
        "Unique": {
            "Mafia": {
                "minPlayers": 1,
                "ply": None
            },
            "Sheriff": {
                "minPlayers": 2,
                "ply": None
            },
            "Prostitute": {
                "minPlayers": 4,
                "ply": None
            },
            "Don": {
                "minPlayers": 5,
                "ply": None
            },
            "Maniac": {
                "minPlayers": 7,
                "ply": None
            },
            "Doctor": {
                "minPlayers": 8,
                "ply": None
            }
        },
        "Сivilians": []
    }

    timer = 0
    nextGameStep = "Prepare"
    night = 0
    def __init__(self, bot, minPlayers = 1):
        self.bot = bot
        self.minPlayers = minPlayers

    async def gameCycle(self):
        chooseTime = 10
        discussionTime = 60
        message = ''

        if (self.timer % 30 == 0) and (self.nextGameStep == "Mafia") and self.timer != 0:
            await self.messagesChannel.send(f"{self.timer} секунд до ночи.")
        if self.timer <= 0:
            match self.nextGameStep:
                case "Prepare":
                    await self.messagesChannel.send(f"{chooseTime} секунд до ночи, приготовьтесь!")
                    self.timer = chooseTime
                    self.nextGameStep = "Mafia"
                case "Mafia":
                    await self.messagesChannel.send("Город засыпает. Просыпается Мафия...")
                    for ply in self.inGamePlayers:
                        await ply.edit(mute = True)
                    message = f'{self.gameRoles["Unique"][self.nextGameStep]["ply"].global_name}, Вы Мафия. Выберите из списка кого хотите завалить:\n'
                    self.timer = chooseTime
                    self.nextGameStep = "Don"
                case "Don":
                    await self.messagesChannel.send("Мафия засыпает. Просыпается Дон...")
                    if self.gameRoles["Unique"][self.nextGameStep]["ply"] != None:
                        message = f'{self.gameRoles["Unique"][self.nextGameStep]["ply"].global_name}, Вы Дон. Выберите из списка того, с кем бы Вы хотели побыть этой ночью:\n'
                    self.timer = chooseTime
                    self.nextGameStep = "Sheriff"
                case "Sheriff":
                    await self.messagesChannel.send("Дон засыпает. Просыпается Шериф...")
                    if self.gameRoles["Unique"][self.nextGameStep]["ply"] != None:
                        message = f'{self.gameRoles["Unique"][self.nextGameStep]["ply"].global_name}, Вы Шериф. Выберите из списка кого вы считаете мафией:\n'
                    self.timer = chooseTime
                    self.nextGameStep = "Prostitute"
                case "Prostitute":
                    await self.messagesChannel.send("Шериф засыпает. Просыпается Шлюха...")
                    if self.gameRoles["Unique"][self.nextGameStep]["ply"] != None:
                        message = f'{self.gameRoles["Unique"][self.nextGameStep]["ply"].global_name}, Вы Проститутка. Выберите из списка того, с кем бы Вы хотели побыть этой ночью:\n'
                    self.timer = chooseTime
                    self.nextGameStep = "Maniac"
                case "Maniac":
                    await self.messagesChannel.send("Шлюха засыпает. Просыпается Маньяк...")
                    if self.gameRoles["Unique"][self.nextGameStep]["ply"] != None:
                        message = f'{self.gameRoles["Unique"][self.nextGameStep]["ply"].global_name}, Вы Маньяк. Выберите любого из списка:\n'
                    self.timer = chooseTime
                    self.nextGameStep = "Doctor"
                case "Doctor":
                    await self.messagesChannel.send("Маньяк засыпает. Просыпается Доктор...")
                    if self.gameRoles["Unique"][self.nextGameStep]["ply"] != None:
                        message = f'{self.gameRoles["Unique"][self.nextGameStep]["ply"].global_name}, Вы Доктор. Выберите любого из списка:\n'
                    self.timer = chooseTime
                    self.nextGameStep = "Discussion"
                case "Discussion":
                    self.night += 1
                    await self.messagesChannel.send(f"Маньяк засыпает.\nДень {self.night}-й. {discussionTime} сек на обсуждение.")
                    for ply in self.inGamePlayers:
                        await ply.edit(mute = False)
                    self.timer = discussionTime
                    self.nextGameStep = "Mafia"
        if message != '':
            for i, ply in enumerate(self.inGamePlayers):
                message += f'{i + 1}. {ply.global_name}\n'
            await self.commandsChannel.send(message)
        self.timer -= 1

    async def giveMafiaRoles(self):
        random.shuffle(self.inGamePlayers)
        playersCount = len(self.inGamePlayers)

        for i, role in enumerate(self.gameRoles["Unique"]):
            if self.gameRoles["Unique"][role]["minPlayers"] <= playersCount:
                if self.gameRoles["Unique"][role]["ply"] == None:
                    self.gameRoles["Unique"][role]["ply"] = self.inGamePlayers[i]
                    await self.inGamePlayers[i].send(f'Ваша роль в городке {role}')
        self.gameRoles["Сivilians"] = [*set(self.inGamePlayers).difference([self.gameRoles["Unique"][role]["ply"] for role in self.gameRoles["Unique"]])]

        for role in self.gameRoles["Unique"]:
            if self.gameRoles["Unique"][role]["ply"] != None:
                print(f'{role}: {self.gameRoles["Unique"][role]["ply"].global_name}')
        for ply in self.gameRoles["Сivilians"]:
            if self.gameRoles["Сivilians"][ply] != None:
                print(f'Сivilian: {self.gameRoles["Сivilians"][ply].global_name}')

    @tasks.loop(seconds=1)
    async def startedGameLoop(self):
        if len(self.cityChannel.members) < self.minPlayers:
            toLobbyMembers = self.cityChannel.members
            for ply in self.inGamePlayers:
                if ply not in toLobbyMembers:
                    await self.messagesChannel.send(f'Игра остановлена. {ply.global_name} съебался с городка.')
                else:
                    await ply.move_to(self.lobbyChannel)
                await ply.remove_roles(self.inCityRole)
                await ply.edit(mute=False)

            self.started = False
            self.startedGameLoop.stop()
            return
        await self.gameCycle()

    @tasks.loop(seconds=10)
    async def checkLobbyLoop(self):
        #voice channels
        self.lobbyChannel = self.bot.get_channel(1125051071623073848)
        self.cityChannel = self.bot.get_channel(1125051072071860274)

        #text channels
        self.messagesChannel = self.bot.get_channel(1125051430651301988)
        self.commandsChannel = self.bot.get_channel(1125051374380519564)

        lobbyCount = len(self.lobbyChannel.members)
        if self.started == False:
            if lobbyCount >= self.minPlayers:
                await self.messagesChannel.send(f'Заебись, начинаем игру!')
                self.inGamePlayers = self.lobbyChannel.members
                self.inCityRole = discord.utils.get(self.bot.guilds[0].roles, name="In city")
                for ply in self.inGamePlayers:
                    await ply.add_roles(self.inCityRole)
                    await ply.move_to(self.cityChannel)
                    await ply.edit(mute=False)
                for i, role in enumerate(self.gameRoles["Unique"]):
                    self.gameRoles["Unique"][role]["ply"] = None
                await self.giveMafiaRoles()

                self.timer = 0
                self.nextGameStep = "Prepare"
                self.night = 0
                self.started = True
                self.startedGameLoop.start()

        print("Lobby checked")

if __name__ == "__main__":
    print("Please run this script from external file")