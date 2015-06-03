# include here only constants and functions that should
# be sourced in non-interactive mode, i.e. from vim

cpp ()
{
    name=$1
    fname=${name}.cpp
    clang++ $fname -o $name -std='c++11' -stdlib='libc++'
}

# Source local
if [ -f $HOME/.zshenv_local ]; then
    source $HOME/.zshenv_local
fi
