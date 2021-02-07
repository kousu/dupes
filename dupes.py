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

import sys
import os, stat
from itertools import count
import binascii
import hashlib
import subprocess

# external requirements:
from tqdm import tqdm

def filetype(p):
    """
    return the filetype of a path:

    - for regular files
    d for directories
    l for symlinks
    b or c for block or character devices
    p for pipes
    s for sockets

    etc
    """
    return stat.filemode(os.stat(p).st_mode)[0]

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

def _internal_diff(p1, p2):

    # this seems to be about 30% faster than shelling out to diff
    if os.path.isdir(p1) and os.path.isdir(p2):
        return False # because probably

    CHUNK_SIZE = 8129
    with open(p1,'rb') as fd1, open(p2,'rb') as fd2:
        while True:
            r1 = fd1.read(CHUNK_SIZE)
            r2 = fd2.read(CHUNK_SIZE)
            if r1 != r2:
                return False
                # uhhh hang on this isn't right
            if not r2: break
        return True

#diff = _internal_diff

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
    # 1. file type
    # 1. file size
    # 2. checksum (md5, or sha256, or something else, but tbh in this application md5 is *better* because it's faster)
    #    - some file types don't have checksums. for these, we make something up.
    # 3. diff

    # between each step non-duplicates, which are the vast majority of data in most cases, are forgotten so they don't slow down the next steps.

    # TODO:
    #  i can probably get a progress bar out of this if i rewrite it so that
    #  instead of handling itself step by step
    #  it's a single loop over all the targets
    #  and they do each step within themselves
    #  CATCH: I *must* do directories in a separate block *after* everything else
    #   ...well maybe not. maybe I can do something like... 
    #   1. make sure to process directories after their contents [x]
    #   2. in checksum(), *look at the overall table* instead of memoizing locally;
    #      this allows us to decide  sneak in something that sneak in a preprocessing step
    #    -> no no no this doesn't work becaaaaaause we don't know if the checksum is needed until we do the entire set of files
    #   because I need to be able to detect isolated files and fill in random checksums for them.
    #   because their checksums need tok happen

    # pass 0: get the complete set of targets to consider
    import time; t0=time.time()
    partitions = {}
    files = set() # notice: initialized with the null tuple as a key, just to make the recursivey bits below nicer
    folders = set()
    for dir in dirs:
        # TODO: handle onerror=?
        if not os.path.isdir(dir):
            raise ValueError(f'{dir} is not a directory') # XXX??? why doesn't os.walk() error on this?
        for (path, dirs, items) in os.walk(dir, topdown=False, followlinks=followlinks):
            folders.add(path)
            for p in [os.path.join(path, e) for e in items]:
                #print("Walking:", p) # DEBUG
                #if os.path.isdir(p): continue # DEBUG: make this like fdupes
                if os.path.islink(p): continue # make this like fdupes, which silently ignores symlinks (as symlinks)
                files.add(p)
    print(f'pass 0: {time.time() - t0:.2f}s')

    # wahhh
    # okay so the ordering is kind of crazed because:
    # - with topdown=False, the *first result* is Music/rave, *because* that's an empty folder in the top level folder
    #   so the thing recurses down into it and produces it *as path/*
    # - then that becomes the first thing in the set
    # - then that means the first *bucket* is ('d', '4096', )
    #   which means *all the folders* end up coming before all the files
    # ..fuck.

    # attempted rewrite to do a single pass over all the files
    # but this can't be a totally single pass because i have to do the dirs in a second pass

    # bah
    # maybe I should keep a second dict just for the deferred checksum
    # the main dict is always keyed (t,s,c,i), and there's *always* (which we enforce
    deferred_checksums = {}
    for p in tqdm(files, "files"):
        t = filetype(p)
        s = os.stat(p).st_size

        # optimization: defer checksumming until we have at least a second file to compare with
        #  this saves a huge amount of time by avoiding checksumming all the files we can tell are unique just from their size
        if (t,s) not in deferred_checksums:
            # first t,s we've seen, just put it aside for now
            # then then *skip forward*
            deferred_checksums[t,s] = p
            continue
        elif deferred_checksums[t,s]:
            # not the first;
            # unpack the deferred checksum and use it to initialize the bucket
            q = deferred_checksums[t,s]

            c = checksum(q)
            partitions[t,s,c,0] = {q}
            deferred_checksums[t,s] = None # mark it finished
        else:
            # already finished;
            pass

        c = checksum(p)

        # run diff to confirm the match or not
        # (this is sort of weird because I'm indexing by integer for the last field of a tuple in a dict;
        #  it might be more obvious to nest a list instead but then the syntax isn't as nicely symmetrical)
        for i in count():
            #print("searching",t,s,c,i)
            if (t,s,c,i) in partitions:
                q = next(iter(partitions[t,s,c,i])) # compare against the first entry of each bucket; there's no need to check all of them
                #print("\t diff",q,p)
                if not diff(q, p):
                    #print("ACCEPTING",i)
                    break
            else:
                # no match, we must be a new group
                break

        # print(t,s,c,i) # DEBUG
        partitions.setdefault((t,s,c,i), set())
        partitions[t,s,c,i].add(p)

    # move the leftovers from deferred_checksum into partitions
    for K, p in tqdm(deferred_checksums.items(), "singletons"):
        if p is None: continue # skip it!
        t, s = K
        # clever hack:
        # Rather than checksumming all the leftover singletons (which we already *know* are singletons)
        # make up fake checksums for them. this is enough to allow *directory* checksumming to behave itself.
        c = os.urandom(32)
        assert p not in checksum._cache
        checksum._cache[p] = c
        # we know there are no other files with (t,s, ..) in their bucket key
        # so we can assume we're the first
        partitions[t, s, c, 0] = {p}
        deferred_checksums[t,s] = None

    # pass 2: bucket directories
    import time; t0=time.time()
    for p in folders:
        t = filetype(p)
        s = os.stat(p).st_size
        c = checksum(p)
        i = 0 # ?
        partitions.setdefault((t,s,c,i), set())
        partitions[t,s,c,i].add(p)
    print(f'pass 2: {time.time() - t0:.2f}s')

    # at this point, each partitions[type, size, checksum, i] are sets of paths, of 'equivalence classes'
    # members of those sets are paths with identical content; and each path can be files or dirs.

    # pass 3: filter out singletons
    partitions = {k: v for k,v in tqdm(partitions.items(), "singletons (again)") if len(v) > 1} # forget non-dupes

    # invert the dataset: throw away the index we partitioned by
    import time; t0=time.time()
    partitions = {frozenset(S) for S in tqdm(partitions.values(), "partitions")}
    print(f'dropping bucket index: {time.time() - t0:.2f}s')

    # now: filter out children when their parents are known to be duplicates,
    # to make the output less overwhelming.
    # to help, re-index by paths
    import time; t0=time.time()
    I = {}
    for S in tqdm(partitions, "partitions"):
        for p in S:
            I[p] = S
    print(f'reindexing: {time.time() - t0:.2f}s')

    # then drop children by check if their *immediate* ancestor is a duplicate
    # but is that..right? this works because we walk the trees bottom-up, hashing as we go
    # this is weird because we're including a complete partition from a single
    # we have to collapse the redundancies back down with set() here :/
    # TODO: can this be more efficient by looping over the partitions directly?
    #       maybe. there should be some invariant here like "if {'p/A', 'q/A'} is a partition, 'p/' is in a partition iff {'p/','q/'} is a partition"
    #              so that we only need to check a single element in each partition to know what to do
    # XXX this part is so weiiiird! I want a second pair of eyes on it.
    import time; t0=time.time()
    partitions = {I[p] for p in tqdm(I, "paths") if not os.path.dirname(p) in I}
    print(f'dropping children: {time.time() - t0:.2f}s')

    # sort output
    # ugh; i wonder if it's possible to achieve this by writing the whole algorithm with lists instead of sets
    # and by being careful about how I use os.walk()?
    # sorting after the fact is annoying
    # it's not especially slow but it's not ideal either
    import time; t0=time.time()
    partitions = sorted([sorted(S) for S in tqdm(partitions, "sorting")])
    print(f'sorting: {time.time() - t0:.2f}s')

    for S in partitions:
        for f in S:
            if os.path.isdir(f) and not f.endswith("/"): f+="/"
            print(f)
        print()


def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    dupes(*argv)


if __name__ == '__main__':
    main()
    
