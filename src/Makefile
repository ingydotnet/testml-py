BASE=../lib/testml/parser

$(BASE)/grammar.py: grammar/grammar.yaml grammar.py Makefile $(BASE)
	python grammar.py $< > $@

$(BASE):
	mkdir -p $@

clean:
	rm -fr $(BASE)/grammar.py
