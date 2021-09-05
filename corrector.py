import re
import numpy as np

def min_edit_dis(target, source):
    target = [i for i in target]
    source = [k for k in source]
    matrix = np.zeros((len(source), len(target)))

    matrix[0] = [i for i in range(len(target))]
    matrix[:,0] = [j for j in range(len(source))]

    if target[1] != source[1]:
        matrix[1,1] = 1
    
    for column in range(1, len(target)):
        for row in range(1, len(source)):
            if target[column] != source[row]:
                matrix[row, column] = min(matrix[row-1, column], matrix[row, column -1], matrix[row-1, column -1]) + 1
            else:
                matrix[row, column] = matrix[row-1, column -1]
    return matrix[-1, -1]

def checks_word_in_dict(word, dict):
    return word in dict.split() or word.lower() in dict.split() or word.isnumeric()

def return_new_word(word, punc1, punc2, final_list):
    new_word = punc1 + word + punc2
    final_list.append(new_word)

with open("austen-sense-corrupted.txt", "r") as f:
    para = f.read()
    split = para.split()

with open("dict.txt", "r") as f:
    dict= f.read()

punc_word_list = []

for word in split:
    if checks_word_in_dict(word, dict):
        punc_word_list.append(word)
    
    else:
        punc_word = re.finditer(r'(\W?)(\w+[-]?\w+)(\W?)', word)

        for word in punc_word:
            dict_count = {}
            punc1, capture_word, punc2 = word.group(1), word.group(2), word.group(3)

            if checks_word_in_dict(capture_word, dict):
                return_new_word(capture_word, punc1, punc2, punc_word_list)
    
            else: 
                capitalised = False

                if capture_word[0].isupper():
                    capitalised = True

                for dict_word in dict.split():
                    dict_count[dict_word] = min_edit_dis(('#' + dict_word), ('#' + capture_word))
                    
                minimum_count = min(dict_count.values())
                key = [k for k in dict_count if dict_count[k] == minimum_count]

                if capitalised: 
                    key[0] = key[0].capitalize()
                return_new_word(key[0], punc1, punc2, punc_word_list)
        
print('LIST', ' '.join(punc_word_list))

    





