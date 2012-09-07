from collections import Counter
from collections import defaultdict
import pickle
import random
import re
import sys


def process_genres():
    """Collect genre information. Be sure to run util.get_songs() first."""

    with open('gm_songs.p', 'rb') as f:
        songs = pickle.load(f)

    print len(songs), " songs found."

    genres = (s.get('genre') for s in songs)

    #Data cleaning: remove nulls and lowercase everything
    genres = (g.lower() for g in genres if g is not None)

    #Create clusters.
    #We also store a set of the words mapped onto the original genre,
    # for interpretation later.

    word_occurances = Counter()
    words_to_genres = defaultdict(list)  # frozenset -> list of genres

    for g in genres:
        words = frozenset(re.findall(r'\w+', g))  # matches only alpha
        words_to_genres[words].append(g)
        word_occurances.update(words)

    word_clusters = defaultdict(set)  # word -> set of genres with this word
    for words, genres in words_to_genres.iteritems():
        for word in words:
            word_clusters[word].update(genres)

    #Show results.
    words = word_occurances.most_common()
    print "most common words:"
    for word, occurances in words[:5]:
        visualize(word, occurances, word_clusters[word])

    print
    print "---"
    print

    print "least common words:"
    for word, occurances in words[:-6:-1]:
        visualize(word, occurances, word_clusters[word])


def visualize(word, occurances, genres):
    print "'{}' found {} times".format(word, occurances)
    print "    %s distinct genre(s) with this word" % len(genres)

    if len(genres) > 1:
        print "    sample of genres: ",
        for sample_genre in random.sample(genres,
                                          min(len(genres), 3)):
            print "'%s'" % sample_genre,
        print

    print


def display_usage():
    print """usage:
    python {0} download   - download data from Google Music (run this first)
    python {0} analyze    - display information on data""".format(sys.argv[0])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        display_usage()
        exit()

    if sys.argv[1] == 'download':
        import util  # defer, since it depends on gmusicapi
        util.get_songs()
    elif sys.argv[1] == 'analyze':
        process_genres()
    else:
        display_usage()
