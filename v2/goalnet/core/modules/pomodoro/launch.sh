
#!/bin/sh
echo "starting pomodoro module"

UTILS=utils__.py
#GLOBAL_UTILS=/home/danlkv/GoalNet/v2/utils.py
GLOBAL_UTILS=$GNET_ROOT/utils.py

if [ ! -e $UTILS ]; then
    echo "No utils file, linking from $GLOBAL_UTILS"
    ln -s $GLOBAL_UTILS $UTILS
fi

PYTHONPATH=$PYTHONPATH:$GNET_ROOT/core/modules:/home/danlkv/GoalNet/v2/core/modules python3 main.py

