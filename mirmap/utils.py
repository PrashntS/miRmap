# -*- coding: utf-8 -*-

#
# Copyright (C) 2011-2013 Charles E. Vejnar
#
# This is free software, licensed under the GNU General Public License v3.
# See /LICENSE for more information.
#

"""Common functions."""

import collections
import itertools
import functools

try:
    # Python 3 support
    from itertools import zip_longest
    maketrans = ''.maketrans
except (AttributeError, ImportError):
    # fallback for Python 2
    from string import maketrans
    from itertools import izip_longest
    zip_longest = izip_longest

def grouper(n, iterable, fillvalue=None):
    """http://docs.python.org/library/itertools.html#recipes"""
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def flatten(l1d):
    return list(itertools.chain.from_iterable(l1d))

def clean_seq(seq, alphabet):
    alphabet_real = list(set(seq))
    for l in alphabet_real:
        if l not in alphabet:
            seq = seq.replace(l, '')
    return seq

def load_fasta(fasta, as_string=None, upper=False):
    if as_string is None:
        as_string = False
    if as_string:
        ff = fasta.split('\n')
    elif fasta.split('.')[-1] == 'gz':
        ff = gzip.open(fasta, 'rb')
    else:
        ff = open(fasta)
    seqs = collections.OrderedDict()
    name_seq = ''
    for line in ff:
        line = line.strip()
        if line.startswith('>'):
            name_seq = line[1:].strip()
            seqs[name_seq] = ''
        else:
            if upper:
                seqs[name_seq] += line.upper()
            else:
                seqs[name_seq] += line
    if as_string is False:
        ff.close()
    return seqs

def reverse_complement(seq):
    """Returns the reverse complement sequence. New string object.
    (Adapted from BioPython)"""
    if 'U' in seq or 'u' in seq:
        ttable = maketrans("ACGUacgu", "UGCAugca")
    else:
        ttable = maketrans("ACGTacgt", "TGCAtgca")
    seq = seq[-1::-1].translate(ttable)
    return seq

def rgetattr(obj, attr):
    return functools.reduce(getattr, [obj]+attr.split('.'))
