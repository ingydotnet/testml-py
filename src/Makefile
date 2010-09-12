SRC=../../testml-pgx
BASE=../testml

$(BASE)/grammar.py: testml.pgx.yaml grammar.py Makefile $(BASE)
	perl grammar.py $< > $@

testml.pgx.yaml: $(SRC)/testml.pgx.yaml
	cp $< $@
