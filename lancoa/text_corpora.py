#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Domagoj Margan <margan.domagoj@gmail.com>

This file is part of LaNCoA.
LaNCoA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LaNCoA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LaNCoA.  If not, see <http://www.gnu.org/licenses/>.
"""

from codecs import open

__author__ = "Domagoj Margan"
__email__ = "margan.domagoj@gmail.com"
__copyright__ = "Copyright 2015, Domagoj Margan"
__license__ = "GPL"


def remove_stopwords(corpus_file, delimiter_list, stopwords_file):
    # TODO: Make it work for word.strip("\"'`.!?;:,*")
    """Remove stopwords from text file and save result in new file.
    Examples of stopwords are: 'is', 'but', 'and', 'some', 'any'...

    Parameters
    ----------
    corpus_file : file
        original text file from which stopwords will be removed
    delimiter_list : list
        list of delimiters
    stopwords_file : file
        file containing the list of stopwords
    """
    punct_split_dict = {d: d + " " for d in delimiter_list}

    with open(corpus_file, "r", encoding="utf-8") as f:
        f_r = f.read()
        for k, v in punct_split_dict.iteritems():
            f_r = f_r.replace(k, v)
        corpus_list = f_r.split()

    with open(stopwords_file, "r", encoding="utf-8") as remove_words:
        remove_words_list = remove_words.read().lower().split()

    for i, word in enumerate(corpus_list):
        for d in delimiter_list:
            if d in word:
                if word[:-len(d)] in remove_words_list:
                    corpus_list[i] = d
                elif word[:-len(d)].lower() in remove_words_list:
                    corpus_list[i] = d
            elif word in remove_words_list or word.lower() in remove_words_list:
                corpus_list[i] = ""
            elif word not in remove_words_list or word.lower() not in remove_words_list:
                pass

    with open(corpus_file.rsplit(".", 1)[0] + "_sw_removed." +
                      corpus_file.rsplit(".", 1)[1], "w",
              encoding="utf-8") as write_f:
        write_f.write(" ".join(word for word in corpus_list if word != ""))


def lemmatize(corpus_file, delimiter_list, lemmas_file, lemma_splitter):
    # TODO: Make it work for word.strip("\"'`.!?;:,*")
    """Group together the different inflected forms of a
    word into a single item.

    For instance words: cars, car's, cars' are converted
    into its standard form car.

    Lemmatization in LaNCoA is based on find-and-replace principle.

    Parameters
    ----------
    corpus_file : file
        original text file on which lemmatization
        process will be applied
    delimiter_list : list
         list of delimiters
    lemmas_file : file
        file containing the list of all word
        form-lemma pairs
    lemma_splitter : char
        char that splits word form-lemma pair in lemmas_file,
        e.g. '\t', ' '
    """
    punct_split_dict = {d: d + " " for d in delimiter_list}
    with open(corpus_file, "r", encoding="utf-8") as f:
        f_r = f.read()
        for k, v in punct_split_dict.iteritems():
            f_r = f_r.replace(k, v)
        corpus_list = f_r.split()

    with open(lemmas_file, "r", encoding="utf-8") as lemmas:
        lemmas_r = lemmas.readlines()

    lemmas_list = [line.split(lemma_splitter) for line in lemmas_r]
    lemmas_dict = {line[0]: line[1] for line in lemmas_list if
                   "#NIL#" not in line[1]}

    for i, word in enumerate(corpus_list):
        for d in delimiter_list:
            if d in word:
                if word[:-len(d)] in lemmas_dict:
                    corpus_list[i] = lemmas_dict[word[:-len(d)]] + d
                elif word[:-len(d)].lower() in lemmas_dict:
                    if word[:-len(d)].istitle():
                        corpus_list[i] = lemmas_dict[word[:-len(d)].lower()].title() + d
                    elif word[:-len(d)].isupper():
                        corpus_list[i] = lemmas_dict[word[:-len(d)].lower()].upper() + d
                    else:
                        corpus_list[i] = lemmas_dict[word[:-len(d)].lower()] + d
            elif word in lemmas_dict:
                corpus_list[i] = lemmas_dict[word]
            elif word.lower() in lemmas_dict:
                if word.istitle():
                    corpus_list[i] = lemmas_dict[word.lower()].title()
                elif word.isupper():
                    corpus_list[i] = lemmas_dict[word.lower()].upper()
                else:
                    corpus_list[i] = lemmas_dict[word.lower()]
            elif word not in lemmas_dict or word.lower() not in lemmas_dict:
                pass

    with open(corpus_file.rsplit(".", 1)[0] + "_lemmatized." +
                      corpus_file.rsplit(".", 1)[1], "w",
              encoding="utf-8") as write_f:
        write_f.write(" ".join(corpus_list))


def clean_corpus(corpus, preserve_list=None, nfkd="No", split="No",
                 replace_char=""):
    """Clean text file from unwanted characters or
    data and save results in new file.

    All UTF-8 characters which are not defined as
    letters or numbers of the classical Latin alphabet
    will be removed from textual corpus.

    The NFKD unicode normalization of all Latin
    script letters can optionally be preformed directly
    in the process of cleaning.

    Parameters
    ----------
    corpus : file
        original text file for text cleaning
    preserve_list: list
        list of interpunctions
    nfkd : Yes or No (default="No")
        if selected choice is Yes than the normal form NFKD
        will replace all compatibility characters with their
        equivalent.
    split : Yes or No (default="No")
        if selected choice is Yes than an empty char behind
        all interpunctions from preserve_list will be added
        in text file
    replace_char : char
        character that will replace all unwanted characters in file

    """
    from unicodedata import normalize

    if not preserve_list:
        preserve_list = [",", ".", ";", "!", "?"]

    with open(corpus, "r", encoding="utf-8") as f:
        f_r = f.read()

    if split == "Yes":
        punct_split_dict = {d: str(d) + " " for d in preserve_list}
        for k, v in punct_split_dict.iteritems():
            f_r = f_r.replace(k, v)

    remove_chars = []
    for i in range(0x0000, 0x0030) + range(0x003A, 0x0041) + \
            range(0x005B, 0x0061) + range(0x007B, 0x00BF) + range(0x0250, 0x27FF):
        if i == 0x0020:
            pass
        else:
            remove_chars.append(eval('u"\\u%04x"' % i))

    for i, char1 in enumerate(preserve_list):
        for j, char2 in enumerate(remove_chars):
            if char1.strip() == char2:
                remove_chars.pop(j)

    for i in remove_chars:
        if i == "\n" or i == "\r" or i == "\r\n":
            f_r = f_r.replace(i, " ")
        else:
            f_r = f_r.replace(i, replace_char)

    if nfkd == "Yes":
        replace_dict = {eval('u"\\u%04x"' % i):
                            normalize("NFKD", eval('u"\\u%04x"' % i)).encode(
                                "ascii", "ignore")
                        for i in range(0x00C0, 0x02AE)}

        for k, v in replace_dict.iteritems():
            if v == "":
                pass
            else:
                f_r = f_r.replace(k, v)

    corpus_list = f_r.split()
    corpus_list = [word for word in corpus_list if
                   word != "" and word not in preserve_list]

    with open(corpus.rsplit(".", 1)[0] + "_cleaned." +
                      corpus.rsplit(".", 1)[1], "w",
              encoding="utf-8") as write_f:
        write_f.write(" ".join(corpus_list))


def shuffle_corpus(corpus, delimiter_list, mode, end_sign):
    """Randomize words in the text, transforming the text
    into the meaningless form.

    Two different shuffling principles are implemented:
    shuffling on the sentence level and
    shuffling on the whole text level.

    In the text-level shuffling, the original text is
    randomized by shuffling the words and punctuation
    marks over the whole text.

    Parameters
    ----------
    corpus : file
        original file on which shuffling
        procedure will be applied
    delimiter_list : list
        list of delimiters
    mode : sentence or text
        shuffling principles
    end_sign : char
        character that will mark end of a sentence
    """
    from re import split as re_split
    from random import shuffle
    from random import randint

    with open(corpus, "r", encoding="utf-8") as f:
        f_r = f.read()

    punct_split_dict = {d: str(d) + " " for d in delimiter_list}

    for k, v in punct_split_dict.iteritems():
        f_r = f_r.replace(k, v)

    corpus_list = f_r.split()
    corpus_list = [word for word in corpus_list if
                   word != "" and word not in delimiter_list]

    if mode == "sentence":
        text = " ".join(corpus_list)
        sentences = re_split('\.|\?|\!|\. |\? |\! ', text)

        sentences_split = [i.split() for i in sentences]
        for i in sentences_split:
            shuffle(i)

        shuffled_list = [x.strip() for x in
                         [" ".join(x) + end_sign for x in sentences_split]]

        with open(corpus.rsplit(".", 1)[0] + "_sentence_shuffled." +
                          corpus.rsplit(".", 1)[1], "w",
                  encoding="utf-8") as write_f:
            write_f.write(" ".join(shuffled_list))

    elif mode == "text":
        shuffled_list = corpus_list
        shuffle(shuffled_list)

        if delimiter_list:
            delimiter_count = 0
            for i, word in enumerate(shuffled_list):
                for d in delimiter_list:
                    if word[-len(d):] == d:
                        delimiter_count += 1
                        shuffled_list[i] = word[:-len(d)]
            while delimiter_count:
                rand = randint(0, len(shuffled_list) - 1)
                if shuffled_list[rand][-len(end_sign):] != end_sign:
                    shuffled_list[rand] += end_sign
                    delimiter_count -= 1

        with open(corpus.rsplit(".", 1)[0] + "_text_shuffled." +
                          corpus.rsplit(".", 1)[1], "w",
                  encoding="utf-8") as write_f:
            write_f.write(" ".join(shuffled_list))