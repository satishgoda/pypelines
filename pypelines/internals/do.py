from .dag import DAGNode


class Do(DAGNode):
    def __init__(self, func):
        super().__init__()
        self._func = func

    def produce(self):
        result = self._func()
        self.forward_data(result)
        self.forward_completed()