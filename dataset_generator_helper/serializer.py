class NormalizedLandmarkListSerializer:
    def __init__(self, data):
        self._data = data

        # Liste des identifiants des repères pour la main selon MediaPipe (pour les 21 points)
        self._landmark_labels = [
            'Wrist', 'Thumb_CMC', 'Thumb_MCP', 'Thumb_IP', 'Thumb_Tip',
            'Index_Finger_MCP', 'Index_Finger_PIP', 'Index_Finger_DIP', 'Index_Finger_Tip',
            'Middle_Finger_MCP', 'Middle_Finger_PIP', 'Middle_Finger_DIP', 'Middle_Finger_Tip',
            'Ring_Finger_MCP', 'Ring_Finger_PIP', 'Ring_Finger_DIP', 'Ring_Finger_Tip',
            'Little_Finger_MCP', 'Little_Finger_PIP', 'Little_Finger_DIP', 'Little_Finger_Tip'
        ]

    def serialize(self):
        # Si des mains sont détectées, on extrait les landmarks et on les transforme en dictionnaire
        positions = {}

        for k, pos in self._data.items():
            hands_data = []

            for hand_landmarks in pos:
                hand_data = []
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    # Chaque landmark est une instance de Point avec des attributs x, y, z
                    hand_data.append({
                        'id': idx,  # Identifiant du repère (de 0 à 20)
                        'label': self._landmark_labels[idx],  # Nom du repère
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    })

                hands_data.append(hand_data)

            positions[k] = hands_data

        return positions
