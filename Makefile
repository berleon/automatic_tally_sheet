
OUTPUT:=output

all: $(OUTPUT)/caffee_schoko.pdf $(OUTPUT)/drinks_stuff.pdf

$(OUTPUT)/caffee_schoko.pdf:
	./ats/main.py names.yaml caffee_schoko.yaml

$(OUTPUT)/drinks_stuff.pdf:
	./ats/main.py names.yaml drinks_stuff.yaml
