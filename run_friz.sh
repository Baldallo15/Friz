#!/bin/bash
cd "$(dirname "$0")"
export PATH=$HOME/.local/bin:/tmp:$PATH
python3 friz.py
