#!/bin/bash

PASSED="passed"
mkdir public
pycodestyle ../ --count -qq &> public/pycodestyle.txt
if [[ -s public/pycodestyle.txt ]]
then PASSED="failed"
fi
anybadge --label=pep8 --value="$PASSED" --file=./public/pep8.svg passed=green failed=red
exit 0
