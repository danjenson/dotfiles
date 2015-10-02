import matplotlib
import matplotlib.pyplot as plt
import itertools as it
import numpy as np
from fractions import Fraction

if matplotlib.__version__ > '1.4':
    plt.style.use('ggplot')


def p(X, Y, title, figname,
      holes=[],
      labels=[],
      trig=False,
      trig_pi_step=Fraction(1, 4),
      xlim=None,
      ylim=None,
      xpad=0.1,
      ypad=0.1):
    '''plot regular X, Y'''

    pp([X], [Y], title, figname,
       holes=holes,
       labels=[],
       trig=trig,
       trig_pi_step=trig_pi_step,
       xpad=xpad,
       ypad=ypad)
    return


def pp(Xs, Ys, title, figname,
       holes=[],
       labels=[],
       same_color=True,
       trig=False,
       trig_pi_step=Fraction(1, 4),
       xlim=None,
       ylim=None,
       xpad=0.1,
       ypad=0.1):
    '''plot piecewise Xs and Ys'''

    _setup(Xs, Ys, title, trig, trig_pi_step, xlim, ylim, xpad, ypad)
    _plot(Xs, Ys, holes, labels, same_color)
    _save(figname)
    _cleanup()
    return


def ped(func, x_range, lim_x, epsilon, delta, title, figname):
    '''plot epsilon-delta'''
    X = np.linspace(x_range[0], x_range[1])
    Y = np.vectorize(func)(X)
    _setup([X], [Y], title, trig=False, trig_pi_sep=0, xpad=0, ypad=0)
    lim_y = func(lim_x)
    Xtop, Ytop = _hline((x_range[0], lim_x - delta), func(lim_x - delta))
    Xbottom, Ybottom = _hline((x_range[0], lim_x + delta), func(lim_x + delta))
    Xleft, Yleft = _vline(lim_x - delta, (0, func(lim_x - delta)))
    Xright, Yright = _vline(lim_x + delta, (0, func(lim_x + delta)))
    _plot([X], [Y])
    _plot([Xtop, Xbottom, Xleft, Xright], [Ytop, Ybottom, Yleft, Yright])
    _save(figname)
    _cleanup()
    return


def _setup(Xs, Ys, title, trig, trig_pi_step, xlim, ylim, xpad, ypad):
    plt.clf()
    plt.title(title)
    if not xlim:
        X = np.concatenate(Xs)
        xbuff = np.fabs(X.max() - X.min()) * xpad
        xmin = X.min() - xbuff
        xmax = X.max() + xbuff
        xlim = (xmin, xmax)
    if not ylim:
        Y = np.concatenate(Ys)
        ybuff = np.fabs(Y.max() - Y.min()) * ypad
        ymin = Y.min() - ybuff
        ymax = Y.max() + ybuff
        ylim = (ymin, ymax)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    if trig:
        _add_trig_labels(plt.axes(), xmin, xmax, ymin, ymax, trig_pi_step)
    return


def _add_trig_labels(axes, xmin, xmax, ymin, ymax, pi_step):
    if xmin >= 0:
        xticks, xlabels = _trig_axis(xmax, pi_step)
    elif xmax <= 0:
        xticks, xlabels = _trig_axis(xmin, pi_step)
    else:
        nxticks, nxlabels = _trig_axis(xmin, pi_step)
        pxticks, pxlabels = _trig_axis(xmax, pi_step)
        xticks = nxticks + pxticks
        xlabels = nxlabels + pxlabels
    axes.set_xticks(xticks)
    axes.set_xticklabels(xlabels)
    return


def _trig_axis(v, pi_step):
    is_neg = False
    if (v < 0):
        v = np.fabs(v)
        is_neg = True

    ticks = [0]
    labels = ['$0$']
    steps = (v / (np.pi * pi_step) + 0.5).astype('int')
    for s in range(1, steps + 1):
        if is_neg:
            s *= -1
        frac = s * pi_step
        ticks.append(frac * np.pi)
        if frac.denominator == 1:
            label = str(frac.numerator) + r'\pi'
        else:
            label = r'\frac{'+ str(frac.numerator) + r'\pi}'\
                    + '{' + str(frac.denominator) + '}'
        labels.append('$' + label + '$')

    if is_neg:
        ticks.reverse()
        labels.reverse()

    return ticks, labels


def _plot(Xs, Ys, holes=None, labels=None, same_color=True):
    # if more Y-sets than X-sets, reuse X coordinates by cycling
    if len(Ys) > len(Xs):
        Xs = it.cycle(Xs)
    if not labels:
        labels = [None] * len(Ys)
    for X, Y, label in zip(Xs, Ys, labels):
        if same_color:
            plt.plot(X, Y, color='red', zorder=1, label=label)
        else:
            plt.plot(X, Y, zorder=1, label=label)
    for x, y in holes:
        plt.scatter(x, y, edgecolor='red', facecolor='white', zorder=2)
    if any(labels):
        plt.legend()
    return


def _hline(x_range, y):
    return np.linspace(x_range[0], x_range[1], 1000), np.linspace(y, y, 1000)


def _vline(x, y_range):
    return np.linspace(x, x, 1000), np.linspace(y_range[0], y_range[1], 1000)
    

def _save(figname):
    plt.savefig('figures/' + figname + '.pdf')
    return


def _cleanup():
    plt.clf()
    return
