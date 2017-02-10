#!/usr/local/bin/python

import os
import sys
import shutil


def find_stipper_path(unity_path):
    if os.name == "nt":
        # Windows (C:\Program Files\Unity\Editor\Data\Tools\UnusedByteCodeStripper2)
        base_path = unity_path or r"C:\Program Files\Unity"
        stripper_path = os.path.join(base_path, r"Editor\Data\Tools\UnusedByteCodeStripper2")
    else:
        # OSX (/Applications/Unity/Unity.app/Contents/Frameworks/Tools/UnusedByteCodeStripper2)
        base_path = unity_path or r"/Applications/Unity/Unity.app"
        stripper_path = os.path.join(base_path, "Contents/Frameworks/Tools/UnusedByteCodeStripper2")
    if os.path.exists(stripper_path):
        print "Path:", stripper_path
        return stripper_path
    else:
        print "ERROR: Cannot find UnusedByteCodeStripper2 directory"
        return None


def install(unity_path):
    target_path = find_stipper_path(unity_path)
    if not target_path:
        return 1

    if os.path.exists(os.path.join(target_path, "UnusedBytecodeStripper2.org.exe")):
        print "ERROR: UnusedByteCodeStripper2.Chain is already installed."
        return 1

    # copy original dlls and executable to origin folder
    path_original = os.path.join(target_path, "original")
    if not os.path.exists(path_original):
        os.mkdir(path_original)

    shutil.copy(os.path.join(target_path, "UnusedBytecodeStripper2.exe"), os.path.join(path_original, "UnusedBytecodeStripper2.exe"))
    shutil.copy(os.path.join(target_path, "UnusedBytecodeStripper2.exe.mdb"), os.path.join(path_original, "UnusedBytecodeStripper2.exe.mdb"))
    shutil.copy(os.path.join(target_path, "Mono.Cecil.dll"), os.path.join(path_original, "Mono.Cecil.dll"))
    shutil.copy(os.path.join(target_path, "Mono.Cecil.Mdb.dll"), os.path.join(path_original, "Mono.Cecil.Mdb.dll"))


    shutil.copy("IProcessDll.dll", os.path.join(target_path, "IProcessDll.dll"))

    shutil.copy("UselessAttributeStripper.dll", os.path.join(target_path, "UselessAttributeStripper.dll"))
    
    shutil.copy("HotPatch.dll", os.path.join(target_path, "HotPatch.dll"))
    shutil.copy("HotPatchEnabler.dll", os.path.join(target_path, "HotPatchEnabler.dll"))

    shutil.copy("Mono.Cecil.dll", os.path.join(target_path, "Mono.Cecil.dll"))
    shutil.copy("Mono.Cecil.Mdb.dll", os.path.join(target_path, "Mono.Cecil.Mdb.dll"))

    # stripper chain will call UnusedBytecodeStripper2.org.exe at end
    shutil.move(os.path.join(target_path, "UnusedBytecodeStripper2.exe"),
                os.path.join(target_path, "UnusedBytecodeStripper2.org.exe"))
    shutil.move(os.path.join(target_path, "UnusedBytecodeStripper2.exe.mdb"),
                os.path.join(target_path, "UnusedBytecodeStripper2.org.exe.mdb"))

    shutil.copy("UnusedBytecodeStripper2.exe", os.path.join(target_path, "UnusedBytecodeStripper2.exe"))
    shutil.copy("UnusedBytecodeStripper2.exe.mdb", os.path.join(target_path, "UnusedBytecodeStripper2.exe.mdb"))
    if os.name == "posix":
        os.chmod(os.path.join(target_path, "UnusedBytecodeStripper2.exe"), 0755)

    print "done!"
    return 0


def uninstall(unity_path):
    target_path = find_stipper_path(unity_path)
    if not target_path:
        return 1

    path_original = os.path.join(target_path, "original")

    if not os.path.exists(os.path.join(target_path, "UnusedBytecodeStripper2.org.exe")) or not os.path.exists(path_original):
        print "ERROR: UnusedByteCodeStripper2.Chain is not installed."
        return 1

    os.remove(os.path.join(target_path, "IProcessDll.dll"))
    os.remove(os.path.join(target_path, "UselessAttributeStripper.dll"))
    os.remove(os.path.join(target_path, "HotPatch.dll"))
    os.remove(os.path.join(target_path, "HotPatchEnabler.dll"))
    os.remove(os.path.join(target_path, "Mono.Cecil.dll"))
    os.remove(os.path.join(target_path, "Mono.Cecil.Mdb.dll"))
    os.remove(os.path.join(target_path, "Mono.Cecil.Rocks.dll"))
    os.remove(os.path.join(target_path, "UnusedBytecodeStripper2.exe"))
    os.remove(os.path.join(target_path, "UnusedBytecodeStripper2.exe.mdb"))
    os.remove(os.path.join(target_path, "UnusedBytecodeStripper2.org.exe"))
    os.remove(os.path.join(target_path, "UnusedBytecodeStripper2.org.exe.mdb"))

    shutil.copy(os.path.join(path_original, "Mono.Cecil.dll"), os.path.join(target_path, "Mono.Cecil.dll"))
    shutil.copy(os.path.join(path_original, "Mono.Cecil.Mdb.dll"), os.path.join(target_path, "Mono.Cecil.Mdb.dll"))
    shutil.copy(os.path.join(path_original, "Mono.Cecil.Rocks.dll"), os.path.join(target_path, "Mono.Cecil.Rocks.dll"))
    shutil.copy(os.path.join(path_original, "UnusedBytecodeStripper2.exe"), os.path.join(target_path, "UnusedBytecodeStripper2.exe"))
    shutil.copy(os.path.join(path_original, "UnusedBytecodeStripper2.exe.mdb"), os.path.join(target_path, "UnusedBytecodeStripper2.exe.mdb"))

    shutil.rmtree(path_original)

    print "done!"
    return 0


def check(unity_path):
    target_path = find_stipper_path(unity_path)
    if not target_path:
        return 1

    if os.path.exists(os.path.join(target_path, "UnusedBytecodeStripper2.org.exe")):
        print "UselessAttributeStripper is installed."
    else:
        print "UselessAttributeStripper is not installed."

    return 0


def show_usage():
    print "setup.py command [unity-path]"
    print "command:"
    print "   install     install UselessAttributeStripper to unity"
    print "   uninstall   uninstall UselessAttributeStripper from unity"
    print "   check       check if UselessAttributeStripper is installed or not"


def main():
    for item in sys.argv:
        print item
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    unity_path = sys.argv[2] if len(sys.argv) > 2 else ""

    print "command: " + command
    print "unity_path: " + unity_path

    if command == "install":
        sys.exit(install(unity_path))
    elif command == "uninstall":
        sys.exit(uninstall(unity_path))
    elif command == "check":
        sys.exit(check(unity_path))
    else:
        show_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
