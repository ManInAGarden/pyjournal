"""Modul zur Speicherung der Tagesdaten
"""
from datetime import date

class DayData():

    def __init__(self, dte=date.today(), text=""):
        self.day = dte
        self.txt = text

    def get_serial(self):
        return '<day date="{0}">{1}</day>'.format(self.day, self.text)

    def to_str(self):
        return "{0:02d}".format(self.day.day)