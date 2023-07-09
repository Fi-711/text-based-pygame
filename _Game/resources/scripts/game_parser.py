import string

# List of "unimportant" words
skip_words = ['a', 'about', 'all', 'an', 'another', 'any', 'around', 'at',
              'bad', 'beautiful', 'been', 'better', 'big', 'can', 'choose', 'every', 'for',
              'from', 'good', 'guess', 'have', 'her', 'here', 'hers', 'his', 'how',
              'i', 'if', 'in', 'into', 'is', 'it', 'its', 'large', 'later',
              'like', 'little', 'main', 'me', 'mine', 'more', 'my', 'now',
              'of', 'off', 'oh', 'on', 'please', 'recogn', 'small', 'some', 'soon',
              'that', 'the', 'them', 'then', 'this', 'those', 'through', 'till', 'to',
              'towards', 'until', 'us', 'want', 'way', 'we', 'what', 'when', 'why',
              'wish', 'with', 'would', 'go', 'move', 'use', 'read', 'please', 'do', 'use']

# Filter superfluous words
def filter_words(words, skip_words):
    return [word for word in words if word not in skip_words]

# Normaliser input and return a string
def normalise_input(choice):
    return ' '.join(filter_words(choice.lower().strip().translate(choice.maketrans('', '', string.punctuation)).split(' '), skip_words))

    