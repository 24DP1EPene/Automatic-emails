from python_backend.main import main
from python_ui.tui.main import EmailAutomationTUI
from multiprocessing import Process, Queue

request_queue = Queue()
receiver_queue = Queue()

if __name__ == '__main__':
    # Start backend process
    backend_process = Process(target=main, args=(request_queue, receiver_queue))
    backend_process.start()
    
    # Launch TUI with queue connection
    tui = EmailAutomationTUI(request_queue=request_queue, response_queue=receiver_queue)
    tui.run()
    
    # Cleanup
    backend_process.terminate()
    backend_process.join()
