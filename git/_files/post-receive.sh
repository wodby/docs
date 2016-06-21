#!/bin/sh
while read oldrev newrev ref
do
    curl -H "Content-type: application/json" -X POST -d '{"ref": "'"$ref"'"}' <WEBHOOK URL>
done
