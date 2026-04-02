from python_backend.main import main
from multiprocessing import Process, Queue

request_queue = Queue()
receiver_queue = Queue()

if __name__ == '__main__':
    Process(target=main, args=(request_queue, receiver_queue))

    # Launch TUI here