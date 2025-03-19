class PositionManager:
    def __init__(self):
        self._positions = {}
        self._observers = []
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update_positions(self._positions)
    
    def add_position(self, label, position):
        if not label in self._positions:
          self._positions[label] = position
          self.notify_observers()
        else:
            raise ValueError("label already exist")
    
    def remove_position(self, label):
        print("removed {}".format(label))
        self._positions.pop(label)
        self.notify_observers()
    
    def get_positions(self):
        return self._positions
    
    def len(self):
        return len(self._positions)