
OUTPUT:=output

all: $(OUTPUT)/caffee_schoko.pdf $(OUTPUT)/drinks_stuff.pdf

$(OUTPUT)/caffee_schoko.pdf: ats/*.py ats/templates/*.tex
	./ats/main.py names.yaml caffee_schoko.yaml

$(OUTPUT)/drinks_stuff.pdf: ats/*.py ats/templates/*.tex
	./ats/main.py names.yaml drinks_stuff.yaml
