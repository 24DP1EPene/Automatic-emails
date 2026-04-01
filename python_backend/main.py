from multiprocessing import Queue
from typing import Callable
from utils import read_json, merge_settings
from commands import send_email
from threading import Thread, Event
from time import sleep

def main(request_queue: Queue, response_queue: Queue) -> None:

    default_settings = read_json('default settings.json')
    settings = read_json('settings.json')
    all_settings = merge_settings(settings, default_settings)
    profiles = read_json('.profile.json')


    def send_response(message: str, status: bool):
        response_queue.put({'message': message, 'status': status})

    def launch_condition(function: Callable, profile_id: str, quit_event: Event):
        profile = profiles[profile_id]
        sender = profile['sender_email']
        receivers = profile['receiver_emails']
        password = profile['password']
        subject = profile['topic']
        body = profile['content']
        
        def thread_function():
            while True:
                if function:
                    for receiver in receivers:
                        send_email(sender, receiver, password, subject, body)
                if quit_event.is_set():
                    break
                sleep(all_settings['nosacijuma cikla laiks'])
        
        Thread(target=thread_function, daemon=True).start()
    
    request = request_queue.get()

    match request['message']:
        case 'add profile':
            pass

