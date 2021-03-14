#!/bin/bash

# Name selection
while [[ -z $name ]] ; do
    read -e -p "Enter a name: " name
done

[[ -e "$name" ]] && echo "File or directory '$name' already exists." && exit 1


# Language selection
LANGUAGES=(
    Python
    C
    CPP
)

declare -A EXTENSIONS=(
    ["Python"]="py"
    ["C"]="c"
    ["CPP"]="cc"
)


language=$(selector "Enter a language:" ${LANGUAGES[*]})


# Git option
[[ "$(read -e -p 'Init a git repository? [Y/n]: '; echo $REPLY)" == [Nn]* ]] || has_git='true'


# License selection
[[ -z $SHARE ]] && SHARE="$HOME/.local/share/"  # If none supplied, use default
SHARE=$(realpath $SHARE)
if [[ -d "$SHARE/HB/licenses" ]] ; then
    LICENSES=`for entry in $SHARE/HB/licenses/*; do echo ${entry##*/}; done`
    license=$(selector "Select a license:" ${LICENSES[*]})
else
    echo "License folder not found."
fi


# Confirmation
echo
echo "Name: $name"
echo "Language: $language"
echo -n "Git: "; [[ -n "$has_git" ]] && echo "Yes"  || echo "No"
echo "Licence: $license"
[[ "$(read -e -p 'Create project? [Y/n]: '; echo $REPLY)" == [Nn]* ]] && echo "Aborting..." && exit 0


# Create it!
echo
mkdir $name && cd $name
[[ -n "$has_git" ]] && git init && touch .gitignore
touch README.md
cp $SHARE/HB/licenses/$license LICENSE
mkdir src && cd src

cp $SHARE/HB/mainfiles/$language "$name.${EXTENSIONS[$language]}"