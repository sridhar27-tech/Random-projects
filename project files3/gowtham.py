import re
from collections import Counter

# Load and build word frequency model
def words(text):
    return re.findall(r'\w+', text.lower())

# Download or place a big English corpus file here (big.txt)
with open('big.txt', 'r', encoding='utf-8') as f:
    WORDS = Counter(words(f.read()))

def P(word, N=sum(WORDS.values())):
    """Probability of `word`."""
    return WORDS[word] / N

def correction(word):
    """Most probable spelling correction for word."""
    return max(candidates(word), key=P)

def candidates(word):
    """Generate possible spelling corrections for word."""
    return (known([word]) or 
            known(edits1(word)) or 
            known(edits2(word)) or 
            [word])

def known(words):
    """The subset of `words` that appear in the dictionary."""
    return set(w for w in words if w in WORDS)

def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# ====================== Usage ======================

if __name__ == "__main__":
    print("Auto Correct Demo")
    while True:
        word = input("\nEnter a word (or 'quit' to exit): ").strip().lower()
        if word == 'quit':
            break
        if not word:
            continue
        corrected = correction(word)
        print(f"Original : {word}")
        print(f"Corrected: {corrected}")
        
        # Show top 5 candidates with probability
        cands = list(candidates(word))
        print("Top suggestions:", sorted(cands, key=P, reverse=True)[:5])