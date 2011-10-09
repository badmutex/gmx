

def g_rms(path, **kws):

    try:                from gmx.classes import G_RMS
    except ImportError: from classes     import G_RMS

    stdout = kws.pop('stdout', None)
    stderr = kws.pop('stderr', None)
    func   = G_RMS(stdout = stdout, stderr = stderr)

    return func(f=path, **kws)


def g_gyrate(path, **kws):

    try:                from gmx.classes import G_GYRATE
    except ImportError: from classes     import G_GYRATE

    stdout = kws.pop('stdout', None)
    stderr = kws.pop('stderr', None)
    func   = G_GYRATE(stdout = stdout, stderr = stderr)

    return func(f=path, **kws)
