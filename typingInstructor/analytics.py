from app.utils import Delta

def getFinalWPM(deltas: list[Delta]) -> float:
    return deltas[-1].deltaStop - deltas[0].deltaStart

def getFinalAccuracy(finalString: str, targetString) -> float:
    numChars = len(targetString)
    errorChars = 0
    for i in range(numChars):
        errorChars += 1 if finalString[i] != targetString[i] else 0

    return errorChars / numChars