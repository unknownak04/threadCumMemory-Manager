import threading
import random

# Memory Manager
class MemoryManager:
    def __init__(self, size):
        self.size = size
        self.memory = [None] * size  # Represents memory blocks
        self.lock = threading.Lock()

    def allocate(self, request_size):
        # Check availability first without locking
        for i in range(self.size - request_size + 1):
            if all(block is None for block in self.memory[i:i + request_size]):
                with self.lock:  # Lock only during allocation
                    # Check again to ensure no other thread has allocated in the meantime
                    if all(block is None for block in self.memory[i:i + request_size]):
                        for j in range(request_size):
                            self.memory[i + j] = "Allocated"
                        return i  # Return starting index
        return -1  # Allocation failed

    def deallocate(self, start_index, request_size):
        with self.lock:
            for j in range(request_size):
                self.memory[start_index + j] = None

    def display_memory(self):
        print("Memory:", self.memory)

# Thread Library
class Thread:
    def __init__(self, target, *args):
        self.target = target
        self.args = args
        self.thread = None
        self.mutex = threading.Lock()

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        with self.mutex:
            self.target(*self.args)

    def join(self):
        self.thread.join()

# Example function to use with threads
def allocate_memory(mm, size):
    index = mm.allocate(size)
    if index != -1:
        print(f"Allocated {size} blocks at index {index}")
    else:
        print(f"Failed to allocate {size} blocks")

# Main function
if __name__ == "__main__":
    mm = MemoryManager(20)  # Initialize memory manager with 20 blocks

    # Create and start threads for memory allocation
    threads = []
    for _ in range(5):
        size = random.randint(1, 5)
        thread = Thread(allocate_memory, mm, size)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Display memory state
    mm.display_memory()
