from multiprocessing import Queue
from typing import Callable
from threading import Thread, Event
from time import sleep

from python_backend.profiles import create_profile, delete_profile, edit_profile
from python_backend.utils import read_json, merge_settings, read_profiles, log_action
from python_backend.commands import send_email
from python_backend.conditions import conditions

def main(request_queue: Queue, response_queue: Queue) -> None:

    default_settings = read_json('default settings.json')
    settings = read_json('settings.json')
    all_settings = merge_settings(settings, default_settings)
    profiles = read_profiles()


    def launch_condition(function: Callable, profile_id: str, quit_event: Event):
        profile = profiles[profile_id]
        sender = profile['sender_email']
        receivers = profile['receiver_emails']
        password = profile['password']
        subject = profile['topic']
        body = profile['content']
        
        def thread_function():
            while True:
                if function():
                    for receiver in receivers:
                        send_email(sender, receiver, password, subject, body)
                if quit_event.is_set():
                    break
                sleep(all_settings['nosacijuma cikla laiks'])
        
        Thread(target=thread_function, daemon=True).start()

    quit_events = {}
    # Palaiž eksistējošos profilus

    for id, profile in profiles.items():
        quit_event = Event()
        launch_condition(conditions[profile['condition']], id, quit_event)
        quit_events[id] = quit_event

    # Aizsūta visus quit event id

    for quit_event in quit_events.items():
        response_queue.put(quit_event[0])

    while True:
        request = request_queue.get()

        match request['message']:
            case 'add profile':
                create_profile(*request['data'])
                print('created', request)
            case 'delete profile':
                delete_profile(*request['data'])
            case 'edit profile':
                edit_profile(*request['data'])
            case 'quit':
                for quit_event in quit_events.items():
                    quit_event[1].set()
                exit()