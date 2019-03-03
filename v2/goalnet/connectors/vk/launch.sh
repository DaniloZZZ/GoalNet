#!/bin/sh
echo "starting vk connector"

UTILS=utils__.py
GLOBAL_UTILS=/home/danlkv/GoalNet/v2/utils.py

if [ ! -e $UTILS ]; then
    echo "No utils file, linking from $GLOBAL_UTILS"
    ln -s $GLOBAL_UTILS $UTILS
fi

PYTHONPATH=$PYTHONPATH:/home/danlkv/GoalNet/v2 python3 main.py

