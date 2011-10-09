#!/usr/bin/env python

import gmx

results = gmx.g_gyrate('test.xtc', s='test.pdb', n='test.ndx')
print results
