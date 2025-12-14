#!/bin/bash

# cronjob
# 30 14 * * * /bin/bash $HOME/comunica-if/web/script.sh >> $HOME/comunica-if/web/.log

python3 $HOME/Projects/comunica-if/web/scraper.py
