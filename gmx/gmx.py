

import ezlog

import numpy as np

import os
import re
import sys
import shutil
import tempfile
import itertools
import subprocess



_logger = ezlog.setup(__name__)



class GMX(object):


    """
    Base class for all python tools wrapping GROMACS utility executables.

    The GMX class provides 3 main abilities:
      1) automatic management of a temprorary workarea accessible in subclasses as self.workarea
      2) method for executing the GROMACS binary that handles redirection
      3) calling parameters mirrors the underlying binary's flags

    Developers need to implement the __call__(self, *args, **kwargs) method for specific utilities.
        class MyUtil(GMX):
            def __call__(self, *args, **kws):
               ...

    This way, a user has an interface similar to calling a commandline:
        util = MyUtil(stdout='/dev/null', stderr='/dev/null')
        results = util(f='traj.xtc', s='structure.tpr', n='foo.ndx')

    """


    def __init__(self, stdout=None, stderr=None):
        """
        @params stdout=None (string), stderr=None (string): the paths to the files to record the std{out,error} output of the underlying GROMACS binary.
        """

        self.stdout = stdout
        self.stderr = stderr

        username = os.environ['LOGNAME']
        classname = self.__class__.__name__
        self.workarea = tempfile.mkdtemp(prefix='%s.%s.' % (username, classname))

    def __del__(self):
        shutil.rmtree(self.workarea, ignore_errors=True)


    def execute(self, command):
        """
        Attempt to execute the command
        @param command (string)
        @return (int): the return code of the called process
        """

        cmd = command
        kws = {}

        try:

            if self.stdout and self.stdout == self.stderr:
                fd = open(self.stdout, 'w')
                kws['stdout'] = fd
                kws['stderr'] = fd
                cmd += ' 2>&1 %s' % self.stdout

            elif self.stdout:
                fd_out = open(self.stdout, 'w')
                kws['stdout'] = fd_out
                cmd += ' 1>%s' % self.stdout

            elif self.stderr:
                fd_err = open(self.stderr, 'w')
                kws['stderr'] = fd_err
                cmd += ' 2>%s' % self.stderr


            _logger.info('Executing: %s' % cmd)
            subprocess.check_call(command.split(), **kws)
            return 0

        except subprocess.CalledProcessError, e:
            _logger.error('Command %s failed with %s' % (cmd, e.returncode))
            return e.returncode

        finally:

            try: fd.close()
            except NameError: pass

            try: fd_out.close()
            except NameError: pass

            try: fd_err.close()
            except NameError: pass

    def flags(self, **kws):
        """
        Accept arbitrary keyword arguments and format them for calling a GROMACS executable
        @return (string)
        """

        return ' '.join([ '-%s %s' % (k, v) for k, v in kws.iteritems() ])



    def __call__(self, *args, **kws):
        raise NotImplementedError




class g_rms (GMX):

    """
    Wrapper for the GROMACS g_rms executable
    """


    def __init__(self, execname='g_rms', **kws):
        self.execname = execname
        self.regex    = re.compile(r'^\s*([-\.\d]+)\s+(?P<rmsd>[-\.\d]+)')

        GMX.__init__(self, **kws)

    def __call__(self, **kws):
        """
        Only a single output file is allowed: use keyword 'o' (as in g_rms -o foo.xvg) for this
        @return (numpy.array of floats)
        """

        output = kws.pop('o', 'rmsd.xvg')
        output = os.path.join(self.workarea, output)

        cmd = '%(exe)s -o %(output)s %(args)s' % {
            'exe' : self.execname,
            'output' : output,
            'args' : self.flags(**kws)}

        self.execute(cmd)
 
        with open(output) as fd:

            _logger.info('Reading RMSD values from %s' % fd.name)

            matches = itertools.ifilter(None, itertools.imap(self.regex.match, fd))
            rmsds   = map(lambda m: float(m.group('rmsd')), matches)
            return np.array(rmsds)




def _test():

    rmsd = g_rms(stdout='/dev/null', stderr='/dev/null')
    rmsds = rmsd(o='foo.xvg', s='tests/test.pdb', f='tests/test.xtc', n='tests/test.ndx')
    print 'Number of values:', len(rmsds)



if __name__ == '__main__':
    _test()
