#!/bin/bash

filename=$1
outfilename=$2
hosts=()

function get_users {
    local host="$1"
    local tmpout="$host.out"
    echo "===============================" > "$tmpout"
    echo "host: $host" >> "$tmpout"
    ssh -n -o BatchMode=yes $line "last | head -n -2 | grep -v 'reboot' | awk '{print \$1}' | head -n 5" >> "$tmpout"
}

if [[ -n "$filename" ]] && [[ -n "$outfilename" ]]; then
    while IFS= read -r line; do
        hosts+=("$line")
        get_users "$line" &
    done < "$filename"
else
    echo "no argument found, please provide file with hosts and output file"
    echo 'syntax: last5users.sh <hosts_file> <out_file>'
    exit
fi

wait

for host in "${hosts[@]}"; do
    tmpout="$host.out"
    cat "$tmpout"
    rm -f "$tmpout"
done > "$outfilename"
