import string

def clean_text(text):
    text = text.lower()
    for punct in string.punctuation:
        text = text.replace(punct, '')
    return text

def count_words(text):
    words = text.split()
    return len(words)

def count_characters(text):
    return len(text)

def word_frequencies(text):
    words = text.split()
    frequencies = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies

def most_common_words(freqs, n=5):
    return sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:n]

def print_report(text):
    print("=== Text Analysis Report ===")
    cleaned = clean_text(text)
    print(f"Total words: {count_words(cleaned)}")
    print(f"Total characters: {count_characters(text)}")
    freqs = word_frequencies(cleaned)
    print("Most common words:")
    for word, freq in most_common_words(freqs):
        print(f"{word}: {freq}")

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    path = input("Enter the path to the text file: ")
    try:
        content = read_file(path)
        print_report(content)
    except FileNotFoundError:
        print("File not found. Please check the path.")

if __name__ == "__main__":
    main()
