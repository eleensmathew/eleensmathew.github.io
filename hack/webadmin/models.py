from django.db import models
import heapq

class PriorityQueue(models.Model):
    data = models.JSONField(default=dict)

    def __init__(self, *args, **kwargs):    #initializing heap as an empty list
        super().__init__(*args, **kwargs)
        self.heap = []
        self._heapify()

    def __str__(self):
        return str(self.data)

    def push(self, priority, value):
        priority = int(priority)
        heapq.heappush(self.heap, (priority, value))
        if priority not in self.data:       #to avoid the overlapping of the values for which keys are same
            self.data[priority] = []
        self.data[priority].append(value)
        self.save()

    def pop(self):              #removes the value with highest priority
        if not self.heap:
            raise IndexError("Heap is empty")
        priority, values = self.heap[0]
        value = values.pop(0)
        if not values:
            del self.data[priority]
            heapq.heappop(self.heap)
        self.save()
        return value

    def peek(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        priority, values = self.heap[0]
        return values[0]

    def _heapify(self):     #populate the dictionary with data keys and values
        for priority, values in self.data.items():
            heapq.heappush(self.heap, (priority, values))

    def total_values(self):
        total = 0
        for values in self.data.values():
            total += len(values)
        return total
    
    class Meta:
        verbose_name_plural = "Priority Queues"


class Admin_info(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)
    priority = models.OneToOneField("PriorityQueue", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username