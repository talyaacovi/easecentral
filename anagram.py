def anagram_lists(wordlist):
    """Given list of words, returns groups of words that are anagrams"""

    results = []
    count = {}

    # for each word, split it into a list and join it to create a key.
    for word in wordlist:
    	key = ''.join(sorted(list(word)))

        # if the key already exists in the dictionary, append the word to the value stored at that key.
    	if count.get(key):
    		count[key].append(word)

        # if the key doesn't exist, add it with the value of an array with the current word.
    	else:
    		count[key] = [word]

    # for each key in the dictionary, check if the number of words stored is greater than 1.
    # if it is, print the words listed in the array at that key in a string with each
    # word separated by commas.
    for key in count:
    	if len(count[key]) > 1:
    		print ', '.join(count[key])

all_words = [w.strip() for w in open('words.txt')]

anagram_lists(all_words)