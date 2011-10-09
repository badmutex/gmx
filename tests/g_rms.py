#!/usr/bin/env python

import gmx

results = gmx.g_rms('test.xtc', s='test.pdb', n='test.ndx')
print results
