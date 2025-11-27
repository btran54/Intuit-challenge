import threading
import queue
import time
from typing import List, Any


def print_status(actor: str, action: str, details: str = "") -> None:
    "formatted status message."
    suffix = f": {details}" if details else ""
    print(f"[{actor}] {action}{suffix}")


class ProducerConsumer:
    """
    Producer reads from source container into a bounded queue.
    Consumer reads from queue into destination container.
    """
    
    def __init__(self, source_data: List[Any]):
        self.source = source_data.copy() # Create a copy to prevent external modification
        self.destination: List[Any] = []
        
        # Queue capacity is half of source size, at least 1 to show blocking behavior
        queue_capacity = max(1, len(self.source) // 2)
        self.shared_queue: queue.Queue = queue.Queue(maxsize=queue_capacity)
        
        self.lock = threading.Lock() # To protect destination list
        self.producer_done = threading.Event() # Signal when producer is done
        
        print(f"Initialized: {len(self.source)} items, queue capacity: {queue_capacity}")
    
    # Producer method:
    # Read items from source and place into queue
    def producer(self) -> None:
        print_status("Producer", "Starting", f"{len(self.source)} items to produce")
        
        for item in self.source:
            # put() blocks if queue is full
            self.shared_queue.put(item)
            print_status("Producer", "Produced", 
                        f"{item} (Queue: {self.shared_queue.qsize()}/{self.shared_queue.maxsize})")
            
            if self.shared_queue.full():
                print_status("Producer", "Queue FULL - blocking until space available")
            
            time.sleep(0.01)
        
        self.producer_done.set() # Signal that production is complete
        print_status("Producer", "Finished")
    
    # Consumer method:
    # Read items from queue and store in destination
    def consumer(self) -> None:
        print_status("Consumer", "Starting")
        
        while True:
            try:
                # get() blocks if queue is empty and timeout allows periodic checks
                item = self.shared_queue.get(timeout=0.1)
                
                # Thread-safe append to destination
                with self.lock:
                    self.destination.append(item)
                
                print_status("Consumer", "Consumed",
                            f"{item} (Destination: {len(self.destination)}/{len(self.source)})")
                
                if self.shared_queue.empty():
                    print_status("Consumer", "Queue EMPTY - waiting for producer")
                
                self.shared_queue.task_done()
                time.sleep(0.015)
            
            # Exit only when producer is done AND queue is empty
            except queue.Empty:
                if self.producer_done.is_set() and self.shared_queue.empty():
                    break
        
        print_status("Consumer", "Finished")

    # Run the producer-consumer process
    def run(self) -> None:
        print("\n" + "=" * 60)
        print("Starting Producer-Consumer Transfer")
        print("=" * 60)
        
        # Start producer and consumer threads
        producer_thread = threading.Thread(target=self.producer, name="Producer")
        consumer_thread = threading.Thread(target=self.consumer, name="Consumer")
        
        # Start consumer first to ensure it's ready to receive items
        consumer_thread.start()
        producer_thread.start()
        
        # Wait for both threads to complete
        producer_thread.join()
        consumer_thread.join()
    
    # Verify that all items were transferred correctly
    def verify(self) -> bool:
        print("\n" + "=" * 60)
        print("Verification Results")
        print("=" * 60)
        
        checks = [
            ("Length match", len(self.source) == len(self.destination)),
            ("Order preserved", self.source == self.destination),
            ("All elements present", sorted(self.source) == sorted(self.destination)),
        ]
        
        for name, passed in checks:
            status = "!!!" if passed else "XXX"
            print(f"  {status} {name}")
        
        success = all(passed for _, passed in checks)
        result = "PASSED" if success else "FAILED"
        print(f"\nResult: {result}")
        print(f"  Source: {len(self.source)} items")
        print(f"  Destination: {len(self.destination)} items")
        
        return success


def main():
    # Using a sample data set of mixed integers and floats
    source_data = [
        1, 2.5, 3, 4.7, 5, 6.3, 7, 8.9, 9, 10.1,
        11, 12.4, 13, 14.8, 15, 16.2, 17, 18.6, 19, 20.0
    ]
    
    pc = ProducerConsumer(source_data)
    pc.run()
    pc.verify()


if __name__ == "__main__":
    main()