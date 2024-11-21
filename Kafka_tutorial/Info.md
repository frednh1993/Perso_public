# Subject : Apache Kafka

* Sources : ***https://www.youtube.com/watch?v=Ch5VhJzaoaI* **

# Architecture and Notes

* Producer := Process that read and write the updates in a queue.
* Consumer := Process that consume (read) the updates in the queue to display them on a channel (ex. : mobile, computer). Consume update using a pointer.
* Queue ( have a Partition number ) := Buffer tank accumulating the updates, and hosted on a server. The total number of partition = a partition count.
* Broker := Server that hold one or more partition(s).
* Record := Item ( or update ) in the queue. Have a sequential number assigned ( Offset ).
* Partition Key := Field that decide where a record is store. If none define, kafka send record randomly.
* Topic := Group of Partitions handling the same type of data.
* Offset := Sequential number assigned to a Record to identify it in the Queue.
* Consumer group := Group of consumers (ex. : mobile, computer) that do not share partition (read different partition from others), and that are identify by a Consumer Group Id.
* Record cleanup policy := Policy who dictate when and what portion of the Queue is ready to be free (delete). Policies included record age limite for exemple.
* Replication Factor := Number who dictate how many broker are used to replicate each partition for persistance in case where a main Broker goes down (Partition leader / Partitions backup).
* Record Storage := Way to store record safely by using persistent storage (ex. : hard disk drives, SSD), and by using a Replication factor.
