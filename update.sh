#!/bin/bash
rm *~ && rm tests/*~ && rm *.pyc
git add . && git commit -m updates && git push -u origin main
