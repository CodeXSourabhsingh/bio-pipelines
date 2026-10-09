
class Blood_group:
    ALL_TYPES = ('O-', 'O+', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-')
    RECEIVE_TABLE = {
        'O-': ['O-'],
        'O+': ['O+', 'O-'],
        'A+': ['A+', 'A-', 'O+', 'O-'],
        'A-': ['A-', 'O-'],
        'B+': ['B+', 'B-', 'O+', 'O-'],
        'B-': ['B-', 'O-'],
        'AB+': ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-'],
        'AB-': ['AB-', 'B-', 'A-', 'O-']
    }

    def __init__(self,BloodGroup):
        self.BloodGroup = BloodGroup
    def can_receive_from(self):
        return self.RECEIVE_TABLE[self.BloodGroup]
    def can_donate_to(self):
        donors = []
        for recipient in self.ALL_TYPES:
            if self.BloodGroup in self.RECEIVE_TABLE[recipient]:
                donors.append(recipient)
        return donors    
if __name__ == "__main__":
    x = input('ENTER BLOOD GROUP: ').upper().strip()
    print(" Blood_group: ", x)
    bg = Blood_group(x)
    print("can_receive_from: ", bg.can_receive_from())
    print("can_donate_to: ", bg.can_donate_to())









    