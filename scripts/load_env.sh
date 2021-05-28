#!/usr/bin/env bash
cat .env | grep -vE "^(#.+)?$" | while read line; do
	echo $line
	export $line
done
