import re

import numpy as np

from typingInstructor.keyboardLayouts import layouts

from typingInstructor import statisticalMethods as sm

def reconstructFinalString2(typingData: list[(str, float)]) -> str:
    typingData = sorted(typingData, key=lambda entry: entry[1])

    finalString = ""
    for item in typingData:
        if item[0][0] == "+":
            finalString += item[0][1]
        if item[0][0] == "-":
            loc = finalString.rfind(item[0][1])
            if loc >= 0:
                finalString = finalString[:loc] + finalString[loc+1:]

    return finalString

def reconstructFinalString(typingData: list[str, float]) -> str:
    def ctrlBackspace(inputString):
        # Strip any trailing whitespace characters for accurate word boundary detection
        inputString = inputString.rstrip()
        
        # Find the last word boundary before the end of the string
        match = re.match(r'((?:.*\s+(?=\S))*(?:.*?(?=\s{2,}))*)', inputString)

        if match:
            # Remove the word and any trailing non-word characters
            output = match[0]
        else:
            # If no match, that means there is only one word
            output = ""
        
        return output
    
    res = ""
    for key in typingData:
        if len(key[0]) == 1:
            res += key[0]
        elif key[0] == "Backspace":
            res = res[:-1]
        elif key[0] == "Ctrl Backspace":
            res = ctrlBackspace(res)

    return res

def constructDeltas(typingData: list[str, float]) -> list[float]:
    # finalDeltas = []
    # for i in range(1, len(typingData)):
    #     finalDeltas.append(typingData[i][1] - typingData[i-1][1])
    
    return [typingData[i][1] - typingData[i-1][1] for i in range(1, len(typingData))]

def processKeyPresses(typingData: list[str, float], deltas: list[float], mean: float, std: float) -> tuple[dict, dict]:
    keysAsKeys = {}
    for i in range(len(deltas)):
        key = typingData[i+1][0]
        delta = deltas[i]

        if key in keysAsKeys:
            keysAsKeys[key].append(delta)
        else:
            keysAsKeys[key] = [delta]

    for key in keysAsKeys:
        keysAsKeys[key] = sm.getMean(keysAsKeys[key])

    fastestKeys = []
    slowestKeys = []

    for key in keysAsKeys:
        m = keysAsKeys[key]
        if m > mean + std:
            slowestKeys.append((key, round(m)))
        elif m < mean - std:
            fastestKeys.append((key, round(m)))

    return sorted(fastestKeys, key=lambda key: key[1]), sorted(slowestKeys, key=lambda key: key[1], reverse=True)

def processFingerPresses(typingData: list[str, float], deltas: list[float], keyboardLayout: str) -> dict:
    layout = layouts[keyboardLayout]

    fingersToTimes = {}
    for i in range(len(deltas)):
        key = typingData[i+1][0].lower()
        if key in layout:
            if layout[key] in fingersToTimes:
                fingersToTimes[layout[key]].append(deltas[i])
            else:
                fingersToTimes[layout[key]] = [deltas[i]]


    for finger in fingersToTimes:
        fingersToTimes[finger] = sm.getMean(fingersToTimes[finger])
    return fingersToTimes 


def processTypingSession(typingData: list[str, int], text) -> dict:
    startTime = typingData[0][1]
    totalTime = typingData[-1][1] - startTime

    # normalizedTypingData = list(map(lambda ks: [ks[0], (ks[1] - startTime)/totalTime], rawTypingData))


    finalString = reconstructFinalString(typingData)

    deltas = constructDeltas(typingData)

    logDeltas = sm.getLogData(deltas)

    logMean = sm.getMean(logDeltas)
    logSTD = sm.getSTD(logDeltas)
    logSkew = sm.getSkew(logDeltas)

    fastestKeys, slowestKeys = processKeyPresses(typingData, logDeltas, logMean, logSTD)

    fingerTimes = processFingerPresses(typingData, logDeltas, keyboardLayout="qwerty")

    return {"final-string": finalString, "total-time-s": totalTime/1000, "mean-key-delta-ms": round(10**logMean), "standard-deviation-key-delta-range-ms": [round(10**(logMean-logSTD)), round(10**(logMean+logSTD))], "skew-log-distribution": logSkew, "fastest-keys": fastestKeys, "slowest-keys": slowestKeys, "finger-times": fingerTimes}

