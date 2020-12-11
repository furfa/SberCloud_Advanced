#! /bin/bash

cd /home/furfa/work/ege_project

source env/bin/activate      

echo "" >> parse_log;

date >> parse_log;

python university/ifmo/prep_ifmo.py && echo "ifmo ok" >>  parse_log;

python university/nsu/nsu.py && echo "nsu ok" >>  parse_log;

python university/spbu/spbu.py && echo "spbu ok" >>  parse_log;

python university/nstu/parser.py && echo "nstu ok" >>  parse_log;

python university/sibsutis/sibsutis.py && echo "sibsuits ok" >>  parse_log;

python university/stu/parser.py && echo "stu ok" >>  parse_log;

python university/admlist.py && echo "admlist ok" >>  parse_log;

python yadisk_sync.py --sync_uni && echo "sync ok" >> parse_log;

python read_data.py && echo "compile ok" >> parse_log;

python yadisk_sync.py --upload_state && echo "upload_state ok" >> parse_log;

