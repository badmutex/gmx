


def g_rms(path, **kws):
    from gmx import g_rms
    stdout = kws.pop('stdout', None)
    stderr = kws.pop('stderr', None)
    func = g_rms(stdout = stdout, stderr = stderr)
    return func(f=path, **kws)
