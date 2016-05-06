## Metrink FE

Frontend version of Metrink. Includes only the graphing engine and leverages an existing backend for the data.

### HOWTO Build
You must have ANTLR4 installed with the Python runtime

`antlr4 -o ./parser -listener -visitor -Dlanguage=Python3 -lib . ./Metrink.g4`
