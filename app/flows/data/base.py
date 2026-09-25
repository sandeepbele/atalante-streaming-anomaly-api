from abc import abstractmethod


class DataflowEngine:
    pass


class DataflowSource:
    pass



class DataflowDestination:
    pass



class DataflowConnection:

    source:DataflowSource
    destination:DataflowDestination
    inSchema = None
    outSchema = None

    def __int__(self, source, destination):
        self.source = source
        self.destination = destination
        pass

    def start(self):
        pass

    def stop(self):
        pass