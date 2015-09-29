def set_trace():
    from IPython.core.debugger import Pdb
    Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)

def debug(f, *args, **kwargs):
    from IPython.core.debugger import Pdb
    pdb = Pdb(color_scheme='Linux')
    return pdb.runcall(f, *args, **kwargs)

def test_df():
    return pd.DataFrame(np.concatenate([np.random.randint(2, size=[50,1]),
                        np.random.randint(1000000000, size=[50,2]),
                        np.random.rand(50, 3),
                        np.random.randint(5, size=[50, 1]),
                        np.random.randint(2, size=[50, 1])], axis=1),
                        columns=['fraud', 'event', 'user',
                                 'f1', 'f2', 'f3', 'f4', 'f5'])

def tyler_says():
    print("Dan is the king; I'm the peasant.")
