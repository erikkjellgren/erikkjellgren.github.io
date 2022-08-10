import time

start_time = time.time()
alphabet = list("abcdefghijklmnopqrstuvwxyz")
values = [2**i for i in range(0, 26)]
letter_to_value = {}
for letter, value in zip(alphabet, values):
    letter_to_value[letter] = value

words5 = []
with open("data/words_alpha.txt", "r") as file:
    for line in file.readlines():
        if len(line.strip()) == 5:
            words5.append(line.strip())
words5_purged = []
for word in words5:
    for letter in alphabet:
        if word.count(letter) >= 2:
            break
    else:
        words5_purged.append(word)

words5_value = []
value_to_word = {}
for word in words5_purged:
    value = 0
    for letter in word:
        value += letter_to_value[letter]
    if value not in words5_value:
        words5_value.append(value)
    if value not in value_to_word:
        value_to_word[value] = [word]
    else:
        value_to_word[value].append(word)

num_words = len(words5_value)
solutions = []
for idx1 in range(0, num_words - 4):
    word1 = words5_value[idx1]
    for idx2 in range(idx1 + 1, num_words - 3):
        word2 = words5_value[idx2]
        if (word1 & word2) != 0:
            continue
        cumulative_word2 = word1 ^ word2
        for idx3 in range(idx2 + 1, num_words - 2):
            word3 = words5_value[idx3]
            if (cumulative_word2 & word3) != 0:
                continue
            cumulative_word3 = cumulative_word2 ^ word3
            for idx4 in range(idx3 + 1, num_words - 1):
                word4 = words5_value[idx4]
                if (cumulative_word3 & word4) != 0:
                    continue
                cumulative_word4 = cumulative_word3 ^ word4
                for idx5 in range(idx4 + 1, num_words):
                    word5 = words5_value[idx5]
                    if (cumulative_word4 & word5) != 0:
                        continue
                    solutions.append([word1, word2, word3, word4, word5])
print(time.time() - start_time)
