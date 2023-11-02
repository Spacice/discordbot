import Player
import discord

class DayTime:
    night: int = 0
    @staticmethod
    async def handle(messageChannel, plyList: []):
        await messageChannel.send('Я не знаю чё делать в это время суток.')

    @staticmethod
    def whoseTurn():
        return None


class Day(DayTime):
    @staticmethod
    async def handle(messageChannel, plyList: []):
        DayTime.night += 1
        await messageChannel.send(f'День {DayTime.night}-й.')
        for ply in plyList:
            await ply.unmute()
        return True

class Night(DayTime):
    _whoseTurn = None
    @staticmethod
    async def handle(messageChannel, plyList: []):
        if Night._whoseTurn == None:
            await messageChannel.send('Город засыпает')
            for ply in plyList:
                await ply.mute()
                ply.resetFlags()
            Night._whoseTurn = plyList[0]
            await messageChannel.send(f'Просыпается {Night._whoseTurn.role}')
            await Night._whoseTurn.wakeup(plyList)
        else:
            sleptFlag = False
            for ply in plyList:
                if ply == Night._whoseTurn:
                    await messageChannel.send(f'{ply.role} засыпает. ')
                    sleptFlag = True
                    continue
                if sleptFlag:
                    await messageChannel.send(f'Просыпается {ply.role}')
                    await ply.wakeup(plyList)
                    sleptFlag = False
                    break
            if sleptFlag:
                Night._whoseTurn = None
                return True
        return False

    @staticmethod
    def whoseTurn():
        return Night._whoseTurn