# phd-thesis-template
A template PhD thesis at UFAL

The font is Linux Libertine and it needs to be installed first (depending on the machine).

Compile with:

```
make
```
... and don't forget to download fresh ACL anthology:

```
wget https://aclanthology.org/anthology.bib.gz
pigz -d anthology.bib.gz
```

(see https://zlib.net/pigz/)


## How to collaborate

Dominik's tips for author-supervisor sharing and collaboration.

Let us assume that the main repository is a private GitHub repo.


### on a local machine:

	- sync GitHub repo (git clone/pull)

	- edit 

	- compile pdf: make

	- or: simple sync with GitHub: make ci

		- it pulls, commits and pushes 


### in overleaf that is connected with the GitHub:

	- sync GitHub: In Overleaf editing page, click to Menu (button in top left) -> GitHub (under Sync label) -> check sync status displayed there and click on pull or push

	- edit, compile, ...

	- do not forget to sync again




### How to send feedback:

- The author will be very thankful for feedback during writing. Most preferrable ways:

1) comments or edit suggestions in Latex macros, e.g.
 - \XXX{YourName: your comment}
 - \repl{to be replaced}{by this}    or   \repl{}{insert this here}   or   \repl{delete this}{}
 - you can add macros for your comments to macros.tex , e.g. \def\Raj#1{\XXX{Raj: #1}}

3) Feedback in any form that is convenient for you, except direct edits larger than typo-fixing. E.g. handwritten annotations on a paper, simple text, etc., everything is OK.

4) Author welcomes your direct edits for clear typo correction. But no large edits, please, the author must be the author. Rather suggestions.

## Credits

See template Chapter 3.
