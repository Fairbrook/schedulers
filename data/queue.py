from pickle import NONE
from typing import List, Set, Tuple
from data.process import Process


class ProcessQueue:
    def __init__(self):
        self.queue: List[Process] = list()
        self.finished_proc: Set[int] = set()
        self.active: List[int] = list()
        self.finished = False
        self.active_index = 0
        self.queues = 3
        self.started = False

    def is_finished(self):
        return len(self.finished_proc) == len(self.queue)

    def get_shortest_remaining(self):
        if (len(self.queue) == 0):
            return None
        shortest_time = None
        shortest_index = self.active_index
        for index, process in enumerate(self.queue):
            if(process.state == Process.FINISH):
                continue
            if (shortest_time == None or process.remaining < shortest_time):
                shortest_time = process.remaining
                shortest_index = index
        if (shortest_time == None):
            return None
        self.active_index = shortest_index
        return self.queue[shortest_index]

    def get_next_inline(self):
        for index, process in enumerate(self.queue):
            if(process.state == Process.WAITING):
                return index
        return None

    def add(self, proc: Process):
        self.queue.append(proc)
        self.finished = False

    def get_active(self):
        return self.queue[self.active_index]

    def next_proc(self):
        if(self.is_finished()):
            self.finished = True
            self.started = False
            return

        updated_active_process = list()
        for queue_index in range(self.queues):
            next_proc_index = self.get_next_inline()
            if len(self.active) <= queue_index or self.active[queue_index] is None:
                updated_active_process.append(next_proc_index)
            else:
                proc_index = self.active[queue_index]
                if self.queue[proc_index].state == Process.RUNING:
                    updated_active_process.append(proc_index)
                    next_proc_index = None

                if self.queue[proc_index].state == Process.FINISH:
                    self.finished_proc.add(proc_index)
                    updated_active_process.append(next_proc_index)

            if next_proc_index is not None:
                self.queue[next_proc_index].state = Process.QUEUED

        self.active = updated_active_process
        print(updated_active_process)

        all_none = True
        for proc_index in self.active:
            all_none = all_none and proc_index == None

        if(all_none):
            self.finished = True
            self.started = False
            return

        if(self.started):
            for proc_index in self.active:
                if proc_index is not None:
                    self.queue[proc_index].state = Process.RUNING


    def start(self):
        self.started = True
        self.next_proc()

    def tick(self):
        if(len(self.queue) == 0 or self.finished):
            return
        for proc in self.queue:
            proc.tick()
        self.next_proc()

    def restart(self):
        self.finished = False
        self.finished_proc = set()
        self.active = list()
        for proc in self.queue:
            proc.restart()
