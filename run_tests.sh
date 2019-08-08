#!/bin/bash
# Find the executable
if [ $(uname) = 'Darwin' ]; then
    SOURCE_DIR=\$(greadlink -f \$0)
else
    SOURCE_DIR=\$(readlink -f \$0)
fi
SCRIPT_PATH=\${SOURCE_DIR%/*}
cd \$SCRIPT_PATH
set -e
PRINT_COV=true
testpath="discover -s tests/"
if [ -e "tests/test_\$1.py" ]; then
    testpath="tests/test_\$1.py"
    PRINT_COV=false
fi
PYTHONWARNINGS="ignore" python3 -m coverage run --source=. -m unittest \$testpath >/dev/null
if \$PRINT_COV ; then
    python3 -m coverage html
    python3 -m coverage report -m
fi
