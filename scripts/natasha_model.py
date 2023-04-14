from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc,
    PER,
    NamesExtractor
)

emb = NewsEmbedding()
segmenter = Segmenter()
morph_vocab = MorphVocab()
ner_tagger = NewsNERTagger(emb)
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)

def extract_ents(text):
  ents = []
  text = Doc(text)
  text.segment(segmenter)
  text.parse_syntax(syntax_parser)
  text.tag_morph(morph_tagger)
  text.tag_ner(ner_tagger)
  for span in text.spans:
    span.normalize(morph_vocab)
    ents.append({"type":span.type, "ent":span.normal})
  return ents