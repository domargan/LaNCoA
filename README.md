# LaNCoA

**Language Networks Construction and Analysis Toolkit**

LaNCoA is a Python toolkit for constructing and analysing **language networks**: graph representations of text in which linguistic units such as words, syllables, or graphemes are represented as nodes and relationships between them are represented as edges.

The toolkit focuses on building networks from textual corpora, preprocessing those corpora, calculating selected network measures, comparing edge overlap between networks, extracting content-level summaries, and producing plots from edge-list data.

LaNCoA was developed for research on linguistic complex networks as part of the [Langnet](https://langnet.uniri.hr/) project, focusing on word co-occurrence networks, syntactic dependency networks, shuffled-text networks, syllable networks, and grapheme networks.

## What LaNCoA can do

* **Corpus preprocessing**

  * remove stopwords from a corpus
  * lemmatise words using a supplied word-form-to-lemma file
  * clean corpus text and optionally normalise Latin-script Unicode characters
  * shuffle text at sentence level or whole-text level

* **Network construction**

  * build word co-occurrence networks from a text corpus
  * build syntactic dependency networks from tab-separated, CoNLL-style parsed corpus files
  * build syllable networks from a corpus and syllabification dictionary
  * build grapheme networks from a syllable network
  * extract word-list subnetworks from existing word networks
  * extract word-centred ego subnetworks from existing word networks

* **Network measures**

  * in-selectivity, out-selectivity, and undirected selectivity
  * in- and out-inverse participation ratio
  * reciprocity for directed networks
  * entropy over a supplied node-measure dictionary
  * Jaccard edge overlap between two networks
  * total edge overlap and total weighted edge overlap

* **Content-level analysis**

  * highest-degree nodes, written to output files
  * highest-weight edges, written to output files
  * distances from one node to a supplied list of nodes

* **Plotting**

  * rank plots
  * histograms
  * scatter plots

## Repository layout

The main modules are:

| File                  | Purpose                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------- |
| `lancoa.py`           | Entry point for the command-line interface.                                                                 |
| `user_interface.py`   | `argparse` command dispatcher for corpus manipulation, network construction, analysis, measures, and plots. |
| `text_corpora.py`     | Corpus cleaning, stopword removal, lemmatisation, and text shuffling.                                       |
| `lang_nets.py`        | Construction of co-occurrence, syntactic, syllable, grapheme, word-list, and ego subnetworks.               |
| `measures.py`         | Selectivity, inverse participation ratio, reciprocity, and entropy functions.                               |
| `overlaps.py`         | Pairwise network-overlap functions.                                                                         |
| `content_analysis.py` | Highest-degree nodes, highest-weight edges, and node-distance reports.                                      |
| `plots.py`            | Matplotlib-based rank, histogram, and scatter plots.                                                        |

## Status and compatibility

This is a **legacy codebase**. It is written in Python 2 style and uses older NetworkX APIs such as `g.edge`, `edges_iter()`, `.iteritems()`, and `number_of_selfloops()`.

Use a legacy Python 2 environment with an older NetworkX release.

```bash
python --version
# Expected: Python 2.7.x

pip install "networkx<2" matplotlib
```

No `setup.py`, `pyproject.toml`, or `requirements.txt` is included in the repository, so the safest way to run the toolkit is directly from the repository checkout.

```bash
git clone https://github.com/domargan/LaNCoA.git
cd LaNCoA
python lancoa/lancoa.py
```

## Command-line interface

LaNCoA exposes five top-level command groups:

```bash
python lancoa/lancoa.py corpora     ...
python lancoa/lancoa.py create      ...
python lancoa/lancoa.py analyse     ...
python lancoa/lancoa.py calculate   ...
python lancoa/lancoa.py draw_plot   ...
```

### Corpus preprocessing

Clean a corpus, preserving selected punctuation, optionally splitting punctuation from words and applying NFKD normalisation:

```bash
python lancoa/lancoa.py corpora clean_corpus corpus.txt \
  --preserve_list . , ! ? \
  --nfkd Yes \
  --split Yes
```

Remove stopwords using a file containing one stopword per line:

```bash
python lancoa/lancoa.py corpora remove_stopwords corpus.txt stopwords.txt
```

Lemmatise a corpus using a word-form-to-lemma mapping file:

```bash
python lancoa/lancoa.py corpora lemmatize corpus.txt lemmas.txt --lemma_splitter $'\t'
```

Shuffle words inside each sentence:

```bash
python lancoa/lancoa.py corpora shuffle_corpus corpus.txt sentence .
```

Shuffle words across the whole text:

```bash
python lancoa/lancoa.py corpora shuffle_corpus corpus.txt text .
```

### Network construction

Build a word co-occurrence network:

```bash
python lancoa/lancoa.py create coocurrence_net corpus_cleaned.txt . , ! ? --window 2
```

Build an undirected or unweighted co-occurrence network:

```bash
python lancoa/lancoa.py create coocurrence_net corpus_cleaned.txt . , ! ? \
  -d undirected \
  -w unweighted \
  --window 2
```

Build a syntactic dependency network from a tab-separated, CoNLL-style parsed corpus file:

```bash
python lancoa/lancoa.py create syntax_net treebank.conll
```

Build a syllable network:

```bash
python lancoa/lancoa.py create syllable_net corpus.tsv syllables.txt
```

Build a grapheme network from a syllable-network edge list:

```bash
python lancoa/lancoa.py create grapheme_net corpus_syllable.edges
```

Extract a word-list subnetwork:

```bash
python lancoa/lancoa.py create wordlist_subnet corpus_cleaned_coocurrence.edges target_word words.txt
```

Extract a word-centred ego subnetwork:

```bash
python lancoa/lancoa.py create ego_word_subnet corpus_cleaned_coocurrence.edges target_word all --radius 2
```

For directed networks, the `neighborhood` argument can be:

```text
successors
predecessors
all
```

### Content analysis

Write the top-degree nodes to a text file:

```bash
python lancoa/lancoa.py analyse hubs corpus_cleaned_coocurrence.edges -n 20
```

Write the highest-weight edges:

```bash
python lancoa/lancoa.py analyse weightiest_edges corpus_cleaned_coocurrence.edges -n 20
```

Calculate distances from one node to a list of nodes:

```bash
python lancoa/lancoa.py analyse node_distance corpus_cleaned_coocurrence.edges source_word nodes.txt
```

In weighted mode, distances are calculated using NetworkX Dijkstra paths over the `weight` attribute, so edge weights are treated as path costs.

### Measures and overlaps

Calculate directed reciprocity:

```bash
python lancoa/lancoa.py calculate reciprocity corpus_cleaned_coocurrence.edges
```

Calculate entropy over one of the supported node-measure dictionaries:

```bash
python lancoa/lancoa.py calculate entropy corpus_cleaned_coocurrence.edges in_selectivity
python lancoa/lancoa.py calculate entropy corpus_cleaned_coocurrence.edges out_selectivity
python lancoa/lancoa.py calculate entropy corpus_cleaned_coocurrence.edges selectivity
python lancoa/lancoa.py calculate entropy corpus_cleaned_coocurrence.edges in_ipr
```

Compare two networks by Jaccard edge overlap:

```bash
python lancoa/lancoa.py calculate jaccard network1.edges network2.edges
```

Calculate total edge overlap:

```bash
python lancoa/lancoa.py calculate total_overlap network1.edges network2.edges
```

Calculate total weighted edge overlap:

```bash
python lancoa/lancoa.py calculate total_weighted_overlap network1.edges network2.edges
```

### Plots

Draw a rank plot for one or more networks:

```bash
python lancoa/lancoa.py draw_plot rankplot rank.png -d in -m degree network1.edges network2.edges
```

Draw a histogram:

```bash
python lancoa/lancoa.py draw_plot histogram histogram.png -d undirected -m selectivity network.edges
```

Draw a scatter plot:

```bash
python lancoa/lancoa.py draw_plot scatterplot scatter.png network.edges -d out -x strength -y selectivity
```

The output filename is passed directly to `matplotlib.pyplot.savefig`, so use a filename extension supported by Matplotlib, such as `.png`, `.pdf`, or `.svg`.

## Programmatic use

The functions can also be imported directly from the modules.

```python
from lancoa import lang_nets
from lancoa import measures

# Build a weighted directed co-occurrence network.
g = lang_nets.cooccurrence_net(
    corpus="corpus_cleaned.txt",
    delimiter_list=[".", ",", "!", "?"],
    d="directed",
    w="weighted",
    window=2,
    lower="Yes",
)

# Calculate out-selectivity from a weighted edge-list file.
out_sel = measures.out_selectivity("corpus_cleaned_coocurrence.edges")
```

When importing the modules directly in a legacy environment, make sure the `lancoa/` directory is on `PYTHONPATH`, because the internal imports use module names such as `import measures` and `import lang_nets` rather than package-relative imports.

## Input formats

### Plain text corpus

The co-occurrence constructor expects a UTF-8 text file. It reads the file, optionally lowercases it, and splits it on whitespace. Delimiters are supplied separately as command-line arguments or as a Python list.

The co-occurrence implementation creates links from previous tokens to the active token within the supplied window. It stops walking backwards when the previous token ends with one of the supplied delimiters, and strips delimiters from the active token when adding the edge.

### Stopword file

The stopword-removal function expects a plain text file containing stopwords. The code lowercases the stopword list and removes matching words from the corpus, while attempting to preserve trailing delimiters.

### Lemma file

The lemmatisation function expects a text file of word-form-to-lemma pairs split by a supplied delimiter, usually a tab:

```text
word_form<TAB>lemma
```

Entries whose lemma contains `#NIL#` are skipped. The implementation preserves title-case and uppercase forms when the lowercase token is matched in the lemma dictionary.

### Tab-separated, CoNLL-style parsed corpus

The syntactic network constructor expects a tab-separated, CoNLL-style parsed corpus with blank lines between sentences. It reads:

* token id from column `0`
* token form from column `1`
* part-of-speech tag from column `4`
* head id from column `6`

Edges are then created from head word to dependent word and weighted by frequency.

### Syllable files

The syllable-network constructor uses two files:

1. a corpus file where each line is split on tabs and the second field is treated as the word form;
2. a syllable list where each line contains a word and its syllabified form.

A syllable-list entry should look like this:

```text
word syl-la-ble
```

Adjacent syllables in the syllabified form are linked and counted.

### Edge-list files

Most analysis functions read weighted edge-list files using NetworkX. Weighted networks are written with `nx.write_weighted_edgelist`; unweighted networks are written with `nx.write_edgelist`.

## Implementation details

### Co-occurrence networks

`cooccurrence_net` builds a `DiGraph` or `Graph` and adds edges within a backward-looking window. In weighted mode, repeated co-occurrences increment the edge's `weight` attribute. In unweighted mode, edges are added without a weight counter.

### Syntactic networks

`syntax_net` parses sentences separated by blank lines and constructs edges from dependency heads to dependents. It performs a small amount of special-token handling: `--` and `-` can be renamed to `HYPHEN`, and `%` can be renamed to `PERCENT`. The generated network is written as a syntax edge list.

### Syllable and grapheme networks

`syllable_net` creates edges between adjacent syllables found in the syllabification file. `grapheme_net` then reads a syllable-network edge list, treats syllable node labels as strings, splits each syllable into characters, and links adjacent graphemes.

The grapheme constructor uses syllable node labels, not the original corpus text, and does not use syllable edge weights when counting grapheme edges.

### Selectivity

For a weighted network, selectivity is calculated as:

```text
selectivity(node) = strength(node) / degree(node)
```

Directed variants are available for incoming and outgoing edges.

### Inverse participation ratio

The directed inverse participation ratio functions calculate the sum of squared normalised incident edge weights for each node. `in_ipr` uses incoming edges; `out_ipr` uses outgoing edges.

### Reciprocity

`reciprocity` reads a weighted directed edge list and returns a tuple:

```text
(r, a, ro)
```

where:

* `r` is the fraction of directed edges with a reciprocal edge;
* `a` is the ratio of observed directed links to possible directed links, excluding self-loops from the numerator;
* `ro` is the Garlaschelli-Loffredo reciprocity value used in the code.

### Entropy

`entropy` accepts a dictionary of node-measure values and returns a normalised entropy value based on the distribution of those values.

### Network overlaps

`jaccard` returns the Jaccard similarity and distance based on edge-set intersection and union. `total_overlap` calculates an edge-overlap ratio over the composed graph. `total_weighted_overlap` compares common edges after normalising edge weights by the maximum edge weight in each input network.

## Citation

If you use this code in academic work, cite the original LaNCoA paper:

```bibtex
@inproceedings{margan2015lancoa,
  title     = {LaNCoA: A Python Toolkit for Language Networks Construction and Analysis},
  author    = {Margan, Domagoj and Me\v{s}trovi\'{c}, Ana},
  booktitle = {Proceedings of the 38th International Convention on Information and Communication Technology, Electronics and Microelectronics (MIPRO)},
  year      = {2015}
}
```

## License

See the repository `LICENSE` file for the full license text.

## Credits

* Original project and code author: **Domagoj Margan**
* LaNCoA paper authors: **Domagoj Margan** and **Ana Meštrović**
* Contribution to CLI and plotting modules: **Tanja Miličić**
