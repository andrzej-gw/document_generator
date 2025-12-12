.PHONY: czlonek clean

all: przyklad


%:
	python3 decyzja.py $@
# 	pdflatex $@.tex
	rm -rf *.aux *.log

clean:
	rm -rf *.aux *.log
