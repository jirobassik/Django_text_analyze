from typing import NoReturn
import re
import spacy
from anytree.exporter import UniqueDotExporter
from nltk.corpus import wordnet as wn
from spacy.util import compile_prefix_regex, compile_suffix_regex
from spacy.tokenizer import Tokenizer
from anytree import Node
import os
from file_upl_sav.svg_html import create_html
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
        self.nlp = spacy.load("en_core_web_sm")
        self.stopwords = self.nlp.Defaults.stop_words
        self.nlp.tokenizer = custom_tokenizer(self.nlp)

    def get_text_punctation(self, text_: str) -> set[str]:
        doc = self.nlp(text_)
        return {token.text.lower() for token in doc
                if not re.match(r'[^\w\s]|(\r\n|\r|\n)', token.text)
                and token.text.lower() not in self.stopwords}

    def tree_(self, text: str):
        create_html()
        set_tokens = self.get_text_punctation(text_=text)
        root_ = Node("S")
        sent = Node("SENT", parent=root_)
        for word in set_tokens:
            ws_node = Node("WS", parent=sent)
            sem_synt_dict = self.sem_synt_analyze(word)
            for key, value in sem_synt_dict.items():
                sem_node = Node(key, parent=ws_node)
                Node(value, parent=sem_node)
        self.__save(root_)

    @staticmethod
    def __save(root_):
        UniqueDotExporter(root_).to_picture("sem_synt/static/upload/tree.svg")
        drawing = svg2rlg("sem_synt/static/upload/tree.svg")
        renderPM.drawToFile(drawing, "sem_synt/static/upload/tree.png", fmt="PNG")

    @staticmethod
    def sem_synt_analyze(word: str) -> dict[str: str]:
        if len(wn.synsets(word)):
            dict_analyze = {"W": word, 'DEF': wn.synsets(word)[0].definition(), }
            word = wn.synsets(word)

            synonyms = [lemma.name() for synset in word for lemma in synset.lemmas()]
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
