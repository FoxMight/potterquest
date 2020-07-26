from database_connection import database_connection
from datetime import datetime, timedelta

"""
Computes the time difference between two datetime objects,
returns the total second difference
"""


def compare_time(datetime_old, datetime_new):
    """
    Tells pycharm what types everything is:

    :type datetime_old: datetime
    :type datetime_new: datetime
    """

    # convert years to days
    dayTotal = datetime_old.year * 365 + calculate_days_up_to_month(datetime_old.month)
    oldTime = timedelta(days=(dayTotal + datetime_old.day), hours=datetime_old.hour, minutes=datetime_old.minute,
                        seconds=datetime_old.second).total_seconds()

    dayTotal = datetime_new.year * 365 + calculate_days_up_to_month(datetime_new.month)
    newTime = timedelta(days=(dayTotal + datetime_new.day), hours=datetime_new.hour, minutes=datetime_new.minute,
                        seconds=datetime_new.second).total_seconds()

    timeDifference = newTime - oldTime

    return timeDifference


def calculate_days_up_to_month(num):
    total_days = 0
    if num > 1:
        total_days += 31

    # does not account for leap years yet,
    # needs to be implemented differently
    if num > 2:
        total_days += 28

    if num > 3:
        total_days += 31
    if num > 4:
        total_days += 30
    if num > 5:
        total_days += 31
    if num > 6:
        total_days += 30
    if num > 7:
        total_days += 31
    if num > 8:
        total_days += 31
    if num > 9:
        total_days += 30
    if num > 10:
        total_days += 31
    if num > 11:
        total_days += 30
    return total_days

"""
Stores a date time object in the database

Returns True on success
"""


def store_date_time(dbConnection, id, current):
    """
    Tells pycharm what types everything is:
    :type dbConnection: database_connection
    :type current: datetime
    """

    try:
        # make a string, add on the year, tab, month, tab, day, tab, hour, tab, minute, tab, second
        toStore = current.strftime("%Y\t%m\t%d\t%H\t%M\t%S")

        # should be equivalent to:
        # current.year + "\t" + current.month + "\t" + current.day + "\t" + current.hour + "\t" +
        # current.minute + "\t" + current.second

        # split it into an array for storage
        dbConnection.profile_update({"id": id}, {"$set": {"dailytime": toStore.split("\t")}})

        return True
    except:
        # the user likely did not set up their profile
        return False


"""
Reconstructs a date time object from the database

Returns True on success
"""


def construct_date_time(user):
    # first parse the string, looking for tabs
    try:
        itemsToCreate = user["dailytime"]

        toReturn = datetime(year=int(itemsToCreate[0]), month=int(itemsToCreate[1]), day=int(itemsToCreate[2]),
                            hour=int(itemsToCreate[3]), minute=int(itemsToCreate[4]), second=int(itemsToCreate[5]),
                            microsecond=0)

        return toReturn
    except Exception:
        return None
