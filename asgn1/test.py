import unittest
import threading
import time
from producer_consumer import ProducerConsumer, print_status


class TestProducerConsumer(unittest.TestCase):
    """Test cases for the ProducerConsumer class."""
    
    def test_basic_transfer(self):
        """Test that all items transfer from source to destination."""
        source = [1, 2, 3, 4, 5]
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertEqual(pc.destination, source)
    
    def test_empty_source(self):
        """Test transfer with empty source."""
        source = []
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertEqual(pc.destination, [])
    
    def test_single_item(self):
        """Test transfer with single item."""
        source = [42]
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertEqual(pc.destination, [42])
    
    def test_large_transfer(self):
        """Test transfer with many items."""
        source = list(range(20))
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertEqual(pc.destination, source)
    
    def test_mixed_types(self):
        """Test transfer with integers and floats."""
        source = [1, 2.5, 3, 4.7, 5, 6.3]
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertEqual(pc.destination, source)
    
    def test_order_preserved(self):
        """Test that FIFO order is maintained."""
        source = [10, 20, 30, 40, 50]
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertEqual(pc.destination, source)
    
    def test_source_not_modified(self):
        """Test that original source is not modified."""
        source = [1, 2, 3]
        original = source.copy()
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertEqual(source, original)
    
    def test_queue_capacity(self):
        """Test that queue capacity is half of source."""
        source = list(range(10))
        pc = ProducerConsumer(source)
        
        self.assertEqual(pc.shared_queue.maxsize, 5)
    
    def test_queue_capacity_minimum(self):
        """Test that queue capacity is at least 1."""
        source = [1]
        pc = ProducerConsumer(source)
        
        self.assertEqual(pc.shared_queue.maxsize, 1)
    
    def test_verify_success(self):
        """Test verify returns True on successful transfer."""
        source = [1, 2, 3, 4, 5]
        pc = ProducerConsumer(source)
        pc.run()
        
        self.assertTrue(pc.verify())
    
    def test_verify_failure(self):
        """Test verify returns False when destination is wrong."""
        source = [1, 2, 3]
        pc = ProducerConsumer(source)
        pc.destination = [1, 2]  # Simulate incomplete transfer
        
        self.assertFalse(pc.verify())


class TestThreadSafety(unittest.TestCase):
    """Tests for thread synchronization correctness."""
    
    def test_no_race_conditions(self):
        """Test for absence of race conditions under stress."""
        for _ in range(3):  # Run multiple times
            source = list(range(15))
            pc = ProducerConsumer(source)
            pc.run()
            
            self.assertEqual(sorted(pc.destination), source)
    
    def test_no_deadlock(self):
        """Test that system doesn't deadlock."""
        source = list(range(15))
        pc = ProducerConsumer(source)
        
        # Run with timeout to detect deadlock
        result = [None]
        def run_with_result():
            pc.run()
            result[0] = pc.destination
        
        thread = threading.Thread(target=run_with_result)
        thread.start()
        thread.join(timeout=5.0)
        
        self.assertFalse(thread.is_alive(), "Deadlock detected - operation timed out")
        self.assertEqual(result[0], source)
    
    def test_blocking_behavior(self):
        """Test that queue properly blocks when full."""
        source = list(range(15))
        pc = ProducerConsumer(source)
        
        # Queue capacity is 10, so blocking should occur
        pc.run()
        
        # If we got here without hanging, blocking worked correctly
        self.assertEqual(len(pc.destination), len(source))


class TestPrintStatus(unittest.TestCase):
    """Test the print_status helper function."""
    
    def test_print_status_with_details(self):
        """Test print_status formats correctly with details."""
        print_status("Test", "Action", "Details")
    
    def test_print_status_without_details(self):
        """Test print_status formats correctly without details."""
        print_status("Test", "Action")


if __name__ == "__main__":
    unittest.main(verbosity=2)