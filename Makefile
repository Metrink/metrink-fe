all: MetrinkFrontend.g4 MetrinkBackend.g4 MetrinkBase.g4
	# build the Python files
	antlr4 -o $(PWD)/frontend/parser -listener -visitor -Dlanguage=Python3 -lib $(PWD) $(PWD)/MetrinkFrontend.g4
	touch frontend/parser/__init__.py
	# build the Java files
	antlr4 -o $(PWD)/backend/src/main/java/com/metrink/parser -visitor -package com.metrink.parser -Dlanguage=Java -lib $(PWD) $(PWD)/MetrinkBackend.g4
	rm $(PWD)/backend/src/main/java/com/metrink/parser/MetrinkBackendBaseVisitor.java
	rm $(PWD)/backend/src/main/java/com/metrink/parser/MetrinkBackendBaseListener.java

clean:
	-rm -rf parser
