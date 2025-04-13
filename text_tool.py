import string

def preprocess_text(txt):
    # Convert to lowercase and remove punctuation
    txt = txt.lower()
    for ch in string.punctuation:
        txt = txt.replace(ch, '')
    return txt

def total_words(txt):
    return len(txt.split())

def total_chars(txt):
    return len(txt)

def compute_frequencies(txt):
    words = txt.split()
    freq_map = {}
    for w in words:
        if w in freq_map:
            freq_map[w] += 1
        else:
            freq_map[w] = 1
    return freq_map

def top_words(freqs, top_n=5):
    return sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top_n]

def display_summary(txt):
    print("*** Analysis Summary ***")
    processed = preprocess_text(txt)
    print(f"Words: {total_words(processed)}")
    print(f"Characters: {total_chars(txt)}")
    freq = compute_frequencies(processed)
    print("Top frequent words:")
    for word, count in top_words(freq):
        print(f"{word}: {count}")

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def run():
    file_input = input("Input file path: ")
    try:
        data = load_text(file_input)
        display_summary(data)
    except FileNotFoundError:
        print("Couldn't locate the file. Please verify the path.")

if __name__ == "__main__":
    run()
