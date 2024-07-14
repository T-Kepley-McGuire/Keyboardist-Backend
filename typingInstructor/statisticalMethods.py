import numpy as np

def rejectoutliers(data: list[float], m: float = 2) -> list[float]:
    mean = getMean(data)
    std = getSTD(data)
    return data[abs(data - mean) < m * std]

def getMean(data: list[float]) -> float:
    return np.mean(data)

def getSTD(data: list[float]) -> float:
    return np.std(data)

def getSkew(data: list[int]) -> float:
    return (getMean(data) - np.median(np.array(data))) / getSTD(data)

def getLogData(data: list[float]) -> list[float]:
    return np.log10(data)