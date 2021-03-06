from pickleablelambda import pickleable

from .dag import DAGNode
import inspect

class FlatMap(DAGNode):
    def __init__(self, func=lambda x: x):
        super().__init__()
        self._func = pickleable(func)

    def on_data(self, data):
        res = self._func(data)
        for item in res:
            self.forward_data(item)

    def name(self):
        return super().name() #+ "; func=" + inspect.getsource(self._func)

