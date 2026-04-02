from pathlib import Path
from typing import Optional
from json import dump, load

def merge_settings(user_settings: dict, default_settings: dict) -> dict:
    """
    funkcija <>
    pieņem <> tipa vērtību <>
    un atgriež <> tipa vērtību <>
    """
    '''
    Merges user settings with default settings, filling in any missing values from the default settings.
    
    :param user_settings: The user settings to merge
    :type user_settings: dict
    :param default_settings: The default settings to use for missing values
    :type default_settings: dict
    :return: The merged settings as a dictionary
    :rtype: dict
    '''

    settings = {}
    for setting in default_settings.items():
        current_setting = user_settings.get(setting[0])
        if current_setting == None:
            current_setting = default_settings[setting[0]]
        settings[setting[0]] = current_setting
    return settings

def read_json(file_name: str | Path, default_values: Optional[dict] = {}, indent: int = 4) -> dict:
    """
    funkcija <>
    pieņem <> tipa vērtību <>
    un atgriež <> tipa vērtību <>
    """
    '''
    Reads a JSON file and returns the data as a dictionary. If the file does not exist, it creates it with the default values.
    
    :param file_name: The name of the JSON file to read
    :type file_name: str | Path
    :param default_values: The default values to use if the file does not exist
    :type default_values: dict
    :param indent: The number of spaces to use for indentation in the JSON file
    :type indent: int
    :return: The data from the JSON file as a dictionary
    :rtype: dict
    '''

    if not Path(file_name).exists():
        with open(file_name, 'w') as f:
            dump(default_values, f, indent=indent)
    with open(file_name, 'r') as f:
        return load(f)

def read_profiles():
    """
    funkcija <>
    pieņem <> tipa vērtību <>
    un atgriež <> tipa vērtību <>
    """
    return read_json('.profile.json')

def log_action(text: str, file_name: str | Path = Path('.log.log'), end: str = '\n') -> None:
    """
    funkcija <>
    pieņem <> tipa vērtību <>
    un atgriež <> tipa vērtību <>
    """
    '''
    Logs an action by appending the specified text to a log file.
    
    :param text: The text to log
    :type text: str
    :param file_name: The name of the log file to append to
    :type file_name: str | Path
    :param end: The string to append at the end of the log entry (default is a newline character)
    :type end: str
    '''

    with open(file_name, 'a') as f:
        f.write(f'{text}{end}')