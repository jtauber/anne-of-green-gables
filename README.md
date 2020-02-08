# anne-of-green-gables
text encoding and analysis of Anne of Green Gables

`/raw/` contains various texts downloaded. See `/raw/sources.md` for details.

The four texts with filenames beginning `gutenberg` have been consolidated into an eclectic corrected text `/gutenberg_0.txt`.

The text beginning `wikisource` is being corrected in `/wikisource_0.txt`.

The equivalent files in `/text-prep/` are a custom-encoding of the texts such that they can easily be compared to both the raw files and to the corrected texts. The script `/scripts/check-text-prep.py` checks that the `text-prep` files do indeed capture both the raw texts and correct texts.
