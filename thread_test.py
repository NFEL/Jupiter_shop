import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
    exit()

def counter():
    for i in range(1,20):
        time.sleep(0.5)
        logging.info("counter : %d" , i)
        
        
    

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    thr2 = threading.Thread(target=counter,daemon=)
    logging.info("Main    : before running thread")
    thr2.start()
    x.start()
    
    # thr2.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")