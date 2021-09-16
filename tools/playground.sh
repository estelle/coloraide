#!/bin/bash
rm docs/src/markdown/playground/*
markdown=https://files.pythonhosted.org/packages/6e/33/1ae0f71395e618d6140fbbc9587cc3156591f748226075e0f7d6f9176522/Markdown-3.3.4-py3-none-any.whl
pymdownx=https://files.pythonhosted.org/packages/35/fa/6631b9aeb25e1bb62bf77c48c86b1677da98a52360cb9b5559dda8d08edb/pymdown_extensions-8.2-py3-none-any.whl
curl -sL ${markdown} -o docs/src/markdown/playground/$(basename ${markdown})
curl -sL ${pymdownx} -o docs/src/markdown/playground/$(basename ${pymdownx})
python3 -m build --wheel -o docs/src/markdown/playground/
cwheel=(docs/src/markdown/playground/coloraide*.whl)
mwheel=(docs/src/markdown/playground/Markdown*.whl)
pwheel=(docs/src/markdown/playground/pymdown_extensions*.whl)
input="tools/playground_pyodide.py"
output="docs/src/markdown/.snippets/playground.txt"
sed "s/^cwheel = .*$/cwheel = '${cwheel##*/}'/;\
s/^mwheel = .*$/mwheel = '${mwheel##*/}'/;\
s/^pwheel = .*$/pwheel = '${pwheel##*/}'/;\
s/\\\\/\\\\\\\\/g;s/\`/\\\\\`/g" $input > $output
