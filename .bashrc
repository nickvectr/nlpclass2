ls --color=al > /dev/null 2>&1 && alias ls='ls -F --color=al' || alias ls='ls -Gp'

git_branch () { git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'; }
USER='\[\e[0;38;05;196m\]\u'
HOST='@\[\e[0;38;05;196m\]\h'
TIME='\[\e[0;38;05;242m\]\t ' #\033[01;32m\]'
LOCATION=' \[\e[0;38;05;069m\]`pwd | sed "s#\(/[^/]\{1,\}/[^/]\{1,\}/[^/]\{1,\}/\).*\(/[^/]\{1,\}/[^/]\{1,\}\)/\{0,1\}#\1_\2#g"`'
BRANCH=' \033[00;33m\]$(git_branch)\[\033[00m\]\n\[\e[0;38;05;002m\]#> \[\e[0m\]' #\[\e[0;38;05;161m\]'
PS1=$TIME$USER$HOST$LOCATION$BRANCH
