class PositionManager:
    def __init__(self):
        self._positions = {}
        self._observers = []
        self._index = 0
        self._index_free = []
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update_positions(self._positions)
    
    def add_position(self, position):
        self._index += 1
        label = "pos-" + str(self._index)
        self._positions[label] = position
        self.notify_observers()
    
    def remove_position(self, label):
        print("removed {}".format(label))
        self._index_free.append(label)
        self._positions.pop(label)
        self.notify_observers()
    
    def get_positions(self):
        return self._positions
    
    def len(self):
        return len(self._positions)