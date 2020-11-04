autoload bashcompinit
bashcompinit

#thx to https://www.endpoint.com/blog/2016/06/03/adding-bash-completion-to-python-script


set DIR = $(pwd)
_show_complete()
{
    local cur prev opts node_names
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts=`parameters -options`
    #node_names=`python $CHEF_DIR/repo_scripts/node_names.py`
    if [[ ${prev} != -* || ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
    #prev_args="${COMP_WORDS:1:-1}"
    if [[ ${prev} == -* ]] ; then
        lookup_arg=$(echo "$prev" | sed 's/^-*\(.*\)/\1/')
        opts_arg=`parameters -options ${lookup_arg}`
        COMPREPLY=( $(compgen -W "${opts_arg}") )
        return 0
    fi

    #COMPREPLY=( $(compgen -W "${node_names}" -- ${cur}) )
}

complete -F _show_complete parameters
