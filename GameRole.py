class GameRole:
    name: str

    def __init__(self, roleName: str):
        self.name = roleName

    def __eq__(self, other: str):
        return self.name == other

    def __repr__(self):
        return self.name


class UniqueGameRole(GameRole):
    __action: str
    __minPlayersToAllowThisRole: int

    def __init__(self, roleName: str, action: str, minPlayers: int):
        super().__init__(roleName)
        self.__action = action
        self.__minPlayersToAllowThisRole = minPlayers

    @property
    def action(self):
        return self.__action

    @property
    def minPlayersToAllowThisRole(self):
        return self.__minPlayersToAllowThisRole

class CiviliansRole(GameRole):
    def __init__(self):
        super().__init__("Сivilians")

class MafiaRole(UniqueGameRole):
    def __init__(self):
        super().__init__("Mafia", "застрелить", 1)


class SheriffRole(UniqueGameRole):
    def __init__(self):
        super().__init__("Sheriff", "проверить на мафию", 2)


class ProstituteRole(UniqueGameRole):
    def __init__(self):
        super().__init__("Prostitute", "переспать ночью", 4)


class ManiacRole(UniqueGameRole):
    def __init__(self):
        super().__init__("Maniac", "убить", 5)


class DoctorRole(UniqueGameRole):
    def __init__(self):
        super().__init__("Doctor", "вылечить", 6)


class DonRole(UniqueGameRole):
    def __init__(self):
        super().__init__("Don", "решить, кого мафия застрелит", 12)
