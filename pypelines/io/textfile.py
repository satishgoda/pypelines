from ..internals.dag import DAGNode


class TextFile(DAGNode):
    def __init__(self, filepath, header=None):
        super().__init__()
        self._filepath = filepath
        self._header = header
        self._encoding = 'utf-8'

    def produce(self):
        #todo: handle exceptions
        #do not declare file pointer in __init__ to pickle object easily during creation of processes
        self._fp = open(str(self._filepath))
        while True:
            line = self._fp.readline()
            if not line:
                break
            self.forward_data(line)

        self._fp.close()
        self.forward_completed()


    def on_data(self, data):
        if not hasattr(self, '_fp'):
            self._ctr = 0
            self._fp = open(str(self._filepath), "w", encoding=self._encoding)
            if self._header:
                self._fp.write(self._header + "\n")
        self._ctr += 1
        self._fp.write(str(data) + "\n")
        if self._ctr % 1000 == 0:
            self.log(str(self._filepath) + "==>" + str(self._ctr))

    def on_completed(self, data=None):
        self.log("ready to close " + str(self._filepath))
        if hasattr(self, '_fp') and not self._fp is None:
            self._fp.close()
            self.log("closed " + str(self._filepath))
        self.forward_completed(data)


    def __getstate__(self):
        """ This is called before pickling. """
        #handle how this class is pickled (pickling happen during creation of processes).
        #Removeing file pointer is important to avoid "TypeError: cannot serialize '_io.TextIOWrapper' object" when object is deserialized in the spawned process
        state = self.__dict__.copy()
        if '_fp' in state:
            del state['_fp']
        return state

    def __setstate__(self, state):
        """ This is called while unpickling. """
        self.__dict__.update(state)
        


#https://github.com/timdelbruegger/freecopter/blob/master/src/python3/sensors/gps_polling_thread.py
#from gpspy3 import gps
# a = gps.GPS()
#g = gpspy3.gps.GPS(mode=gpspy3.gps.WATCH_ENABLE)        