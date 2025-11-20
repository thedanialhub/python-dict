# dictionary.py

dictionary = [
    {
        "word": "example",
        "definition": "something that serves as a model",
        "pronunciation": "ɪɡˈzæmpəl"
    },
    {
        "word": "computer",
        "definition": "an electronic device for storing and processing data",
        "pronunciation": "kəmˈpjuːtər"
    },
    {
        "word": "programming",
        "definition": "the process of writing computer programs",
        "pronunciation": "ˈproʊɡræmɪŋ"
    }
]

# Example usage
if __name__ == "__main__":
    for entry in dictionary:
        print(f"{entry['word']} [{entry['pronunciation']}]: {entry['definition']}")