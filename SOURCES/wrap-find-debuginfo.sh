#!/bin/bash
# Wrapper script for find-debuginfo.sh
#
# Usage:
#  wrap-find-debuginfo.sh SYSROOT-PATH SCRIPT-PATH SCRIPT-ARGS...
#
# The wrapper saves the original version of ld.so found in SYSROOT-PATH,
# invokes SCRIPT-PATH with SCRIPT-ARGS, and then restores the
# LDSO-PATH file, followed by note merging and DWZ compression.
# As a result, ld.so has (mostly) unchanged debuginfo even
# after debuginfo extraction.
#
# For libc.so.6, a set of strategic symbols is preserved in .symtab
# that are frequently used in valgrind suppressions and elsewhere.

set -ex

ldso_tmp="$(mktemp)"
libc_tmp="$(mktemp)"

# Prefer a separately installed debugedit over the RPM-integrated one.
if command -v debugedit >/dev/null ; then
    debugedit=debugedit
else
    debugedit=/usr/lib/rpm/debugedit
fi

cleanup () {
    rm -f "$ldso_tmp" "$libc_tmp"
}
trap cleanup 0

sysroot_path="$1"
shift
script_path="$1"
shift

# See ldso_path setting in glibc.spec.
ldso_path=
for ldso_candidate in `find "$sysroot_path" -regextype posix-extended \
  -regex '.*/ld(-.*|64|)\.so\.[0-9]+$' -type f` ; do
    if test -z "$ldso_path" ; then
	ldso_path="$ldso_candidate"
    else
	echo "error: multiple ld.so candidates: $ldso_path, $ldso_candidate"
	exit 1
    fi
done

# libc.so.6 always uses this name, so it is simpler to locate.
libc_path=
for libc_candidate in `find "$sysroot_path" -name libc.so.6`; do
    if test -z "$libc_path" ; then
	libc_path="$libc_candidate"
    else
	echo "error: multiple libc.so.6 candidates: $libc_path, $libc_candidate"
	exit 1
    fi
done


# Preserve the original files.
cp "$ldso_path" "$ldso_tmp"
cp "$libc_path" "$libc_tmp"

# Run the debuginfo extraction.
"$script_path" "$@"

# Restore the original files.
cp "$ldso_tmp" "$ldso_path"
cp "$libc_tmp" "$libc_path"

# Reduce the size of notes.  Primarily for annobin.
objcopy --merge-notes "$ldso_path"
objcopy --merge-notes "$libc_path"

# libc.so.6: Reduce to valuable symbols.  Eliminate file symbols,
# annobin symbols, and symbols used by the glibc build to implement
# hidden aliases (__EI_*).  We would also like to remove __GI_*
# symbols, but even listing them explicitly (as in -K __GI_strlen)
# still causes strip to remove them, so there is no filtering of
# __GI_* here.  (Debuginfo is gone after this, so no need to optimize
# it.)
strip -w \
    -K '*' \
    -K '!*.c' \
    -K '!*.os' \
    -K '!.annobin_*' \
    -K '!__EI_*' \
    -K '!__PRETTY_FUNCTION__*' \
    "$libc_path"

# ld.so: Rewrite the source file paths to match the extracted
# locations.  First compute the arguments for invoking debugedit.
# See find-debuginfo.sh.
debug_dest_name="/usr/src/debug"
last_arg=
while true ; do
    arg="$1"
    shift || break
    case "$arg" in
	(--unique-debug-src-base)
	    debug_dest_name="/usr/src/debug/$1"
	    shift
	    ;;
	(-*)
	    ;;
	(*)
	    last_arg="$arg"
	    ;;
    esac
done
debug_base_name=${last_arg:-$RPM_BUILD_ROOT}
$debugedit -b "$debug_base_name" -d "$debug_dest_name" -n $ldso_path

# Apply single-file DWARF optimization.
dwz $ldso_path
