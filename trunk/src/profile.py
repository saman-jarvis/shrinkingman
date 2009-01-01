from gettext import gettext as _

m, f = range(2)

class Profile:
    def __init__(self, name):
        self.name   = name
        self.height = 160.0
        self.gender = m

    def set_name(self, name):
        if name == "":
            self.name = _("Unknown")
        else:
            self.name = name

    def get_name(self):
        return self.name

    def set_height(self, height):
        self.height = float(height)

    def get_height(self):
        return self.height

    def set_gender(self, gender):
        if gender > 1: return
        self.gender = gender

    def get_gender(self):
        return self.gender

    name   = property(set_name,   get_name)
    height = property(set_height, get_height)
    gender = property(set_gender, get_gender)
