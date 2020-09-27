import logging
import json
import pickle
with open("codeitsuisse/routes/tree.pkl", 'rb') as f:
    word_dict = pickle.load(f)
    f.close()

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/slsm', methods=['POST'])
def evaluate_scribe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results = []
    for i in data:
        output = scribe(i.get("encryptedText"))
        output = {
            "id":i.get("id"),
            "encryptionCount": output[0],
            "originalText": output[1]}
        results.append(output)
    logging.info("My result :{}".format(results))
    return jsonify(results)


def decipher(shift, msg):
    shift = shift%26
    out = ""
    for char in msg:
        char_val = ord(char)
        correction = 65 if char.isupper() else 97
        char_val -= correction
        char_val -= shift
        char_val = 26+char_val if char_val<0 else char_val

        out += chr(char_val + correction)
    return out

def cipher(shift, msg):
    shift = shift%26
    out = ""
    for char in msg:
        char_val = ord(char)
        correction = 65 if char.isupper() else 97
        char_val -= correction
        char_val += shift
        char_val %= 26

        out += chr(char_val + correction)
    return out

def palins(word):
    palins = []
    longest = [0, 0]
    i=0
    while i<len(word)-1:
        if word[i] == word [i+1]:
            left = i
            right = i+1
        elif word[i-1] == word[i+1]:
            left = i-1
            right = i+1
        else:
            i += 1
            continue
        # record first palindeome along with length
        plen = (right-left+1)
        if (plen)>2:
            palins.append((plen, left, right))
            if (plen)>longest[0]:
                longest[0] = plen
                longest[1] = len(palins)-1
        # start finding palindrome
        while (left>0 and right<len(word)-1):
            if (word[left-1] == word[right+1]):
                left -= 1
                right += 1
                plen = (right-left+1)
                palins.append((plen, left, right))
                if plen>longest[0]:
                    longest[0] = plen
                    longest[1] = len(palins)-1
            else:
                break
        i = right + 1
    return palins, longest

def to_words(msg):
    score = 0
    words = []
    prev_word = ["", (-1, -1)]
    no_words = True
    sub_tree = word_dict
    at_root = True
    c = 0
    word_start = 0
    while (c<len(msg)):
        char = msg[c]
        if c==5 and (at_root and no_words):
            break

        if sub_tree.get(char) is None:
            # overide the prev word if possible
            if sub_tree.get('words') is not None:
                prev_word[0] = sub_tree['words'][0]
                prev_word[1] = (word_start, c-1)
                no_words = False
            
            if prev_word[0] != "":
                words.append(prev_word)
                word_start = prev_word[1][1]+1
                c = word_start
                prev_word = ["", (-1, -1)]
            else:
                word_start += 1
                c = word_start
                score -= 1
            sub_tree = word_dict
            at_base = True
            
        else:
            if sub_tree.get('words') is not None:
                prev_word[0] = sub_tree['words'][0]
                prev_word[1] = (word_start, c-1)
                no_words = False

            sub_tree = sub_tree[char]
            c += 1
    score += len(words)
    if words != []:
        return score, words
    else:
        return None
            

def scribe(msg):
    key = 0
    best_words = None
    for i in range(0, 26):
        check = decipher(i, msg)
        words = to_words(check)
        if words == None:
            continue
        else:
            if best_words is None:
                best_words = words
                key = i
            elif words[0] > best_words[0]:
                best_words = words
                key = i
    
    enc = msg
    msg = decipher(key, msg)
    count = 0
    while msg[0] != enc[0] and count<26:
        pals = palins(msg)
        longest = sorted(pals[0])[-1]
        longest = msg[longest[1]:longest[2]+1]
        shift = sum([ord(i) for i in longest]) + len(pals[0])
        if shift == 0:
            break
        msg = cipher(shift, msg)
        count += 1
    best_words = [i[0] for i in best_words[1]]
    if len(msg) == len(''.join(best_words)):
        return count, ' '.join(best_words)
    else:
        return count, decipher(key, enc)