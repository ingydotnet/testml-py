#!/bin/bash

for f in tests/*.py; do PYTHONPATH=. python $f; done
