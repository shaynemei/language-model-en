from collections import Counter
import re, sys, os


def printCounter(f, counter_obj, n):
    sorted_counter = sorted(counter_obj.items(), key=lambda item: (-item[1], item[0]))
    if n==1:
        for entry in sorted_counter:
            f.write(str(entry[1]) + "\t" + str(entry[0]) + "\n")
    else:
        for entry in sorted_counter:
            f.write(str(entry[1]) + "\t" + " ".join(entry[0]) + "\n")

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        data = f.readlines()
        words = " ".join(["<s> " + line.lower().replace("\n", " </s>") for line in data]).split(" ")
        unigrams = Counter(words)
        bigrams = Counter(zip(words,words[1:]))
        trigrams = Counter(zip(words,words[1:],words[2:]))
            
    with open(sys.argv[2], 'w') as f:
        printCounter(f, unigrams, 1)
        printCounter(f, bigrams, 2)
        printCounter(f, trigrams, 3)