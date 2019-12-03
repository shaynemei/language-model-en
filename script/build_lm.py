import sys, re, math

def truncate(n, decimals=10):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def main():
    with open(sys.argv[1], 'r') as f:
        data = f.readlines()
    
    unigram_dict = {}
    bigram_dict = {}
    trigram_dict = {}
    for line in data:
        line = line.replace("\n", "")
        splits = line.split('\t')
        count = int(splits[0])
        ngram = splits[1]
        if(len(re.findall("\s", ngram)) == 1):
            bigram_dict[ngram] = count
        elif (len(re.findall("\s", ngram)) == 2):
            trigram_dict[ngram] = count
        else:
            unigram_dict[ngram] = count
    
    unigram_num_tokens = sum(unigram_dict.values())
    bigram_num_tokens = sum(bigram_dict.values())
    trigram_num_tokens = sum(trigram_dict.values())
    
    unigram_num_types = len(unigram_dict)
    bigram_num_types = len(bigram_dict)
    trigram_num_types = len(trigram_dict)
    
    
    with open(sys.argv[2], "w") as f:
        f.write("\\data\\\n")
        f.write("ngram 1: ")
        f.write("type=" + str(unigram_num_types) + " token=" + str(unigram_num_tokens) + "\n")
        f.write("ngram 2: ")
        f.write("type=" + str(bigram_num_types) + " token=" + str(bigram_num_tokens) + "\n")
        f.write("ngram 3: ")
        f.write("type=" + str(trigram_num_types) + " token=" + str(trigram_num_tokens) + "\n")
        f.write("\n")
        f.write("\\1-grams:\n")
        start_bigram = 0
        start_trigram = 0
        for idx, line in enumerate(data):
            line = line.replace("\n", "")
            splits = line.split('\t')
            count = int(splits[0])
            ngram = splits[1]
            words = re.findall("\S+", ngram)
            
            if(len(re.findall("\s", ngram)) == 1):
                start_bigram = idx
                break
    
            prob = truncate(count/unigram_num_tokens)
            if prob == 0:
                continue
            lgprob = truncate(math.log10(prob))
            f.write(str(count) + " " + str(prob) + " " + str(lgprob) + " " + ngram + "\n")
        
        f.write("\n")
        f.write("\\2-grams:\n")
        for idx, line in enumerate(data[start_bigram:]):
            line = line.replace("\n", "")
            splits = line.split('\t')
            count = int(splits[0])
            ngram = splits[1]
            words = re.findall("\S+", ngram)
            
            if (len(re.findall("\s", ngram)) == 2):
                start_trigram = idx
                break
                
            prob = truncate(count/unigram_dict[words[0]])
            if prob == 0:
                continue
            lgprob = truncate(math.log10(prob))
            f.write(str(count) + " " + str(prob) + " " + str(lgprob) + " " + ngram + "\n")
        
        f.write("\n")
        f.write("\\3-grams:\n")
        for line in data[start_bigram + start_trigram:]:
            line = line.replace("\n", "")
            splits = line.split('\t')
            count = int(splits[0])
            ngram = splits[1]
            words = re.findall("\S+", ngram)
            prob = truncate(count/bigram_dict[words[0] + " " + words[1]])
            if prob == 0:
                continue
            lgprob = truncate(math.log10(prob))
            f.write(str(count) + " " + str(prob) + " " + str(lgprob) + " " + ngram + "\n")

        f.write("\n")
        f.write("\\end\\")

if __name__ == "__main__":
	main()
    