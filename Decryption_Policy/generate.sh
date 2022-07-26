#!/bin/bash

antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar'
$antlr4 -visitor -Dlanguage=Python3 dp.g4
