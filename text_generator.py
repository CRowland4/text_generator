import random
import nltk
from nltk.util import trigrams


class TextGenerator:
    def __init__(self):
        self.file_content = ''
        self.tokenized_content = []
        self.bigrams = []
        self.heads_and_tails = {
            # head: {
            # tail_1: <frequency>
            # tail_2: <frequency>
        # }
        }

    def main_call(self):
        self._set_file_content()
        self._set_tokenized_content()
        self._set_bigrams()
        self._set_heads_and_tails()
        self._generate_sentences(10)

    def _set_file_content(self) -> None:
        """Sets the file_content attribute from the file entered by the user."""
        file_name = input("Give the filename (plus extension) of the corpus you would like to generate sentences from: ")
        with open(file_name, 'r', encoding='utf-8') as corpus:
            self.file_content = corpus.read()

        return

    def _set_tokenized_content(self) -> None:
        """Sets the tokenized_content attribute from the file_content attribute."""
        tokenizer = nltk.tokenize.WhitespaceTokenizer()
        self.tokenized_content = tokenizer.tokenize(self.file_content)
        return

    def _set_bigrams(self):
        """Sets the bigrams attribute from the tokenized_content attribute."""
        initial_trigrams = trigrams(self.tokenized_content)
        bigrams = []

        for trigram in initial_trigrams:
            bigram_head = trigram[0] + ' ' + trigram[1]
            bigram_tail = trigram[2]
            bigram = [bigram_head, bigram_tail]
            bigrams.append(bigram)

        self.bigrams = bigrams
        return

    def _set_heads_and_tails(self):
        """Sets the heads_and_tails attribute using the list of bigrams."""
        for bigram in self.bigrams:
            self.heads_and_tails.setdefault(bigram[0], {})
            self.heads_and_tails[bigram[0]].setdefault(bigram[1], 0)
            self.heads_and_tails[bigram[0]][bigram[1]] += 1

        return

    def _generate_sentences(self, count):
        """Generates <count> lines, each with <length> words."""
        for _ in range(count):
            sentence = self._generate_sentence()
            print(' '.join(sentence))

        return

    def _generate_sentence(self) -> list:
        """Generates one sentence."""
        head = self._appropriate_head()
        line = head.split()
        length = len(line)
        while True:
            tail = self._appropriate_tail(length, head)

            if tail == 'restart sentence':
                return self._generate_sentence()

            line.append(tail)
            length = len(line)

            if self._ends_with_punctuation(tail):
                return line
            else:
                head = line[-2] + ' ' + line[-1]

    def _appropriate_tail(self, line_length, head) -> str:
        """Returns a tail that either ends a chain or continues it, depending on the index."""
        tails = [tail for tail in self.heads_and_tails[head].keys()]
        weights = [self.heads_and_tails[head][tail] for tail in tails]

        while True:
            tail = random.choices(tails, weights=weights)  # Note to self: This is a list with one element, NOT a string

            if line_length < 5 and all([self._ends_with_punctuation(tail) for tail in tails]):
                # This prevents the situation where the line is shorter than 5 words, but every tail in tails
                # ends with a punctuation mark.
                return 'restart sentence'

            if line_length < 5 and self._ends_with_punctuation(tail[0]):
                continue

            return tail[0]

    def _appropriate_head(self) -> str:
        """Returns a random, capitalized token word from the tokenized_content attribute."""
        head = random.choice(list(self.heads_and_tails.keys()))
        if all([head[0] == head[0].capitalize(), not self._ends_with_punctuation(head.split()[0]), head[0].isalpha()]):
            return head
        else:
            return self._appropriate_head()

    def _ends_with_punctuation(self, token) -> bool:
        """Determines if the passed token ends with a punctuation mark."""
        if token[-1] in ['.', '!', '?']:
            return True

        return False


stage = TextGenerator()
stage.main_call()
