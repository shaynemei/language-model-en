import sys, re, math

def truncate(n, decimals=10):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lm = f.readlines()
    
    with open(sys.argv[5]) as f:
        data = f.readlines()

    data = [line.lower() for line in data]
    
    unigram_prob_dict = {}
    bigram_prob_dict = {}
    trigram_prob_dict = {}
        
    start_unigram = 0
    start_bigram = 0
    start_trigram = 0
    
    for idx, line in enumerate(lm):
        if (line == "\\1-grams:\n"):
            start_unigram = idx + 1
        elif (line == "\\2-grams:\n"):
            start_bigram = idx + 1
        elif (line == "\\3-grams:\n"):
            start_trigram = idx + 1
    
    for line in lm[start_unigram:start_bigram]:
        line = line.replace("\n", "")
        splits = line.split(' ')
        try:
            prob = float(splits[1])
            ngram = splits[3]
            unigram_prob_dict[ngram] = prob
        except:
            continue
    
    for line in lm[start_bigram:start_trigram]:
        line = line.replace("\n", "")
        splits = line.split(' ')
        try:
            prob = float(splits[1])
            ngram = " ".join(splits[3:])
            bigram_prob_dict[ngram] = prob
        except:
            continue
    
    for line in lm[start_trigram:]:
        line = line.replace("\n", "")
        splits = line.split(' ')
        try:
            prob = float(splits[1])
            ngram = " ".join(splits[3:])
            trigram_prob_dict[ngram] = prob
        except:
            continue
    
    l1 = float(sys.argv[2])
    l2 = float(sys.argv[3])
    l3 = float(sys.argv[4])
    
    with open(sys.argv[6], "w") as f:
        f.write("\n")
        lgprob_sum = 0
        word_num = 0
        oov_num = 0
        sent_num = len(data)
        for i, line in enumerate(data):
            cur_word_num = 0
            cur_oov_num = 0
            cur_lgprob_sum = 0
            line = line.replace("\n", "")
            line = "<s> " + line + " </s>"
            f.write("Sent #" + str(i+1) + ": " + line)
            f.write("\n")
            words = line.split(" ")
            cur_word_num = len(words) - 2
            word_num += cur_word_num
            for idx, word in enumerate(words):
                if idx == 0:
                    continue
                unseen = False
                if word in unigram_prob_dict:
                    p1 = unigram_prob_dict[word]
                    if idx == 1:
                        bigram = words[idx-1] + " " + word
                        p3 = 0
                        try: 
                            p2 = bigram_prob_dict[bigram]
                        except:
                            p2 = 0
                        f.write(str(idx) + ": lg P(" + word + " | " + words[idx-1] + ") = ")
                    else:
                        bigram = words[idx-1] + " " + word
                        trigram = words[idx-2] + " " + words[idx-1] + " " + word
                        try:
                            p2 = bigram_prob_dict[bigram]
                        except:
                            p2 = 0
                            unseen = True
                        try:
                            p3 = trigram_prob_dict[trigram]
                        except:
                            p3 = 0
                            unseen = True
                        f.write(str(idx) + ": lg P(" + word + " | " + words[idx-2] + " " + words[idx-1] + ") = ")
                    prob = l1 * p1 + l2 * p2 + l3 * p3
                    lgprob = math.log10(prob)
                    cur_lgprob_sum += lgprob
                    
                    f.write(str(lgprob))
                    if unseen:
                        f.write(" (unseen ngrams)")
                    f.write("\n")
                else:
                    cur_oov_num += 1
                    if idx == 1:
                        f.write(str(idx) + ": lg P(" + word + " | " + words[idx-1] + ") = -inf (unknown word)")
                        f.write("\n")
                    else:
                        f.write(str(idx) + ": lg P(" + word + " | " + words[idx-2] + " " + words[idx-1] + ") = -inf (unknown word)")
                        f.write("\n")
            lgprob_sum += cur_lgprob_sum
            oov_num += cur_oov_num
            cur_ppl = truncate(pow(10, (-cur_lgprob_sum)/(cur_word_num+1-cur_oov_num)))
            f.write("1 sentence, " + str(cur_word_num) + " words, " + str(cur_oov_num) + " OOVs")
            f.write("\n")
            f.write("lgprob=" + str(truncate(cur_lgprob_sum)) + " ppl=" + str(cur_ppl))
            f.write("\n\n\n\n")
        count = word_num + sent_num - oov_num
        ppl = truncate(pow(10, (-lgprob_sum)/count))
        f.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        f.write("\n")
        f.write("sent_num=" + str(len(data)) + " word_num=" + str(word_num) + " oov_num=" + str(oov_num))
        f.write("\n")
        f.write("lgprob=" + str(truncate(lgprob_sum)) + " ave_lgprobsum=" + str(truncate(lgprob_sum/count)) + " ppl=" + str(ppl))
        f.write("\n")    