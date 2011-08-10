You may import the :py:class:`Generator` class to instantiate your generator
with your own sample text and a dictionary:

>>> from loremipsum import Generator
>>> 
>>> sample = file('data/sample.txt').read()
>>> dictionary = file('data/dictionary.txt').read().split()
>>> 
>>> g = Generator(sample, dictionary)
>>> g.generate_sentence() #doctest: +ELLIPSIS
(...)
>>> 

or just import :py:func:`get_sentences` or :py:func:`get_paragraphs`
which interface to a module wide :py:class:`Generator` instance.

>>> from loremipsum import get_paragraphs, get_sentences
>>> 
>>> get_sentences(5) #doctest: +ELLIPSIS
['...', '...', '...', '...', '...']
>>> get_paragraphs(3) #doctest: +ELLIPSIS
['...', '...', '...']
