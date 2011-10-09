


def g_rms(path, **kws):

    from gmx.classes import G_RMS

    stdout = kws.pop('stdout', None)
    stderr = kws.pop('stderr', None)
    func   = G_RMS(stdout = stdout, stderr = stderr)

    return func(f=path, **kws)
