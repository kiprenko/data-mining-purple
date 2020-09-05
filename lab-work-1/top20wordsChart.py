import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    with open("spam-words.json") as file:
        spam_words = json.load(file)
    frequent_spam_words_stat = spam_words[0:20]
    frequent_spam_words = [word[0] for word in frequent_spam_words_stat]
    frequent_spam_counts = [word[1] for word in frequent_spam_words_stat]

    ypos = np.arange(len(frequent_spam_words))
    plt.yticks(ypos, frequent_spam_words)
    plt.xlabel('words')
    plt.ylabel('count')
    plt.title('Top 20 spam words')
    plt.barh(ypos, frequent_spam_counts)
    plt.show()
