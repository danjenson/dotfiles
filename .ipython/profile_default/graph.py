import os
import matplotlib
import matplotlib.pyplot as plt
import itertools as it
import numpy as np
from matplotlib.patches import Rectangle
from fractions import Fraction

if matplotlib.__version__ > '1.4':
    plt.style.use('ggplot')


class Hole():
    def __init__(self, x, y, filled=False, color='red'):
        self.x = x
        self.y = y
        self.filled = filled
        self.color = color


def pp(Xs, Ys,
       title=None,
       figname=None,
       holes=[],
       rects=[],
       labels=[],
       color='red',
       same_color=True,
       trig=False,
       trig_pi_step=Fraction(1, 4),
       xlabel=None,
       ylabel=None,
       xlim=None,
       ylim=None,
       xpad=(0.0, 0.0),
       ypad=(0.0, 0.0),
       xticks={},
       yticks={}):
    '''plot piecewise Xs and Ys'''

    _setup(Xs, Ys, title, holes, trig, trig_pi_step,
           xlabel, ylabel, xlim, ylim, xpad, ypad, xticks, yticks)
    _plot(Xs, Ys, holes, rects, labels, color, same_color)
    if figname:
        _save(figname)
    return


def p(X, Y, **kwargs):
    '''plot regular X, Y'''
    pp([X], [Y], **kwargs)
    return


def pf(func_domains_tpl_list, **kwargs):
    '''Plot functions'''
    Xs = []
    Ys = []
    # convenience when plotting only one function
    if isinstance(func_domains_tpl_list, tuple):
        func_domains_tpl_list = [func_domains_tpl_list]
    for func, domains in func_domains_tpl_list:
        # convert to list if single tuple passed
        vfunc = np.vectorize(func)
        if isinstance(domains, tuple):
            domains = [domains]
        for start_x, end_x in domains:
            X = np.linspace(start_x, end_x, 10000)
            Y = vfunc(X)
            Xs.append(X)
            Ys.append(Y)

    pp(Xs, Ys, **kwargs)
    return


def ped(func, x_range, lim_xy, epsilon, delta, **kwargs):
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
    if kwargs['figname']:
        _save(kwargs['figname'])
    else:
        plt.show()
    _cleanup()
    return


def psum(func, domain, n_rects, position='left', **kwargs):
    dx = (domain[1] - domain[0]) / n_rects
    rects = []
    for i in range(n_rects):
        x = {'left': i * dx,
             'right': i * dx + dx,
             'midpoint': ((i * dx) + (i * dx + dx)) / 2}[position]
        y = func(x)
        rects.append(Rectangle((i * dx, 0),     # (x, y)
                                dx, y,          # width, height
                                alpha=0.5))     # alpha
    pf([(func, domain)], rects=rects, **kwargs)


def _setup(Xs, Ys,
           title=None,
           holes=[],
           trig=False,
           trig_pi_step=0,
           xlabel=None,
           ylabel=None,
           xlim=None,
           ylim=None,
           xpad=(0.0, 0.0),
           ypad=(0.0, 0.0),
           xticks={},
           yticks={}):
    plt.clf()
    if title:
        plt.title(title)
    if not xlim:
        Xholes = np.array([h.x for h in holes])
        Xall = np.concatenate(Xs + [Xholes])
        xbuff_left = np.fabs(Xall.max() - Xall.min()) * xpad[0]
        xbuff_right = np.fabs(Xall.max() - Xall.min()) * xpad[1]
        xmin = Xall.min() - xbuff_left
        xmax = Xall.max() + xbuff_right
        xlim = (xmin, xmax)
    if not ylim:
        Yholes = np.array([h.y for h in holes])
        Yall = np.concatenate(Ys + [Yholes])
        ybuff_bottom = np.fabs(Yall.max() - Yall.min()) * ypad[0]
        ybuff_top = np.fabs(Yall.max() - Yall.min()) * ypad[1]
        ymin = Yall.min() - ybuff_bottom
        ymax = Yall.max() + ybuff_top
        ylim = (ymin, ymax)
    if trig:
        _add_trig_labels(plt.axes(), xmin, xmax, ymin, ymax, trig_pi_step)
    if xlabel:
        plt.axes().set_xlabel(xlabel)
    if ylabel:
        plt.axes().set_ylabel(ylabel)
    plt.xlim(xlim)
    plt.ylim(ylim)
    if xticks:
        _add_ticks(plt.axes(), xticks, 'x')
    if yticks:
        _add_ticks(plt.axes(), yticks, 'y')
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
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


def _plot(Xs, Ys, holes=[], rects=[], labels=[], color='red', same_color=True):
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
    for hole in holes:
        facecolor = 'white'
        if hole.filled:
            facecolor = hole.color
        plt.scatter(hole.x, hole.y,
                    edgecolor=hole.color,
                    facecolor=facecolor,
                    zorder=2)
    if rects:
        ax = plt.gca()
        for rect in rects:
            ax.add_patch(rect)
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
    directory = 'figures'
    if not os.path.exists(directory):
        os.makedirs(directory)
    full_path = os.path.join(directory, figname + '.pdf')
    plt.savefig(full_path)
    return


def _cleanup():
    plt.clf()
    return
