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


# This is a tree-hash based implementation. It's a relatively simple extension from what fdupes does:
# https://github.com/adrianlopezroche/fdupes/blob/master/fdupes.c
# Basically, it hashes everything, *including folders themselves*, and uses that to sort content into buckets.
# Then it filters out all the non-duplicates, *and child duplicates*, and prints.
#
# There are some problems with the tree-hash:
# 1. it implies you need checksums computed for all files, even ones you wouldn't otherwise need to checksum
#    - worked around with a clever hack, but it's definitely a hack
# 2. the diff(1) step ends up re-diffing subtrees
# 3. it doesn't handle non-files (i.e. sockets, fifos, block devices, symlinks)
#    - I hacked in symlink support, but the others are trickier
#    - fdupes doesn't handle symlinks either it turns out! it completely ignores them!
#
# I think it should be possible to replace the tree hash with a dynamic program.
# That is, cleverly work upwards from the leaves to construct equivalence classes of directories.
# That should make it easier to handle non-regular-files and it will definitely avoid needing to run `diff -r`.

import os
import sys
import binascii
import hashlib
import subprocess

# external requirements:
from tqdm import tqdm

def checksum(p, hash=hashlib.md5):
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

                H.update(os.fsencode(f)+b":"+checksum(path))
        elif os.path.islink(p):
            raise TypeError(f'{p} is a symlink') # :?????
            b = os.fsencode(os.readlink(p)) #? ???
            H.update(b)
        elif os.path.isfile(p):
            # file

            # TODO: I wonder if it would be faster to use md5sum(1), sha256sum(1), sha256(1), etc, which are C programs, instead of hashing in python
            #checksum._cache[p] = binascii.unhexlify(subprocess.check_output(['sha256sum', '-b', p]).split()[0])
            #return checksum._cache[p]
            # huh, it was actually faster to do the in-python version
            # 

            #print(f"checksumming {p}") # DEBUG #TODO: logging.info()

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


def diff(p1, p2):
    "return True if paths p1 and p2 differ, false otherwise"

    #print(['diff','-r',p1,p2]) # TODO: logging.info()
    # ..wait
    r = subprocess.run(['diff','-r',p1,p2], stdout=subprocess.DEVNULL).returncode
    if r == 0:
        return False
    if r == 1:
        return True
    else:
        # NB: this intentionally doesn't capture stderr; so that actual errors are reported.
        raise Exception('diff failed')        

    #TODO: fallback to internal diff if diff isn't available

def dupes(*dirs, followlinks=False):
    """
    Print


    # TODO: make this return instead of print directly
    """

    # We have a set of sets -- a set of partitions.
    # Everything starts out in a single partition and we progressively split it up
    # each step using a more precise -- and more computationally expensive -- operation.
    # by trading off this way the expensive operations only run a small number of times.

    # The steps are:
    # 1. file size
    # 2. checksum (md5, or sha256, or something else, but tbh in this application md5 is *better* because it's faster)
    # 3. diff

    # between each step non-duplicates, which are the vast majority of data in most cases, are forgotten so they don't slow down the next steps.

    # pass 0: get the complete set of targets to consider
    partitions = {}
    partitions[()] = set() # notice: initialized with the null tuple as a key, just to make the recursivey bits below nicer
    for dir in dirs:
        # TODO: handle onerror=?
        if not os.path.isdir(dir):
            raise ValueError(f'{dir} is not a directory') # XXX??? why doesn't os.walk() error on this?
        for (path, dirs, files) in os.walk(dir, topdown=False, followlinks=followlinks):
            for p in [os.path.join(path, e) for e in files] + [path]:
                #print("Walking:", p) # DEBUG
                #if os.path.isdir(p): continue # DEBUG: make this like fdupes
                if os.path.islink(p): continue # make this like fdupes, which silently ignores symlinks (as symlinks)
                partitions[()].add(p)

    # pass 1: partition by size
    _partitions = {}
    for K,partition in partitions.items():
        for p in partition:
            size = os.stat(p).st_size # subtlety: this *does* work on directories, and always returns the same size; at least on linux?
              # if it didn't, then dirs need to be special-cased here
            _partitions.setdefault(K + (size,), set())
            _partitions[K + (size,)].add(p)

    partitions = _partitions # forget the previous level
    for partition in partitions.values():
        if len(partition) == 1:
            # uhhhh hack?
            # make up fake, but probably distinct, checksums for the non-dupe files
            # in order to allow *directory* checksumming to behave itself
            # even if there is a collision here pass 3 will double-check this work.
            checksum._cache[list(partition)[0]] = os.urandom(32)
    partitions = {k: v for k,v in partitions.items() if len(v) > 1} # forget non-dupes

    # pass 2: partition by checksum
    _partitions = {}
    for K,partition in partitions.items():
        for p in partition:
            c = checksum(p)
            _partitions.setdefault(K + (c,), set())
            _partitions[K + (c,)].add(p)

    partitions = _partitions # forget the previous level
    partitions = {k: v for k,v in partitions.items() if len(v) > 1} # forget non-dupes

    # pass 3: partition by diff
    # this could be optional; even md5 is safe against accidental collisions and sha256 certainly is;
    # it's only if you don't trust your storage that you really need this.
    _partitions = {}
    for K,partition in partitions.items():
        # this is trickier because we don't have anything to key on
        # we just have to compare files pairwise and see what's what
        # we can do a littttle bit better than that though

        # this loop is awkward; I *want* to loop over a set, *shrinking* it as I go
        # but that's illegal in python. so instead I use a : continue
        # maybe it would be better to simply write it with indecies?
        subpartitions = []
        _partition = list(partition)
        for i,p in enumerate(_partition):
            if p not in partition: continue # skip if already decided
            subpartitions.append(set())

            subpartitions[-1].add(p)
            partition.remove(p)
            for j,p2 in enumerate(_partition[i+1:]):
                if p2 not in partition: continue
                if not diff(p,p2): # hmmm will this do redundant work? will it re-diff things we've already diffed?
                    subpartitions[-1].add(p2)
                    partition.remove(p2) # ???
                    # and scratch p and p2 off the list
        assert not partition, "Partition must be empty, but instead was {p}"

        for i,S in enumerate(subpartitions):
            _partitions[K + (i,)] = S

    partitions = _partitions # forget the previous level
    partitions = {k: v for k,v in partitions.items() if len(v) > 1} # forget non-dupes

    # at this point, each partitions[size, checksum, i] are sets of paths, of 'equivalence classes'
    # members of those sets are paths with identical content

    # invert the dataset: throw away the index we partitioned by
    partitions = {frozenset(S) for S in partitions.values()}

    # now: filter out children when their parents are known to be duplicates,
    # to make the output less overwhelming.
    # to help, re-index by paths
    I = {}
    for S in partitions:
        for p in S:
            I[p] = S
    # then drop children by check if their *immediate* ancestor is a duplicate
    # but is that..right? this works because we walk the trees bottom-up, hashing as we go
    # this is weird because we're including a complete partition from a single
    # we have to collapse the redundancies back down with set() here :/
    # TODO: can this be more efficient by looping over the partitions directly?
    #       maybe. there should be some invariant here like "if {'p/A', 'q/A'} is a partition, 'p/' is in a partition iff {'p/','q/'} is a partition"
    #              so that we only need to check a single element in each partition to know what to do
    partitions = {I[p] for p in I if not os.path.dirname(p) in I}

    # sort output
    # ugh; i wonder if it's possible to achieve this by writing the whole algorithm with lists instead of sets
    # and by being careful about how I use os.walk()?
    # sorting after the fact is annoying
    # it's not especially slow but it's not ideal either
    partitions = sorted([sorted(S) for S in partitions])

    for S in partitions:
        for f in S:
            if os.path.isdir(f) and not f.endswith("/"): f+="/"
            print(f)
        print()


if __name__ == '__main__':
    dupes(*sys.argv[1:])
    


