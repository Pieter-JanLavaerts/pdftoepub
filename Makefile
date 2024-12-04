SHELL = /bin/sh

BOOK = Algorithm_Design_with_Haskell_by_Richard_Bird,_Jeremy_Gibbons

$(BOOK).html: $(BOOK).epub
	pandoc $(BOOK).epub -o $(BOOK).html

$(BOOK).epub: $(BOOK).md
	./epubtohtml.sh $(BOOK).epub -o $(BOOK).html

$(BOOK).md: convert_to_md.py $(BOOK).txt
	./convert_to_md.py $(BOOK).txt > $(BOOK).md

$(BOOK).txt: $(BOOK).pdf
	pdftotext $(BOOK).pdf > $(BOOK).txt

clean:
	rm $(BOOK).txt $(BOOK).epub $(BOOK).html $(BOOK).md
