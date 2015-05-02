<center>Introduction to Data Science </center>
===========

## Week 1: Introduction to Unix

### Lesson 1: Virtualization and Dockers

- dockerizing applications:
    - run an application: `sudo docker run ubuntu /bin/echo 'hello world' `
    - run "hello world" application in the background (as a **daemon**): `sudo docker run -d ubuntu /bin/sh -c "while truel; do echo hello world; sleep 1; done" `
    - check the log of daemonized hello world: `sudo docker logs [ID of the container]`
    - stop the container: `docker stop`
        
### Lesson 2: The Unix Shell

- `pwd, ls, cd`

- determine a file's type: `file [filename]`

- view a file contents encoded in ASCII code: `less`

- manipulating files and directiries: `cp, mv, mkdir, rm, ln`
    - it would be safe to use `cp -i ...` and `mv -i ...` (interactive mode)
    - be careful with `rm`! Linux does not have an undelete command! So make sure what you are going to delete (you can use `ls` to check). e.g. if you type `rm *.html` you will delete all files with a name ended with 'html', but if you mistakenly type `rm * .html`, this additional whitespace will **wipe out all of your files**! (use `ls * .html` to check in this case)
    - wildcards (used to match file names): `*, ?, [characters], [!characters], [[:class:]]`

- hard links and symbolic links 

- reference
    - http://www.tldp.org/LDP/intro-linux/html/index.html (about Linux system)
        
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
        - use `sudo updatedb` to update the database for `locate`
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
        ```shell
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

- comprehensions
    - working with files and directories
        - `os`, `os.path` module
    - list/directory/set comprehensions
        ```python
        a = range(10)
        [element ** 2 for element in a if element > 5]
        ```

- regular expressions
    - an example: matching phone numbers
    ```python
    import re
    phonePattern = re.compile(r'^\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$') # \D matches any non-numeric character, \D* is used as an optional separator
    phonePattern.search('(800)123-3453 ext 1234').groups() # groups patterns in the string
    ```
    
- classes and objects
    
- classes and functions
    
- classes and methods
    - some special methods: `__init__`, `__str__`, `__doc__`, `__iter__`, `__next__` (the last two are for **iterators**)
    - operator overloading: e.g. `__add__`
    - type-based dispatch
    - polymorphic functions: functions that can work with several types
    
- inheritance

## Week 5: Introduction to Visualization

### Lesson 1: Introduction to Numpy

- the basics
    - the Numpy's main object is the **homogeneous multidimensional array**, it belongs to class `numpy.ndarray` (or `numpy.array`)
    - attributes of array: `ndim`, `shape`, `size`, `dtype`, `itemsize`, `data`
    - creating array: `array([1,2,4])`, `zeros`, `linspace`, `arange`, `reshape`, etc
    - basic operations
    - universal functions: `sin`, `cos`, `exp`, etc
    - indexing, slicing and iterating
        - boolean indexing (also very useful in `pandas`)
        ```python
        import numpy
        A = numpy.arange(10)
        c = (A < 5) & (A > 1)
        A[c]
        ```
        - list-of-locations indexing
    
- shape manipulation
    - changing the shape of an array
        - `ravel()`, `transpose()`, `resize()`, `reshape()`
    - stacking together different arrays
        - `hstack`, `vstack`, `column_stack`, `row_stack`
    - splitting one array into several smaller ones
    
- copies and views
    - no copy at all: same array object
        - `b = a` (we can see `b` as a new pointer to object referred by `a`)
    - `view` or shallow copy: different array objects, share the same data
    - deep copy: different array objects and different copies of data
    
### Lesson 2: Introduction to Python Plotting with Matplotlib

- pyplot tutorial
    - two kinds of API
        - MATLAB API
            - easy to use for simple plots, but not recommended
            ```python
            import matplotlib.pyplot as plt
            x = plt.linspace(0, 5, 10)
            y = x ** 2
            plt.figure()
            plt.plot(x, y, 'r')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('title')
            plt.show()
            ```
            - note that Matlab and pyplot have the concept of **the current figure and the current axes** (important for MATLAB API)
        - matplotlib object-oriented API
            - recommended, more powerful
            - key idea: no objects, no program states should be **global**, much better especially when there are multiple figures
            ```python
            %matplotlib inline
            import numpy as np, matplotlib.pyplot as plt
            fig, ax = plt.subplots() # create a figure and axes for plotting
            x = np.arange(0, 10, .1)
            ax.plot(x, x ** 2, '-')
            plt.show()
            ```
    - controlling line properties
    - working with multiple figures and axes
    - working with text
        - using mathematical expressions in text
        - annotating text
    - saving your plot: `savefig`
    - scatter plots
    - legends, labels and titles
    - formatting text: LaTeX, fontsize, font family
        - when using LaTeX, we should use raw text strings, like `label = r"$\alpha^2$"` instead of `label = "$\alpha^2$"`
    - reference
        - http://matplotlib.org/users/pyplot_tutorial.html (mainly about MATLAB API)
        - http://nbviewer.ipython.org/github/ProfessorBrunner/lcdm-info/blob/master/info490nb/info490w5m1.ipynb
        - http://nbviewer.ipython.org/github/ProfessorBrunner/lcdm-info/blob/master/info490nb/info490w5m2.ipynb (about scatter plots)
        - http://nbviewer.ipython.org/github/jrjohansson/scientific-python-lectures/blob/master/Lecture-4-Matplotlib.ipynb (very detailed instructions about matplotlib plotting)
        
### Lesson 3: Making Data Visualizations in Python

- histograms
    - binning
        - options: number, center, color, etc
    - four types: `bar`, `barstacked`, `step`, `stepfilled`
    - logarithm plot: `log` option
    - probability: `normed` option
    - multiple histograms
        - overlap multiple histograms (use `alpha` option when needed)
        - plot multiple histograms side by side
    - return values of `hist`: `n, bins, patches`
    - reference
        - http://nbviewer.ipython.org/github/ProfessorBrunner/lcdm-info/blob/master/info490nb/info490w5m3.ipynb
        
- seaborn
    - `matplotlib` is useful, but not very satisfactory, `seaborn` provides an API on top of `matplotlib` which uses sane plot & color defaults, uses simple functions for common statistical plot types, and which integrates with the functionality provided by `pandas` dataframes.
        
- data looks better naked
    - remove redundancy!
    - reference
        - http://darkhorseanalytics.com/blog/data-looks-better-naked/
        
## Week 6: Introduction to Data Analysis in Python

### Lesson 1: Data Access and Selection

- pandas overview
    - basic data structure: Series, TimeSeries, DataFrame, Panel
        - built on top of `NumPy`, so they are fast
        - DataFrame is the container for Series, and Panel is the container for DataFrame
    - mutability and copying of data
        - all pandas data structures are **value-mutable** but not always **size-mutable**
    - object creation
    - viewing data
    - selection
        - standard numpy/python way of selecting data
            - selection by label, position, boolean indexing etc
        - pandas access methods: `.at`, `.iat`, `.loc`, `.iloc`, `.ix`
    - missing data: `np.nan`
    - operations
        - stats
        - applying functions to data: `apply`
        - histogramming: `value_counts`
        - string methods
    - merge
        - `concat`
        - `merge`
        - `append`
    - grouping: `groupby`, `aggregate`
    - reshaping
    - time series
    - categoricals
    - plotting
    - getting data in/out from csv files
        - load data using `pd.read_csv` function (specifying separators, encoding, date forms etc.)
    - reference
        - http://pandas.pydata.org/pandas-docs/stable/overview.html (brief overview)
        - http://www.gregreda.com/2013/10/26/intro-to-pandas-data-structures/ (detailed discussion of data structures)
        - http://pandas.pydata.org/pandas-docs/stable/10min.html (a good introduction to various features in pandas in 10 mins)
        - https://github.com/jvns/pandas-cookbook (chapter 1 & 2 here)
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week09/intro2pandas.ipynb (another introduction to pandas)
        
### Lesson 2: Data Manipulation and Analysis

- some examples
    - Which borough has the most noise complaints (or, more selecting data)
        - boolean indexing
        - `value_counts`
    - Find out on which weekday people bike the most with `groupby` and `aggregate`
        - two arguments when parsing dates: `parse_dates=['Date'], dayfirst=True`, so that we can use the functionality related to dates and time
        - use of `groupby` and `aggregate`: `weekday_counts = berri_bikes.groupby('weekday').aggregate(sum)`
    - Combining dataframes and scraping Canadian weather data
        - clear null data: `weather_mar2012.dropna(axis=1, how='any')` (drop any data that are emtpy, `axis = 1` means drop columns instead of rows)
        - drop data: `weather_mar2012.drop(['Year', 'Month', 'Day', 'Time', 'Data Quality'], axis=1)`
    - String Operations- Which month was the snowiest
        - conversion and resampling of regular time-series data using `resample`
            - `weather_2012['Temp (C)'].resample('M', how=np.median).plot(kind='bar')`
            - `is_snowing.astype(float).resample('M', how=np.mean).plot(kind = 'bar')`
    - Cleaning up messy data
    - reference
        - https://github.com/jvns/pandas-cookbook (chapter 3-8 here)

### Lesson 3: Summary Statistics

- think stats (http://www.greenteapress.com/thinkstats/thinkstats.pdf)

- simple statistics with scipy
    - introduction
        - scipy is built on top of Numpy and therefore we can use all array manipulation and indexing methods provided by Numpy.
    - descriptive statistics
        - generate random numbers from a standard Gaussian: `sp.randn(100)`
        - min, max, median, var, etc.
    - probability distributions
        - Scipy has functions that deal with at lease 81 common probability distributions.
        - e.g. `n = stats.norm(loc=3.5, scale=2.0)` (here `loc` is mean, `scale` is standard deviation)
    - probability density function (PDF) and probability mass function (PMF)
    - cumulative density function (CDF)
    - Percent point function (PPF) or inverse cumulative function
    - Survival function (SF)
    - Inverse survival function (ISF)
    - Random variates
        - we can draw values from a distribution using `rvs`.
        - e.g. `sp.stats.poisson.rvs(1.0, size = 100) # 100 random values from a Poisson distribution with mu = 1.0`
    - reference
        - https://oneau.wordpress.com/2011/02/28/simple-statistics-with-scipy/
        
## Week 7: Introduction to Statistical Analysis

### Lesson 1: Rules of Probability Theory

- Bayes theorem
    - diachronic interpretation: probability information gets updated when new evidence come in. prior probability -> posterior probability (probability changes over time)

- computational statistics

- estimation
    - the locomotive problem
        - description: "A railroad numbers its locomotives in order 1..N. One day you see a locomotive with the number 60. Estimate how many locomotives the railroad has."
        - the estimation depends both on prior probability (uniform prior from 1 to 1000, or power law prior) and number of data (in this question, we have only a data point, increasing the number of data would significantly make the estimation more convincing and less dependent on the prior you choose)
    - credible intervals
    - informative prior vs. uninformative prior

- reference
    - http://www.greenteapress.com/thinkbayes/thinkbayes.pdf (Chapter 1-3)

### Lesson 2: Statistical Decision Making

- hypothesis testing
    - introduction
        - when we see some "apparent effects" in a data set, the first question to ask is whether they are real or simply occurred by chance
        - general structure to test **statistical significance** (similar to proof by contradiction)
            - null hypothesis
            - p-value
            - interpretation
    - testing a difference in means
    - choosing a threshold
        - Type I error (false positive), and Type II error (false negative)
        - choose a threshold $\alpha$, to determine whether to accept the hypothesis based on whether p-value is less than $\alpha$
        - obviously the false positive in this case is $\alpha$. By decreasing $\alpha$, we can decrease false positive, but we increase false negative, so there is a **tradeoff between Type I and Type II errors**
    - defining the effect
        - two-sided test and one-sided test
    - interpreting the result
        - three ways of interpretation
            - classical: simply compare p-value and $\alpha$ and get the result
            - practical: report p-value without apology, readers interprete the data themselves
            - Bayesian: let $H_0$ and $H_A$ to be the hypothesis that the effect is not real and that the effect is real. the evidence (data set) is E, we want to calculate $P(H_A | E) = \frac{P(E | H_A) P(H_A)}{P(E)}$ based on some prior probability assumption (e.g. we can assume $P(H_A) = P(H_0) = 0.5$)
    - cross-validation
        - use one set of data to formulate the hypothesis, and a **different set** of data to test it
    - chi-square test
    - efficient resampling
    - power: The probability that a test will reject the null hypothesis if it is false

- estimation
    - estimation of some parameters of a specific distribution
    - confidence intervals
    - Bayesian estimation

- correlation
    - standard scores
    - covariance
    - correlation
        - Pearson’s correlation: decide whether two variables have linear dependence
    - scatter plots in python
    - Spearman’s rank correlation
    - least squares fit
    - goodness of fit ($R^2$)

- reference
    - http://www.greenteapress.com/thinkbayes/thinkstats.pdf (Chapter 7-9)

### Lesson 3: Linear Modeling

- basic linear regression plotting
```python
%matplotlib inline

import numpy as np, pandas as pd, seaborn as sns, matplotlib as mpl, matplotlib.pyplot as plt
import statsmodels

np.random.seed(sum(map(ord, "linear_quantitative")))
tips = sns.load_dataset("tips")

sns.lmplot("total_bill", "tip", tips, ci = 100); # two parts, one is scatter plot, the other is the regression line
sns.lmplot("size", "tip", tips, x_jitter = .15); # add some jitter to improve the plot
sns.lmplot("size", "tip", tips, x_estimator = np.mean) 
bins = [10, 20, 30, 40]
sns.lmplot("total_bill", "tip", tips, x_bins=bins)
```

- Faceted linear model plots
```python
sns.lmplot("total_bill", "tip", tips, hue="smoker", ci = 40, markers = ["x", "o"]); # plot in the same graph
sns.lmplot("total_bill", "tip", tips, hue="smoker", ci = 40, col = "smoker"); # plot in the different graphs

g = sns.lmplot("total_bill", "tip", tips, hue="day", palette="Set2",
               hue_order=["Thur", "Fri", "Sat", "Sun"]) # here lmplot() returns a grid object for further use
g.set_axis_labels("Total bill (US Dollars)", "Tip");
g.set(xticks=[10, 30, 50], ylim=(0, 10), yticks=[0, 2.5, 5, 7.5, 10]);
```

- plot different linear relationships
```python
sns.lmplot("total_bill", "tip", tips, hue="time", palette="Set1", fit_reg=False);
sns.lmplot("size", "total_bill", tips, order = 2); # nonlinear plot
```

- Plotting logistic regression
```python
tips["big_tip"] = (tips["tip"] / tips["total_bill"]) > .15
sns.lmplot("total_bill", "big_tip", tips, y_jitter=.05, logistic = True); # logistic regression (see http://en.wikipedia.org/wiki/Logistic_regression)
```

- Plotting data with outliers
```python
sns.lmplot("total_bill", "tip", tips, robust=True, n_boot=500); # with robust option
```

- Plotting simple regression with `regplot()`
    - regplot() is lower-level of lmplot() and it would give you more control, every time you use lmplot(), you can the lower-level regplot()

- Examining model residuals using `residplot()`

- Plotting marginal distributions using `jointplot()`
```python
sns.jointplot("total_bill", "tip", tips, kind="reg", color="seagreen"); # plot regression
sns.jointplot("total_bill", "tip", tips, kind="resid", color="#774499"); # plot residue, similar to residue plotting
```

- Describing continuous interactions with `interactplot()`

- Plotting many pairwise relationships with `corrplot()`

- Plotting model coefficients with `coefplot()`

- reference
    - http://web.stanford.edu/~mwaskom/software/seaborn/tutorial/quantitative_linear_models.html

## Week 8: Introduction to Time Series Data

### Lesson 1: Introduction to Tim Series Data with Pandas

- basic oprations
```python
import pandas as pd, numpy as np

rng = pd.date_range('1/1/2011', periods = 72, freq = "H") # create a range of dates
ts = pd.Series(np.random.randn(len(rng)), index=rng)
converted = ts.asfreq('45Min', method = "pad") # change the frequency
ts.resample('D', how = 'mean') # resample data
```

- Time Stamps (time points) vs. Time Spans (time periods)
```python
from pandas import *

dates = [datetime(2012, 5, 1), datetime(2012, 5, 2), datetime(2012, 5, 3)] # three time points
periods = PeriodIndex([Period('2012-01'), Period('2012-02'), Period('2012-03')]) # three time periods (each one spams one month)
```

- Converting to Timestamps
    - `to_datatime` (with `dayfirst` option)
    - invalid data
    - epoch timestamps
        - note the default unit is nanosecond

- Generating Ranges of Timestamps
    - `date_range` (default is calendar day) and `bdate_range` (default is business day)
    ```python
    index = date_range('2000-1-1', periods=1000, freq='M')

    start = datetime(2011,1,1)
    end = datetime(2012,1,1)
    rng = date_range(start, end, freq = "W")
    ```

- DatetimeIndex
    - One of the main uses for DatetimeIndex is as an index for pandas objects. 
    - DatetimeIndex Partial String Indexing
        - suppose `ts` is a Series indexed by a TimeSeries, then we can use partial string such as `ts['2011']` or `ts['2011-6']` or `ts['2011-6':'2011-8']` to extract data
        - see reference for more partial string indexing
    - Truncating & Fancy Indexing
    - Time/Date Components

- DateOffset objects
    - "DateOffset objects" represent frequency increments, such as month, business day, one hours, etc
    - key features
        - added to a datetime object to obtain a shifted date
        - multiplied by an integer so that the increment will be applied multiple times
        - has `rollforward` and `rollback` methods for moving a date forward or backward to the next or previous "offset date"
    - Parametric offsets
    - Custom Business Days
    - Offset Aliases, Combining Aliases, Anchored Offsets, Legacy Aliases
    - Holidays / Holiday Calendars

- Time series-related instance methods
    - shifting the values in a TimeSeries in time
        - `shift`: it can accept `freq` argument or `DataOffset` class
    - Frequency conversion
        - `asfreq`
    - Filling forward / backward
        - `fillna` can fill the NA data associated with `asfreq` or `reindex`
    - Converting to Python datatimes

- Resampling
    - e.g. `ts.resample('D', how = 'mean') # resample data`
    - `how` methods: `sum`, `mean`, `std`, `sem`, `max`, `min`, `median`, `first`, `last`, `ohlc`
    - downsampling option: `closed` (set to `left` or `right`)
    - upsampling option: `fill_method`, `limit`

- Time Span Representation
    - introduction
        - TimeSpan is quite similar to TimeStamp mentioned before. We have `Period` instead of `datetime`, `period_range` instead of `date_range`. 
    - Period
    - PeriodIndex and period_range
    - PeriodIndex Partial String Indexing
    - Frequency Conversion and Resampling with PeriodIndex
        - in time span, we can set `how` option to `start` or `end` of the period when doing frequency conversion

- Converting between Representations
    - `to_period` and `to_timestamp` 

- Representing out-of-bounds spans

- Time Zone Handling

- reference
    - http://pandas.pydata.org/pandas-docs/stable/timeseries.html (TimeSeries documentation)
    - http://nbviewer.ipython.org/github/twiecki/financial-analysis-python-tutorial/blob/master/1.%20Pandas%20Basics.ipynb
    - http://nbviewer.ipython.org/github/chrisalbon/code_py/blob/master/pandas_time_series_basics.ipynb (an introduction to TimeSeries with examples)

### Lesson 2: Introduction to Time Series Data with Seaborn

- Plotting statistical timeseries data
    - introduction
        - `tsplot`: plot statistical timeseries data (e.g. confidence interval, error bar, etc)
    - two kinds of input data of tsplot
        - multidimensional array
        - long-form DataFrames
            - spedify options such as `time`, `unit`, `condition`, `value`, `color`, `err_kws`, `ci`, etc
    - Different approaches to representing estimator variability
        - Visualizing uncertainty at each observation with error bars
            - e.g. `ax = sns.tsplot(sines, err_style="ci_bars", interpolate=False)`
        - Drawing comparisons with overlapping error bands
        - Representing a distribution with multiple confidence intervals
        - Visualizing the data for each sampling unit
    
- reference
    - http://web.stanford.edu/~mwaskom/software/seaborn/tutorial/timeseries_plots.html
    - http://nbviewer.ipython.org/github/chrisalbon/code_py/blob/master/seaborn_pandas_timeseries_plot.ipynb
    - http://nbviewer.ipython.org/github/chrisalbon/code_py/blob/master/seaborn_pretty_timeseries_plots.ipynb
    - http://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.tsplot.html (tsplot documentation)

### Lesson 3: Introduction to Twitter Data Mining

- Exploring Twitter's API
    - Fundamental Twitter Terminology
    - Creating a Twitter API Connection
    ```python
    import twitter
    
    CONSUMER_KEY = 'LItYWbMkoEt6KRbznvoCQcP5i'
    CONSUMER_SECRET = 'NVhC9F6W77iO99Ut1aJDX7ut0DP8GqHyVFdtEWpRboFlpcvqnv'
    OAUTH_TOKEN = '2870997399-kNPx3rODRpF1YwmxQm9AQ4pIArfoHHgU7M8jR8Y'
    OAUTH_TOKEN_SECRET = 'sh6aEqDKoDJ2biDWtXXH4PCpiR4IBhKvOFLEAEWDRUym1'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    
    print(twitter_api)
    ```
    - Exploring Trending Topics
        - get trending topics in the world and the US
        ```python
        # The Yahoo! Where On Earth ID for the entire world is 1. See https://dev.twitter.com/docs/api/1.1/get/trends/place and     http://developer.yahoo.com/geo/geoplanet/
        WORLD_WOE_ID = 1
        US_WOE_ID = 23424977
        # Prefix ID with the underscore for query string parameterization.
        # Without the underscore, the twitter package appends the ID value
        # to the URL itself as a special case keyword argument.
        world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
        us_trends = twitter_api.trends.place(_id=US_WOE_ID)
    
        import json # use json package to pretty print it
        print(json.dumps(world_trends, indent=4), "\n",json. dumps(us_trends, indent=4))
        ```
        - get common trends
        ```python
        # find the intersection of two sets (world trend and US trend)
        world_trends_set = set([trend['name' ] for trend in world_trends[0]['trends' ]])
        us_trends_set = set([trend['name' ] for trend in us_trends[0]['trends' ]])
        common_trends = world_trends_set.intersection(us_trends_set)
        print(common_trends)
        ```
    - Searching for Tweets
    ```python
    import twitter

    q = '#illini' # how to use query operators to build a query? see https://dev.twitter.com/rest/public/search 
    count = 10 # count is The number of tweets to return per page
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q = q, count = count) # search_results contains two fields: "statuses" and "search_metadata" 
    statuses = search_results['statuses' ]
    # Iterate through 5 more batches of results by following the cursor
    for _ in range(5):
        print("Length of statuses" , len(statuses))
        try:
            next_results = search_results['search_metadata']['next_results'] # get information related to next page
        except KeyError: # No more results when next_results doesn't exist
            break
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=' ) for kv in next_results[1:].split("&" ) ]) # get the arguments to search the next page
        search_results = twitter_api.search.tweets(**kwargs) # here double stars unpack the values in dict into arguments of the function
        statuses += search_results['statuses' ]
        
    print(json.dumps(statuses[0], indent=4))
    ```

- Analyzing the 140 Characters
    - Extracting Tweet Entities
        - The entities in the text of a tweet are conveniently processed and available through t['entities']
        ```python
        q = "illini"
        count = 3
        search_results = twitter_api.search.tweets(q = q, count = count) # search_results contains two fields: "statuses" and "search_      metadata" 
        first_status = search_results['statuses'][0] # get the first status
        print("keys = ", first_status.keys()) # show the structure of the first tweet

        print("\n\ntext = ", first_status["text"], "\n\nentities = ", first_status['entities'])
        ```
    - Analyzing Tweets and Tweet Entities with Frequency Analysis
        - we use `collections.Counter` to analyze the frequency
    - Computing the Lexical Diversity of Tweets
        - definition of lexical diversity: the number of **unique** tokens in the text divided by the total number of tokens in the text, a function is as follows
        ```python
        # A function for computing lexical diversity
        def lexical_diversity(tokens):
            return 1.0*len(set(tokens))/len(tokens) 
        ```
    - Examining Patterns in Retweets
    - Visualizing Frequency Data with Histograms

- introduction to JSON
    - JSON is a lightweight, human-readable text-based open standard data-interchange format
    - JSON vs XML
    - Typical uses of JSON
        - API
        - NoSQL 
        - AJAX
        - Package Management
    - JSON in Python
        - `json.loads(json_obj)`, `json.dumps(json_obj, indent = 4)`, `json.load()`, `json.dump()`

- reference
    - https://rawgit.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition/master/ipynb/html/__Chapter%201%20-%20Mining%20Twitter%20(Full-Text%20Sampler).html
    - http://www.w3resource.com/JSON/introduction.php (an introduction of JSON)
    - http://json.org/
    - https://freepythontips.wordpress.com/2013/08/08/storing-and-loading-data-with-json/ (discuss how to load and store data with json in python)
    - https://rawgit.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition/master/ipynb/html/Chapter%209%20-%20Twitter%20Cookbook.html (cookbook of mining twitter)
    
## Week 9: Introduction to Data Processing

### Lesson 1: Data Formats

- introduction

- formatted text
    - fixed-width format
    ```python
    # First we define our format specification codes
    hfmt = "{0:5s}{1:29s}{2:27s}{3:6s}{4:10s}{5:12s}{6:10s}\n" 
    fmt = "{0:5s}{1:29s}{2:30s}{3:3s}{4:4s}{5:14.8f}{6:14.8f}\n" # {0:5s} means the 0th element is 5-character string, etc
    
    # We need to treat the first row special since it is the header row
    flag = True
    
    # Now open file and write out airports.
    with open('fixed-width.txt', 'w') as fout:
        for row in airports:
            # We output first line special since it is a header row.
            if flag:
                fout.write(hfmt.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                flag = False
            else:
                fout.write(fmt.format(row[0], row[1], row[2], row[3], row[4], float(row[5]), float(row[6])))
    ```
        - a trick to quantify the width of each column: print "1234567890" multiple times
    - Delimiter Separated Values
        - using `csv` module with `delimiter` option to read and write data
        ```python
        fout = csv.writer(csvfile, delimiter='|')
        ```

- JSON (see week 8)

- XML
    - introduction
        - XML is a simple, self-describing structured text-based data format. XML is based on the **concept of element**, that can have attributes and values. Elements can be nested, which can indicate parent-child relationships or a form of containerization
    - some examples: HTML5, SVG (Scalable Vector Graphics)
    - creating a XML file
    ```python
    import html 
    import xml.etree.ElementTree as ET
    
    data = '<?xml version="1.0"?>\n' + '<airports>\n'
    for airport in airports[1:]:
        data += '    <airport name="{0}">\n'.format(html.escape(airport[1]))
        data += '        <iata>' + str(airport[0]) + '</iata>\n'
        data += '        <city>' + str(airport[2]) + '</city>\n'
        data += '        <state>' + str(airport[3]) + '</state>\n'
        data += '        <country>' + str(airport[4]) + '</country>\n'
        data += '        <latitude>' + str(airport[5]) + '</latitude>\n'
        data += '        <longitude>' + str(airport[6]) + '</longitude>\n'
        data += '    </airport>\n'
    
    data += '</airports>\n'
    tree = ET.ElementTree(ET.fromstring(data))
    
    with open('data.xml', 'w') as fout:
        tree.write(fout, encoding='unicode')
    ```
    - parsing a XML file
    ```python
    data = [["iata", "airport", "city", "state", "country", "lat", "long"]]

    tree = ET.parse('data.xml') # parsing result return a ElementTree object, more info here: https://docs.python.org/3.4/library/xml.etree.elementtree.html
    root = tree.getroot() 
    
    for airport in root.findall('airport'):
        row = []
        row.append(airport[0].text)
        row.append(airport.attrib['name']) # extract attribute "name"
        row.append(airport[1].text)
        row.append(airport[2].text)
        row.append(airport[3].text)
        row.append(airport[4].text)
        row.append(airport[5].text)
    
        data.append(row)
        
    print(data[:5])
    ```

- HDF (Hierarchical Data Format)
    - HDF is a data format that is designed to efficiently handle large data sets that might be difficult to persist by using either database systems, XML documents, or other custom-defined user formats.

- reference
    - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week09/dataformats.ipynb
    - https://en.wikipedia.org/wiki/XML
    - http://www.hdfgroup.org/

### Lesson 2: Data Parsing

- introduction to data parsing
    - two techniques used to parse a structured file (like XML)
        - Simple API for XML (SAX): event driven parser that reads and processes **each part** of XML file sequentially
        - Document Object Model (DOM): reads and parses the **entire** document

- introduction to BeautifulSoup
    - quick start
    ```python
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>
    
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    
    <p class="story">...</p>
    """
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_doc) # making the soup from string
    
    print(soup.findAll("p")) # get all paragraphs
    print(soup.find("p")) # find the first paragraphs
    
    for link in soup.findAll("a"):
        print(link.get("href")) # get all urls
    ```
    - making the soup
    - kinds of objects
        - tag
        - name (each tag has a name)
        - attributes
        - multi-valued attributes
        - navigableString
    - comments and other special strings
    - Navigating the tree
        - going down
            - Navigating using tag names
            - `.contents` and `.children`
            - `.descendants`: iterate over **all** tag's children
            - `.string`
            - `.strings` and `stripped_strings`
        - going up
            - `.parent` vs `.parents`
        - going sideways
            - `.next_sibling` and `.previous_sibling`
            - `.next_siblings` and `.previous_siblings`
        - going back and forth
    - searching the tree
        - Kinds of filters
            - the filters could be a string, a regular expression, a list, `True`, or a function
        - `find_all()`
            - shortcut: calling a tag is like calling find_all()
            ```python
            soup("a") # equivalent to soup.find_all("a")
            soup(text = True) # equivalent to soup.find_all(text = True)
            ```
            - the `name` argument
            - the keyword arguments
            - searching by CSS class
            - the `text` argument: search for strings instead of tags
            - the `recursive` argument: set to `False` to consider only the direct children
            - the `limit` argument: set the max number of results
        - other search functions: `find()`, `find_parents()`, `find_parent()`, etc
        - CSS selectors
            - `.select()`
            - reference
                - http://www.w3schools.com/cssref/css_selectors.asp
    - modifying the tree
    - output
        - pretty-printing and non-pretty printing
        - output formatters
    - specifying the parser to use
    - encodings
        - BeautifulSoup converts encoding to unicode automatically
    - parsing only part of a document

- reference
    - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week09/intro2dp.ipynb (general introduction to data parsing)
    - http://www.crummy.com/software/BeautifulSoup/bs4/doc/ (BeautifulSoup documentation)
    - http://nbviewer.ipython.org/urls/dl.dropboxusercontent.com/u/33663928/dst4l-projects/week5/Web_Scraping_Tutorial-TotalFilm_50_Adaptations.ipynb (web scraping using python requests and lxml)

### Lesson 3: Working with Data

- visualizing the unemployment rate of all counties in the US
    - key points in this example
        - SVG file is a kind of XML file
        - each county info is store in a <path> item, there are 3143 items in total
        - in each item, the attribute "id" represents "FIPS code" of the county
        - match the unemployment rate data to the graph by FIPS code
        - use proper color scale to visualize the data
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week09/dataviz.ipynb
        - http://colorbrewer2.org/ (color scale reference)

- requests package
    - reference
        - http://docs.python-requests.org/en/latest/

## Week 10: Introduction to Data Persistence

### Lesson 1: Rational Databases

- introduction to data persistence
    - data persistence using basic file input/output in Python
        - method: directly write and read data in **string form** into/out of a file
        - not optimal, for following reasons    
            - not convenient to convert some types of data into strings
            - costly in terms of storage space
            - rely completely on the underlying file system **consistency** and **durability**
    - pickling
        - using `pickle` package and **binary** reading/writing mode
        ```python
        import numpy as np
        import pickle
        
        # writing
        data = np.random.rand(100)
        
        with open('test.p', 'wb') as fout:
            pickle.dump(data, fout)

        # reading
        with open('test.p', 'rb') as fin:
            newData = pickle.load(fin)

        print(newData[0:20:4])
        ```
        - While easier than custom read/write routines, pickling still requires the file system to provide support for concurrency, consistency, and durability. To go any further with data persistence, we need to move beyond Python language constructs and employ additional software tools.
    - database systems
        - classification
            - Relational Database Management Systems
                - rely on a tabular data model
                - e.g. MySQL, PostgreSQL, etc
            - NoSQL systems
                - not rely on the tabular data model
                - many are developed to meet the big data challenges by Google, Facebook etc
                - e.g. Dynamo, ZopeDB, MongoDB, etc
        - database roles
            - database administrator, database developer, database application developer
        - The ACID Test
            - test the **atomicity, consistency, isolation, durability** of a database system
            - reference
                - http://en.wikipedia.org/wiki/ACID (ACID test)
        - SQLite
            - SQLite is a software library that implements a **self-contained, serverless, zero-configuration, transactional** SQL database engine. SQLite is the most widely deployed SQL database engine in the world.
            - reference
                - https://www.sqlite.org/ (general introduction)
                - https://www.sqlite.org/famous.html (some famous users of SQLite)

- reference
    - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week10/intro2db.ipynb
    
### Lesson 2: Using SQL for Schema Manipulation

- introduction to SQL
    - the basics of relational database systems
        - relational database hold data of different types
        - style convention: all SQL commands are presented entirely in uppercase, and item names use camelCase.
        - Related tables are often grouped together into a schema
    - brief history of SQL
        - initially many kinds of database systems have different APIs. SQL is developed as a standard language to access and manipulate them (but there are some different versions of SQL)
    - two main components in SQL
        - Data Definition Language (DDL): used to create, modify, or delete items (such as tables) in a database
        - Data Manipulation Language (DML): used to add, modify, delete, or select data from a table in the database
    - SQL data types
        - While the SQL standard defines basic data types, different database systems can support the standard to varying degrees. SQLite supports: NULL, INTEGER, REAL, TEXT, BLOB
    - create table
        - syntax: `CREATE TABLE tableName ( { <columnDefinition> | <tableLevelConstraint> } [, { <columnDefinition> | <tableLevelConstraint> } ]* ); `
        - explanation
            - "|" means "either/or"
            - content between "[" and "]" is optional
            - "*" indicates that multiple enclosing items can be included
    - drop table
        - `DROP TABLE tableName ;`
        - an example of creating and droping tables
        ```SQL
        %%writefile create.sql
        -- First we drop any tables if they exist
        -- Ignore the no such Table error if present
          
        DROP TABLE myVendors ;
        DROP TABLE myProducts ;
            
        -- Vendor Table: Could contain full vendor contact information.
                
        CREATE TABLE myVendors (
            itemNumber INT NOT NULL,
            vendornumber INT NOT NULL,
            vendorName TEXT
        ) ;
           
        -- Product Table: Could include additional data like quantity
               
        CREATE TABLE myProducts (
            itemNumber INT NOT NULL,
            price REAL,
            stockDate TEXT,
            description TEXT
        ) ;
        ```
    - SQL script
        - we can write SQL commands into a script file for execution. this technique is useful for debugging and command reuse.
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week10/intro2sqlddl.ipynb

- SQL tutorials
    - basic statements
        - `SELECT`
        - `DISTINCT`
        - `WHERE`
        - `AND/OR`
        - `ORDER BY`
        - `INSERT INTO`
        - `UPDATE...SET`
        - `DELETE`
        - `SELECT TOP` 
        - `LIKE` (together with SQL wildcard characters)
        - `IN`, `BETWEEN`
        - `SELECT ... AS` (aliases)
        - `INNER JOIN`, `LEFT/RIGHT JOIN`, `FULL OUTER JOIN`
        - `SELECT INTO` (create a new table), `INSERT INTO ... SELECT` (insert into an existing table)
        - `CREATE DATABASE`
        - `CREATE TABLE` (specifying column_names, data_types and optional_constaints)
            - some constaints: `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `DEFAULT`, `AUTO INCREMENT`
        - `CREATE INDEX`
        - `DROP INDEX/TABLE/DATABASE`
        - `ALTER TABLE`
        - `CREATE VIEW`
        - `GROUP BY`
        - Date functions
        - Null functions
    - general data types & data types for various databases
    - SQL injection 
        - a technique where malicious users can **inject SQL commands into an SQL statement**, via web page input.
    - SQL functions
        - aggregate functions
            - `AVG()`, `COUNT()`, `FIRST()`, `LAST()`, `MAX()`, `MIN()`, `SUM()`
        - scalar functions
            - `UCASE()`, `LCASE()`, `MID()`, `LEN()`, `ROUND()`, `NOW()`, `FORMAT()`
    - reference
        - http://www.w3schools.com/sql/default.asp
        - http://www.tutorialspoint.com/sql/ 

- SQLite tutorials
    - similar to SQL standard, only a little difference
    - reference
        - http://www.tutorialspoint.com/sqlite/ 

### Lesson 3: Using SQL for Data Manipulation

- introduction to SQL data manipulation language
    - most are covered in references in Lesson 2, an additional reference: http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week10/intro2sqldml.ipynb

## Week 11: Advanced Data Persistence

### Lesson 1: Python Database Programming

- introduction
    - previously, we use a dababase client tool to do operations on a database, now we are going to interact with databases using a python program. We will mainly focus on SQLite, for other databases, we can refer to related API.

- using SQLite
    - to work with a database within a Python program, we follow three steps
        - establish a **connection** to a databse. in most cases, we need to connect to a remote database server through a network connection, for SQLite, we can work locally
        - obtain a **cursor** from the database connection
        - execute SQL commands by using the database cursor
    - useful methods
        - `execute()`, `executemany()`, `executescript()`
        - `fetchone()`, `fetchmany()`, `fetchall()`
    - example
    ```python
    # We define our Create Table SQL command
    createSQL = '''
    CREATE TABLE myProducts (
        itemNumber INT NOT NULL,
        price REAL,
        stockDate TEXT,
        description TEXT);
    '''
    
    # Tuple containing data values to insert into our database
    items = ((1,19.95,'2015-03-31','Hooded sweatshirt'), 
             (2,99.99,'2015-03-29','Beach umbrella'),
             (3,0.99,'2015-02-28', None),
             (4,29.95,'2015-02-10','Male bathing suit, blue'),
             (5,49.95,'2015-02-20','Female bathing suit, one piece, aqua'),
             (6,9.95,'2015-01-15','Child sand toy set'),
             (7,24.95,'2014-12-20','White beach towel'),
             (8,32.95,'2014-12-22','Blue-striped beach towel'),
             (9,12.95,'2015-03-12','Flip-flop'),
             (10,34.95,'2015-01-24','Open-toed sandal'))
    
    # user-defined function
    def myYear(date):
        return int(date[:4])
    
    # Open a database connection, here we use an in memory DB
    
    with sl.connect(":memory:") as con: # ':memory:' indicates that our database will be temporary and maintained in the program's memory space
    
        # Now we obtain our cursor
        cur = con.cursor()   
        
        # First we create the table
        cur.execute(createSQL)
        
        # Now populate the table using all items
        cur.executemany("INSERT INTO myProducts VALUES(?, ?, ?, ?)", items) 
        # two kinds of placeholders for holding value:
        # 1. put ? as a placeholder wherever you want to use a value
        # 2. use named placeholder starting with ":" like ":name", 
        # e.g. cur.execute("INSERT INTO myProducts VALUES(:id, :price, :sdate, :desc)", {"id" : item[0], "price" : item[1], "sdate" : item[2], "desc" : item[3]})
        
        con.create_function("fYear", 1, myYear) # user-defined function
        
        for row in cur.execute('SELECT fYear(stockDate) FROM myProducts'): # apply function in a query
            print(row)
    ```

- reference
    - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week11/dbNpy.ipynb
    - https://docs.python.org/3.4/library/sqlite3.html

### Lesson 2: Advanced Python Database Programming

- Introduction to Pandas & Databases
    - `read_sql()`: Read SQL query or database table into a DataFrame, it is a convenient **wrapper** around `read_sql_table()` and `read_sql_query()` depending on the provided input
    ```python
    import sqlite3 as sl, pandas as pd

    query = "SELECT code, airport, city, state, latitude, longitude FROM airports LIMIT 100 ;"

    with sl.connect(database) as con:
        data = pd.read_sql(query, con, index_col ='code')
        print(data[data.state == 'MS'])
    ```
    - `to_sql()`: Write records stored in a DataFrame to a SQL database.
    ```python
    query = "SELECT code, airport, city, state, latitude, longitude FROM airports ;"
    with sl.connect(database) as con:
        data = pd.read_sql(query, con)

        data[data.state == 'IL'].to_sql('ILAirports', con)
    ```

- comparison between pandas and SQL
    - `SELECT`: indexing in pandas
    - `WHERE`: boolean indexing and NULL check
    - `GROUP BY`: `groupby()` function
    - `JOIN`: `join()` or `merge()`
    - `UNION`: `concat()`

- reference
    - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week11/intro2pandasdb.ipynb
    - http://pandas.pydata.org/pandas-docs/stable/comparison_with_sql.html (discussing the comparison between pandas and SQL)

### Lesson 3: NoSQL Data Storage

- NoSQL
    - introduction
        - provides a mechanism other than the tabular relations used in relational databases
        - make some operations faster than relational databases
    - examples
        - document store
            - documents encapsulate and encode data in some standard formats such as XML, JSON, etc
        - graph
            - designed for data whose relations are well represented as a graph, like social relations, transport links, etc
        - key-value stores
            - data is represented as a collection of key-value pairs
        - others
    
- reference 
    - https://en.wikipedia.org/wiki/NoSQL
    - http://planetcassandra.org/what-is-apache-cassandra/
    - http://jimbojw.com/wiki/index.php?title=Understanding_Hbase_and_BigTable

## Week 12: Data Exploration

### Lesson 1: Data Preparation

- introduction to data preparation
    - before we can explore and analyze a data set, we probably need to do some preparation work, because many data sets may contain lots of **dirty data** and are not ready to use, or they may be **in bad form** which would consume lots of system resources.
    - example
        - main idea
            - previously we have already construct a database using flights data in `2001.csv`. 
            - If we want to load all the data, we will probably run out of memory. 
            - Even if we only want two columns named `arrivalDelay` and `departureDelay`, we will still use too much memory. Main reason is that the Pandas DataFrame needs to store the data in the format of `object` when there are "NA" value, which **consumes much more memory** than `int64` format. 
            - so in order to save memory, we drop "NA" before reading into a DataFrame by using 
            ```python
            query = '''SELECT arrivalDelay, departureDelay 
                FROM flights
                WHERE arrivalDelay != 'NA' AND
                    departureDelay != 'NA' ; '''
            
            with sl.connect(database) as con:
                data = pd.read_sql(query, con)
            ```
            - to further save memory, we examine the data by `data.describe()` and find that it is enough to use `int16` format, so we convert data into this format by using 
            ```python
            import numpy as np
            data[['arrivalDelay']] = data[['arrivalDelay']].astype(np.int16)
            data[['departureDelay']] = data[['departureDelay']].astype(np.int16)
            ```
            - also we can read data directly from original csv file instead of the database by using 
            ```python
            newdata = pd.read_csv('/notebooks/i2ds/data/2001.csv', dtype=np.float, header=0, na_values=['NA'], usecols=(14, 15)) # use na_values to define NA data
            newdata = newdata.dropna() # drop NA data in the dataFrame
            ```
            - we can save the data in `hdf` format by using `to_hdf()` function
        - details here: http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week12/intro2de.ipynb

- pandas reading and writing HDF files
    - http://pandas.pydata.org/pandas-docs/stable/io.html#io-hdf5

### Lesson 2: Visual Exploration

- introduction to data exploration
    - here we see some visualization techniques of datasets using seaborn
        - pairplot: compare different dimensions in the dataset
        - box plot and violin plot
        - histogram
        - jointplot: see correlation of two variables
        - FacetGrid
        - HeatMaps
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week12/dataexplore.ipynb
        - http://web.stanford.edu/~mwaskom/software/seaborn/tutorial.html

### Lesson 3: Statistical Exploration

- probabilistic programming
    - frequentists vs Bayesians
        - frequentists: probability = **long-run frequency** of events
        - Bayesians: probability = belief of an event occuring, and belief is **modified based on evidence** (prior -> posterior)
    - Bayesian framework
    \begin{align}
    P( A | X ) = & \frac{ P(X | A) P(A) } {P(X) } \\\\[5pt]
    & \propto P(X | A) P(A)\;\; (\propto \text{is proportional to } )
    \end{align}
    - probability mass function and probability distribution function
    - PyMC: Python library for programming Bayesian analysis

- reference
    - http://nbviewer.ipython.org/github/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Chapter1_Introduction/Chapter1.ipynb

## Week 13: Introduction to Machine Learning

### Lesson 1: Supervised Learning

- introduction to data mining
    - classification of machine learning techniques
        - by problems
            - classification
            - regression
            - dimensionality reduction
            - clustering
        - by methods
            - supervised learning
            - unsupervised learning
    - k-nearest neighbors algorithms
        - one of the simplest machine learning algorithms, get classification or value based on information of its k-nearest neighbors (k is usually a small integer)
        - https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
    - support vector machine
        - https://en.wikipedia.org/wiki/Support_vector_machine
        - http://nbviewer.ipython.org/github/jakevdp/sklearn_pycon2015/blob/master/notebooks/03.1-Classification-SVMs.ipynb
    - desicion tree
        - https://en.wikipedia.org/wiki/Decision_tree_learning
    - random forest
        - useful for large datasets
        - build a set of decision trees and each uses a randomly selected amount of data and training attributes to make a prediction. the predictions from different trees are statistically combined to make a final prediction
        - https://en.wikipedia.org/wiki/Random_forest
        - http://nbviewer.ipython.org/github/jakevdp/sklearn_pycon2015/blob/master/notebooks/03.2-Regression-Forests.ipynb
    - cross-validation
        - So far we have simple quantified the performance of the different algorithms by comparing their performance on a single test data. This introduces a potential problem that certain training/testing data combinations may preferentially work best with one type of algorithm. To obtain a better characterization of the performance of a given algorithm we can employ cross-validation, where we **repeatedly select different training and testing data sets** from the original data and accumulate the **statistical measures** of the performance for each new sample.
    - reference
        - http://nbviewer.ipython.org/github/weiHelloWorld/introduction-to-data-science/blob/master/week13/intro2dm.ipynb

### Lesson 2: Unsupervised Learning

- introduction to dimension reduction
    - introduction
        - for a large, multi-dimensional data set, one approach to simplify subsequent analysis is to **reduce the number of dimensions that must be processed**. In some cases, dimensions can be removed from analysis based on business logic. More generally, however, we can employ machine learning to seek out relationships between the original dimensions to identify new dimensions that better capture the inherent relationships within the data.
        - The standard technique to perform this is known as **principal component analysis (PCA)**. Mathematically,we can derive PCA by using linear algebra to solve a set of linear equations. This process effectively rotates the data into a new set of dimensions, and by ranking the importance of the new dimensions, we can actually leverage fewer dimensions in machine learning algorithms. 
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week13/intro2dr.ipynb

- dimension reduction with Principal Component Analysis
    - basic idea
        - introduction example
            - use `sklearn.decomposition.PCA` to read a dataset to find the components with **maximum variance** (principal components)
            - keep 95% of variance and data is **reduced by 1 dimension** and the size of data is **compressed by 50%**
        - Application of PCA to Digits
            - every digit figure has 64 pixels, which means 64 dimensions. 
            - one way to see components is to think of them as different pixels, but in this way, we cannot get good approximation with a few number of components
            - instead, we find **the best series of basis** to approximate the digit figure using machine learning techniques, so that we can get very good approximation with less than 6 components. The dimensionality is reduced from 64 to 6 or less.
            - this is some kind of **lossy data compression**
    - reference
        - http://nbviewer.ipython.org/github/jakevdp/sklearn_pycon2015/blob/master/notebooks/04.1-Dimensionality-PCA.ipynb

- Decomposing signals in components (matrix factorization problems)
    - principal component analysis
        - exact PCA
        - incremental PCA
            - do not require to load all data into memory, allow partial computations
        - approximate PCA
            - greatly reduce time complexity
        - kernal PCA
            - an extension of PCA which achieves **non-linear dimensionality reduction** through the use of kernels
        - SparsePCA and MiniBatchSparsePCA
    - Truncated singular value decomposition and latent semantic analysis
    - Dictionary Learning
    - factor analysis
    - independent component analysis (ICA)
    - Non-negative matrix factorization (NMF or NNMF)
    - reference
        - http://scikit-learn.org/stable/modules/decomposition.html#dictionary-learning

### Lesson 3: Clustering

- introduction to clustering
    - k-means algorithm
        - basic idea
            - select k initial means (based on experience or randomly)
            - k clusters are created by **associating each point with the nearest mean**
            - the centroid of each cluster becomes the new mean
            - repeat until convergence
        - caveats
            - the convergence is not guaranteed, so scikit-learn by default uses a large number of random initializations to find the best results
        - examples
            - classifying figures of digits
                - we load digits figures and they can be divided into 10 clusters with accuracy of nearly 80%
            - color compression
                - initially there are $256^3$ colors, by clustering into 64 groups, we greatly reduce the size of color information
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week13/intro2clust.ipynb
        - https://en.wikipedia.org/wiki/Cluster_analysis
        - http://nbviewer.ipython.org/github/jakevdp/sklearn_pycon2015/blob/master/notebooks/04.2-Clustering-KMeans.ipynb

## Week 14: Introduction to Cloud Computing

### Lesson 1: Introduction to Cloud Computing

- Introduction to Cloud Computing with Docker
    - docker overview
        - docker daemon process
        - docker images
        - docker containers
            - a docker container can run in either detached mode (in the background) or foreground mode (through network connection or shared volumes)
    - docker volumes
        - mount a volume from host to docker container
        ```bash
        sudo docker tag sequenceiq/hadoop-ubuntu:2.6.0 had # add a tag to simplify typing
        sudo docker run -it -v /data:/file had /bin/bash # mount /data in host to /file in the container
        ```
        - reference
            - http://docs.docker.com/userguide/dockervolumes/
    - linking containers
    - advanced docker commands
        - `cp`: used to copy data into a running Docker container from the host operating system.
        - `history`: displays the history of a Docker image.
        - `info`: displays system-wide docker information.
        - `restart`: used to restart a stopped container.
        - `rm`: remove docker container, use -f flag to force removal
        - `rmi`: remove a Docker image, use the -f flag to force removal
        - `search`: search the Docker official registry for specific Docker images.
        - `stats`: used to monitor the system resources used by a running container.
        - `stop`: used to stop a running Docker container.
        - `tag`: used to add tags, like a new, human-readable name to a image or container.
        - `top`: used to monitor usage of a running container.
    - docker resource usage
    - docker cleanup
        - `sudo docker rm $(sudo docker ps -a -q)`
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week14/intro2cloud.ipynb

- introduction to cloud computing by Amazon
    - how does AWS work?
        - get access to servers, storage, databases, apps over the internet
    - advantages
        - Trade capital expense for variable expense
        - Benefit from massive economies of scale
        - Stop guessing capacity
        - Increase speed and agility
        - Stop spending money on running and maintaining data centers
        - Go global in minutes
    - type of cloud computing
        -  Infrastructure as a Service (IaaS), Platform as a Service (PaaS), Software as a Service (SaaS).
    - reference
        - http://aws.amazon.com/what-is-cloud-computing/ (general introduction)
        - https://aws.amazon.com/articles/Python/3998 (using python to work with AWS)

### Lesson 2: Running Containers in the Cloud

- introduction to Google Cloud SDK
    - preparation work
        - `docker pull google/cloud-sdk`
        - login with google account
        - `docker pull sequenceiq/hadoop-ubuntu:2.6.0`
    - setting up virtual machine on Google compute engine
        - see reference for details
    - using virtual machines on Google compute engine
        - two ways
            - set up SSH connection using `google/cloud-sdk`
            - directly get access from the google developer console "VM instances" page
    - reference
        - https://github.com/INFO490/spring2015/blob/master/week14/README.md (preparation)
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week14/intro2gc.ipynb (detailed steps on how to set up virtual machines on Google compute engine)
        - https://cloud.google.com/compute/docs/ (official introduction)

### Lesson 3: Introduction to Hadoop

- introduction to Hadoop
    - basic idea
        - write mapper and reducer programs for a specific problem (e.g. word count problem)
        - running Hadoop within the docker image `sequenceiq/hadoop-ubuntu:2.6.0`
        - load data into the HDFS (Hadoop Distributed File System) by using `$HADOOP_PREFIX/bin/hdfs dfs` commands
        - use Hadoop streaming to do map/reduce processing
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week14/intro2dh.ipynb
        
## Week 15: Introduction to Python High Performance Computing

### Lesson: Introduction to Python High Performance Computing

- Optimizing Python Performance
    - introduction
        - warning: one should not worry about optimization until it has been **shown to be necessary**
    - related Python modules
        - `threading` module
            - we can use `threading.Thread()` to create a `Thread` object with a specific name and a function to execute and then start it
        - `multiprocessing` module
            - the standard Python interpreter only allows one thread to execute Python code at a time, this si called Global Interpreter Lock (GIL). One way to circumvent it is to use **multiple Python interpreters** that each runs in their own process
            - these processes all share the same Python code (which needs to create other processes), so how can we avoid the infinite loop of creating processes? by specifying `if __name__ = '__main__' `, so that only `__main__` process creates other processes
    - IPython cluster
    - third-party Python tools
        - Numba
        - PYPY
        - Cython
    - reference
        - http://nbviewer.ipython.org/github/INFO490/spring2015/blob/master/week15/pyhpc.ipynb