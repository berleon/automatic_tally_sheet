OUTPUT:=output

.PHONY: $(OUTPUT)/drinks.pdf

all: $(OUTPUT)/drinks.pdf

$(OUTPUT)/drinks.pdf: ats/*.py ats/templates/*.tex
	./ats/main.py --placeholders 5 names.yaml drinks.yaml
