#!/usr/bin/env bash
SESSION="node"

tmux -2 new-session -d -s $SESSION

tmux new-window -t $SESSION:1 -n 'node'
tmux split-window -v
tmux select-pane -t 1
tmux send-keys "nload" C-m
tmux select-pane -t 0
tmux send-keys "docker stats $1" C-m
tmux select-pane -t 1
tmux send-keys C-Right

# Set default window
tmux select-window -t $SESSION:1

# Attach to session
tmux -2 attach-session -t $SESSION
