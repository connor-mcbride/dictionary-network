import json
import pickle
from collections import defaultdict
import networkx as nx


def create_graph(input, output):
    # Load in dictionary json file as dict
    with open(input, 'r') as f:
        data = json.load(f)

    G = nx.DiGraph()

    # Add in defined words as nodes
    for word, _ in data.items():
        G.add_node(word)

    # Add edges only to words that are defined
    for word, definition in data.items():
        word_counts = defaultdict(int)

        for word_def in definition.split(" "):
            # Remove extraneous punctuation or newlines
            cleaned_word = word_def.lower().strip(r".,!?:;()[]{}<>\\\"'\n")

            # Only add word in definition if the word itself is defined
            if cleaned_word in G.nodes:
                # Number of times word appears in dictionary becomes weight
                word_counts[cleaned_word] += 1

        for word_found in word_counts:
            G.add_edge(word, word_found, weight=word_counts[word_found])

    # Pickle dictionary network
    with open(output, "wb") as f:
        pickle.dump(G, f)


if __name__ == "__main__":
    create_graph("data/dictionary.json", "data/dictionary.pickle")