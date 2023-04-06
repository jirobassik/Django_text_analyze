from typing import NoReturn
from threading import Thread
import re
import spacy
from anytree.exporter import UniqueDotExporter
from nltk.corpus import wordnet as wn
from spacy.util import compile_prefix_regex, compile_suffix_regex
from spacy.tokenizer import Tokenizer
from anytree import Node
import os
from utilities.file_upl_sav.svg_html import create_html
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

os.environ["PATH"] += os.pathsep + 'D:/Programs/Graphviz/bin/'


def custom_tokenizer(nlp) -> NoReturn:
    infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\`\“\”\"\'~]''')
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                     token_match=None)


class SemSyntAnalyzer:
    def __init__(self):
        self.doc = None
        self.nlp = spacy.load("en_core_web_sm")
        self.stopwords = self.nlp.Defaults.stop_words
        self.nlp.tokenizer = custom_tokenizer(self.nlp)

    def get_text_punctation(self) -> set[str]:
        return {token.text.lower() for token in self.doc
                if not re.match(r'[^\w\s]|(\r\n|\r|\n)', token.text)
                and token.text.lower() not in self.stopwords}

    def tree_(self, text: str):
        create_html()
        root_ = Node("S")
        self.doc = self.nlp(text)
        self.get_word_sentence(root_)
        self.__save(root_)

    def get_word_sentence(self, root_):
        for sentence in [sent for sent in self.doc.sents]:
            sent = Node("SENT", parent=root_)
            Node(sentence, parent=sent)
            for word in self.get_text_punctation():
                ws_node = Node("WS", parent=sent)
                self.__add_sem_node(self.sem_synt_analyze(word), ws_node)

    @staticmethod
    def __add_sem_node(sem_synt_dict: dict, ws_node):
        for key, value in sem_synt_dict.items():
            sem_node = Node(key, parent=ws_node)
            Node(value, parent=sem_node)

    @staticmethod
    def __save(root_):
        UniqueDotExporter(root_).to_picture("sem_synt/static/upload/tree.svg")

        def save_png():
            drawing = svg2rlg("sem_synt/static/upload/tree.svg")
            renderPM.drawToFile(drawing, "sem_synt/static/upload/tree.png", fmt="PNG")
            print("PNG SAVED")
        Thread(target=save_png).start()

    @staticmethod
    def sem_synt_analyze(word: str) -> dict[str: str]:
        if len(wn.synsets(word)):
            dict_analyze = {"W": word, 'DEF': wn.synsets(word)[0].definition(), }
            word = wn.synsets(word)

            synonyms = {lemma.name() for synset in word for lemma in synset.lemmas()}
            antonyms = [lemma.antonyms()[0].name() for synset in word for lemma in synset.lemmas() if lemma.antonyms()]
            hyponym = [hyponym.name() for hyponym in word[0].hyponyms()]
            hypernym = [hypernym.name() for hypernym in word[0].hypernyms()]

            dict_synct = {"SYN": synonyms, "ANT": antonyms, "HYPO": hyponym, "HYPE": hypernym}
            join_values_dict = dict(map(lambda kv: (kv[0], "|".join(kv[1])), dict_synct.items()))
            for key, value in join_values_dict.items():
                if len(value):
                    dict_analyze.update([(key, value)])
            return dict_analyze
        return {"W": word, }
