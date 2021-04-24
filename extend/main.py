from __future__ import print_function
from os.path import join
from SCons.Script import (AlwaysBuild, Builder, COMMAND_LINE_TARGETS, Default, DefaultEnvironment)
from colorama import Fore
from pioasm import dev_pioasm

env = DefaultEnvironment()
print( '<<<<<<<<<<<< ' + env.BoardConfig().get("name").upper() + " . >>>>>>>>>>>>" )

dev_pioasm(env)

elf = env.BuildProgram()
src = env.ElfToBin( join("$BUILD_DIR", "${PROGNAME}"), elf )
prg = env.Alias( "buildprog", src, [ env.VerboseAction("", "DONE") ] )
AlwaysBuild( prg )

upload = env.Alias("upload", prg, [
    env.VerboseAction("$UPLOADCMD", "Uploading..."),
    env.VerboseAction("", "  DONE"),
])
AlwaysBuild( upload )

debug_tool = env.GetProjectOption("debug_tool")
if None == debug_tool:
    Default( prg )
else:
    if 'cmsis-dap' in debug_tool:
        Default( upload )
    else:
        Default( prg )

