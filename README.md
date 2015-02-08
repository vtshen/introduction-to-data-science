<center>Introduction to Data Science </center>
===========

[TOC]

## Week 1: Introduction to Unix

### Lesson 1: Virtualization and Dockers

- dockerizing applications:
    - run an application: ```sudo docker run ubuntu /bin/echo 'hello world' ```
    - run "hello world" application in the background (as a **daemon**): ```sudo docker run -d ubuntu /bin/sh -c "while truel; do echo hello world; sleep 1; done" ```
    - check the log of daemonized hello world: ```sudo docker logs [ID of the container]```
    - stop the container: ```docker stop```
        
### Lesson 2: The Unix Shell

- `pwd, ls, cd`

- determine a file's type: `file [filename]`

- view a file contents encoded in ASCII code: `less`

- manipulating files and directiries: `cp, mv, mkdir, rm, ln`
    - it would be safe to use `cp -i ...` and `mv -i ...` (interactive mode)
    - be careful with `rm`! Linux does not have an undelete command! So make sure what you are going to delete (you can use `ls` to check). e.g. if you type `rm *.html` you will delete all files with a name ended with 'html', but if you mistakenly type `rm * .html`, this additional whitespace will **wipe out all of your files**! (use `ls * .html` to check in this case)
    - wildcards (used to match file names): `*, ?, [characters], [!characters], [[:class:]]`

- hard links and symbolic links 

- some reference of Linux system: http://www.tldp.org/LDP/intro-linux/html/index.html
        
### Lesson 3: Basic Unix Concepts

- working with commands
    - `type`: indicate how a command name is interpreted
    - `which`: display which executable program will be executed
    - `help`: get help for **shell builtins**
    - `man`: get the manual
    - `apropos`: display a list of appropriate commands
    - `info`: display a command's info entry
    - `whatis`: display a very brief description of a command
    - `alias`: create an alias for a command

- redirection
    - default input and output: stdin, stdout, stderr (by default both stdout and stderr are linked to the screen, and stdin attached to the keyboard)
    - redirect stdout
        - overwrite the file if existed: `ls -l /usr/bin > ls-output.txt`
        - append the output to the file: `ls -l /usr/bin >> ls-output.txt`
    - redirect stderr
        - file descriptor: 0 standard input, 1 standard output, 2 standard error
        - `ls -l /usr/bin 2> ls-output.txt`
    - redirect both stdout and stderr (two methods)
        - `ls -l /bin/usr > ls-output.txt 2>&1` where `2>&1` redirect stderror to stdout. The **order** is important!
        - `ls -l /bin/usr &> ls-output.txt`
    - disposing of unwanted output
        - redirect the output to `/dev/null` e.g. `ls -l /bin/usr 2> /dev/null`
    - redirect stdin
        - `cat`
        - pipeline: `command1 | command2` e.g. `ls /bin /usr/bin | sort | uniq | wc`
        - `wc`: word count
        - `grep [pattern] [file...]`: print lines matching a pattern, a pattern is a regular expression
        - `head/tail`: print first/last part of files
        - `tee`: read from stdin and output to **both stdout and files** (so the stdout can go down the pipeline and the intermediate stage data can be captured by files). e.g. `ls /usr/bin | tee ls.txt |grep zip`

- seeing the world as the shell sees it
    - expansion
        - pathname expansion: `echo *`, `echo [[:upper:]]*`, `echo *d`, `echo /bin/*`
        - tilde expansion: `echo ~`
        - arithmetic expansion: `echo $((2*2))`, `echo five divided by two is $((5/2))`
        - brace expansion
            - `echo front-{a..f}-back`
            - `mkdir -p playground/dir-{001..100}`, `touch playground/dir-{001..100}/file-{A..Z}` (create 2600 files!!)
        - parameter expansion: `echo $USER`, `echo $PATH`, `echo $HOME`, `echo $SHELL`, `echo $PS1` (prompt string 1, see later)
        - command substitution
            - examples: `echo $(ls)`, `ls -l $(which cp)`, `file $(ls -d /usr/bin/* | grep zip)`
            - a similar application in docker: `docker stop $(docker ps -a -q)` (it stops all containers)
            - note: `ls | echo` is not equivalent to `echo $(ls)` because the input of `echo` cannot be the standard input, it should be some arguments. we can use `xargs` to convert it to `ls | xargs echo`, which is equivalent to `echo $(ls)`
    - quoting
        - double quotes: `ls -l "two words.txt"`, `echo "$((2+2)) $PATH" ` 
        - single quotes: `echo '$((2+2)) $PATH'` (single quotes **supress the expansion**)
        - escaping characters: `echo this is \$5.00` (so the expansion is suppressed)
        
- advanced keyboard tricks
    - command line editing
    - completion: using `tab`
    - using bash `history`: `!!`, `!number`, `!string`, `!?string`
    
- permissions
    - Linux is a **multi-user** system
    - owners, group members and everybody else
    - reading writing and executing
        - `ls -l` shows the information of files: the first ten characters are the **file attributes** (consist of the file type and the permission attrs)
        - `chmod`
        - `umask`: default permission mode
    - changing identities
        - `su`
            - start an interactive command: `su [-[l]] [user]` (enter `exit` to log out)
            - execute a single command: `su -c 'command' `
        - `sudo`
        - `chown`, `chgrp`
    - exercising our privileges
    - changing your password
    
- processes
    - viewing processes
        - `ps`, `ps x`, `ps aux`, `top`, `jobs`
    - controlling processes
        - `bg, fg`
        - `kill, killall`
        - `shutdown`
            
## Week 2: Introduction to CLI Data Science

### Lesson 1: Unix File Processing and Management

- the environment
    - shell variables (data placed by `bash`), and environment variables (everything else)
    - `printenv`: print part or all of the environment
        - `printenv | less`
        - `printenv $USER`
    - `set`: display both the shell and environment variables, as well as defined shell functions
    - `alias`
        - show all alias defined in shell
        - create an alias for a command
    - how it the environment established? 
        - startup files: in `/etc` and the user's home directory, used to configure the environment
    - modifying the environment
        - which files should we modify?
        - text editors
    - `export`: export environment to subsequently executed programs
    
- a gentle introduction to vi
    - quit and save: `:q!`, `:w`, `ZZ`, `:wq`
    - moving the cursor: `0`, `^`, `$`, `w`, `W`, `b`, `B`, `5G`, `G`, `hjkl`
    - basic editing
        - appending text: `a`, `A`
        - opening a line: `o`, `O`
        - deleting text: `x`, `3x`, `dd`, `5dd`, `dW`, `d$`, `d0`, `d^`, `dG`, `d20G`
        - undo and redo: `u`, `ctrl+r`
        - copying: (basically same with deleting): `yy`, `5yy`, `yW`, `y$`, `y0`, `y^`, `yG`, `y20G`
        - pasting: `p`, `P`, `5p`
        - joining lins: `J`
    - search and replace
        - searching within a line: `fa`
        - searching the entire file: `/` (together with strings or regular expressions)
        - global search and replace
            - an example: `:%s/Line/line/g`
                - `%`: specify the range of this operation
                - `s`: specify the operation: substitution
                - `/Line/line/`: the search pattern and the replacement text
                - `g`: "global" option
    - editing multiple files
        - `n`, `N`, `buffers`
        - opening additional files for editing: `:e`
        - copying content from one file into another
        - inserting an entire file into another: `:r`
        
- networking
    - examining and monitoring a network
        - `ping`: sends a special network packet called **IMCP ECHO_REQUEST** to a specified host and get responses, see if some packets are lost
        - `traceroute`: trace all network "hops"
        - `netstat`: examine various network settings and statistics
    - transporting files over a network
        - `ftp` and `lftp`: trasmitting everything in clear text, not secure
        - `wget`: download content from both web and FTP sites
    - secure communication with remote hosts
        - `ssh`: log into a remote machine and execute commands there
        - `scp` and `sftp`
        
- searching for files
    - `locate`: find files by name
        - e.g. `locate bin/zip`
    - `find`: find files the hard way
        - lots of **tests** we can use, such as file type, name, size, permission, user etc
            - e.g. `find ~ -type f -name "*.jpg" -size +1M -perm 0600 -user me | wc -l`
        - operators: describe the **logical relationships** between the tests
            - e.g. `find ~ \( -type f -not -perm 0600 \) -or \( -type d -not -perm 0700 \)`
        - predefined actions: doing something on the matching files
            - some actions: `-delete`, `-ls`, `-print` (default option), `-quit`
            - e.g. `fubd ~ -type f -name '*.BAK' -delete`
        - user-defined actions: `-exec command '{}' ';' ` or `-ok command '{}' ';' ` (with prompted to confirm)
            - e.g. `find ~ -type f -name 'foo*' -exec ls -l '{}' ';'`, `find ~ -type f -name 'foo*' -ok ls -l '{}' ';'`
        - improving efficiency
            - e.g. `find ~ -type f -name 'foo*' -exec ls -l '{}' '+'`
        - `xargs`: accept input from **standard input** and convert it into **an argument list** for a specific command
            - e.g. `find ~ -type f -name 'foo*' | ls -l` is wrong, because `ls` does not accept the standard input as its input. So we need to convert it as `find ~ -type f -name 'foo*' | xargs ls -l`
        - options: control the scope of the search
            - `-depth`, `maxdepth [levels]`, `mindepth [levels]`, `-mount`
            
- customizing the prompt
    - anatomy of a prompt
        - `echo $PS1`: display this prompt string 1, we can change it to anything we like and add colors
        
### Lesson 2: Unix Data Processing

- archiving and backup
    - compressing files
        - `gzip` and `gunzip`
        - `bzip2` and `bunzip2`
    - archiving files
        - `tar`
        - `zip`: mainly used to exchange files with Windows system
    - synchronizing files and directories
        - `rsync [options] [source] [destination]` (where source or dest could be either local files or remote files)
            - e.g. `rsync -av /bin /etc /backup` (here we backup /bin and /etc to /backup directory)
            - to make it simple, we can use an alias: `alias backup='rsync -av /bin /etc /backup'`
        - using `rsync` over a network
        
- regular expressions
    - `grep`
        - function: output any lines that contain the specified regular expression
    - metacharacters and literals
    - any character: `.`
    - anchors: `^` (beginning of the line), `$` (end of the line)
        - e.g. `^.zip`
    - bracket expressions and character classes
        - e.g. `[bg]zip`
        - negation: `[^bc]zip`
        - traditional character ranges: `[A-Za-z0-9]`, `[a-d]zip`
        - POSIX character classes: `[:alnum:]`, `[:word:]`, `[:alpha:]`, `[:lower:]`, `[:upper:]`, etc
    - POSIX basic (BRE) vs extended regular expressions (ERE)
        - BRE metacharacters include `^ $ . [ ] *`, all others are literals
        - additional metacharacters in ERE are `( ) { } ? + |`
        - we need to use `grep -E` when using ERE   
            - e.g. `ls /bin | grep -Eh '^(bz|gz|zip)'`
        - `? + *` and `{}`: specify the **number of times** an element is matched
    - putting regular expressions to work
        - `find` with RE (using `-regex` option)
            - note the difference between `find` and `grep`: `find` gets the pathnames **exactly matching** the RE, while `grep` gets the   lines **containing** the RE
            - e.g. `find . -regex '.*[^-_./0-9A-Za-z]'`, it finds all "bad" pathnames
        - `locate` with RE
        - searching for text in `less` and `vim`
        
- text processing
    - revisiting some old friends
        - `cat`
            - `-A`: show all characters including non-printing ones
            - `-n`: show line numbers
            - `-s`: suppress the output of blank lines
        - `sort`
            - e.g. sort and merge: `sort file1 file2 file3 > final_sorted_file`
            - some interesting options: `-n`, `-k` (sorted based on a key field), `-t`
        - `uniq`
            - perform on a **sorted** file
    - slicing and dicing
        - `cut`
            - `-c` (char_list), `-f` (field_list), `-d` (define delimiting character), `--complement`
            - e.g. `cut -f 3 distro.txt | cut -c 7-10`, `cut -d ':' -f 1 /etc/passwd`
        - `paste`: merge lines of files
        - `join`: join data from multiple files based on a **shared key field**
    - comparing text
        - `comm`
        - `diff`
            - `-c` (context format)
        - `patch`
            - accepts output from `diff` and applies changes to text files
            - it would be very efficient to use `diff/patch`, especially when the original text files are large and the `diff` files are relatively small (especially useful for collaborative software developing)
    - editing on the fly
        - `tr`: transliterate characters
            - e.g. `echo "lowercase letters" | tr a-z A-Z`, `-s` (delete repeated instances)
        - `sed`: stream editor, very powerful and complicated
            - e.g. `echo "front" | sed '1s/front/back/g'`
                - explain: `1` is the first line (range), `s` means substitution (operation), `front` and `back` are the args of the operation, `g` means that the substitution is global
            - address notation: specifies the **range of the operation**
                - line range, regular expressions, etc
                - e.g. `sed -n '/SUSE/p' distros.txt` (where /SUSE/ is the regular expression notating the address)
            - basid editing commands: specifies the operation
                - output, append, delete, insert, print, quit, substitute, transliterate, etc
            - more complex editting: `sed` script with option `-f`
        - `aspell`: interactive spelling checker
            - e.g. `aspell check foo.txt`

- writing your first script
    - how to write a shell script
        - write a script
        - make the script executable
        - put the script somewhere the shell can find it
    - script file format
        - an example (saved as `hello_world`)
        ```
        #!/bin/bash
        # this is a script
        echo 'hello world!'
        ```
    - executable permissions
    - script file location
        - we can execute the previous program by `./hello_world`
        - if we want to use `hello_world` to execute it, we need to add the current directory to `$PATH`, or move this script to one of the `$PATH` directories
    - more formatting tricks
        - long option names
            - e.g. `ls -a` vs `ls --all`
        - indentation and line-continuation: make scripts more readable by using indentation (using `\` to continue a line)
        
- `awk` tutorials
    - what is `awk`?
        - a programming language that allows easy manipulation of structured data and the generation of formatted reports
    - syntax: `awk '/search_pattern_1/ {action_1} /search_pattern_2/ {action_2} ...' file`
        - search patterns: regular expressions
        - several patterns and actions are possible
        - either search patterns or actions are **optional**, but not both
            - no pattern: action on all lines
            - no action: printing the matching lines
        - each statement in actions should be delimited by `;`
    - powerful awk built-in variables: `FS, OFS, RS, ORS, NR, NF, FILENAME, FNR`
        - see http://www.thegeekstuff.com/2010/01/8-powerful-awk-built-in-variables-fs-ofs-rs-ors-nr-nf-filename-fnr/
    - 7 Powerful Awk Operators Examples (Unary, Binary, Arithmetic, String, Assignment, Conditional, Reg-Ex Awk Operators)
        - see http://www.thegeekstuff.com/2010/02/unix-awk-operators/
    - awk conditional statements
        - see http://www.thegeekstuff.com/2010/02/awk-conditional-statements/
        
### Lesson 3: Source Code Control with Git & GitHub

- getting started (http://git-scm.com/book/en/v1/Getting-Started-Installing-Git)
    - about version control
        - local version control systems
        - centralized version control systems 
        - distributed version control systems
    - a short history of Git
    - Git basics
        - snapshots, not differences
        - nearly every operation is local
        - Git has integrity
        - Get generally only adds data
            - we can easily undo operations and recover data
        - the three states
            - working directory, staging area, repository (git directory)
    - installing git
    
- Git basics
    - getting a Git repository
        - initializing a repository in an existing directory
            - go to the project's directory and `git init`, `git add`
        - cloning an existing repository: `git clone [url]`
    - recording changes to the repository
        - `git status`, `git diff`
        - `git commit`
        - ignoring files: by editing `.gitignore` file
        - `git rm`, `git mv`
    - viewing the commit history
        - `git log`
            - `git log -p`: show the difference
            - `git log --pretty=format:"%h - %an, %ar : %s"`: formatting output
            - `git log --since=2.weeks`: limiting log output
    - undoing things
        - changing your last commit: `git commit --amend`
        - unstaging a staged file: `git reset HEAD <file>`
        - unmodifying a modified file: `git checkout -- <file>`
    - working with remotes
        - showing your remotes: `git remote -v`
        - adding remote repositories: `git remote add [shortname] [url]`
            - e.g. `git remote add origin https://github.com/weiHelloWorld/python.git`
        - fetching and pulling from your remotes: `git fetch [remote-name]`
        - pushing to your remotes: `git push [remote-name] [branch-name]`
            - e.g. `git push origin master`
        - removing and renaming remotes
    - tagging
    - tips and tricks
        - auto completion
        - Git aliases

- Git branching
    - (there are lots of diagrams in this chapter, so refer to http://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell/)
    
- GitHub

## Week 3: Introduction to iPython

### Lesson 1: Working with the iPython Notebook

### Lesson 2: Introduction to Python Programming

- reference for python
    - http://www.diveintopython3.net/index.html
    - http://faculty.stedwards.edu/mikek/python/thinkpython.pdf

### Lesson 3: Python Functions

## Week 4: Introduction to Python Programming

### Lessom 1: Python Data Structures

- string

- lists
    - note that list is mutable, while string is immutable
    - shallow copy and deep copy of a list
        - shallow copy: `b = a`
        - deep copy: `b = a[:]`
    - when a list is used as an argument, it is **passed by reference**, so it may be modified in the process
    
- dictionaries
    - the order of items is unpredictable
    - global variable
        - to reassign a global variable **inside a function** we need to **declare** the global variable before you use it, e.g.
        ```python
        count = 0
        
        def example():
            global count # in this way, count will be referred to the global variable within this function
            count += 1
        ```
    - `hash` function
    
- tuples
    - tuples are immutable
    - variable-length argument tuples
        - the parameters should begin with '*', e.g.
        ```python
        def printall(*args):
            print(args)
        ```
    - lists and tuples
        - `zip`
    - dictionaries and tuples
        - `items`
    - sequences of sequences
    
### Lesson 2: Working with the Underlying File System

- files
    - reading from text files
        - character encoding
        - `open`, `read`, `seek`, `close`
        - closing files automatically
            - `try...finally` approach: good
            - `with` approach: better! see this example:
            ```python
            with open("temp.txt") as a_file:
                a_file.seek(17)
                a_character = a_file.read(1)
                print(a_character)
            # when this block ends, the with statement will close the file automatically, no matter what exception happens
            ```
        - read one line at a time
    - writing into text files
        - two modes: `a`, `w`
    - binary files
    - stream objects from non-file sources
        - handling string
        ```python
        a = 'hello'
        import io
        b = io.StringIO(a)
        b.write('df') # modify the first two characters of this string
        b.seek(0) # go to the beginning of this string
        b.read()
        b.write('df') # now append 'df' to the end of this string
        b.seek(0) 
        b.read()
        ```
        - handling compressed files
    - standard input, output and error
        - `sys.stdin`, `sys.stdout`, `sys.stderr`: similar to those in Linux (see "redirection" in Week 1 Lesson 3), see example:
        ```python
        import sys
        sys.stdout.write("abc")
        sys.stderr.write("dfsfsd")
        ```
        - redirecting standard output
        
### Lesson 3: Advanced Concepts

- 
