all: Metrink.g4
	antlr4 -o $(PWD)/parser -listener -visitor -Dlanguage=Python3 -lib $(PWD) $(PWD)/Metrink.g4
	touch parser/__init__.py

clean:
	-rm -rf parser
