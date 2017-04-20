```
$ pip freeze > requirements.txt
This will create a requirements.txt file, which contains a simple list of all the packages in the current environment, and their respective versions. You can see the list of installed packages without the requirements format using “pip list”. Later it will be easier for a different developer (or you, if you need to re-create the environment) to install the same packages using the same versions:

$ pip install -r requirements.txt
```


```bash
// You should install protobuf compiler. On OS X you can do it with command
brew install protobuf

// Install library 
pip install protobuf3

// Compile the schema
protoc --python3_out=$DEST_DIR foo.proto
```

alias less='less -r'
02	# --show-control-chars: help showing Korean or accented characters
03	alias ls='ls -F --color --show-control-chars'
04	alias ll='ls -l'
05	alias gs='git status '
06	alias ga='git add '
07	alias gb='git branch '
08	alias gc='git commit'
09	alias gd='git diff'
10	alias go='git checkout '
11	alias gk='gitk --all&'
12	alias gx='gitx --all'