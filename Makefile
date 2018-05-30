
OUTPUT:=output

all: $(OUTPUT)/drinks.pdf

$(OUTPUT)/drinks.pdf: ats/*.py ats/templates/*.tex
	./ats/main.py names.yaml drinks.yaml
