#!/bin/bash
export PYTHONPATH=$PYTHONPATH:`pwd`/..
for theme in `python doc.py`;
do
    [ -e "$theme.png" ] && continue;
    nohup python markment/bin.py -t $theme -s ../spec 2>&1>/dev/null &
    sleep 5
    (python screenshot.py $theme 2>&1>/dev/null) 2>&1>/dev/null
    echo "Done with $theme"
    bye python
done

say "Done with screenshots"
