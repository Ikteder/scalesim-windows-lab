import sys, struct, platform
if sys.version_info[:2] != (3, 12) or struct.calcsize('P') != 8 or platform.machine().lower() not in ('amd64', 'x86_64'):
    print('Install and select x64 CPython 3.12. This interpreter is incompatible:', sys.executable, sys.version, file=sys.stderr)
    sys.exit(1)
print('Python preflight passed:', sys.executable, sys.version)
