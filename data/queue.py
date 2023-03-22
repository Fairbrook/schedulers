from data.process import Process

class ProcessQueue:
    def __init__(self):
        self.queue: List[Process] = list()
        self.finished_proc: Set[int] = set()
        self.finished = False
        self.active_index = 0
        self.started = False

    def is_finished(self):
        return len(self.finished_proc) == len(self.queue)

    def get_shortest_remaining(self):
        if (len(self.queue)==0):
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


    def add(self, proc: Process):
        self.queue.append(proc)
        self.next_proc()

    def get_active(self):
        return self.queue[self.active_index]

    def next_proc(self):
        if(self.is_finished()):
            self.finished = True
            return
        if(self.get_active().state ==Process.RUNING):
            self.get_active().state = Process.WAITING
        shortest = self.get_shortest_remaining()
        if(shortest == None):
            self.finished = True
            return
        if(self.started):
            self.get_active().state = Process.RUNING

    def start(self):
        self.get_active().state = Process.RUNING
        self.started = True

    def tick(self):
        if(len(self.queue) == 0 or self.finished):
            return
        if(self.get_active().state == Process.WAITING):
            self.get_active().state = Process.RUNING
        for proc in self.queue:
            proc.tick()
        if(self.get_active().state == Process.FINISH):
            self.finished_proc.add(self.active_index)
            self.next_proc()

    def restart(self):
        self.active_index = 0
        self.finished = False
        self.finished_proc = set()
        for proc in self.queue:
            proc.restart()
        self.get_shortest_remaining()
