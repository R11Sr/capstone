class Room():
    def __init__(self,title: str,capacity: int) -> None:

        self.title = title
        self.capacity = capacity


def exe():
    r1 = Room('ere',34)
    r2 = Room('fvger',45)

    print(r1.title)

exe()