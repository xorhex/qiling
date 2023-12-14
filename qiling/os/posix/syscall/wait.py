#!/usr/bin/env python3
#
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import os

from qiling import Qiling
from qiling.os.posix.const import ECHILD

def ql_syscall_wait4(ql: Qiling, pid: int, wstatus: int, options: int, rusage: int):
    # convert to signed (pid_t is 32bit)
    pid = ql.unpack32s(ql.pack32(pid))
    # python expects options to be a signed 32bit int
    options = ql.unpack32s(ql.pack32(options))

    try:
        spid, status, _ = os.wait4(pid, options)

        if wstatus:
            ql.mem.write_ptr(wstatus, status, 4)

        retval = spid
    except ChildProcessError:
        retval = -ECHILD

    return retval
