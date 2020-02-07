# anne-of-green-gables
text encoding and analysis of Anne of Green Gables

`/raw/` contains various texts downloaded. See `/raw/sources.md` for details.

The four texts with filenames beginning `gutenberg` have been consolidated into an eclectic text `/gutenberg_0.txt`.

The equivalent files in `/text-prep/` are a custom-encoding of the texts such that they can easily be compared to both the raw files and to the eclectic text. The script `/scripts/check-text-prep.py` checks that the `text-prep` files do indeed capture both the raw text and eclectic text.
