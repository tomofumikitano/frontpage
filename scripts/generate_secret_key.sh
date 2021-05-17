#!/usr/bin/env bash

SECRET_KEY_LENGTH=50

printf -v chars "%s%s" {a..z} {A..Z} {0..9} "!#$%&()-^_~[]{}+*;"
chars_len=${#chars}

result=''
for (( i = 0; i < SECRET_KEY_LENGTH; i++ )); do
	idx=$(( RANDOM % chars_len ))
	c=${chars:$idx:${idx+1}}
	result+=$c
done

# export SECRET_KEY="$result"
echo "$result"

# Reference:
# https://stackoverflow.com/questions/61590006/generate-random-string-where-it-must-have-a-special-character-in-shell-script
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
