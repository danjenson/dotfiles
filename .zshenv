# include here only constants and functions that should
# be sourced in non-interactive mode, i.e. from vim

cpp ()
{
    name=$1
    mkdir -p out
    clang++ $name -o out/${name:r} -std='c++11' -stdlib='libc++'
}

hs ()
{
    name=$1
    mkdir -p out
    ghc --make $name -o out/${name:r}
}

# Source local
if [ -f $HOME/.zshenv_local ]; then
    source $HOME/.zshenv_local
fi
