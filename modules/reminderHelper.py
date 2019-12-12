from datetime import datetime, timedelta
from discord.ext import tasks, commands

class reminderHelper():
    def __init__(self, member, duration, reminder, remindersList):
        self.__member = member
        self.__reminder = reminder
        self.__remindersList = remindersList
        self.__reminderDue = datetime.now() + timedelta(seconds=int(duration))
        self.sendReminder.start()

    def checkReminderDue(self):
        # print(datetime.now())
        # print(self.__reminderDue)
        return True if datetime.now() > self.__reminderDue else False

    def stopReminderCheck(self):
        # print(self.__remindersList)
        self.sendReminder.cancel()
        self.__remindersList.remove(self)
        # print(self.__remindersList)

    @tasks.loop(seconds=1.0)
    async def sendReminder(self):
        if self.checkReminderDue():
            await self.__member.create_dm()
            await self.__member.dm_channel.send(self.__reminder)
            self.stopReminderCheck()