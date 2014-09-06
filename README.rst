A Lorem Ipsum text generator
============================

You may import the **Generator** class to instantiate your generator
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

or just import **get_sentences** or **get_paragraphs**
which interface to a module wide **Generator** instance.

>>> from loremipsum import get_paragraphs, get_sentences
>>> 
>>> get_sentences(5) #doctest: +ELLIPSIS
['...', '...', '...', '...', '...']
>>> get_paragraphs(3) #doctest: +ELLIPSIS
['...', '...', '...']
