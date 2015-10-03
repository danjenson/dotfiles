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
      color='red',
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
       color='red',
       trig=trig,
       trig_pi_step=trig_pi_step,
       xpad=xpad,
       ypad=ypad)
    return


def pp(Xs, Ys, title, figname,
       holes=[],
       labels=[],
       color='red',
       same_color=True,
       trig=False,
       trig_pi_step=Fraction(1, 4),
       xlim=None,
       ylim=None,
       xpad=0.1,
       ypad=0.1):
    '''plot piecewise Xs and Ys'''

    _setup(Xs, Ys, title, trig, trig_pi_step, xlim, ylim, xpad, ypad)
    _plot(Xs, Ys, holes, labels, color, same_color)
    _save(figname)
    _cleanup()
    return


def ped(func, x_range, lim_xy, epsilon, delta, title, figname):
    '''plot epsilon-delta'''
    X = np.linspace(x_range[0], x_range[1])
    Y = np.vectorize(func)(X)
    lim_x = lim_xy[0]
    lim_y = lim_xy[1]
    _setup([X], [Y], title, xlim=(x_range))
    Xtop, Ytop = _hline((x_range[0], lim_x - delta), func(lim_x - delta))
    Xbottom, Ybottom = _hline((x_range[0], lim_x + delta), func(lim_x + delta))
    Xleft, Yleft = _vline(lim_x - delta, (0, func(lim_x - delta)))
    Xright, Yright = _vline(lim_x + delta, (0, func(lim_x + delta)))
    _plot([X], [Y], color='darkblue')
    _plot([Xtop, Xbottom, Xleft, Xright], [Ytop, Ybottom, Yleft, Yright])
    _add_limit_label(plt.axes(), lim_xy)
    _add_epsilon_labels(plt.axes(), lim_y, epsilon)
    _add_delta_labels(plt.axes(), lim_x, delta)
    _save(figname)
    _cleanup()
    return


def _setup(Xs, Ys, title,
          trig=False, trig_pi_step=0,
          xlim=None, ylim=None,
          xpad=0.1, ypad=0.1):
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


def _plot(Xs, Ys, holes=[], labels=[], color='red', same_color=True):
    # if more Y-sets than X-sets, reuse X coordinates by cycling
    if len(Ys) > len(Xs):
        Xs = it.cycle(Xs)
    if not labels:
        labels = [None] * len(Ys)
    for X, Y, label in zip(Xs, Ys, labels):
        if same_color:
            plt.plot(X, Y, color=color, zorder=1, label=label)
        else:
            plt.plot(X, Y, zorder=1, label=label)
    for x, y in holes:
        plt.scatter(x, y, edgecolor=color, facecolor='white', zorder=2)
    if any(labels):
        plt.legend()
    return


def _hline(x_range, y):
    return np.linspace(x_range[0], x_range[1], 1000), np.linspace(y, y, 1000)


def _vline(x, y_range):
    return np.linspace(x, x, 1000), np.linspace(y_range[0], y_range[1], 1000)


def _add_limit_label(axes, lim_xy):
    lim_x = lim_xy[0]
    lim_y = lim_xy[1]
    _add_ticks(axes, {lim_x: str(lim_x)}, 'x')
    _add_ticks(axes, {lim_y: str(lim_y)}, 'y')
    return


def _add_epsilon_labels(axes, lim_y, epsilon):
    tick_labels_dict = {
        lim_y - epsilon: '$%g - \\varepsilon$' % lim_y,
        lim_y + epsilon: '$%g + \\varepsilon$' % lim_y
    }
    _add_ticks(axes, tick_labels_dict, 'y')
    return
    

def _add_delta_labels(axes, lim_x, delta):
    tick_labels_dict = {
        lim_x - delta: '$%g - \\delta$' % lim_x,
        lim_x + delta: '$%g + \\delta$' % lim_x
    }
    _add_ticks(axes, tick_labels_dict, 'x')
    return


def _add_ticks(axes, tick_labels_dict, axis='x'):
    if axis == 'x':
        locs = axes.get_xticks().tolist()
    elif axis == 'y':
        locs = axes.get_yticks().tolist()
    else:
        raise Exception('specify either x or y axis')
    labels = [str(loc) for loc in locs]

    d = dict(zip(locs, labels))
    for tick, label in tick_labels_dict.items():
        d[tick] = label  # add or replace label

    new_locs = list(d.keys())
    new_labels = list(d.values())

    if axis == 'x':
        axes.set_xticks(new_locs)
        axes.set_xticklabels(new_labels)
    if axis == 'y':
        axes.set_yticks(new_locs)
        axes.set_yticklabels(new_labels)
    return


def _save(figname):
    plt.savefig('figures/' + figname + '.pdf')
    return


def _cleanup():
    plt.clf()
    return
