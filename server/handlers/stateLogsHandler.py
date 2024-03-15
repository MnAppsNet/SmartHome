

from datetime import datetime
import json
import pytz
from const import Constants


class LOG_KEYS:
    TIME = 'time'
    STATE = 'state'
    TEMPERATURE = 'temp'
    REQUIRED_TEMPERATURE = 'req_temp'


class StateLogs:
    def __init__(self):
        self._openLogs()

    def __del__(self):
        try: self._closeLogs()
        except: pass

    def _openLogs(self):
        self._day = datetime.now(pytz.timezone(Constants.TIMEZONE)).strftime("%d")
        self._month = datetime.now(pytz.timezone(Constants.TIMEZONE)).strftime("%m")
        self._year = datetime.now(pytz.timezone(Constants.TIMEZONE)).strftime("%Y")
        try:
            self._file = open(Constants.LOCAL_FILE_NAME_STATE_LOGS, 'r+')
        except:
            self._file = open(Constants.LOCAL_FILE_NAME_STATE_LOGS, "w+")
        try:
            self._logs = json.load(self._file)
        except json.JSONDecodeError:
            self._logs  = {}
        self._file.seek(0)
        # Initialize
        if not self._year in self._logs :
            self._logs [self._year] = {}
        if not self._month in self._logs [self._year]:
            self._logs [self._year][self._month] = {}
        if not self._day in self._logs [self._year][self._month]:
            self._logs [self._year][self._month][self._day] = []

    def _closeLogs(self):
        json.dump(self._logs, self._file)
        self._file.truncate()
        self._file.close()

    def insert(self,time,state,temperature,requiredTemperature):
        self._logs[self._year][self._month][self._day].append({
            LOG_KEYS.TIME: time,
            LOG_KEYS.STATE: state,
            LOG_KEYS.TEMPERATURE: temperature,
            LOG_KEYS.REQUIRED_TEMPERATURE: requiredTemperature
        })

    def get(self, year = None,month = None,day = None)->list:
        if (year == None ): year = self._year
        if (month == None ): month = self._month
        if (day == None ): day = self._day
        if (type(year) != str): year = str(year)
        if (type(month) != str): month = "{0:0=2d}".format(month)
        if (type(day) != str): day = "{0:0=2d}".format(day)
        result = self._logs
        if year in result: result = result[year]
        else: return []
        if month in result: result = result[month]
        else: return []
        if day in result: result = result[day]
        else: return []
        return result

    def destroy(self):
        self._closeLogs()

#>> Static Methods :

    def addEntry(state, temperature, threshold):
        # Read datetime values
        time = datetime.now(pytz.timezone(
            Constants.TIMEZONE)).strftime("%H:%M:%S")

        logs = StateLogs()
        logs.insert(time,state,temperature,threshold)
        logs.destroy()

    def getEntries( year=None, month=None, day=None)->list:
        logs = StateLogs()
        values = logs.get(year,month,day)
        logs.destroy()
        return values