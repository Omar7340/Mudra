class PositionManager:
    def __init__(self):
        self._positions = []
        self._observers = []
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update_positions(self._positions)
    
    def add_position(self, position):
        self._positions.append(position)
        self.notify_observers()
    
    def remove_position(self, label):
        self._positions = [p for p in self._positions if p['label'] != label]
        self.notify_observers()
    
    def get_positions(self):
        return self._positions
    
    def len(self):
        return len(self._positions)