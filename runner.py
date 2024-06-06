import ctypes
import os

pathC = os.path.abspath(r"libfun.so")
pathDictionary = os.path.abspath(r"Dictionary.txt")
fun = ctypes.CDLL(pathC)
fun.levenshtein.argtypes = [ctypes.c_char_p, ctypes.c_char_p]


def checkNeed(word):
    f = open(pathDictionary)
    for target in f:
        target = target.rstrip()
        if target == word:
            return False
    return True


def distance_all(word):
    final = {"1": [], "2": [], "3": [], "4": []}
    f = open(pathDictionary)
    for target_word in f:
        target_word = target_word.rstrip()
        s11 = word.encode('utf-8')
        s22 = target_word.encode('utf-8')
        des = fun.levenshtein(s11, s22)
        match des:
            case 1:
                final["1"].append(target_word)
            case 2:
                final["2"].append(target_word)
            case 3:
                final["3"].append(target_word)
            case 4:
                final["4"].append(target_word)
    return final


