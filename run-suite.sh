#!/usr/bin/env bash

python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1
