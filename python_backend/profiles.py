import json
import uuid


def create_profile(sender_email: str, receiver_emails: list[str], password: str, topic: str, email_content: str, condition: int) -> dict[str, dict[str: list[str] | str | int]]:
    """
    Funkcija <create_profile>
    pieņem <list[str], list[str], str, str, str, int>
    tipa vērtību <sender_email, receiver_email, password, topic, email_content, condition>
    un atgriež <dict[str, dict[str: list[str] | str | int]]>
    tipa vērtību <new_profile>
    """ 
    new_profile = {
        str(uuid.uuid1()): {
            "sender_email": sender_email,
            "receiver_emails": receiver_emails,
            "password": password,
            "topic": topic,
            "email_content": email_content,
            "condition": condition
        }
    }
    try:
        with open(".profiles.json", "r") as f:
            profiles = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}
    profiles.update(new_profile)
    with open(".profiles.json", "w") as f:
        json.dump(profiles, f)

    return new_profile