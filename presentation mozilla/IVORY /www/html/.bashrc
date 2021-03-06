# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
PATH=/usr/java/jdk1.7.0_51/bin:$PATH:/root/Desktop
export JAVA_HOME=/usr/java/jdk1.7.0_51
