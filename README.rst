Overview
========

You may import the :py:class:`Generator` class to instantiate your generator
with a sample text and a dictionary:

>>> from loremipsum import Generator
>>> 
>>> sample = file('data/sample.txt').read()
>>> dictionary = file('data/dictionary.txt').read().split()
>>> 
>>> g = Generator(sample, dictionary)
>>> g.generate_sentence(True)
...

or just import any of :py:func:`generate_sentences`,
:py:func:`generate_paragraphs`, :py:func:`generate_words` which interface to a
module wide :py:class:`Generator` instance.

>>> from loremipsum import generate_paragraphs, generate_sentences
>>> 
>>> generate_sentences(5)
['...', '...', '...', '...', '...']
>>> generate_paragraphs(3)
['...', '...', '...']
