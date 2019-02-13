#!/bin/zsh
SESSIONNAME="gnet"

tmux new-session -d zsh

tmux split-window -v 'python3 -m connectors.console'
tmux split-window -h 'python3 -m core.mux.MUX'
tmux split-window -h 'python3 -m core.modules.logger'
tmux split-window -h 'python3 -m core.modules.echo'
tmux split-window -h 'python3 -m core.dmx.DMX'
tmux split-window -v 'python3 config_server.py'

tmux attach-session -d
