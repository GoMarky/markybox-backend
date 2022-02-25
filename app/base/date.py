import datetime

def dt_converter(dt):
    if isinstance(dt, datetime.datetime):
        return dt.timestamp().__str__()
