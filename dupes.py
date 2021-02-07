#!/usr/bin/env python3


# tip: to compare this against fdupes, try:
#
# # set up some test data
# python -m virtualenv venv1
# python -m virtualenv venv2
# . venv1/bin/activate
# pip install requests dcm2bids
#  deactivate 
# . venv2/bin/activate
#  pip install dcm2bids future
# deactivate
#
# # symlinks too:
# mkdir links
# echo wtf > lol
# ln -s ../lol links/a
# ln -s ../lol links/b

# Then try:
# diff -ru <(fdupes -r . | sort | sed '/^$/d')  <(./dupes.py . | sort |  sed '/^$/d')

import os
import sys
import hashlib

# external requirements:
from tqdm import tqdm

def checksum(p, hash=hashlib.sha256):
    # TODO: should the checksum include the filesize?
    if p not in checksum._cache:
        # memoize
        H = hash()
        if os.path.isdir(p):
            # directory: do a tree hash
            H.update(b".") # ??? this is to make sure the hash of the empty dir != the hash of the empty file
            for f in os.listdir(p):
                path = os.path.join(p,f)
                if not (os.path.isdir(path) or os.path.isfile(path)): continue # skip non-regular files
                if os.path.islink(path): continue # make this like fdupes, which silently ignores symlinks (as symlinks)
                 # TODO: this bit of code clearly should be overlapping with the code under os.walk()


                # ack this is a stupid bug:
                #./.git/objects/info
                #./.git/refs/heads
                #./.git/refs/tags
                #./links
                #./.git/objects/pack
                #./.git/branches

                # ie *because* links only contains symlinks, the checksum considers it empty
                # this is a problem fdupes doesn't have, because it never tries to compare directories
                # hmmmm
                # probably the same applies for non device files too
                # device files are...never equal to anything else, let's say
                # which is easy enough to declare
                # but then how do you program around that?

                H.update(f.encode('utf-8')+b":"+checksum(path))
        elif os.path.islink(p):
            raise TypeError(f'{p} is a symlink') # :?????
            b = os.readlink(p).encode('utf-8') #? ???
            H.update(b)
        elif os.path.isfile(p):
            # file

            # TODO: I wonder if it would be faster to use md5sum(1), sha256sum(1), sha256(1), etc, which are C programs, instead of hashing in python
            BLOCK_SIZE = 65536
            with open(p, 'rb') as f:
                while True:
                    b = f.read(BLOCK_SIZE)
                    if not b: break
                    H.update(b)
        else:
            raise TypeError(f'{p} is not a regular file or directory')                    
        checksum._cache[p] = H.digest()
    return checksum._cache[p]
checksum._cache = {} # cache of checksums; I know I could use @functools.lru_cache or write my own @memoize but I want to be explicit for now so I can see all the parts


def dupes(*dirs, followlinks=False):
    
    # first pass: compute list of targets to hash
    # the reason for a separate pass is to let us give a progress bar
    targets = []
    for dir in dirs:
        # TODO: handle onerror=?
        if not os.path.isdir(dir):
            raise ValueError(f'{dir} is not a directory') # XXX??? why doesn't os.walk() error on this?
        for (path, dirs, files) in os.walk(dir, topdown=False, followlinks=followlinks):
            for p in [os.path.join(path, e) for e in files] + [path]:
                #print("Walking:", p) # DEBUG
                #if os.path.isdir(p): continue # DEBUG: make this like fdupes
                if os.path.islink(p): continue # make this like fdupes, which silently ignores symlinks (as symlinks)
                targets.append(p)

    # second pass: compute checksum of every file and group files by their checksums
    # note: this relies on topdown=False (above!) + memoization inside of checksum() to ensure checksums are computed bottom-up
    D = {} # contains sets of duplicates, each such that f in D[checksum(f)] for all f, and each f is *only in one* set
    for p in tqdm(targets):
        if checksum(p) not in D:
            D[checksum(p)] = set()
        D[checksum(p)].add(p)
    # uhhh now I need to invert the dataset?
    # in fact we can throw away the keys here
    D = {frozenset(S) for S in D.values()}
    #D = list(D.values())

    # filter out non-dupes
    D = {S for S in D if len(S) > 1}

    # okay now go through the sets in D and confirm the matches by using diff
    # compare [`int confirmmatch(FILE *file1, FILE *file2)`](https://github.com/adrianlopezroche/fdupes/blob/2209aff509bd15e8641cb9ae3c9bbb8056f7dd7b/fdupes.c#L690)
    # TODO:
    # for S in D:
    # go through the set S and produce multiple sets, one for each equivalence class
    # Ss = []
    # what's the best way to do this? uh, compare everything to f, the first 
    #   for f in S: # <-- this can be made more efficient by only doing the upper triangle
    #     matches = set()
    #     for g in S:
    #       if subprocess.run(['diff','-r',f,g]).returncode == 0: # identical, good
    #         S.remove(g); matches.add(g)
    #     Ss.append(matches)
    # something like that anyway
    # you could do the same but with S == all files, but it would be slower because you'd be byte-for-byte comparing 
    # except... in the case where you mostly only have two dupes of everything

    # make an index by path
    I = {}
    for S in D:
        for p in S:
            I[p] = S

    # now: filter out children.
    # to do this efficiently I should reshape the dataset with an index first, probably
    # should I loop over parents and remove their children or loop over children and remove their parents?
    #
    # this is also sort of weird because I'm look at paths but removing entire sets? Is that going to work?
    #D = {I[p] for p in I if not any(isancestor(P, p) for P in I)} # <__ VERY SLOW
    # okay maybe for each, we can check if their *immediate* ancestor is in the list
    # aha, this worked!
    # but is that..right? this works because we walk the trees bottom-up, hashing as we go
    # what is this saying?
    # it's saying: if 
    # TODO: this should be able to be more efficient by considering 
    D = {I[p] for p in I if not os.path.dirname(p) in I}

    #print("dupes:")
    D = sorted([sorted(S) for S in D]) # ugh; i wonder if it's possible to achieve this just by the order of os.walk()? e.g. store things as lists?
    for S in D:
        for f in S:
            if os.path.isdir(f) and not f.endswith("/"): f+="/"
            print(f)
        print()


if __name__ == '__main__':
    dupes(*sys.argv[1:])
    


