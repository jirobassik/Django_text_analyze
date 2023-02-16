import spacy
import re
import pathlib
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_suffix_regex
from striprtf.striprtf import rtf_to_text
from spacy import displacy


def open_file_txt(path: str) -> str:
    ext = pathlib.Path(path).suffix
    with open(path, 'r', encoding='utf-8') as file:
        match ext:
            case '.txt':
                return file.read()
            case '.rtf':
                return rtf_to_text(file.read())


def custom_tokenizer(nlp):
    infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\`\“\”\"\'~]''')
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                     token_match=None)


class RoleAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("ru_core_news_sm")
        self.nlp.tokenizer = custom_tokenizer(self.nlp)

    def display(self, text: str):
        doc = self.nlp(text)
        #sentence_split = list(doc.sents)
        return displacy.render(doc, style="dep")
        # displacy.serve(sentence_split, style="dep")
        # http://localhost:5000/

# a = RoleAnalyzer()
# print(open_file_txt("test1.txt"))
# a.display(open_file_txt("test1.txt"))
