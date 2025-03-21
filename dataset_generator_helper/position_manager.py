from serializer import NormalizedLandmarkListSerializer

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

        position = NormalizedLandmarkListSerializer(position).serialize()

        self._positions[label] = position
        self.notify_observers()
    
    def remove_position(self, label):
        print("removed {}".format(label))
        self._index_free.append(label)
        self._positions.pop(label)
        self.notify_observers()
    
    def get_positions(self, include_img=True, include_coord=True):

        if include_img and include_coord:
            return self._positions
        
        positions = {}

        for k,v in self._positions.items():
            pos = []

            if not include_coord:
                pos = {
                    "img": v['img']
                }
            
            if not include_img:
                pos = {
                    "pos": v['pos']
                }

            positions[k] = pos

        return positions
    
    def len(self):
        return len(self._positions)