#### Setup Instructions:
1. Clone into local machine
2. Access the directory with `cd Intuit-challenge/asgn1`
2. Run with `python3 -m unittest test -v`

#### Sample Output:
```
test_print_status_with_details (test.TestPrintStatus.test_print_status_with_details)
Test print_status formats correctly with details. ... [Test] Action: Details
ok
test_print_status_without_details (test.TestPrintStatus.test_print_status_without_details)
Test print_status formats correctly without details. ... [Test] Action
ok
test_basic_transfer (test.TestProducerConsumer.test_basic_transfer)
Test that all items transfer from source to destination. ... Initialized: 5 items, queue capacity: 2

============================================================
Starting Producer-Consumer Transfer
============================================================
[Consumer] Starting
[Producer] Starting: 5 items to produce
[Producer] Produced: 1 (Queue: 1/2)
[Consumer] Consumed: 1 (Destination: 1/5)
[Consumer] Queue EMPTY - waiting for producer
[Producer] Produced: 2 (Queue: 1/2)
[Consumer] Consumed: 2 (Destination: 2/5)
[Consumer] Queue EMPTY - waiting for producer
[Producer] Produced: 3 (Queue: 1/2)
[Consumer] Consumed: 3 (Destination: 3/5)
[Consumer] Queue EMPTY - waiting for producer
[Producer] Produced: 4 (Queue: 1/2)
[Producer] Produced: 5 (Queue: 2/2)
[Producer] Queue FULL - blocking until space available
[Consumer] Consumed: 4 (Destination: 4/5)
[Producer] Finished
[Consumer] Consumed: 5 (Destination: 5/5)
[Consumer] Queue EMPTY - waiting for producer
[Consumer] Finished
ok
test_empty_source (test.TestProducerConsumer.test_empty_source)
Test transfer with empty source. ... Initialized: 0 items, queue capacity: 1

============================================================
Starting Producer-Consumer Transfer
============================================================
[Consumer] Starting
[Producer] Starting: 0 items to produce
[Producer] Finished
[Consumer] Finished
ok
test_large_transfer (test.TestProducerConsumer.test_large_transfer)
Test transfer with many items. ... Initialized: 20 items, queue capacity: 10
```