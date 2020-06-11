#!/bin/bash

anybadge --value='Sphinx' --file=public/sphinx.svg --label='documentation'

cat docs/source/conf.py | grep release > conf.txt
python -c "t=open('conf.txt', 'r').readline(); t = t.split()[2]; open('conf.txt', 'w').write(t[1:len(t)-1]);"
release=$(cat conf.txt)
anybadge --value=$release --file=public/release.svg --label='release'
rm conf.txt
exit 0
