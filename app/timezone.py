import datetime


# Obtain the UTC Offset for the current system:
def get_utc_offset_timezone(unix_timestamp):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcfromtimestamp(unix_timestamp) - datetime.datetime.utcnow()
    local_datetime = datetime.datetime.utcnow()
    result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
    return local_datetime.day - result_utc_datetime.day

def get_time_from_another_timezone(current_time,UTC_offset):
    current_time_in_utc = datetime.datetime.now()
    return current_time_in_utc + datetime.timedelta(hours=UTC_offset)
