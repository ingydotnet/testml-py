DEVLIB=../../testml-pm/lib

tests:
	perl -MTestML::Setup -e setup testml.yaml

dev:
	perl -I$(DEVLIB) -MTestML::Setup -e setup testml.yaml

clean:
	rm -fr testml/*.tml
