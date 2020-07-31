#!/bin/bash
echo "Setting ~/.bashrc and ~/.bash-git-prompt"
cat .devcontainer/.bashrc > /root/.bashrc
git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt