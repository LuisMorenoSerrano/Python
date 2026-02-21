#!/bin/bash

read -p "Introduce la versión (v.X): " version
read -p "Introduce el nombre la animación (extensión .mp4 ya incluida): " nombre_anim

python3 anim/animar.py "$version" "$nombre_anim"
