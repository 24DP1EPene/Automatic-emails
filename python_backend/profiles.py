import json
import uuid


def create_profile(sender_email: str, name: str, receiver_emails: list[str], description: str, password: str, topic: str, email_content: str, condition: int) -> dict[str, dict[str: list[str] | str | int]]:
    """
    Funkcija <create_profile>
    pieņem <str, list[str], str, str, str, str, str, int> tipa vērtību <sender_email, name, receiver_email, description, password, topic, email_content, condition>
    un atgriež <dict[str, dict[str: list[str] | str | int]]> tipa vērtību <new_profile>
    """ 
    new_profile = {
        str(uuid.uuid1()): {
            "sender_email": sender_email,
            "name": name,
            "receiver_emails": receiver_emails,
            "description": description,
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
        json.dump(profiles, f, indent=4)

    return new_profile

def edit_profile(name: str, description: str, updates: dict):
    """
    Funkcija <edit_profile>
    pieņem <str, str, dict[str, dict[str: list[str] | str | int]]> tipa vērtību <name, description, updates>
    un atgriež <dict[str, dict[str: list[str] | str | int]]> tipa vērtību <profile_data>
    """
    try:
        with open(".profiles.json", "r") as f:
            profiles = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    for profile_id, profile_data in profiles.items():
        if profile_data.get("name") == name and profile_data.get("description") == description:
            for key, value in updates.items():
                if value is not None:
                    profile_data[key] = value
            with open(".profiles.json", "w") as f:
                json.dump(profiles, f, indent=4)

            return {profile_id: profile_data}

def delete_profile(name: str, description: str):
    """
    Funkcija <delete_profile>
    pieņem <str, str> tipa vērtību <name, description>
    un atgriež <Null> tipa vērtību <Null>
    """
    try:
        with open(".profiles.json", "r") as f:
            profiles = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    
    profile_to_delete = None
    for profile_id, profile_data in profiles.items():
        if profile_data.get("name") == name and profile_data.get("description") == description:
            profile_to_delete = profile_id
            break
    if profile_to_delete is None:
        return
    del profiles[profile_to_delete]
    with open(".profiles.json", "w") as f:
        json.dump(profiles, f, indent=4)