import ctypes
import os

path_function = os.path.abspath(r"editDistance.so")
path_dictionary = os.path.abspath(r"words.txt")
edit_distance = ctypes.CDLL(path_function)
edit_distance.levenshtein.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
edit_distance.levenshtein.restype = ctypes.c_int


# to check if the word is not correctly written
def check_need(target):
    with open(path_dictionary, encoding="utf-8") as dictionary:
        for word in dictionary:
            word = word.rstrip()
            if word == target:
                return False
    return True


# find the closest word to the incorrectly written word
def find_closet_distance(target):
    final = [[], [], [], []]
    target_encoded = target.encode('utf-8')

    # finding the distance for the target and every word in dictionary
    with open(path_dictionary, encoding="utf-8") as dictionary:
        for word in dictionary:
            word = word.rstrip()
            word_encoded = word.encode('utf-8')
            distance = edit_distance.levenshtein(target_encoded, word_encoded)

            # Store the closest word
            match distance:
                case 1:
                    final[0].append(word)
                case 2:
                    final[1].append(word)
                case 3:
                    final[2].append(word)
                case 4:
                    final[3].append(word)

    # just return the nearest words in the dictionary at least 5 of them
    closest_word = []
    for i in range(0, 4):
        if len(closest_word) < 5:
            for x in final[i]:
                closest_word.append(x)
    return closest_word

# Example usage:
# target_word = "example"  # target word must be a string object
# print(check_need(target_word))
# print(find_closet_distance(target_word))
