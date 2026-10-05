
# Philosophy Tree - Wikipedia

## Description

In roughly 97% of **Wikipedia** articles, following the *first valid link* eventually leads to the **Philosophy** article. This project explores that phenomenon by scraping Wikipedia pages, following the first suitable link in each article, and tracing the path until it reaches a target page.

The scraper uses **Requests** and **BeautifulSoup** to extract links, stores the resulting paths in a tree structure, and visualizes the tree with **Pyvis** and **NetworkX**.

This implementation is configured for **Spanish Wikipedia**:

```python
BASE_URL = "https://es.wikipedia.org/wiki"
TARGET = "/Filosofía"
```

*It is intended as a small experimental/visual project, not as a production-scale crawler.*


## Tech Stack

- **Python 3.11**
- **Requests** — HTTP requests to Wikipedia.
- **BeautifulSoup4** — HTML parsing and link extraction.
- **Pyvis** — Interactive graph visualization.
- **NetworkX** — Graph construction for Pyvis.
- **Jupyter / IPython** — Notebook-based experimentation.
- **venv** — Local Python environment.

## Setup

Use `environment.ipynb` steps, or run manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then use VisualStudio notebooks extensions or start Jupyter:

```bash
jupyter notebook
```

---

## Execution Flow

1. **Configure the project**
   - Edit `config.py` if needed.
   - Default configuration targets Spanish Wikipedia:
     ```python
     BASE_URL = "https://es.wikipedia.org/wiki"
     TARGET = "/Filosofía"
     RANDOM_FUNCTION_URI = "/Special:Random"
     FAILSAFE = 100
     ```

2. **Choose a starting page**
   - Use a specific Wikipedia page path, e.g. `"/Mork"`.
   - Or use a random page via `from_random_all_the_ways_lead_to()`.

3. **Trace the path**
   - `all_the_ways_lead_to(starting_page)` repeatedly follows the first valid link.
   - It stops when it reaches `TARGET` (*Philosophy* on the configured language), or when `FAILSAFE` iterations are exceeded.

4. **Extract the next page**
   - `get_next_page(page)`:
     - Fetches the Wikipedia page.
     - Parses it with BeautifulSoup.
     - Keeps the first content section: `data-mw-section-id="0"`.
     - Removes infobox tables and reference superscripts.
     - Selects paragraphs with `p[id]`.
     - Removes parenthesized text from paragraph HTML.
     - Selects the first valid `a[id]` link.
     - Skips red links (`?action=edit&redlink=1`).
     - Returns the normalized page path.

5. **Build the tree**
   - `add_to_tree(path, tree)` inserts the traced path into a tree of `Node` objects.
   - The root of the tree is the target page, i.e. `/Filosofía`.
   - Leaves are the starting pages.

6. **Visualize the tree**
   - `plot_tree(root_node)` converts the tree to a NetworkX graph.
   - It renders an interactive Pyvis graph, saves it as `aux_tree.html`, and embeds it as an `IFrame`.
   - `leaf_page_to_graph(leaf_page)` is the convenience function used in notebooks.

---

## Example Usage

### Print a path

```python
from src.scrapping import all_the_ways_lead_to

testing = all_the_ways_lead_to(">/Índice_de_Jaccard")

for p, i in enumerate(testing):
    print(" " * p + ">" + i)
```

Example output:

```text
>/Índice_de_Jaccard 
 >/Ecología 
  >/Biología 
   >/Ciencia_natural 
    >/Experimento 
     >/Hipótesis_(método_científico) 
      >/Proposición 
       >/Filosofía
```

### Visualize a path/tree

```python
from src.tree import leaf_page_to_graph

leaf_page_to_graph("/Wonder_of_Stardom_Championship")
```

This returns an embedded Pyvis graph showing the path from `/Wonder_of_Stardom_Championship` to `/Filosofía`.

### Build a merged tree

```python
from src.scrapping import all_the_ways_lead_to
from src.tree import add_to_tree

path = all_the_ways_lead_to("/Mork")
tree = add_to_tree(path)
tree.basic_print()
```

---

## Compromises / Limitations

1. **Tested mainly on Spanish Wikipedia**
   - The project uses:
     ```python
     BASE_URL = "https://es.wikipedia.org/wiki"
     TARGET = "/Filosofía"
     ```
   - Adapting it to another language edition requires changing these constants and possibly link-handling rules.

2. **Parenthesized URLs/content are skipped**
   - Wikipedia articles often contain pronunciation, word roots, or citations inside parentheses.
   - These are useful, but for this exercise they are out of scope and can cause unexpected loops.
   - The scraper removes parenthesized text before selecting the first link.

3. **Red-linked articles are skipped**
   - Red links point to pages that do not exist yet.
   - They are more common on non-English Wikipedias.
   - Following them would break the chain, so the scraper skips links ending with:
     ```text
     ?action=edit&redlink=1
     ```

4. **Infoboxes and tables are ignored**
   - The scraper removes tables from the first content section.
   - The focus is on the first paragraph(s) of the article, not infoboxes or navigation templates.

5. **Only the first valid link is followed**
   - This matches the classic “first link” rule.
   - It does not explore all outgoing links or build a full Wikipedia graph.

6. **Failsafe limit**
   - `FAILSAFE = 100` stops runaway paths before they become too long.
   - When triggered, the scraper prints:
     ```text
     stoped before target
     ```

7. **Not a production crawler**
   - There is no caching, concurrency, rate limiting, or retry strategy.
   - Be respectful to Wikipedia when running repeated requests.

---

## Notebooks

### `environment.ipynb`

Creates a virtual environment and installs the project dependencies from `requirements.txt`. Use this first when setting up the project locally.

### `path.ipynb`

Demonstrates `all_the_ways_lead_to()` for several starting pages and prints the path from the starting article to `/Filosofía`.

Examples include:

- `/Wonder_of_Stardom_Championship`
- `/Índice_de_Jaccard`
- `/Mork`

### `trees.ipynb`

Builds and prints a merged tree for multiple paths using `add_to_tree()`.

It shows how different starting pages converge on the same target and how the tree grows as more paths are added.

### `graph.ipynb`

Visualizes the tree/path with Pyvis using `leaf_page_to_graph()`.

It includes examples such as:

- `/Wonder_of_Stardom_Championship`
- `/Mork`
- `/Ayuda:Espacio_de_nombres`
- `/Sam_Lake`
- `/El_Otro_Yo_del_Otro_Yo:_Esencia`
- `/Alejandra_Gils_Carbó`
- random pages

---

## Main Modules

### `src/config.py`

Project constants:

```python
BASE_URL = "https://es.wikipedia.org/wiki"
TARGET = "/Filosofía"
RANDOM_FUNCTION_URI = "/Special:Random"
FAILSAFE = 100
```

Also contains request headers used by `requests`.

### `src/scrapping.py`

Scraping logic:

- `valid_url(page)`
- `trim_page(page)`
- `random_starting_page()`
- `clean_html_parentheses(html_string)`
- `get_next_page(page)`
- `all_the_ways_lead_to(starting_page)`
- `from_random_all_the_ways_lead_to()`

### `src/node.py`

Simple tree node:

- `Node(value)`
- `contains(value)`
- `search(value)`
- `basic_print(level=0)`

### `src/tree.py`

Tree and visualization logic:

- `add_to_tree(branch, tree=None)`
- `build_networkx_graph(node, G=None, level=0)`
- `plot_tree(root_node)`
- `leaf_page_to_graph(leaf_page=None, reset=False)`

---

## Notes

- The generated `aux_tree.html` file is overwritten each time `plot_tree()` is called.
- The graph is hierarchical and directed.
- Because paths are stored from starting page to target, the tree root is the target page `/Filosofía`, and the leaves are the starting articles.
- The project is useful for demonstrating the “getting to Philosophy” phenomenon and for experimenting with Wikipedia link-following behavior.
```