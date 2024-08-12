
import sys
def mfw(x,n):
    try:
        with open(x, 'r') as f:
            f_words = f.read()
        f_words = str(f_words).split()

        word_count = {}

        for word in f_words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        sorted_word_count = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))


        for word, count in sorted_word_count.items():
            print(f"the word {word} is shown {count} times")
            n -= 1
            if n == 0:
                break
    except FileNotFoundError:
        print(f"File {x} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    

x=input("Enter the file name: ")
n = int(input("Enter the number of most frequent words: "))
print(mfw(x,n))
       
