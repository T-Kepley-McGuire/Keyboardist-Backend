import time

def validateTypingData(data):
    def validateKeyStrokes(keyStrokes):
        if not isinstance(keyStrokes, list):
            return False
        for item in keyStrokes:
            if not isinstance(item, list):
                return False
            
            if len(item) != 2:
                return False
            
            if not isinstance(item[0], str):
                return False
            if not isinstance(item[1], int):
                return False
        return True

    if not isinstance(data, dict):
        return False
    if data["keyStrokes"] is None:
        return False
    if not validateKeyStrokes(data["keyStrokes"]):
        return False
    if data["text"] is None:
        return False
    if not isinstance(data["text"], str):
        return False

    return True

def logWithTime(message: str):
    print(f"'{message}' at {time.time()}")

def isAscii(s):
    return all(ord(c) < 128 for c in s)

completion_dict = {
    "closed": 1,
    "opened": 0,
    "started": -1
}

class Delta:
    isAddition: bool
    deltaStart: int
    deltaStop: int
    characters: str

    def __init__(self, isAddition, deltaStart, deltaStop, characters):
        self.isAddition = isAddition
        self.deltaStart = deltaStart
        self.deltaStop = deltaStop
        self.characters = characters

    def __repr__(self):
        return f"<{"+" if self.isAddition else "-"}{self.characters}, {self.deltaStart}-{self.deltaStop}>"