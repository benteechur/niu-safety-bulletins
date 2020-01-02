class Bulletin:
    def __init__(self, incident, date, location, details):
        self.incident = incident
        self.date = date
        self.location = location
        self.details = details

    def __repr__(self):
        return repr((self.incident, self.date, self.location, self.details))