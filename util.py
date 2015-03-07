from getpass import getpass
import json
import pickle

try:
    from gmusicapi import Mobileclient
except ImportError:
    print "You need gmusicapi to work with Google Music:"
    print "    pip install gmusicapi"
    exit()


class SetEncoder(json.JSONEncoder):
    """Json doesn't have a set; use a list when dumping."""

    def default(self, obj):
        if isinstance(obj, set) or isinstance(obj, frozenset):
            return list(obj)

        return json.JSONEncoder.default(self, obj)


def dump_to_json(**kwargs):
    """Given kwargs of (filename, object), dump object to filename.json."""
    for fn, obj in kwargs.items():
        with open(fn + '.json', 'wb') as f:
            f.write(json.dumps(obj, cls=SetEncoder))


def get_songs():
    """Run once to get all the user's songs."""
    api = init_api()
    songs = api.get_all_songs()
    with open('gm_songs.p', 'wb') as f:
        pickle.dump(songs, f)

    print "Library information downloaded to to gm_songs.p"


def init_api():
    """Makes an instance of the api and attempts to login with it.
    Returns the authenticated api."""

    api = Mobileclient()

    logged_in = False
    attempts = 0

    print "Please log in to Google Music. OTP users should use an",
    print "application specific password."

    while not logged_in and attempts < 3:
        email = raw_input("Email: ")
        password = getpass()

        logged_in = api.login(email, password)
        attempts += 1

    return api
