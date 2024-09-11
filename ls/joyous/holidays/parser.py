# ------------------------------------------------------------------------------
# Holidays settings parser
# ------------------------------------------------------------------------------
from __future__ import unicode_literals
import re
import holidays

__all__ = ["parseHolidays"]

HolsRe = re.compile(r"(\w[\w\ ]*|\*)(\[.+?\])?")
SplitRe = re.compile(r",\s*")

def _parseSubdivisions(holidaysStr, pais):
    # * = all states and provinces
    retval = holidays.HolidayBase()
    if holidaysStr[0] != '[' or holidaysStr[-1] != ']':
        return holidays.HolidayBase()

    for subdivision in SplitRe.split(holidaysStr[1:-1]):
        subdivision = subdivision.strip()
        if subdivision == "*":
            retval = holidays.country_holidays(pais)
            break
        else:
            retval = holidays.HolidaysSum(retval, holidays.country_holidays(pais, subdiv=subdivision))
    return retval

def parseHolidays(holidaysStr, holidayMap=None):
    """
    Takes a string like NZ[WTL,Nelson],AU[*],Northern Ireland and builds a HolidaySum from it
    """
    if holidayMap is None:
        holidayMap = holidays.utils.list_supported_countries()
    retval = holidays.HolidaySum(holidays.HolidayBase(), holidays.HolidayBase())
    holidaysStr = holidaysStr.strip()
    for (country, subdivisions) in HolsRe.findall(holidaysStr):
        if country == "*":
            for pais in holidayMap.keys():
                if subdivisions:
                    subval = _parseSubdivisions(subdivisions, pais)
                    retval = holidays.HolidaySum(retval, subval)
                else:
                    retval = holidays.HolidaySum(retval, holidays.country_holidays(pais))
            break
        cls = holidays.utils.country_holidays(country)
        if cls is not None:
            if subdivisions:
                subval = _parseSubdivisions(subdivisions, country)
                retval = holidays.HolidaySum(retval, subval)
            else:
                retval = holidays.HolidaySum(retval, cls)
    return retval

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
