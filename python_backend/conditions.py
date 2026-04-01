from datetime import datetime
from time import sleep


def string_to_date(send_date: str) -> datetime.date:
    """
    funkcija <string_to_date>
    pieņem <str>
    tipa vērtību <send_date>
    un atgriež <datetime.date>
    tipa vērtību <date>
    """
    date = datetime.strptime(send_date, "%Y-%m-%d").date()
    return date

def string_to_time(send_time: str) -> datetime.time:
    """
    funkcija <string_to_time>
    pieņem <str>
    tipa vērtību <send_time>
    un atgriež <datetime.time>
    tipa vērtību <time>
    """
    time = datetime.strptime(send_time, "%H:%M").time()
    return time

def combined_date_time(send_date: str, send_time: str) -> datetime:
    """
    funkcija <string_to_date, string_to_time>
    pieņem <str, str>
    tipa vērtību <send_date, send_time>
    un atgriež <datetime>
    tipa vērtību <date>
    """
    date = datetime.strptime(f"{send_date} {send_time}", "%Y-%m-%d %H:%M")
    return date

def send_email_on(send_date: str, send_time: str) -> bool:
    """
    funkcija <send_email_on>
    pieņem <str, str>
    tipa vērtību <send_date, send_time>
    un atgriež <bool>
    tipa vērtību <bool>
    """
    if combined_date_time(send_date, send_time) == datetime.now():
        return True
    else:
        return False

def send_email_until(send_date: str, send_time: str) -> bool:
    """
    funkcija <send_email_until>
    pieņem <str, str>
    tipa vērtību <send_date, send_time>
    un atgriež <bool>
    tipa vērtību <bool>
    """
    if combined_date_time(send_date, send_time) > datetime.now():
        return True
    else:
        return False