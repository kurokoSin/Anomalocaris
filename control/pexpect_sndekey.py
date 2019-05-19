#!/usr/bin/env python
import pexpect
import sys

args = sys.argv
p = pexpect.spawn("ssh-copy-id " + args[1] )
p.logfile_read = sys.stdout

p.expect   ("Are you sure you want to continue connecting (yes/no)?")
p.sendline ("yes")
p.expect   ("password:")
p.sendline ("vagrant")
p.terminate()
p.expect(pexpect.EOF)
