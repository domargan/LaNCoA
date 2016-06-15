# LaNCoA #

### Language Networks Construction and Analysis Toolkit ###

The package provides procedures for construction and analysis of complex language networks. 

__Written, as well as spoken language can be modeled via complex networks__ where the lingual units (e.g. words) are represented by vertices and their linguistic interactions by links. Language networks are a powerful formalism to the quantitative study of language structure at various language sublevels. Complex network analysis provides mechanisms that can reveal new patterns in complex structure and can thus be applied to the study of patterns that occur in the natural languages. Thus, complex network analysis may contribute to a better understanding of the organization, structure and evolution of a language.

__LaNCoA toolkit__ is focused mainly on the language networks construction task which includes various methods for the corpora manipulation (text preprocessing and cleaning, lemmatization, shuffling procedures and preparation for the language networks construction) and procedures for generation of various word-level and subword-level networks directly from the given corpora. 
The toolkit enables complex network analysis in terms of calculating all important global and local network measures, network and text content analysis, and data plotting possibilities. To some extent, LaNCoA toolkit uses existing functions from NetworkX and matplotlib Python packages as a basic foundation for some more specific network construction and analysis tasks.

With LaNCoA, networks can be constructed from the text corpora on word and sub-word levels:
* word level:
 * co-occurence networks, 
 * syntax networks,
 * shuffled networks,
* sub-word level:
 * syllable networks,
 * grapheme networks.
