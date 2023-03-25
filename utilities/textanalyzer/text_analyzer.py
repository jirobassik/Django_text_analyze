import spacy
import pymorphy3
import re
import pathlib
from typing import NoReturn
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_suffix_regex
from striprtf.striprtf import rtf_to_text


def custom_tokenizer(nlp) -> NoReturn:
    infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\`\“\”\"\'~]''')
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                     token_match=None)


def open_file_txt(path: str) -> str:
    ext = pathlib.Path(path).suffix
    with open(path, 'r', encoding='utf-8') as file:
        match ext:
            case '.txt':
                return file.read()
            case '.rtf':
                return rtf_to_text(file.read())


class TextAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("ru_core_news_sm")
        self.nlp.tokenizer = custom_tokenizer(self.nlp)
        self.morph = pymorphy3.MorphAnalyzer()

    def get_text_punctation(self, text_: str) -> list[tuple[str, str, str]]:
        doc = self.nlp(text_)
        return {(token.text.lower(), self.role_in_sentence(token.text), self.morph_analyzer(token.text))
                for token in doc if not re.match(r'[^\w\s]|(\r\n|\r|\n)', token.text)}  # [^\w\s]|\n

    def morph_analyzer(self, word: str) -> str:
        return self.morph.parse(word.lower())[0].tag.cyr_repr

    def role_in_sentence(self, word: str) -> str:
        morph_analyze = self.morph.parse(word.lower())[0]
        match morph_analyze:
            case _ if morph_analyze.tag.case == "nomn" or morph_analyze.tag.POS == "NUMR":
                return "Подлежащее"
            case _ if morph_analyze.tag.POS == "VERB":
                return "Сказуемое"
            case _ if morph_analyze.tag.POS == "NOUN" and morph_analyze.tag.case != "nomn":
                return "Дополнение"
            case _ if morph_analyze.tag.POS == "ADJF":
                return "Определение"
            case _ if morph_analyze.tag.POS == "ADVB":
                return "Обстоятельство"
            case _:
                return "Не определен"
