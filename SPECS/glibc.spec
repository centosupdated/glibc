%define glibcsrcdir glibc-2.34
%define glibcversion 2.34
# Pre-release tarballs are pulled in from git using a command that is
# effectively:
#
# git archive HEAD --format=tar --prefix=$(git describe --match 'glibc-*')/ \
#	> $(git describe --match 'glibc-*').tar
# gzip -9 $(git describe --match 'glibc-*').tar
#
# glibc_release_url is only defined when we have a release tarball.
# Conversly, glibc_autorequires is set for development snapshots, where
# dependencies based on symbol versions are inaccurate.
%{lua: if string.match(rpm.expand("%glibcsrcdir"), "^glibc%-[0-9.]+$") then
    rpm.define("glibc_release_url https://ftp.gnu.org/gnu/glibc/")
  end
  local major, minor = string.match(rpm.expand("%glibcversion"),
                                    "^([0-9]+)%.([0-9]+)%.9000$")
  if major and minor then
    rpm.define("glibc_autorequires 1")
    -- The minor version in a .9000 development version lags the actual
    -- symbol version by one.
    local symver = "GLIBC_" .. major .. "." .. (minor + 1)
    rpm.define("glibc_autorequires_symver " .. symver)
  else
    rpm.define("glibc_autorequires 0")
  end}
##############################################################################
# We support the following options:
# --with/--without,
# * testsuite - Running the testsuite.
# * benchtests - Running and building benchmark subpackage.
# * bootstrap - Bootstrapping the package.
# * werror - Build with -Werror
# * docs - Build with documentation and the required dependencies.
# * valgrind - Run smoke tests with valgrind to verify dynamic loader.
#
# You must always run the testsuite for production builds.
# Default: Always run the testsuite.
%bcond_without testsuite
# Default: Always build the benchtests.
%bcond_without benchtests
# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Enable using -Werror
%bcond_without werror
# Default: Always build documentation.
%bcond_without docs

# Default: Always run valgrind tests if there is architecture support.
%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif
# Restrict %%{valgrind_arches} further in case there are problems with
# the smoke test.
%if %{with valgrind}
%ifarch ppc64 ppc64p7
# The valgrind smoke test does not work on ppc64, ppc64p7 (bug 1273103).
%undefine with_valgrind
%endif
%endif

%if %{with bootstrap}
# Disable benchtests, -Werror, docs, and valgrind if we're bootstrapping
%undefine with_benchtests
%undefine with_werror
%undefine with_docs
%undefine with_valgrind
%endif

# The annobin annotations cause binutils to produce broken ARM EABI
# unwinding information.  Symptom is a hang/test failure for
# malloc/tst-malloc-stats-cancellation.  See
# <https://bugzilla.redhat.com/show_bug.cgi?id=1951492>.
%ifarch armv7hl
%undefine _annotated_build
%endif

##############################################################################
# Any architecture/kernel combination that supports running 32-bit and 64-bit
# code in userspace is considered a biarch arch.
%define biarcharches %{ix86} x86_64 s390 s390x

# Avoid generating a glibc-headers package on architectures which are
# not biarch.
%ifarch %{biarcharches}
%define need_headers_package 1
%if 0%{?rhel} > 0
%define headers_package_name glibc-headers
%else
%ifarch %{ix86} x86_64
%define headers_package_name glibc-headers-x86
%endif
%ifarch s390 s390x
%define headers_package_name glibc-headers-s390
%endif
%dnl !rhel
%endif
%else
%define need_headers_package 0
%dnl !biarcharches
%endif

##############################################################################
# Utility functions for pre/post scripts.  Stick them at the beginning of
# any lua %pre, %post, %postun, etc. sections to have them expand into
# those scripts.  It only works in lua sections and not anywhere else.
%define glibc_post_funcs() \
-- We use lua posix.exec because there may be no shell that we can \
-- run during glibc upgrade.  We used to implement much of %%post as a \
-- C program, but from an overall maintenance perspective the lua in \
-- the spec file was simpler and safer given the operations required. \
-- All lua code will be ignored by rpm-ostree; see: \
-- https://github.com/projectatomic/rpm-ostree/pull/1869 \
-- If we add new lua actions to the %%post code we should coordinate \
-- with rpm-ostree and ensure that their glibc install is functional. \
function post_exec (program, ...) \
  local pid = posix.fork () \
  if pid == 0 then \
    posix.exec (program, ...) \
    assert (nil) \
  elseif pid > 0 then \
    posix.wait (pid) \
  end \
end \
\
function update_gconv_modules_cache () \
  local iconv_dir = "%{_libdir}/gconv" \
  local iconv_cache = iconv_dir .. "/gconv-modules.cache" \
  local iconv_modules = iconv_dir .. "/gconv-modules" \
  if (posix.utime (iconv_modules) == 0) then \
    if (posix.utime (iconv_cache) == 0) then \
      post_exec ("%{_prefix}/sbin/iconvconfig", \
		 "-o", iconv_cache, \
		 "--nostdlib", \
		 iconv_dir) \
    else \
      io.stdout:write ("Error: Missing " .. iconv_cache .. " file.\n") \
    end \
  end \
end \
%{nil}

##############################################################################
# %%package glibc - The GNU C Library (glibc) core package.
##############################################################################
Summary: The GNU libc libraries
Name: glibc
Version: %{glibcversion}
Release: 25%{?dist}

# In general, GPLv2+ is used by programs, LGPLv2+ is used for
# libraries.
#
# LGPLv2+ with exceptions is used for things that are linked directly
# into dynamically linked programs and shared libraries (e.g. crt
# files, lib*_nonshared.a).  Historically, this exception also applies
# to parts of libio.
#
# GPLv2+ with exceptions is used for parts of the Arm unwinder.
#
# GFDL is used for the documentation.
#
# Some other licenses are used in various places (BSD, Inner-Net,
# ISC, Public Domain).
#
# HSRL and FSFAP are only used in test cases, which currently do not
# ship in binary RPMs, so they are not listed here.  MIT is used for
# scripts/install-sh, which does not ship, either.
#
# GPLv3+ is used by manual/texinfo.tex, which we do not use.
#
# LGPLv3+ is used by some Hurd code, which we do not build.
#
# LGPLv2 is used in one place (time/timespec_get.c, by mistake), but
# it is not actually compiled, so it does not matter for libraries.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv2+ with exceptions and BSD and Inner-Net and ISC and Public Domain and GFDL

URL: http://www.gnu.org/software/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.xz
Source1: nscd.conf
Source2: bench.mk
Source3: glibc-bench-compare
Source4: glibc.req.in
Source5: glibc.attr
Source10: wrap-find-debuginfo.sh
Source11: parse-SUPPORTED.py
# Include in the source RPM for reference.
Source12: ChangeLog.old

######################################################################
# Activate the wrapper script for debuginfo generation, by rewriting
# the definition of __debug_install_post.
%{lua:
local wrapper = rpm.expand("%{SOURCE10}")
local sysroot = rpm.expand("%{glibc_sysroot}")
local original = rpm.expand("%{macrobody:__debug_install_post}")
-- Strip leading newline.  It confuses the macro redefinition.
-- Avoid embedded newlines that confuse the macro definition.
original = original:match("^%s*(.-)%s*$"):gsub("\\\n", "")
rpm.define("__debug_install_post bash " .. wrapper
  .. " " .. sysroot .. " " .. original)
}

# The wrapper script relies on the fact that debugedit does not change
# build IDs.
%define _no_recompute_build_ids 1
%undefine _unique_build_ids

##############################################################################
# Patches:
# - See each individual patch file for origin and upstream status.
# - For new patches follow template.patch format.
##############################################################################
Patch1: glibc-fedora-nscd.patch
Patch4: glibc-fedora-linux-tcsetattr.patch
Patch6: glibc-fedora-localedef.patch
Patch8: glibc-fedora-manual-dircategory.patch
Patch9: glibc-rh827510.patch
Patch13: glibc-fedora-localedata-rh61908.patch
Patch15: glibc-rh1070416.patch
Patch16: glibc-nscd-sysconfig.patch
Patch17: glibc-cs-path.patch
Patch18: glibc-c-utf8-locale-1.patch
Patch19: glibc-c-utf8-locale-2.patch
Patch23: glibc-python3.patch
Patch29: glibc-fedora-nsswitch.patch
Patch30: glibc-deprecated-selinux-makedb.patch
Patch31: glibc-deprecated-selinux-nscd.patch
Patch32: glibc-upstream-2.34-1.patch
Patch33: glibc-upstream-2.34-2.patch
Patch34: glibc-upstream-2.34-3.patch
Patch35: glibc-upstream-2.34-4.patch
Patch36: glibc-upstream-2.34-5.patch
Patch37: glibc-upstream-2.34-6.patch
Patch38: glibc-upstream-2.34-7.patch
Patch39: glibc-upstream-2.34-8.patch
Patch40: glibc-upstream-2.34-9.patch
Patch41: glibc-upstream-2.34-10.patch
Patch42: glibc-upstream-2.34-11.patch
Patch43: glibc-upstream-2.34-12.patch
Patch44: glibc-upstream-2.34-13.patch
Patch45: glibc-upstream-2.34-14.patch
Patch46: glibc-upstream-2.34-15.patch
Patch47: glibc-upstream-2.34-16.patch
Patch48: glibc-upstream-2.34-17.patch
Patch49: glibc-upstream-2.34-18.patch
Patch50: glibc-upstream-2.34-19.patch
Patch51: glibc-upstream-2.34-20.patch
Patch52: glibc-upstream-2.34-21.patch
Patch53: glibc-upstream-2.34-22.patch
Patch54: glibc-upstream-2.34-23.patch
Patch55: glibc-upstream-2.34-24.patch
Patch56: glibc-upstream-2.34-25.patch
Patch57: glibc-upstream-2.34-26.patch
Patch58: glibc-upstream-2.34-27.patch
Patch59: glibc-upstream-2.34-28.patch
Patch60: glibc-upstream-2.34-29.patch
Patch61: glibc-upstream-2.34-30.patch
Patch62: glibc-upstream-2.34-31.patch
Patch63: glibc-upstream-2.34-32.patch
Patch64: glibc-upstream-2.34-33.patch
Patch65: glibc-upstream-2.34-34.patch
Patch66: glibc-upstream-2.34-35.patch
Patch67: glibc-upstream-2.34-36.patch
Patch68: glibc-upstream-2.34-37.patch
Patch69: glibc-upstream-2.34-38.patch
Patch70: glibc-upstream-2.34-39.patch
Patch71: glibc-upstream-2.34-40.patch
Patch72: glibc-upstream-2.34-41.patch
Patch73: glibc-upstream-2.34-42.patch
Patch74: glibc-upstream-2.34-43.patch
Patch75: glibc-upstream-2.34-44.patch
Patch76: glibc-upstream-2.34-45.patch
Patch77: glibc-upstream-2.34-46.patch
Patch78: glibc-upstream-2.34-47.patch
Patch79: glibc-upstream-2.34-48.patch
Patch80: glibc-upstream-2.34-49.patch
Patch81: glibc-rh2027789.patch
Patch82: glibc-rh2023422-1.patch
Patch83: glibc-rh2023422-2.patch
Patch84: glibc-rh2023422-3.patch
Patch85: glibc-rh2029410.patch
Patch86: glibc-upstream-2.34-50.patch
Patch87: glibc-upstream-2.34-51.patch
Patch88: glibc-upstream-2.34-52.patch
Patch89: glibc-upstream-2.34-53.patch
Patch90: glibc-rh1988382.patch
Patch91: glibc-upstream-2.34-54.patch
Patch92: glibc-upstream-2.34-55.patch
Patch93: glibc-upstream-2.34-56.patch
Patch94: glibc-upstream-2.34-57.patch
Patch95: glibc-upstream-2.34-58.patch
Patch96: glibc-upstream-2.34-59.patch
Patch97: glibc-upstream-2.34-60.patch
Patch98: glibc-upstream-2.34-61.patch
Patch99: glibc-upstream-2.34-62.patch
Patch100: glibc-upstream-2.34-63.patch
Patch101: glibc-upstream-2.34-64.patch
Patch102: glibc-upstream-2.34-65.patch
Patch103: glibc-upstream-2.34-66.patch
Patch104: glibc-upstream-2.34-67.patch
Patch105: glibc-upstream-2.34-68.patch
Patch106: glibc-upstream-2.34-69.patch
Patch107: glibc-upstream-2.34-70.patch
Patch108: glibc-upstream-2.34-71.patch
Patch109: glibc-upstream-2.34-72.patch
Patch110: glibc-upstream-2.34-73.patch
Patch111: glibc-rh2032647-1.patch
Patch112: glibc-rh2032647-2.patch
Patch113: glibc-rh2032647-3.patch
Patch114: glibc-rh2032647-4.patch
Patch115: glibc-rh2032647-5.patch
Patch116: glibc-rh2032647-6.patch
Patch117: glibc-rh2024347-1.patch
Patch118: glibc-rh2024347-2.patch
Patch119: glibc-rh2024347-3.patch
Patch120: glibc-rh2024347-4.patch
Patch121: glibc-rh2024347-5.patch
Patch122: glibc-rh2024347-6.patch
Patch123: glibc-rh2024347-7.patch
Patch124: glibc-rh2024347-8.patch
Patch125: glibc-rh2024347-9.patch
Patch126: glibc-rh2024347-10.patch
Patch127: glibc-rh2024347-11.patch
Patch128: glibc-rh2024347-12.patch
Patch129: glibc-rh2024347-13.patch
Patch130: glibc-rh2040657-1.patch
Patch131: glibc-rh2040657-2.patch
Patch132: glibc-rh2040657-3.patch
Patch133: glibc-rh2040657-4.patch
Patch134: glibc-rh2040657-5.patch
Patch135: glibc-rh2040657-6.patch
Patch136: glibc-rh2040657-7.patch
Patch137: glibc-rh2040657-8.patch
Patch138: glibc-rh2040657-9.patch
Patch139: glibc-rh2040657-10.patch
Patch140: glibc-rh2040657-11.patch
Patch141: glibc-rh2040657-12.patch
Patch142: glibc-upstream-2.34-74.patch
Patch143: glibc-upstream-2.34-75.patch
Patch144: glibc-upstream-2.34-76.patch
Patch145: glibc-upstream-2.34-77.patch
Patch146: glibc-upstream-2.34-78.patch
Patch147: glibc-upstream-2.34-79.patch
Patch148: glibc-upstream-2.34-80.patch
Patch149: glibc-upstream-2.34-81.patch
Patch150: glibc-upstream-2.34-82.patch
Patch151: glibc-upstream-2.34-83.patch
Patch152: glibc-upstream-2.34-84.patch
Patch153: glibc-upstream-2.34-85.patch
Patch154: glibc-upstream-2.34-86.patch
Patch155: glibc-upstream-2.34-87.patch
Patch156: glibc-upstream-2.34-88.patch
Patch157: glibc-upstream-2.34-89.patch
# glibc-2.34-90-g1b9cd6a721 only changes NEWS.
Patch158: glibc-upstream-2.34-91.patch
Patch159: glibc-upstream-2.34-92.patch
# glibc-2.34-93-g72123e1b56 only changes NEWS.
# glibc-2.34-94-g31186e2cb7 is glibc-rh2040657-1.patch.
# glibc-2.34-95-g511b244cc5 is glibc-rh2040657-2.patch.
# glibc-2.34-96-gde6cdd6875 is glibc-rh2040657-6.patch.
Patch160: glibc-upstream-2.34-97.patch
Patch161: glibc-upstream-2.34-98.patch
Patch162: glibc-upstream-2.34-99.patch
Patch163: glibc-c-utf8-locale-3.patch
Patch164: glibc-c-utf8-locale-4.patch
Patch165: glibc-c-utf8-locale-5.patch
Patch166: glibc-upstream-2.34-100.patch
Patch167: glibc-upstream-2.34-101.patch
Patch168: glibc-upstream-2.34-102.patch
Patch169: glibc-upstream-2.34-103.patch
Patch170: glibc-upstream-2.34-104.patch
Patch171: glibc-upstream-2.34-105.patch
Patch172: glibc-upstream-2.34-106.patch
Patch173: glibc-upstream-2.34-107.patch

##############################################################################
# Continued list of core "glibc" package information:
##############################################################################
Obsoletes: glibc-profile < 2.4
Provides: ldconfig

# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

# We need libgcc for cancellation support in POSIX threads.
Requires: libgcc%{_isa}

Requires: glibc-common = %{version}-%{release}

# Various components (regex, glob) have been imported from gnulib.
Provides: bundled(gnulib)

Requires(pre): basesystem
Requires: basesystem

%ifarch %{ix86}
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# after nss_*.x86_64.  (See below for the other ordering.)
Recommends: (nss_db(x86-32) if nss_db(x86-64))
Recommends: (nss_hesiod(x86-32) if nss_hesiod(x86-64))
%endif

# This is for building auxiliary programs like memusage, nscd
# For initial glibc bootstraps it can be commented out
%if %{without bootstrap}
BuildRequires: gd-devel libpng-devel zlib-devel
%endif
%if %{with docs}
%endif
%if %{without bootstrap}
BuildRequires: libselinux-devel >= 1.33.4-3
%endif
BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
# We need procps-ng (/bin/ps), util-linux (/bin/kill), and gawk (/bin/awk),
# but it is more flexible to require the actual programs and let rpm infer
# the packages. However, until bug 1259054 is widely fixed we avoid the
# following:
# BuildRequires: /bin/ps, /bin/kill, /bin/awk
# And use instead (which should be reverted some time in the future):
BuildRequires: procps-ng, util-linux, gawk
BuildRequires: systemtap-sdt-devel

%if %{with valgrind}
# Require valgrind for smoke testing the dynamic loader to make sure we
# have not broken valgrind.
BuildRequires: valgrind
%endif

# We use systemd rpm macros for nscd
BuildRequires: systemd

# We use python for the microbenchmarks and locale data regeneration
# from unicode sources (carried out manually). We choose python3
# explicitly because it supports both use cases.  On some
# distributions, python3 does not actually install /usr/bin/python3,
# so we also depend on python3-devel.
BuildRequires: python3 python3-devel

# This GCC version is needed for -fstack-clash-protection support.
BuildRequires: gcc >= 7.2.1-6
%define enablekernel 3.2
Conflicts: kernel < %{enablekernel}
%define target %{_target_cpu}-redhat-linux
%ifarch %{arm}
%define target %{_target_cpu}-redhat-linuxeabi
%endif
%ifarch ppc64le
%define target ppc64le-redhat-linux
%endif

# GNU make 4.0 introduced the -O option.
BuildRequires: make >= 4.0

# The intl subsystem generates a parser using bison.
BuildRequires: bison >= 2.7

# binutils 2.30-17 is needed for --generate-missing-build-notes.
BuildRequires: binutils >= 2.30-17

# Earlier releases have broken support for IRELATIVE relocations
Conflicts: prelink < 0.4.2

%if %{without bootstrap}
%if %{with testsuite}
# The testsuite builds static C++ binaries that require a C++ compiler,
# static C++ runtime from libstdc++-static, and lastly static glibc.
BuildRequires: gcc-c++
BuildRequires: libstdc++-static
# A configure check tests for the ability to create static C++ binaries
# before glibc is built and therefore we need a glibc-static for that
# check to pass even if we aren't going to use any of those objects to
# build the tests.
BuildRequires: glibc-static

# libidn2 (but not libidn2-devel) is needed for testing AI_IDN/NI_IDN.
BuildRequires: libidn2

# The testsuite runs mtrace, which is a perl script
BuildRequires: perl-interpreter
%endif
%endif

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should not be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1
%global __provides_exclude ^libc_malloc_debug\\.so.*$

# For language packs we have glibc require a virtual dependency
# "glibc-langpack" wich gives us at least one installed langpack.
# If no langpack providing 'glibc-langpack' was installed you'd
# get language-neutral support e.g. C, POSIX, and C.UTF-8 locales.
# In the past we used to install the glibc-all-langpacks by default
# but we no longer do this to minimize container and VM sizes.
# Today you must actively use the language packs infrastructure to
# install language support.
Requires: glibc-langpack = %{version}-%{release}
Suggests: glibc-minimal-langpack = %{version}-%{release}

# Suggest extra gconv modules so that they are installed by default but can be
# removed if needed to build a minimal OS image.
Recommends: glibc-gconv-extra%{_isa} = %{version}-%{release}
# Use redhat-rpm-config as a marker for a buildroot configuration, and
# unconditionally pull in glibc-gconv-extra in that case.
Requires: (glibc-gconv-extra%{_isa} = %{version}-%{release} if redhat-rpm-config)

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

######################################################################
# libnsl subpackage
######################################################################

%package -n libnsl
Summary: Legacy support library for NIS
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n libnsl
This package provides the legacy version of libnsl library, for
accessing NIS services.

This library is provided for backwards compatibility only;
applications should use libnsl2 instead to gain IPv6 support.

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary: Object files for development using standard C libraries.
Requires: %{name} = %{version}-%{release}
Requires: libxcrypt-devel%{_isa} >= 4.0.0
Requires: kernel-headers >= 3.2
BuildRequires: kernel-headers >= 3.2
%if %{need_headers_package}
Requires: %{headers_package_name} = %{version}-%{release}
%endif
%if !(0%{?rhel} > 0 && %{need_headers_package})
# For backwards compatibility, when the glibc-headers package existed.
Provides: glibc-headers = %{version}-%{release}
Provides: glibc-headers(%{_target_cpu})
Obsoletes: glibc-headers < %{version}-%{release}
%endif

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "doc" sub-package
##############################################################################
%if %{with docs}
%package doc
Summary: Documentation for GNU libc
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

# Removing texinfo will cause check-safety.sh test to fail because it seems to
# trigger documentation generation based on dependencies.  We need to fix this
# upstream in some way that doesn't depend on generating docs to validate the
# texinfo.  I expect it's simply the wrong dependency for that target.
BuildRequires: texinfo >= 5.0

%description doc
The glibc-doc package contains The GNU C Library Reference Manual in info
format.  Additional package documentation is also provided.
%endif

##############################################################################
# glibc "static" sub-package
##############################################################################
%package static
Summary: C library static libraries for -static linking.
Requires: %{name}-devel = %{version}-%{release}
Requires: libxcrypt-static%{?_isa} >= 4.0.0

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

##############################################################################
# glibc "headers" sub-package
# - The headers package includes all common headers that are shared amongst
#   the multilib builds. It avoids file conflicts between the architecture-
#   specific glibc-devel variants.
#   Files like gnu/stubs.h which have gnu/stubs-32.h (i686) and gnu/stubs-64.h
#   are included in glibc-headers, but the -32 and -64 files are in their
#   respective i686 and x86_64 devel packages.
##############################################################################
%if %{need_headers_package}
%package -n %{headers_package_name}
Summary: Additional internal header files for glibc-devel.
Requires: %{name} = %{version}-%{release}
%if 0%{?rhel} > 0
Provides: %{name}-headers(%{_target_cpu})
Obsoletes: glibc-headers-x86 < %{version}-%{release}
Obsoletes: glibc-headers-s390 < %{version}-%{release}
%else
BuildArch: noarch
%endif

%description -n %{headers_package_name}
The %{headers_package_name} package contains the architecture-specific
header files which cannot be included in glibc-devel package.
%endif

##############################################################################
# glibc "common" sub-package
##############################################################################
%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2003a

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

######################################################################
# File triggers to do ldconfig calls automatically (see rhbz#1380878)
######################################################################

# File triggers for when libraries are added or removed in standard
# paths.
%transfiletriggerin common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

%transfiletriggerpostun common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

# We need to run ldconfig manually because __brp_ldconfig assumes that
# glibc itself is always installed in $RPM_BUILD_ROOT, but with sysroots
# we may be installed into a subdirectory of that path.  Therefore we
# unset __brp_ldconfig and run ldconfig by hand with the sysroots path
# passed to -r.
%undefine __brp_ldconfig

######################################################################

%package locale-source
Summary: The sources for the locales
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description locale-source
The sources for all locales provided in the language packs.
If you are building custom locales you will most likely use
these sources as the basis for your new locale.

%{lua:
-- To make lua-mode happy: '

-- List of supported locales.  This is used to generate the langpack
-- subpackages below.  This table needs adjustments if the set of
-- glibc locales changes.  "code" is the glibc code for the language
-- (before the "_".  "name" is the English translation of the language
-- name (for use in subpackage descriptions).  "regions" is a table of
-- variant specifiers (after the "_", excluding "@" and "."
-- variants/charset specifiers).  The table must be sorted by the code
-- field, and the regions table must be sorted as well.
--
-- English translations of language names can be obtained using (for
-- the "aa" language in this example):
--
-- python3 -c 'import langtable; print(langtable.language_name("aa", languageIdQuery="en"))'

local locales =  {
  { code="aa", name="Afar", regions={ "DJ", "ER", "ET" } },
  { code="af", name="Afrikaans", regions={ "ZA" } },
  { code="agr", name="Aguaruna", regions={ "PE" } },
  { code="ak", name="Akan", regions={ "GH" } },
  { code="am", name="Amharic", regions={ "ET" } },
  { code="an", name="Aragonese", regions={ "ES" } },
  { code="anp", name="Angika", regions={ "IN" } },
  {
    code="ar",
    name="Arabic",
    regions={
      "AE",
      "BH",
      "DZ",
      "EG",
      "IN",
      "IQ",
      "JO",
      "KW",
      "LB",
      "LY",
      "MA",
      "OM",
      "QA",
      "SA",
      "SD",
      "SS",
      "SY",
      "TN",
      "YE" 
    } 
  },
  { code="as", name="Assamese", regions={ "IN" } },
  { code="ast", name="Asturian", regions={ "ES" } },
  { code="ayc", name="Southern Aymara", regions={ "PE" } },
  { code="az", name="Azerbaijani", regions={ "AZ", "IR" } },
  { code="be", name="Belarusian", regions={ "BY" } },
  { code="bem", name="Bemba", regions={ "ZM" } },
  { code="ber", name="Berber", regions={ "DZ", "MA" } },
  { code="bg", name="Bulgarian", regions={ "BG" } },
  { code="bhb", name="Bhili", regions={ "IN" } },
  { code="bho", name="Bhojpuri", regions={ "IN", "NP" } },
  { code="bi", name="Bislama", regions={ "VU" } },
  { code="bn", name="Bangla", regions={ "BD", "IN" } },
  { code="bo", name="Tibetan", regions={ "CN", "IN" } },
  { code="br", name="Breton", regions={ "FR" } },
  { code="brx", name="Bodo", regions={ "IN" } },
  { code="bs", name="Bosnian", regions={ "BA" } },
  { code="byn", name="Blin", regions={ "ER" } },
  { code="ca", name="Catalan", regions={ "AD", "ES", "FR", "IT" } },
  { code="ce", name="Chechen", regions={ "RU" } },
  { code="chr", name="Cherokee", regions={ "US" } },
  { code="ckb", name="Central Kurdish", regions={ "IQ" } },
  { code="cmn", name="Mandarin Chinese", regions={ "TW" } },
  { code="crh", name="Crimean Turkish", regions={ "UA" } },
  { code="cs", name="Czech", regions={ "CZ" } },
  { code="csb", name="Kashubian", regions={ "PL" } },
  { code="cv", name="Chuvash", regions={ "RU" } },
  { code="cy", name="Welsh", regions={ "GB" } },
  { code="da", name="Danish", regions={ "DK" } },
  {
    code="de",
    name="German",
    regions={ "AT", "BE", "CH", "DE", "IT", "LI", "LU" } 
  },
  { code="doi", name="Dogri", regions={ "IN" } },
  { code="dsb", name="Lower Sorbian", regions={ "DE" } },
  { code="dv", name="Divehi", regions={ "MV" } },
  { code="dz", name="Dzongkha", regions={ "BT" } },
  { code="el", name="Greek", regions={ "CY", "GR" } },
  {
    code="en",
    name="English",
    regions={
      "AG",
      "AU",
      "BW",
      "CA",
      "DK",
      "GB",
      "HK",
      "IE",
      "IL",
      "IN",
      "NG",
      "NZ",
      "PH",
      "SC",
      "SG",
      "US",
      "ZA",
      "ZM",
      "ZW" 
    } 
  },
  { code="eo", name="Esperanto", regions={} },
  {
    code="es",
    name="Spanish",
    regions={
      "AR",
      "BO",
      "CL",
      "CO",
      "CR",
      "CU",
      "DO",
      "EC",
      "ES",
      "GT",
      "HN",
      "MX",
      "NI",
      "PA",
      "PE",
      "PR",
      "PY",
      "SV",
      "US",
      "UY",
      "VE" 
    } 
  },
  { code="et", name="Estonian", regions={ "EE" } },
  { code="eu", name="Basque", regions={ "ES" } },
  { code="fa", name="Persian", regions={ "IR" } },
  { code="ff", name="Fulah", regions={ "SN" } },
  { code="fi", name="Finnish", regions={ "FI" } },
  { code="fil", name="Filipino", regions={ "PH" } },
  { code="fo", name="Faroese", regions={ "FO" } },
  { code="fr", name="French", regions={ "BE", "CA", "CH", "FR", "LU" } },
  { code="fur", name="Friulian", regions={ "IT" } },
  { code="fy", name="Western Frisian", regions={ "DE", "NL" } },
  { code="ga", name="Irish", regions={ "IE" } },
  { code="gd", name="Scottish Gaelic", regions={ "GB" } },
  { code="gez", name="Geez", regions={ "ER", "ET" } },
  { code="gl", name="Galician", regions={ "ES" } },
  { code="gu", name="Gujarati", regions={ "IN" } },
  { code="gv", name="Manx", regions={ "GB" } },
  { code="ha", name="Hausa", regions={ "NG" } },
  { code="hak", name="Hakka Chinese", regions={ "TW" } },
  { code="he", name="Hebrew", regions={ "IL" } },
  { code="hi", name="Hindi", regions={ "IN" } },
  { code="hif", name="Fiji Hindi", regions={ "FJ" } },
  { code="hne", name="Chhattisgarhi", regions={ "IN" } },
  { code="hr", name="Croatian", regions={ "HR" } },
  { code="hsb", name="Upper Sorbian", regions={ "DE" } },
  { code="ht", name="Haitian Creole", regions={ "HT" } },
  { code="hu", name="Hungarian", regions={ "HU" } },
  { code="hy", name="Armenian", regions={ "AM" } },
  { code="ia", name="Interlingua", regions={ "FR" } },
  { code="id", name="Indonesian", regions={ "ID" } },
  { code="ig", name="Igbo", regions={ "NG" } },
  { code="ik", name="Inupiaq", regions={ "CA" } },
  { code="is", name="Icelandic", regions={ "IS" } },
  { code="it", name="Italian", regions={ "CH", "IT" } },
  { code="iu", name="Inuktitut", regions={ "CA" } },
  { code="ja", name="Japanese", regions={ "JP" } },
  { code="ka", name="Georgian", regions={ "GE" } },
  { code="kab", name="Kabyle", regions={ "DZ" } },
  { code="kk", name="Kazakh", regions={ "KZ" } },
  { code="kl", name="Kalaallisut", regions={ "GL" } },
  { code="km", name="Khmer", regions={ "KH" } },
  { code="kn", name="Kannada", regions={ "IN" } },
  { code="ko", name="Korean", regions={ "KR" } },
  { code="kok", name="Konkani", regions={ "IN" } },
  { code="ks", name="Kashmiri", regions={ "IN" } },
  { code="ku", name="Kurdish", regions={ "TR" } },
  { code="kw", name="Cornish", regions={ "GB" } },
  { code="ky", name="Kyrgyz", regions={ "KG" } },
  { code="lb", name="Luxembourgish", regions={ "LU" } },
  { code="lg", name="Ganda", regions={ "UG" } },
  { code="li", name="Limburgish", regions={ "BE", "NL" } },
  { code="lij", name="Ligurian", regions={ "IT" } },
  { code="ln", name="Lingala", regions={ "CD" } },
  { code="lo", name="Lao", regions={ "LA" } },
  { code="lt", name="Lithuanian", regions={ "LT" } },
  { code="lv", name="Latvian", regions={ "LV" } },
  { code="lzh", name="Literary Chinese", regions={ "TW" } },
  { code="mag", name="Magahi", regions={ "IN" } },
  { code="mai", name="Maithili", regions={ "IN", "NP" } },
  { code="mfe", name="Morisyen", regions={ "MU" } },
  { code="mg", name="Malagasy", regions={ "MG" } },
  { code="mhr", name="Meadow Mari", regions={ "RU" } },
  { code="mi", name="Maori", regions={ "NZ" } },
  { code="miq", name="Miskito", regions={ "NI" } },
  { code="mjw", name="Karbi", regions={ "IN" } },
  { code="mk", name="Macedonian", regions={ "MK" } },
  { code="ml", name="Malayalam", regions={ "IN" } },
  { code="mn", name="Mongolian", regions={ "MN" } },
  { code="mni", name="Manipuri", regions={ "IN" } },
  { code="mnw", name="Mon", regions={ "MM" } },
  { code="mr", name="Marathi", regions={ "IN" } },
  { code="ms", name="Malay", regions={ "MY" } },
  { code="mt", name="Maltese", regions={ "MT" } },
  { code="my", name="Burmese", regions={ "MM" } },
  { code="nan", name="Min Nan Chinese", regions={ "TW" } },
  { code="nb", name="Norwegian Bokmål", regions={ "NO" } },
  { code="nds", name="Low German", regions={ "DE", "NL" } },
  { code="ne", name="Nepali", regions={ "NP" } },
  { code="nhn", name="Tlaxcala-Puebla Nahuatl", regions={ "MX" } },
  { code="niu", name="Niuean", regions={ "NU", "NZ" } },
  { code="nl", name="Dutch", regions={ "AW", "BE", "NL" } },
  { code="nn", name="Norwegian Nynorsk", regions={ "NO" } },
  { code="nr", name="South Ndebele", regions={ "ZA" } },
  { code="nso", name="Northern Sotho", regions={ "ZA" } },
  { code="oc", name="Occitan", regions={ "FR" } },
  { code="om", name="Oromo", regions={ "ET", "KE" } },
  { code="or", name="Odia", regions={ "IN" } },
  { code="os", name="Ossetic", regions={ "RU" } },
  { code="pa", name="Punjabi", regions={ "IN", "PK" } },
  { code="pap", name="Papiamento", regions={ "AW", "CW" } },
  { code="pl", name="Polish", regions={ "PL" } },
  { code="ps", name="Pashto", regions={ "AF" } },
  { code="pt", name="Portuguese", regions={ "BR", "PT" } },
  { code="quz", name="Cusco Quechua", regions={ "PE" } },
  { code="raj", name="Rajasthani", regions={ "IN" } },
  { code="ro", name="Romanian", regions={ "RO" } },
  { code="ru", name="Russian", regions={ "RU", "UA" } },
  { code="rw", name="Kinyarwanda", regions={ "RW" } },
  { code="sa", name="Sanskrit", regions={ "IN" } },
  { code="sah", name="Sakha", regions={ "RU" } },
  { code="sat", name="Santali", regions={ "IN" } },
  { code="sc", name="Sardinian", regions={ "IT" } },
  { code="sd", name="Sindhi", regions={ "IN" } },
  { code="se", name="Northern Sami", regions={ "NO" } },
  { code="sgs", name="Samogitian", regions={ "LT" } },
  { code="shn", name="Shan", regions={ "MM" } },
  { code="shs", name="Shuswap", regions={ "CA" } },
  { code="si", name="Sinhala", regions={ "LK" } },
  { code="sid", name="Sidamo", regions={ "ET" } },
  { code="sk", name="Slovak", regions={ "SK" } },
  { code="sl", name="Slovenian", regions={ "SI" } },
  { code="sm", name="Samoan", regions={ "WS" } },
  { code="so", name="Somali", regions={ "DJ", "ET", "KE", "SO" } },
  { code="sq", name="Albanian", regions={ "AL", "MK" } },
  { code="sr", name="Serbian", regions={ "ME", "RS" } },
  { code="ss", name="Swati", regions={ "ZA" } },
  { code="st", name="Southern Sotho", regions={ "ZA" } },
  { code="sv", name="Swedish", regions={ "FI", "SE" } },
  { code="sw", name="Swahili", regions={ "KE", "TZ" } },
  { code="szl", name="Silesian", regions={ "PL" } },
  { code="ta", name="Tamil", regions={ "IN", "LK" } },
  { code="tcy", name="Tulu", regions={ "IN" } },
  { code="te", name="Telugu", regions={ "IN" } },
  { code="tg", name="Tajik", regions={ "TJ" } },
  { code="th", name="Thai", regions={ "TH" } },
  { code="the", name="Chitwania Tharu", regions={ "NP" } },
  { code="ti", name="Tigrinya", regions={ "ER", "ET" } },
  { code="tig", name="Tigre", regions={ "ER" } },
  { code="tk", name="Turkmen", regions={ "TM" } },
  { code="tl", name="Tagalog", regions={ "PH" } },
  { code="tn", name="Tswana", regions={ "ZA" } },
  { code="to", name="Tongan", regions={ "TO" } },
  { code="tpi", name="Tok Pisin", regions={ "PG" } },
  { code="tr", name="Turkish", regions={ "CY", "TR" } },
  { code="ts", name="Tsonga", regions={ "ZA" } },
  { code="tt", name="Tatar", regions={ "RU" } },
  { code="ug", name="Uyghur", regions={ "CN" } },
  { code="uk", name="Ukrainian", regions={ "UA" } },
  { code="unm", name="Unami language", regions={ "US" } },
  { code="ur", name="Urdu", regions={ "IN", "PK" } },
  { code="uz", name="Uzbek", regions={ "UZ" } },
  { code="ve", name="Venda", regions={ "ZA" } },
  { code="vi", name="Vietnamese", regions={ "VN" } },
  { code="wa", name="Walloon", regions={ "BE" } },
  { code="wae", name="Walser", regions={ "CH" } },
  { code="wal", name="Wolaytta", regions={ "ET" } },
  { code="wo", name="Wolof", regions={ "SN" } },
  { code="xh", name="Xhosa", regions={ "ZA" } },
  { code="yi", name="Yiddish", regions={ "US" } },
  { code="yo", name="Yoruba", regions={ "NG" } },
  { code="yue", name="Cantonese", regions={ "HK" } },
  { code="yuw", name="Yau", regions={ "PG" } },
  { code="zh", name="Mandarin Chinese", regions={ "CN", "HK", "SG", "TW" } },
  { code="zu", name="Zulu", regions={ "ZA" } } 
}

-- Prints a list of LANGUAGE "_" REGION pairs.  The output is expected
-- to be identical to parse-SUPPORTED.py.  Called from the %%prep section.
function print_locale_pairs()
   for i = 1, #locales do
      local locale = locales[i]
      if #locale.regions == 0 then
	 print(locale.code .. "\n")
      else
	 for j = 1, #locale.regions do
	    print(locale.code .. "_" .. locale.regions[j] .. "\n")
	 end
      end
   end
end

local function compute_supplements(locale)
   local lang = locale.code
   local regions = locale.regions
   result = "langpacks-core-" .. lang
   for i = 1, #regions do
      result = result .. " or langpacks-core-" .. lang .. "_" .. regions[i]
   end
   return result
end

-- Emit the definition of a language pack package.
local function lang_package(locale)
   local lang = locale.code
   local langname = locale.name
   local suppl = compute_supplements(locale)
   print(rpm.expand([[

%package langpack-]]..lang..[[

Summary: Locale data for ]]..langname..[[

Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Supplements: (glibc and (]]..suppl..[[))
%description langpack-]]..lang..[[

The glibc-langpack-]]..lang..[[ package includes the basic information required
to support the ]]..langname..[[ language in your applications.
%files -f langpack-]]..lang..[[.filelist langpack-]]..lang..[[
]]))
end

for i = 1, #locales do
   lang_package(locales[i])
end
}

# The glibc-all-langpacks provides the virtual glibc-langpack,
# and thus satisfies glibc's requirement for installed locales.
# Users can add one more other langauge packs and then eventually
# uninstall all-langpacks to save space.
%package all-langpacks
Summary: All language packs for %{name}.
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-langpack = %{version}-%{release}
%description all-langpacks

# No %files, this is an empty package. The C/POSIX and
# C.UTF-8 files are already installed by glibc. We create
# minimal-langpack because the virtual provide of
# glibc-langpack needs at least one package installed
# to satisfy it. Given that no-locales installed is a valid
# use case we support it here with this package.
%package minimal-langpack
Summary: Minimal language packs for %{name}.
Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description minimal-langpack
This is a Meta package that is used to install minimal language packs.
This package ensures you can use C, POSIX, or C.UTF-8 locales, but
nothing else. It is designed for assembling a minimal system.
%files minimal-langpack

# Infrequently used iconv converter modules.
%package gconv-extra
Summary: All iconv converter modules for %{name}.
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description gconv-extra
This package contains all iconv converter modules built in %{name}.

##############################################################################
# glibc "nscd" sub-package
#
# Deprecated in Fedora 34 and planned for removal in Fedora 35.
#
# systemd-resolved is now enabled by default for DNS caching in Fedora, and
# sssd is capable of caching the remaining named services that nscd handles.
# It is therefore time to retire nscd in Fedora and move to more modern named
# services caches.
#
# For details, see:
# bug 1905135: https://fedoraproject.org/wiki/Changes/DeprecateNSCD
# bug 1905142: https://fedoraproject.org/wiki/Changes/RemoveNSCD
##############################################################################
%package -n nscd
Summary: A Name Service Caching Daemon (nscd).
# Fedora 35 is planned for release on Oct 26 2021, with nscd removed
Provides: deprecated() = 20211026
Requires: %{name} = %{version}-%{release}
%if %{without bootstrap}
Requires: libselinux >= 1.17.10-1
%endif
Requires: audit-libs >= 1.1.3
Requires(pre): /usr/sbin/useradd, coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd, /usr/sbin/userdel

%description -n nscd
The nscd daemon caches name service lookups and can improve
performance with LDAP, and may help with DNS as well.

##############################################################################
# Subpackages for NSS modules except nss_files, nss_compat, nss_dns
##############################################################################

# This should remain it's own subpackage or "Provides: nss_db" to allow easy
# migration from old systems that previously had the old nss_db package
# installed. Note that this doesn't make the migration that smooth, the
# databases still need rebuilding because the formats were different.
# The nss_db package was deprecated in F16 and onwards:
# https://lists.fedoraproject.org/pipermail/devel/2011-July/153665.html
# The different database format does cause some issues for users:
# https://lists.fedoraproject.org/pipermail/devel/2011-December/160497.html
%package -n nss_db
Summary: Name Service Switch (NSS) module using hash-indexed files
Requires: %{name}%{_isa} = %{version}-%{release}
%ifarch x86_64
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# before nss_db.x86_64.  (See above for the other ordering.)
Recommends: (nss_db(x86-32) if glibc(x86-32))
%endif

%description -n nss_db
The nss_db Name Service Switch module uses hash-indexed files in /var/db
to speed up user, group, service, host name, and other NSS-based lookups.

%package -n nss_hesiod
Summary: Name Service Switch (NSS) module using Hesiod
Requires: %{name}%{_isa} = %{version}-%{release}
%ifarch x86_64
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# before nss_hesiod.x86_64.  (See above for the other ordering.)
Recommends: (nss_hesiod(x86-32) if glibc(x86-32))
%endif

%description -n nss_hesiod
The nss_hesiod Name Service Switch module uses the Domain Name System
(DNS) as a source for user, group, and service information, following
the Hesiod convention of Project Athena.

%package nss-devel
Summary: Development files for directly linking NSS service modules
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: nss_db%{_isa} = %{version}-%{release}
Requires: nss_hesiod%{_isa} = %{version}-%{release}

%description nss-devel
The glibc-nss-devel package contains the object files necessary to
compile applications and libraries which directly link against NSS
modules supplied by glibc.

This is a rare and special use case; regular development has to use
the glibc-devel package instead.

##############################################################################
# glibc "utils" sub-package
##############################################################################
%package utils
Summary: Development utilities from GNU C library
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

%if %{with benchtests}
%package benchtests
Summary: Benchmarking binaries and scripts for %{name}
%description benchtests
This package provides built benchmark binaries and scripts to run
microbenchmark tests on the system.
%endif

##############################################################################
# compat-libpthread-nonshared
# See: https://sourceware.org/bugzilla/show_bug.cgi?id=23500
##############################################################################
%package -n compat-libpthread-nonshared
Summary: Compatibility support for linking against libpthread_nonshared.a.

%description -n compat-libpthread-nonshared
This package provides compatibility support for applications that expect
libpthread_nonshared.a to exist. The support provided is in the form of
an empty libpthread_nonshared.a that allows dynamic links to succeed.
Such applications should be adjusted to avoid linking against
libpthread_nonshared.a which is no longer used. The static library
libpthread_nonshared.a is an internal implementation detail of the C
runtime and should not be expected to exist.

##############################################################################
# Prepare for the build.
##############################################################################
%prep
%autosetup -n %{glibcsrcdir} -p1

##############################################################################
# %%prep - Additional prep required...
##############################################################################
# Make benchmark scripts executable
chmod +x benchtests/scripts/*.py scripts/pylint

# Remove all files generated from patching.
find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

# Ensure timestamps on configure files are current to prevent
# regenerating them.
touch `find . -name configure`

# Ensure *-kw.h files are current to prevent regenerating them.
touch locale/programs/*-kw.h

# Verify that our locales table is compatible with the locales table
# in the spec file.
set +x
echo '%{lua: print_locale_pairs()}' > localedata/SUPPORTED.spec
set -x
python3 %{SOURCE11} localedata/SUPPORTED > localedata/SUPPORTED.glibc
diff -u \
  --label "spec file" localedata/SUPPORTED.spec \
  --label "glibc localedata/SUPPORTED" localedata/SUPPORTED.glibc
rm localedata/SUPPORTED.spec localedata/SUPPORTED.glibc

##############################################################################
# Build glibc...
##############################################################################
%build
# Log osystem information
uname -a
LD_SHOW_AUXV=1 /bin/true
cat /proc/cpuinfo
cat /proc/sysinfo 2>/dev/null || true
cat /proc/meminfo
df

# We build using the native system compilers.
GCC=gcc
GXX=g++

# Part of rpm_inherit_flags.  Is overridden below.
rpm_append_flag ()
{
    BuildFlags="$BuildFlags $*"
}

# Propagates the listed flags to rpm_append_flag if supplied by
# redhat-rpm-config.
BuildFlags="-O2 -g"
rpm_inherit_flags ()
{
	local reference=" $* "
	local flag
	for flag in $RPM_OPT_FLAGS $RPM_LD_FLAGS ; do
		if echo "$reference" | grep -q -F " $flag " ; then
			rpm_append_flag "$flag"
		fi
	done
}

# Propgate select compiler flags from redhat-rpm-config.  These flags
# are target-dependent, so we use only those which are specified in
# redhat-rpm-config.  We keep the -m32/-m32/-m64 flags to support
# multilib builds.
#
# Note: For building alternative run-times, care is required to avoid
# overriding the architecture flags which go into CC/CXX.  The flags
# below are passed in CFLAGS.

rpm_inherit_flags \
	"-Wp,-D_GLIBCXX_ASSERTIONS" \
	"-fasynchronous-unwind-tables" \
	"-fstack-clash-protection" \
	"-funwind-tables" \
	"-m31" \
	"-m32" \
	"-m64" \
	"-march=armv8-a+lse" \
	"-march=armv8.1-a" \
	"-march=haswell" \
	"-march=i686" \
	"-march=x86-64" \
	"-march=x86-64-v2" \
	"-march=x86-64-v3" \
	"-march=x86-64-v4" \
	"-march=z13" \
	"-march=z14" \
	"-march=z15" \
	"-march=zEC12" \
	"-mbranch-protection=standard" \
	"-mcpu=power10" \
	"-mcpu=power8" \
	"-mcpu=power9" \
	"-mfpmath=sse" \
	"-msse2" \
	"-mstackrealign" \
	"-mtune=generic" \
	"-mtune=power10" \
	"-mtune=power8" \
	"-mtune=power9" \
	"-mtune=z13" \
	"-mtune=z14" \
	"-mtune=z15" \
	"-mtune=zEC12" \
	"-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1" \

# Use the RHEL 8 baseline for the early dynamic loader code, so that
# running on too old CPUs results in a diagnostic.
%if 0%{?rhel} >= 9
%ifarch ppc64le
%define glibc_rtld_early_cflags -mcpu=power8
%endif
%ifarch s390x
%define glibc_rtld_early_cflags -march=z13
%endif
%ifarch x86_64
%define glibc_rtld_early_cflags -march=x86-64
%endif
%endif

# libc_nonshared.a cannot be built with the default hardening flags
# because the glibc build system is incompatible with
# -D_FORTIFY_SOURCE.  The object files need to be marked as to be
# skipped in annobin annotations.  (The -specs= variant of activating
# annobin does not work here because of flag ordering issues.)
# See <https://bugzilla.redhat.com/show_bug.cgi?id=1668822>.
BuildFlagsNonshared="-fplugin=annobin -fplugin-arg-annobin-disable -Wa,--generate-missing-build-notes=yes"

# Special flag to enable annobin annotations for statically linked
# assembler code.  Needs to be passed to make; not preserved by
# configure.
%define glibc_make_flags_as ASFLAGS="-g -Wa,--generate-missing-build-notes=yes"
%define glibc_make_flags %{glibc_make_flags_as}

##############################################################################
# %%build - Generic options.
##############################################################################
EnableKernel="--enable-kernel=%{enablekernel}"
# Save the used compiler and options into the file "Gcc" for use later
# by %%install.
echo "$GCC" > Gcc

##############################################################################
# build()
#	Build glibc in `build-%{target}$1', passing the rest of the arguments
#	as CFLAGS to the build (not the same as configure CFLAGS). Several
#	global values are used to determine build flags, kernel version,
#	system tap support, etc.
##############################################################################
build()
{
	local builddir=build-%{target}${1:+-$1}
	${1+shift}
	rm -rf $builddir
	mkdir $builddir
	pushd $builddir
	../configure CC="$GCC" CXX="$GXX" CFLAGS="$BuildFlags $*" \
		--prefix=%{_prefix} \
		--with-headers=%{_prefix}/include $EnableKernel \
		--with-nonshared-cflags="$BuildFlagsNonshared" \
		--enable-bind-now \
		--build=%{target} \
		--enable-stack-protector=strong \
		--enable-tunables \
		--enable-systemtap \
		${core_with_options} \
		%{?glibc_rtld_early_cflags:--with-rtld-early-cflags=%glibc_rtld_early_cflags} \
%ifarch x86_64 %{ix86}
	       --enable-cet \
%endif
%ifarch %{ix86}
		--disable-multi-arch \
%endif
%if %{without werror}
		--disable-werror \
%endif
		--disable-profile \
%if %{with bootstrap}
		--without-selinux \
%endif
%ifarch aarch64
		--enable-memory-tagging \
%endif
		--disable-crypt ||
		{ cat config.log; false; }

	%make_build -r %{glibc_make_flags}
	popd
}

# Default set of compiler options.
build

##############################################################################
# Install glibc...
##############################################################################
%install

# The built glibc is installed into a subdirectory of $RPM_BUILD_ROOT.
# For a system glibc that subdirectory is "/" (the root of the filesystem).
# This is called a sysroot (system root) and can be changed if we have a
# distribution that supports multiple installed glibc versions.
%define glibc_sysroot $RPM_BUILD_ROOT

# Remove existing file lists.
find . -type f -name '*.filelist' -exec rm -rf {} \;

# Reload compiler and build options that were used during %%build.
GCC=`cat Gcc`

%ifarch riscv64
# RISC-V ABI wants to install everything in /lib64/lp64d or /usr/lib64/lp64d.
# Make these be symlinks to /lib64 or /usr/lib64 respectively.  See:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/DRHT5YTPK4WWVGL3GIN5BF2IKX2ODHZ3/
for d in %{glibc_sysroot}%{_libdir} %{glibc_sysroot}/%{_lib}; do
	mkdir -p $d
	(cd $d && ln -sf . lp64d)
done
%endif

# Build and install:
pushd build-%{target}
%make_build install_root=%{glibc_sysroot} install
%make_build install_root=%{glibc_sysroot} \
	install-locales -C ../localedata objdir=`pwd`
popd
# Locale creation may produce different groups of hardlinks in an
# unpredictable manner.  Re-grouping makes those differences go away.
hardlink %{glibc_sysroot}/usr/lib/locale

# install_different:
#	Install all core libraries into DESTDIR/SUBDIR. Either the file is
#	installed as a copy or a symlink to the default install (if it is the
#	same). The path SUBDIR_UP is the prefix used to go from
#	DESTDIR/SUBDIR to the default installed libraries e.g.
#	ln -s SUBDIR_UP/foo.so DESTDIR/SUBDIR/foo.so.
#	When you call this function it is expected that you are in the root
#	of the build directory, and that the default build directory is:
#	"../build-%{target}" (relatively).
#	The primary use of this function is to install alternate runtimes
#	into the build directory and avoid duplicating this code for each
#	runtime.
install_different()
{
	local lib libbase libbaseso dlib
	local destdir="$1"
	local subdir="$2"
	local subdir_up="$3"
	local libdestdir="$destdir/$subdir"
	# All three arguments must be non-zero paths.
	if ! [ "$destdir" \
	       -a "$subdir" \
	       -a "$subdir_up" ]; then
		echo "One of the arguments to install_different was emtpy."
		exit 1
	fi
	# Create the destination directory and the multilib directory.
	mkdir -p "$destdir"
	mkdir -p "$libdestdir"
	# Walk all of the libraries we installed...
	for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
	do
		libbase=${lib#*/}
		# Take care that `libbaseso' has a * that needs expanding so
		# take care with quoting.
		libbaseso=$(basename %{glibc_sysroot}/%{_lib}/${libbase}-*.so)
		# Only install if different from default build library.
		if cmp -s ${lib}.so ../build-%{target}/${lib}.so; then
			ln -sf "$subdir_up"/$libbaseso $libdestdir/$libbaseso
		else
			cp -a ${lib}.so $libdestdir/$libbaseso
		fi
		dlib=$libdestdir/$(basename %{glibc_sysroot}/%{_lib}/${libbase}.so.*)
		ln -sf $libbaseso $dlib
	done
}

##############################################################################
# Remove the files we don't want to distribute
##############################################################################

# Remove the libNoVersion files.
# XXX: This looks like a bug in glibc that accidentally installed these
#      wrong files. We probably don't need this today.
rm -f %{glibc_sysroot}/%{_libdir}/libNoVersion*
rm -f %{glibc_sysroot}/%{_lib}/libNoVersion*

# Remove the old nss modules.
rm -f %{glibc_sysroot}/%{_lib}/libnss1-*
rm -f %{glibc_sysroot}/%{_lib}/libnss-*.so.1

# This statically linked binary is no longer necessary in a world where
# the default Fedora install uses an initramfs, and further we have rpm-ostree
# which captures the whole userspace FS tree.
# Further, see https://github.com/projectatomic/rpm-ostree/pull/1173#issuecomment-355014583
rm -f %{glibc_sysroot}/{usr/,}sbin/sln

######################################################################
# Run ldconfig to create all the symbolic links we need
######################################################################

# Note: This has to happen before creating /etc/ld.so.conf.

mkdir -p %{glibc_sysroot}/var/cache/ldconfig
truncate -s 0 %{glibc_sysroot}/var/cache/ldconfig/aux-cache

# ldconfig is statically linked, so we can use the new version.
%{glibc_sysroot}/sbin/ldconfig -N -r %{glibc_sysroot}

##############################################################################
# Install info files
##############################################################################

%if %{with docs}
# Move the info files if glibc installed them into the wrong location.
if [ -d %{glibc_sysroot}%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p %{glibc_sysroot}%{_infodir}
  mv -f %{glibc_sysroot}%{_prefix}/info/* %{glibc_sysroot}%{_infodir}
  rm -rf %{glibc_sysroot}%{_prefix}/info
fi

# Compress all of the info files.
gzip -9nvf %{glibc_sysroot}%{_infodir}/libc*

# Copy the debugger interface documentation over to the right location
mkdir -p %{glibc_sysroot}%{_docdir}/glibc
cp elf/rtld-debugger-interface.txt %{glibc_sysroot}%{_docdir}/glibc
%else
rm -f %{glibc_sysroot}%{_infodir}/dir
rm -f %{glibc_sysroot}%{_infodir}/libc.info*
%endif

##############################################################################
# Create locale sub-package file lists
##############################################################################

olddir=`pwd`
pushd %{glibc_sysroot}%{_prefix}/lib/locale
rm -f locale-archive
$olddir/build-%{target}/elf/ld.so \
        --library-path $olddir/build-%{target}/ \
        $olddir/build-%{target}/locale/localedef \
	--alias-file=$olddir/intl/locale.alias \
        --prefix %{glibc_sysroot} --add-to-archive \
        eo *_*
# Historically, glibc-all-langpacks deleted the file on updates (sic),
# so we need to restore it in the posttrans scriptlet (like the old
# glibc-all-langpacks versions)
ln locale-archive locale-archive.real

# Create the file lists for the language specific sub-packages:
for i in eo *_*
do
    lang=${i%%_*}
    if [ ! -e langpack-${lang}.filelist ]; then
        echo "%dir %{_prefix}/lib/locale" >> langpack-${lang}.filelist
    fi
    echo "%dir  %{_prefix}/lib/locale/$i" >> langpack-${lang}.filelist
    echo "%{_prefix}/lib/locale/$i/*" >> langpack-${lang}.filelist
done
popd
pushd %{glibc_sysroot}%{_prefix}/share/locale
for i in */LC_MESSAGES/libc.mo
do
    locale=${i%%%%/*}
    lang=${locale%%%%_*}
    echo "%lang($lang) %{_prefix}/share/locale/${i}" \
         >> %{glibc_sysroot}%{_prefix}/lib/locale/langpack-${lang}.filelist
done
popd
mv  %{glibc_sysroot}%{_prefix}/lib/locale/*.filelist .

##############################################################################
# Install configuration files for services
##############################################################################

install -p -m 644 nss/nsswitch.conf %{glibc_sysroot}/etc/nsswitch.conf

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf %{glibc_sysroot}/etc
mkdir -p %{glibc_sysroot}%{_tmpfilesdir}
install -m 644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}
mkdir -p %{glibc_sysroot}/lib/systemd/system
install -m 644 nscd/nscd.service nscd/nscd.socket %{glibc_sysroot}/lib/systemd/system

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > %{glibc_sysroot}/etc/ld.so.conf
truncate -s 0 %{glibc_sysroot}/etc/ld.so.cache
chmod 644 %{glibc_sysroot}/etc/ld.so.conf
mkdir -p %{glibc_sysroot}/etc/ld.so.conf.d
mkdir -p %{glibc_sysroot}/etc/sysconfig
truncate -s 0 %{glibc_sysroot}/etc/sysconfig/nscd
truncate -s 0 %{glibc_sysroot}/etc/gai.conf

# Include %{_libdir}/gconv/gconv-modules.cache
truncate -s 0 %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache
chmod 644 %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache

# Remove any zoneinfo files; they are maintained by tzdata.
rm -rf %{glibc_sysroot}%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp across multilib packages.
#
# XXX: Ideally ld.so.conf should have the timestamp of the spec file, but there
# doesn't seem to be any macro to give us that.  So we do the next best thing,
# which is to at least keep the timestamp consistent. The choice of using
# SOURCE0 is arbitrary.
touch -r %{SOURCE0} %{glibc_sysroot}/etc/ld.so.conf
touch -r inet/etc.rpc %{glibc_sysroot}/etc/rpc

%if %{with benchtests}
# Build benchmark binaries.  Ignore the output of the benchmark runs.
pushd build-%{target}
make BENCH_DURATION=1 bench-build
popd

# Copy over benchmark binaries.
mkdir -p %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests
cp $(find build-%{target}/benchtests -type f -executable) %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
# ... and the makefile.
for b in %{SOURCE2} %{SOURCE3}; do
	cp $b %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
done
# .. and finally, the comparison scripts.
cp benchtests/scripts/benchout.schema.json %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/compare_bench.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/import_bench.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/validate_benchout.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
%endif

# The #line directives gperf generates do not give the proper
# file name relative to the build directory.
pushd locale
ln -s programs/*.gperf .
popd
pushd iconv
ln -s ../locale/programs/charmap-kw.gperf .
popd

%if %{with docs}
# Remove the `dir' info-heirarchy file which will be maintained
# by the system as it adds info files to the install.
rm -f %{glibc_sysroot}%{_infodir}/dir
%endif

mkdir -p %{glibc_sysroot}/var/{db,run}/nscd
touch %{glibc_sysroot}/var/{db,run}/nscd/{passwd,group,hosts,services}
touch %{glibc_sysroot}/var/run/nscd/{socket,nscd.pid}

# Move libpcprofile.so and libmemusage.so into the proper library directory.
# They can be moved without any real consequences because users would not use
# them directly.
mkdir -p %{glibc_sysroot}%{_libdir}
mv -f %{glibc_sysroot}/%{_lib}/lib{pcprofile,memusage}.so \
	%{glibc_sysroot}%{_libdir}

# Disallow linking against libc_malloc_debug.
rm %{glibc_sysroot}%{_libdir}/libc_malloc_debug.so

# Strip all of the installed object files.
strip -g %{glibc_sysroot}%{_libdir}/*.o

# The xtrace and memusage scripts have hard-coded paths that need to be
# translated to a correct set of paths using the $LIB token which is
# dynamically translated by ld.so as the default lib directory.
for i in %{glibc_sysroot}%{_prefix}/bin/{xtrace,memusage}; do
%if %{with bootstrap}
  test -w $i || continue
%endif
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_libdir}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
      -i $i
done

##############################################################################
# Build an empty libpthread_nonshared.a for compatiliby with applications
# that have old linker scripts that reference this file. We ship this only
# in compat-libpthread-nonshared sub-package.
##############################################################################
ar cr %{glibc_sysroot}%{_prefix}/%{_lib}/libpthread_nonshared.a

##############################################################################
# Beyond this point in the install process we no longer modify the set of
# installed files.
##############################################################################

##############################################################################
# Build the file lists used for describing the package and subpackages.
##############################################################################
# There are several main file lists (and many more for
# the langpack sub-packages (langpack-${lang}.filelist)):
# * master.filelist
#	- Master file list from which all other lists are built.
# * glibc.filelist
#	- Files for the glibc packages.
# * common.filelist
#	- Flies for the common subpackage.
# * utils.filelist
#	- Files for the utils subpackage.
# * nscd.filelist
#	- Files for the nscd subpackage.
# * devel.filelist
#	- Files for the devel subpackage.
# * doc.filelist
#	- Files for the documentation subpackage.
# * headers.filelist
#	- Files for the headers subpackage.
# * static.filelist
#	- Files for the static subpackage.
# * libnsl.filelist
#       - Files for the libnsl subpackage
# * nss_db.filelist
# * nss_hesiod.filelist
#       - File lists for nss_* NSS module subpackages.
# * nss-devel.filelist
#       - File list with the .so symbolic links for NSS packages.
# * compat-libpthread-nonshared.filelist.
#	- File list for compat-libpthread-nonshared subpackage.

# Create the main file lists. This way we can append to any one of them later
# wihtout having to create it. Note these are removed at the start of the
# install phase.
touch master.filelist
touch glibc.filelist
touch common.filelist
touch utils.filelist
touch gconv.filelist
touch nscd.filelist
touch devel.filelist
touch doc.filelist
touch headers.filelist
touch static.filelist
touch libnsl.filelist
touch nss_db.filelist
touch nss_hesiod.filelist
touch nss-devel.filelist
touch compat-libpthread-nonshared.filelist

###############################################################################
# Master file list, excluding a few things.
###############################################################################
{
  # List all files or links that we have created during install.
  # Files with 'etc' are configuration files, likewise 'gconv-modules'
  # and 'gconv-modules.cache' are caches, and we exclude them.
  find %{glibc_sysroot} \( -type f -o -type l \) \
       \( \
	 -name etc -printf "%%%%config " -o \
	 -name gconv-modules.cache \
	 -printf "%%%%verify(not md5 size mtime) " -o \
	 -name gconv-modules* \
	 -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " \
	 , \
	 ! -path "*/lib/debug/*" -printf "/%%P\n" \)
  # List all directories with a %%dir prefix.  We omit the info directory and
  # all directories in (and including) /usr/share/locale.
  find %{glibc_sysroot} -type d \
       \( -path '*%{_prefix}/share/locale' -prune -o \
       \( -path '*%{_prefix}/share/*' \
%if %{with docs}
	! -path '*%{_infodir}' -o \
%endif
	  -path "*%{_prefix}/include/*" \
       \) -printf "%%%%dir /%%P\n" \)
} | {
  # Also remove the *.mo entries.  We will add them to the
  # language specific sub-packages.
  # libnss_ files go into subpackages related to NSS modules.
  # and .*/share/i18n/charmaps/.*), they go into the sub-package
  # "locale-source":
  sed -e '\,.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo,d' \
      -e '\,.*/share/i18n/locales/.*,d' \
      -e '\,.*/share/i18n/charmaps/.*,d' \
      -e '\,.*/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\|rpc\|gai\.conf\),d' \
      -e '\,.*/%{_libdir}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,.*/bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > master.filelist

# The master file list is now used by each subpackage to list their own
# files. We go through each package and subpackage now and create their lists.
# Each subpackage picks the files from the master list that they need.
# The order of the subpackage list generation does not matter.

# Make the master file list read-only after this point to avoid accidental
# modification.
chmod 0444 master.filelist

###############################################################################
# glibc
###############################################################################

# Add all files with the following exceptions:
# - The info files '%{_infodir}/dir'
# - The partial (lib*_p.a) static libraries, include files.
# - The static files, objects, unversioned DSOs, and nscd.
# - The bin, locale, some sbin, and share.
#   - We want iconvconfig in the main package and we do this by using
#     a double negation of -v and [^i] so it removes all files in
#     sbin *but* iconvconfig.
# - All the libnss files (we add back the ones we want later).
# - All bench test binaries.
# - The aux-cache, since it's handled specially in the files section.
# - Extra gconv modules.  We add the required modules later.
cat master.filelist \
	| grep -v \
	-e '%{_infodir}' \
	-e '%{_libdir}/lib.*_p.a' \
	-e '%{_prefix}/include' \
	-e '%{_libdir}/lib.*\.a' \
        -e '%{_libdir}/.*\.o' \
	-e '%{_libdir}/lib.*\.so' \
	-e '%{_libdir}/gconv/.*\.so$' \
	-e '%{_libdir}/gconv/gconv-modules.d/gconv-modules-extra\.conf$' \
	-e 'nscd' \
	-e '%{_prefix}/bin' \
	-e '%{_prefix}/lib/locale' \
	-e '%{_prefix}/sbin/[^i]' \
	-e '%{_prefix}/share' \
	-e '/var/db/Makefile' \
	-e '/libnss_.*\.so[0-9.]*$' \
	-e '/libnsl' \
	-e 'glibc-benchtests' \
	-e 'aux-cache' \
	> glibc.filelist

# Add specific files:
# - The nss_files, nss_compat, and nss_db files.
# - The libmemusage.so and libpcprofile.so used by utils.
for module in compat files dns; do
    cat master.filelist \
	| grep -E \
	-e "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
	>> glibc.filelist
done
grep -e "libmemusage.so" -e "libpcprofile.so" master.filelist >> glibc.filelist

###############################################################################
# glibc-gconv-extra
###############################################################################

grep -e "gconv-modules-extra.conf" master.filelist > gconv.filelist

# Put the essential gconv modules into the main package.
GconvBaseModules="ANSI_X3.110 ISO8859-15 ISO8859-1 CP1252"
GconvBaseModules="$GconvBaseModules UNICODE UTF-16 UTF-32 UTF-7"
%ifarch s390 s390x
GconvBaseModules="$GconvBaseModules ISO-8859-1_CP037_Z900 UTF8_UTF16_Z9"
GconvBaseModules="$GconvBaseModules UTF16_UTF32_Z9 UTF8_UTF32_Z9"
%endif
GconvAllModules=$(cat master.filelist |
                 sed -n 's|%{_libdir}/gconv/\(.*\)\.so|\1|p')

# Put the base modules into glibc and the rest into glibc-gconv-extra
for conv in $GconvAllModules; do
    if echo $GconvBaseModules | grep -q $conv; then
	grep -E -e "%{_libdir}/gconv/$conv.so$" \
	    master.filelist >> glibc.filelist
    else
	grep -E -e "%{_libdir}/gconv/$conv.so$" \
	    master.filelist >> gconv.filelist
    fi
done

###############################################################################
# glibc-devel
###############################################################################

# Static libraries that land in glibc-devel, not glibc-static.
devel_static_library_pattern='/lib\(\(c\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\|pthread\|dl\|rt\|util\|anl\)\.a$'
# Static libraries neither in glibc-devel nor in glibc-static.
other_static_library_pattern='/libpthread_nonshared\.a'

grep '%{_libdir}/lib.*\.a' master.filelist \
  | grep "$devel_static_library_pattern" \
  | grep -v "$other_static_library_pattern" \
  > devel.filelist

# Put all of the object files and *.so (not the versioned ones) into the
# devel package.
grep '%{_libdir}/.*\.o' < master.filelist >> devel.filelist
grep '%{_libdir}/lib.*\.so' < master.filelist >> devel.filelist
# The exceptions are:
# - libmemusage.so and libpcprofile.so in glibc used by utils.
# - libnss_*.so which are in nss-devel.
sed -i -e '\,libmemusage.so,d' \
	-e '\,libpcprofile.so,d' \
	-e '\,/libnss_[a-z]*\.so$,d' \
	devel.filelist

%if %{glibc_autorequires}
mkdir -p %{glibc_sysroot}/%{_rpmconfigdir} %{glibc_sysroot}/%{_fileattrsdir}
sed < %{SOURCE4} \
    -e s/@VERSION@/%{version}/ \
    -e s/@RELEASE@/%{release}/ \
    -e s/@SYMVER@/%{glibc_autorequires_symver}/ \
    > %{glibc_sysroot}/%{_rpmconfigdir}/glibc.req
cp %{SOURCE5} %{glibc_sysroot}/%{_fileattrsdir}/glibc.attr
%endif

###############################################################################
# glibc-doc
###############################################################################

%if %{with docs}
# Put the info files into the doc file list, but exclude the generated dir.
grep '%{_infodir}' master.filelist | grep -v '%{_infodir}/dir' > doc.filelist
grep '%{_docdir}' master.filelist >> doc.filelist
%endif

###############################################################################
# glibc-headers
###############################################################################

%if %{need_headers_package}
# The glibc-headers package includes only common files which are identical
# across all multilib packages. We must keep gnu/stubs.h and gnu/lib-names.h
# in the glibc-headers package, but the -32, -64, -64-v1, and -64-v2 versions
# go into glibc-devel.
grep '%{_prefix}/include/gnu/stubs-.*\.h$' < master.filelist >> devel.filelist || :
grep '%{_prefix}/include/gnu/lib-names-.*\.h$' < master.filelist >> devel.filelist || :
# Put the include files into headers file list.
grep '%{_prefix}/include' < master.filelist \
  | egrep -v '%{_prefix}/include/gnu/stubs-.*\.h$' \
  | egrep -v '%{_prefix}/include/gnu/lib-names-.*\.h$' \
  > headers.filelist
%else
# If there is no glibc-headers package, all header files go into the
# glibc-devel package.
grep '%{_prefix}/include' < master.filelist >> devel.filelist
%endif

###############################################################################
# glibc-static
###############################################################################

# Put the rest of the static files into the static package.
grep '%{_libdir}/lib.*\.a' < master.filelist \
  | grep -v "$devel_static_library_pattern" \
  | grep -v "$other_static_library_pattern" \
  > static.filelist

###############################################################################
# glibc-common
###############################################################################

# All of the bin and certain sbin files go into the common package except
# iconvconfig which needs to go in glibc. Likewise nscd is excluded because
# it goes in nscd. The iconvconfig binary is kept in the main glibc package
# because we use it in the post-install scriptlet to rebuild the
# gconv-modules.cache.  The makedb binary is in nss_db.
grep '%{_prefix}/bin' master.filelist \
	| grep -v '%{_prefix}/bin/makedb' \
	>> common.filelist
grep '%{_prefix}/sbin' master.filelist \
	| grep -v '%{_prefix}/sbin/iconvconfig' \
	| grep -v 'nscd' >> common.filelist
# All of the files under share go into the common package since they should be
# multilib-independent.
# Exceptions:
# - The actual share directory, not owned by us.
# - The info files which go into doc, and the info directory.
# - All documentation files, which go into doc.
grep '%{_prefix}/share' master.filelist \
	| grep -v \
	-e '%{_prefix}/share/info/libc.info.*' \
	-e '%%dir %{prefix}/share/info' \
	-e '%%dir %{prefix}/share' \
	-e '%{_docdir}' \
	>> common.filelist

###############################################################################
# nscd
###############################################################################

# The nscd binary must go into the nscd subpackage.
echo '%{_prefix}/sbin/nscd' > nscd.filelist

###############################################################################
# glibc-utils
###############################################################################

# Add the utils scripts and programs to the utils subpackage.
cat > utils.filelist <<EOF
%if %{without bootstrap}
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%endif
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

###############################################################################
# nss_db, nss_hesiod
###############################################################################

# Move the NSS-related files to the NSS subpackages.  Be careful not
# to pick up .debug files, and the -devel symbolic links.
for module in db hesiod; do
  grep -E "/libnss_$module\\.so\\.[0-9.]+\$" \
    master.filelist > nss_$module.filelist
done
grep -E "%{_prefix}/bin/makedb$" master.filelist >> nss_db.filelist

###############################################################################
# nss-devel
###############################################################################

# Symlinks go into the nss-devel package (instead of the main devel
# package).
grep '/libnss_[a-z]*\.so$' master.filelist > nss-devel.filelist

###############################################################################
# libnsl
###############################################################################

# Prepare the libnsl-related file lists.
grep -E '/libnsl\.so\.[0-9]+$' master.filelist > libnsl.filelist
test $(wc -l < libnsl.filelist) -eq 1

%if %{with benchtests}
###############################################################################
# glibc-benchtests
###############################################################################

# List of benchmarks.
find build-%{target}/benchtests -type f -executable | while read b; do
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)"
done >> benchtests.filelist
# ... and the makefile.
for b in %{SOURCE2} %{SOURCE3}; do
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)" >> benchtests.filelist
done
# ... and finally, the comparison scripts.
echo "%{_prefix}/libexec/glibc-benchtests/benchout.schema.json" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/compare_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/import_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/validate_benchout.py*" >> benchtests.filelist
%endif

###############################################################################
# compat-libpthread-nonshared
###############################################################################
echo "%{_libdir}/libpthread_nonshared.a" >> compat-libpthread-nonshared.filelist

##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}

# Run the glibc tests. If any tests fail to build we exit %check with
# an error, otherwise we print the test failure list and the failed
# test output and continue.  Write to standard error to avoid
# synchronization issues with make and shell tracing output if
# standard output and standard error are different pipes.
run_tests () {
  # This hides a test suite build failure, which should be fatal.  We
  # check "Summary of test results:" below to verify that all tests
  # were built and run.
  %make_build check |& tee rpmbuild.check.log >&2
  test -n tests.sum
  if ! grep -q '^Summary of test results:$' rpmbuild.check.log ; then
    echo "FAIL: test suite build of target: $(basename "$(pwd)")" >& 2
    exit 1
  fi
  set +x
  grep -v ^PASS: tests.sum > rpmbuild.tests.sum.not-passing || true
  if test -n rpmbuild.tests.sum.not-passing ; then
    echo ===================FAILED TESTS===================== >&2
    echo "Target: $(basename "$(pwd)")" >& 2
    cat rpmbuild.tests.sum.not-passing >&2
    while read failed_code failed_test ; do
      for suffix in out test-result ; do
        if test -e "$failed_test.$suffix"; then
	  echo >&2
          echo "=====$failed_code $failed_test.$suffix=====" >&2
          cat -- "$failed_test.$suffix" >&2
	  echo >&2
        fi
      done
    done <rpmbuild.tests.sum.not-passing
  fi

  # Unconditonally dump differences in the system call list.
  echo "* System call consistency checks:" >&2
  cat misc/tst-syscall-list.out >&2
  set -x
}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================

# Default libraries.
pushd build-%{target}
run_tests
popd

echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr %{glibc_sysroot}/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr %{glibc_sysroot}/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

# Obtain a way to run the dynamic loader.  Avoid matching the symbolic
# link and then pick the first loader (although there should be only
# one).  See wrap-find-debuginfo.sh.
ldso_path="$(find %{glibc_sysroot}/ -regextype posix-extended \
  -regex '.*/ld(-.*|64|)\.so\.[0-9]+$' -type f | LC_ALL=C sort | head -n1)"
run_ldso="$ldso_path --library-path %{glibc_sysroot}/%{_lib}"

# Show the auxiliary vector as seen by the new library
# (even if we do not perform the valgrind test).
LD_SHOW_AUXV=1 $run_ldso /bin/true

%if 0%{?_enable_debug_packages}
# Finally, check if valgrind runs with the new glibc.
# We want to fail building if valgrind is not able to run with this glibc so
# that we can then coordinate with valgrind to get it fixed before we update
# glibc.
%if %{with valgrind}
$run_ldso /usr/bin/valgrind --error-exitcode=1 \
	$run_ldso /usr/bin/true
# true --help performs some memory allocations.
$run_ldso /usr/bin/valgrind --error-exitcode=1 \
	$run_ldso /usr/bin/true --help >/dev/null
%endif
%endif

%endif


%pre -p <lua>
-- Check that the running kernel is new enough
required = '%{enablekernel}'
rel = posix.uname("%r")
if rpm.vercmp(rel, required) < 0 then
  error("FATAL: kernel too old", 0)
end

%post -p <lua>
%glibc_post_funcs
-- (1) Remove multilib libraries from previous installs.
-- In order to support in-place upgrades, we must immediately remove
-- obsolete platform directories after installing a new glibc
-- version.  RPM only deletes files removed by updates near the end
-- of the transaction.  If we did not remove the obsolete platform
-- directories here, they may be preferred by the dynamic linker
-- during the execution of subsequent RPM scriptlets, likely
-- resulting in process startup failures.

-- Full set of libraries glibc may install.
install_libs = { "anl", "BrokenLocale", "c", "dl", "m", "mvec",
		 "nss_compat", "nss_db", "nss_dns", "nss_files",
		 "nss_hesiod", "pthread", "resolv", "rt", "SegFault",
		 "thread_db", "util" }

-- We are going to remove these libraries. Generally speaking we remove
-- all core libraries in the multilib directory.
-- For the versioned install names, the version are [2.0,9.9*], so we
-- match "libc-2.0.so" and so on up to "libc-9.9*".
-- For the unversioned install names, we match the library plus ".so."
-- followed by digests.
remove_regexps = {}
for i = 1, #install_libs do
  -- Versioned install name.
  remove_regexps[#remove_regexps + 1] = ("lib" .. install_libs[i]
                                         .. "%%-[2-9]%%.[0-9]+%%.so$")
  -- Unversioned install name.
  remove_regexps[#remove_regexps + 1] = ("lib" .. install_libs[i]
                                         .. "%%.so%%.[0-9]+$")
end

-- Two exceptions:
remove_regexps[#install_libs + 1] = "libthread_db%%-1%%.0%%.so"
remove_regexps[#install_libs + 2] = "libSegFault%%.so"

-- We are going to search these directories.
local remove_dirs = { "%{_libdir}/i686",
		      "%{_libdir}/i686/nosegneg",
		      "%{_libdir}/power6",
		      "%{_libdir}/power7",
		      "%{_libdir}/power8",
		      "%{_libdir}/power9",
		    }

-- Add all the subdirectories of the glibc-hwcaps subdirectory.
repeat
  local iter = posix.files("%{_libdir}/glibc-hwcaps")
  if iter ~= nil then
    for entry in iter do
      if entry ~= "." and entry ~= ".." then
        local path = "%{_libdir}/glibc-hwcaps/" .. entry
        if posix.access(path .. "/.", "x") then
          remove_dirs[#remove_dirs + 1] = path
        end
      end
    end
  end
until true

-- Walk all the directories with files we need to remove...
for _, rdir in ipairs (remove_dirs) do
  if posix.access (rdir) then
    -- If the directory exists we look at all the files...
    local remove_files = posix.files (rdir)
    for rfile in remove_files do
      for _, rregexp in ipairs (remove_regexps) do
	-- Does it match the regexp?
	local dso = string.match (rfile, rregexp)
        if (dso ~= nil) then
	  -- Removing file...
	  os.remove (rdir .. '/' .. rfile)
	end
      end
    end
  end
end

-- (2) Update /etc/ld.so.conf
-- Next we update /etc/ld.so.conf to ensure that it starts with
-- a literal "include ld.so.conf.d/*.conf".

local ldsoconf = "/etc/ld.so.conf"
local ldsoconf_tmp = "/etc/glibc_post_upgrade.ld.so.conf"

if posix.access (ldsoconf) then

  -- We must have a "include ld.so.conf.d/*.conf" line.
  local have_include = false
  for line in io.lines (ldsoconf) do
    -- This must match, and we don't ignore whitespace.
    if string.match (line, "^include ld.so.conf.d/%%*%%.conf$") ~= nil then
      have_include = true
    end
  end

  if not have_include then
    -- Insert "include ld.so.conf.d/*.conf" line at the start of the
    -- file. We only support one of these post upgrades running at
    -- a time (temporary file name is fixed).
    local tmp_fd = io.open (ldsoconf_tmp, "w")
    if tmp_fd ~= nil then
      tmp_fd:write ("include ld.so.conf.d/*.conf\n")
      for line in io.lines (ldsoconf) do
        tmp_fd:write (line .. "\n")
      end
      tmp_fd:close ()
      local res = os.rename (ldsoconf_tmp, ldsoconf)
      if res == nil then
        io.stdout:write ("Error: Unable to update configuration file (rename).\n")
      end
    else
      io.stdout:write ("Error: Unable to update configuration file (open).\n")
    end
  end
end

-- (3) Rebuild ld.so.cache early.
-- If the format of the cache changes then we need to rebuild
-- the cache early to avoid any problems running binaries with
-- the new glibc.

-- Note: We use _prefix because Fedora's UsrMove says so.
post_exec ("%{_prefix}/sbin/ldconfig")

-- (4) Update gconv modules cache.
-- If the /usr/lib/gconv/gconv-modules.cache exists, then update it
-- with the latest set of modules that were just installed.
-- We assume that the cache is in _libdir/gconv and called
-- "gconv-modules.cache".

update_gconv_modules_cache()

-- (5) On upgrades, restart systemd if installed.  "systemctl -q" does
-- not suppress the error message (which is common in chroots), so
-- open-code post_exec with standard error suppressed.
if tonumber(arg[2]) >= 2
   and posix.access("%{_prefix}/bin/systemctl", "x")
then
  local pid = posix.fork()
  if pid == 0 then
    posix.redirect2null(2)
    assert(posix.exec("%{_prefix}/bin/systemctl", "daemon-reexec"))
  elseif pid > 0 then
    posix.wait(pid)
  end
end

%posttrans all-langpacks -e -p <lua>
-- The old glibc-all-langpacks postun scriptlet deleted the locale-archive
-- file, so we may have to resurrect it on upgrades.
local archive_path = "%{_prefix}/lib/locale/locale-archive"
local real_path = "%{_prefix}/lib/locale/locale-archive.real"
local stat_archive = posix.stat(archive_path)
local stat_real = posix.stat(real_path)
-- If the hard link was removed, restore it.
if stat_archive ~= nil and stat_real ~= nil
    and (stat_archive.ino ~= stat_real.ino
         or stat_archive.dev ~= stat_real.dev) then
  posix.unlink(archive_path)
  stat_archive = nil
end
-- If the file is gone, restore it.
if stat_archive == nil then
  posix.link(real_path, archive_path)
end
-- Remove .rpmsave file potentially created due to config file change.
local save_path = archive_path .. ".rpmsave"
if posix.access(save_path) then
  posix.unlink(save_path)
end

%post gconv-extra -p <lua>
%glibc_post_funcs
update_gconv_modules_cache ()

%postun gconv-extra -p <lua>
%glibc_post_funcs
update_gconv_modules_cache ()

%pre -n nscd
getent group nscd >/dev/null || /usr/sbin/groupadd -g 28 -r nscd
getent passwd nscd >/dev/null ||
  /usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
		    -c "NSCD Daemon" -u 28 -g nscd nscd

%post -n nscd
%systemd_post nscd.service

%preun -n nscd
%systemd_preun nscd.service

%postun -n nscd
if test $1 = 0; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
%systemd_postun_with_restart nscd.service

%files -f glibc.filelist
%dir %{_prefix}/%{_lib}/audit
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%verify(not md5 size mtime) %config(noreplace) /etc/rpc
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_libdir}/gconv
%dir %{_libdir}/gconv/gconv-modules.d
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/gai.conf
# If rpm doesn't support %license, then use %doc instead.
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB LICENSES

%files -f common.filelist common
%dir %{_prefix}/lib/locale
%dir %{_prefix}/lib/locale/C.utf8
%{_prefix}/lib/locale/C.utf8/*

%files all-langpacks
%{_prefix}/lib/locale/locale-archive
%{_prefix}/lib/locale/locale-archive.real
%{_prefix}/share/locale/*/LC_MESSAGES/libc.mo

%files locale-source
%dir %{_prefix}/share/i18n/locales
%{_prefix}/share/i18n/locales/*
%dir %{_prefix}/share/i18n/charmaps
%{_prefix}/share/i18n/charmaps/*

%files -f devel.filelist devel
%if %{glibc_autorequires}
%attr(0755,root,root) %{_rpmconfigdir}/glibc.req
%{_fileattrsdir}/glibc.attr
%endif

%if %{with docs}
%files -f doc.filelist doc
%endif

%files -f static.filelist static

%if  %{need_headers_package}
%files -f headers.filelist -n %{headers_package_name}
%endif

%files -f utils.filelist utils

%files -f gconv.filelist gconv-extra

%files -f nscd.filelist -n nscd
%config(noreplace) /etc/nscd.conf
%dir %attr(0755,root,root) /var/run/nscd
%dir %attr(0755,root,root) /var/db/nscd
/lib/systemd/system/nscd.service
/lib/systemd/system/nscd.socket
%{_tmpfilesdir}/nscd.conf
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/services
%ghost %config(missingok,noreplace) /etc/sysconfig/nscd

%files -f nss_db.filelist -n nss_db
/var/db/Makefile
%files -f nss_hesiod.filelist -n nss_hesiod
%doc hesiod/README.hesiod
%files -f nss-devel.filelist nss-devel

%files -f libnsl.filelist -n libnsl
/%{_lib}/libnsl.so.1

%if %{with benchtests}
%files benchtests -f benchtests.filelist
%endif

%files -f compat-libpthread-nonshared.filelist -n compat-libpthread-nonshared

%changelog
* Thu Feb  3 2022 Florian Weimer <fweimer@redhat.com> - 2.34-25
- Sync with upstream branch release/2.34/master,
  commit 6eaf10cbb78d22eae7999d9de55f6b93999e0860:
- socket: Do not use AF_NETLINK in __opensock
- hurd if_index: Explicitly use AF_INET for if index discovery
- Linux: Simplify __opensock and fix race condition [BZ #28353]
- linux: __get_nprocs_sched: do not feed CPU_COUNT_S with garbage [BZ #28850]

* Tue Feb  1 2022 Florian Weimer <fweimer@redhat.com> - 2.34-24
- Sync with upstream branch release/2.34/master,
  commit 008003dc6e83439c5e04a744b7fd8197df19096e:
- tst-socket-timestamp-compat.c: Check __TIMESIZE [BZ #28837]
- Linux: Only generate 64 bit timestamps for 64 bit time_t recvmsg/recvmmsg
- linux: Fix ancillary 64-bit time timestamp conversion (BZ #28349, BZ#28350)
- support: Add support_socket_so_timestamp_time64

* Tue Feb  1 2022 Florian Weimer <fweimer@redhat.com> - 2.34-23
- Align with glibc 2.35 version of C.UTF-8

* Tue Feb  1 2022 Florian Weimer <fweimer@redhat.com> - 2.34-22
- Sync with upstream branch release/2.34/master,
  commit aa601d024424c40ae9a69b0c4e394a70ea0570c8:
- x86: Use CHECK_FEATURE_PRESENT to check HLE [BZ #27398]
- x86: Filter out more Intel CPUs for TSX [BZ #27398]
- Fix glibc 2.34 ABI omission (missing GLIBC_2.34 in dynamic loader)
- x86: Fix __wcsncmp_evex in strcmp-evex.S [BZ# 28755]
- x86: Fix __wcsncmp_avx2 in strcmp-avx2.S [BZ# 28755]

* Mon Jan 24 2022 Florian Weimer <fweimer@redhat.com> - 2.34-21
- Sync with upstream branch release/2.34/master,
  commit 3438bbca90895d32825a52e31a77dc44d273c1c1:
- Linux: Detect user namespace support in io/tst-getcwd-smallbuff
- realpath: Avoid overwriting preexisting error
- CVE-2021-3999: getcwd: Set errno to ERANGE for size == 1
- tst-realpath-toolong: Fix hurd build
- CVE-2021-3998: realpath: ENAMETOOLONG for result larger than PATH_MAX
- stdlib: Fix formatting of tests list in Makefile
- stdlib: Sort tests in Makefile
- support: Add helpers to create paths longer than PATH_MAX
- powerpc: Fix unrecognized instruction errors with recent binutils
- x86: use default cache size if it cannot be determined [BZ #28784]
- CVE-2022-23218: Buffer overflow in sunrpc svcunix_create (bug 28768)
- sunrpc: Test case for clnt_create "unix" buffer overflow (bug 22542)
- CVE-2022-23219: Buffer overflow in sunrpc clnt_create for "unix" (bug 22542)
- socket: Add the __sockaddr_un_set function
- Disable debuginfod in printer tests [BZ #28757]
- Update syscall lists for Linux 5.16

* Wed Jan 19 2022 Florian Weimer <fweimer@redhat.com> - 2.34-20
- More reliable CPU compatibility diagnostics (#2040657)

* Fri Jan 14 2022 Florian Weimer <fweimer@redhat.com> - 2.34-19
- Optionally accelerate sched_getcpu using rseq (#2024347)

* Thu Jan 13 2022 Florian Weimer <fweimer@redhat.com> - 2.34-18
- Backport optimized ELF dependency sorting algorithm (#2032647)

* Thu Jan 13 2022 Florian Weimer <fweimer@redhat.com> - 2.34-17
- Sync with upstream branch release/2.34/master,
  commit 2fe2af88abd13ae5636881da2e26f461ecb7dfb5
- i386: Remove broken CAN_USE_REGISTER_ASM_EBP (bug 28771)
- Update syscall lists for Linux 5.15
- powerpc: Fix unrecognized instruction errors with recent GCC
- timezone: test-case for BZ #28707
- timezone: handle truncated timezones from tzcode-2021d and later (BZ #28707)
- Fix subscript error with odd TZif file [BZ #28338]
- AArch64: Check for SVE in ifuncs [BZ #28744]
- intl/plural.y: Avoid conflicting declarations of yyerror and yylex
- Linux: Fix 32-bit vDSO for clock_gettime on powerpc32
- linux: Add sparck brk implementation
- Update sparc libm-test-ulps
- Update hppa libm-test-ulps
- riscv: align stack before calling _dl_init [BZ #28703]
- riscv: align stack in clone [BZ #28702]
- powerpc64[le]: Allocate extra stack frame on syscall.S
- elf: Fix tst-cpu-features-cpuinfo for KVM guests on some AMD systems [BZ #28704]
- nss: Use "files dns" as the default for the hosts database (bug 28700)
- arm: Guard ucontext _rtld_global_ro access by SHARED, not PIC macro
- mips: increase stack alignment in clone to match the ABI
- mips: align stack in clone [BZ #28223]

* Tue Dec 14 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.34-16
- Enable PIE by default on all architectures (#1988382)

* Tue Dec 14 2021 Florian Weimer <fweimer@redhat.com> - 2.34-15
- Sync with upstream branch release/2.34/master,
  commit 06865865151579d1aa17d38110060a68b85c5d90:
- pthread/tst-cancel28: Fix barrier re-init race condition
- Use $(pie-default) with conformtest
- Run conform/ tests using newly built libc
- nptl: Add one more barrier to nptl/tst-create1

* Fri Dec 10 2021 Florian Weimer <fweimer@redhat.com> - 2.34-13
- x86-64: Remove LD_PREFER_MAP_32BIT_EXEC support (#2029410)

* Fri Dec 10 2021 Florian Weimer <fweimer@redhat.com> - 2.34-12
- Add /usr/bin/ld.so --list-diagnostics (#2023422)

* Tue Dec  7 2021 Florian Weimer <fweimer@redhat.com> - 2.34-11
- backtrace function crashes without vDSO on ppc64le (#2027789)

* Fri Dec  3 2021 Florian Weimer <fweimer@redhat.com> - 2.34-10
- Sync with upstream branch release/2.34/master,
  commit 387bff63dc2dccd62b09aa26dccf8cdc5f3c985c:
- powerpc64[le]: Fix CFI and LR save address for asm syscalls [BZ #28532]
- linux: Use /proc/stat fallback for __get_nprocs_conf (BZ #28624)
- nptl: Do not set signal mask on second setjmp return [BZ #28607]
- s390: Use long branches across object boundaries (jgh instead of jh)
- elf: Earlier missing dynamic segment check in _dl_map_object_from_fd
- gconv: Do not emit spurious NUL character in ISO-2022-JP-3 (bug 28524)

* Tue Nov 16 2021 Arjun Shankar <arjun@redhat.com> - 2.34-9
- Create /{bin,lib,lib64,sbin} as symbolic links in test-container

* Wed Nov  3 2021 Florian Weimer <fweimer@redhat.com> - 2.34-8
- Sync with upstream branch release/2.34/master,
  commit 6548a9bdba95b3e1fcdbd85445342467e4b0cd4f:
- Avoid warning: overriding recipe for .../tst-ro-dynamic-mod.so
- ld.so: Initialize bootstrap_map.l_ld_readonly [BZ #28340]
- ld.so: Replace DL_RO_DYN_SECTION with dl_relocate_ld [BZ #28340]
- Handle NULL input to malloc_usable_size [BZ #28506]
- elf: Avoid deadlock between pthread_create and ctors [BZ #28357]
- timex: Use 64-bit fields on 32-bit TIMESIZE=64 systems (BZ #28469)
- y2038: Use a common definition for stat for sparc32
- elf: Replace nsid with args.nsid [BZ #27609]
- S390: Add PCI_MIO and SIE HWCAPs
- support: Also return fd when it is 0

* Fri Oct  1 2021 Florian Weimer <fweimer@redhat.com> - 2.34-7
- Drop glibc-rh1992702-*.patch, applied upstream.  (#1992702)
- Sync with upstream branch release/2.34/master,
  commit a996d13b8a2e101bedbb1bdaa7ffcfea3b959bb2:
- Add missing braces to bsearch inline implementation [BZ #28400]
- Suppress -Wcast-qual warnings in bsearch
- linux: Revert the use of sched_getaffinity on get_nproc (BZ #28310)
- linux: Simplify get_nprocs
- misc: Add __get_nprocs_sched
- nptl: pthread_kill must send signals to a specific thread [BZ #28407]
- support: Add check for TID zero in support_wait_for_thread_exit

* Thu Sep 23 2021 Florian Weimer <fweimer@redhat.com> - 2.34-6
- Sync with upstream branch release/2.34/master,
  commit 33adeaa3e2b9143c38884bc5aa65ded222ed274e:
- nptl: Avoid setxid deadlock with blocked signals in thread exit [BZ #28361]
- Use support_open_dev_null_range io/tst-closefrom, misc/tst-close_range, and
  posix/tst-spawn5 (BZ #28260)
- support: Add support_open_dev_null_range
- nptl: Fix type of pthread_mutexattr_getrobust_np,
  pthread_mutexattr_setrobust_np (bug 28036)
- nptl: pthread_kill needs to return ESRCH for old programs (bug 19193)

* Wed Sep 15 2021 Florian Weimer <fweimer@redhat.com> - 2.34-5
- Use system CPU count for sysconf(_SC_NPROCESSORS_*) (#1992702)

* Wed Sep 15 2021 Florian Weimer <fweimer@redhat.com> - 2.34-4
- Sync with upstream branch release/2.34/master,
  commit 4ed990e5b97a61f29f929bdeb36c5b2abb547a64:
- Add MADV_POPULATE_READ and MADV_POPULATE_WRITE from Linux 5.14 to
  bits/mman-linux.h
- Update kernel version to 5.14 in tst-mman-consts.py
- Update syscall lists for Linux 5.14
- Use Linux 5.14 in build-many-glibcs.py
- Fix failing nss/tst-nss-files-hosts-long with local resolver
- iconvconfig: Fix behaviour with --prefix [BZ #28199]
- nptl: Fix race between pthread_kill and thread exit (swbz#12889, #1994068)
- nptl: pthread_kill, pthread_cancel should not fail after exit
  (swbz#19193, #1994068)
- support: Add support_wait_for_thread_exit
- MIPS: Setup errno for {f,l,}xstat
- x86-64: Use testl to check __x86_string_control
- elf: Fix missing colon in LD_SHOW_AUXV output (swbz#28253, #1995648)
- librt: add test (swbz#28213, #1994264)
- CVE-2021-38604: fix NULL pointer dereference in mq_notify
  (swbz#28213, #1994264)
- Linux: Fix fcntl, ioctl, prctl redirects for _TIME_BITS=64 (bug 28182)
- iconv_charmap: Close output file when done
- copy_and_spawn_sgid: Avoid double calls to close()
- gaiconf_init: Avoid double-free in label and precedence lists
- gconv_parseconfdir: Fix memory leak
- ldconfig: avoid leak on empty paths in config file

* Wed Sep 15 2021 Florian Weimer <fweimer@redhat.com> - 2.34-3
- Switch to upstream version of C.UTF-8 (#1997589)

* Wed Aug 25 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.34-2
- Disable dependencies and linking for libc_malloc_debug.so (#1985048).

* Mon Aug  2 2021 Florian Weimer <fweimer@redhat.com> - 2.34-1
- Switch to glibc 2.34 release tarball:
- Update ChangeLog.old/ChangeLog.23.
- Prepare for glibc 2.34 release.
- po/nl.po: Update Dutch translation.
- Update install.texi, and regenerate INSTALL.
- Update translations.
- Update NEWS.
- NEWS: Fix typos, grammar, and missing words
- elf: Fix audit regression

* Fri Jul 30 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.33.9000-56
- Port post scripts for gconv-extra to lua and drop dependency across
  architectures for x86 multilib (#1988344).

* Thu Jul 29 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-55
- Auto-sync with upstream branch master,
  commit c37fc3ebf0607ce1953c565ffe56d56555eeb25e:
- Update libc.pot for 2.34 release.
- x86-64: Add Avoid_Short_Distance_REP_MOVSB
- Typo: Rename HAVE_CLONE3_WAPPER to HAVE_CLONE3_WRAPPER
- build-many-glibcs.py: Add x86_64-linux-gnu-minimal configuration
- tests: use xmalloc to allocate implementation array
- xmalloc: Fix warnings with gcc analyzer
- __cxa_thread_atexit_impl: Abort on allocation failure [BZ #18524]
- manual: Drop the .so suffix in libc_malloc_debug description
- hurd: _Fork: unlock malloc before calling fork child hooks

* Tue Jul 27 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-54
- Revert to old C.UTF-8 locale

* Mon Jul 26 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.33.9000-53
- Loosen dependency on glibc-gconv-extra (#1812191).

* Mon Jul 26 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-52
- Switch to new version of C.UTF-8 locale

* Mon Jul 26 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-51
- Auto-sync with upstream branch master,
  commit ddcc612ce923038b867083a0c55d6e034951155a:
- Exclude static tests for mcheck and malloc-check
- i386: Regenerate ulps

* Sat Jul 24 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-50
- Auto-sync with upstream branch master,
  commit d34ed66f96fa9316654d7adb2afcce4be1d1c4f5:
- manual: Document unsupported cases for interposition
- x86: Install <bits/platform/x86.h> [BZ #27958]
- Fix build and tests with --disable-tunables

* Sat Jul 24 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-49
- Remove both old and new library names in glibc-hwcaps removal (#1983677)

* Fri Jul 23 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-48
- Auto-sync with upstream branch master,
  commit 9a7ab0769b295cbf5232140401742a8f34bda3de:
- hurd: Fix glob lstat compatibility
- socket: Add time64 alias for setsockopt
- socket: Add time64 alias for getsockopt
- mcheck Fix malloc_usable_size [BZ #22057]
- Remove malloc hooks [BZ #23328]
- Move malloc_{g,s}et_state to libc_malloc_debug
- glibc.malloc.check: Wean away from malloc hooks
- mtrace: Wean away from malloc hooks
- Simplify __malloc_initialized
- mcheck: Wean away from malloc hooks [BZ #23489]
- Move malloc hooks into a compat DSO
- Remove __morecore and __default_morecore
- Remove __after_morecore_hook
- Make mcheck tests conditional on GLIBC_2.23 or earlier
- posix: Add sysconf(_SC_{MIN,}SIGSTKSZ) support
- malloc: Fix tst-mallocfork3-malloc-check link
- ARC: elf: make type safe
- ARC: fp: (micro)optimize FPU_STATUS read by eliding FWE bit clearing

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.9000-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-46
- Auto-sync with upstream branch master,
  commit 77ede5f010f1b144e067ec035e422a13bb57c55d:
- socket: Add time64 alias for sendmsg
- socket: Add time64 alias for recvmsg
- socket: Add time64 alias for sendmmsg
- Linux: Add time64 alias for prctl
- io: Add time64 alias for fcntl
- misc: Add time64 alias for ioctl
- RISC-V: Update rv64 ULPs
- resolv: Do not install libnss_dns.a, libnss_dns.so
- hurd: Add support for spawn_do_closefrom
- elf: Fix tst-cpu-features-cpuinfo on some AMD systems (BZ #28090)
- i386: Add the clone3 wrapper

* Mon Jul 19 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-45
- Remove glibc-hwcaps multilibs on upgrade (#1983677)

* Mon Jul 19 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-44
- Auto-sync with upstream branch master,
  commit ee5ed99922ca90bcea4a2f9a48a0c9ae4b534ece:
- nss: Directly load nss_dns, without going through dlsym/dlopen
- resolv: Move nss_dns into libc
- resolv: Move res_query functions into libc
- resolv: Move res_mkquery, res_nmkquery into libc
- resolv: Move res_send, res_nsend into libc
- resolv: Move res_hostalias into its own file, along with hostalias
- resolv: Move __res_context_hostalias into its own file and into libc
- resolv: Move res_queriesmatch to its own file and into libc
- resolv: Move res_nameinquery to its own file and into libc
- resolv: Move ns_samename into its own file, and into libc
- resolv: Move ns_makecanon into its own file, and into libc
- resolv: Move res_isourserver to its own file and reformat to GNU style
- resolv: Move __res_get_nsaddr to its own file and into libc
- resolv: Rename res_comp.c to res-name-checking.c and move into libc
- resolv: Move dn_skipname to its own file and into libc
- resolv: Move dn_comp to its own file and into libc
- resolv: Move _getlong, _getshort, __putlong, __putshort to res-putget
- resolv: Move dn_expand to its own file and into libc
- resolv: Move ns_name_compress into its own file and into libc
- resolv: Move ns_name_pack into its own file and into libc
- resolv: Move ns_name_pton into its own file and into libc
- resolv: Move ns_name_uncompress into its own file and into libc
- resolv: Move ns_name_skip to its own file and into libc (bug 28091)
- resolv: Deprecate legacy interfaces in libresolv
- tst-safe-linking: make false positives even more improbable
- htl: Do not expose pthread hidden proto outside libpthread
- elf: Fix a wrong array access on tst-tls20
- elf: Add -Wl,--no-as-needed for tst-tls-manydynamic*mod-dep-bad.so (BZ #28089)
- resolv: Move ns_name_unpack to its own file and into libc
- resolv: Remove unnecessary res_isourserver_p call from send_dg
- resolv: Move ns_name_ntop to its own file and into libc
- nss_dns: Do not use deprecated packet parsing functions
- resolv: Sort Makefile routines and Versions lexicographically
- socket: Add hidden prototype for setsockopt
- elf: Fix DTV gap reuse logic (BZ #27135)
- Fix linknamespace errors and local-plt-usages in nss_files.
- Add static tests for __clone_internal
- x86-64: Add the clone3 wrapper
- Add an internal wrapper for clone, clone2 and clone3
- nss: Fix build error with --disable-nscd
- htl: Fix linking static examples against libpthread
- htl: Let libc call __pthread_mutex_{,try,un}lock
- posix: Ignore non opened files on tst-spawn5
- mcheck: Align struct hdr to MALLOC_ALIGNMENT bytes [BZ #28068]

* Thu Jul 15 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.33.9000-43
- Run postun only if the main gconv-modules configuration file exists.
  (#1981013)
- Own %{libdir}/gconv/gconv-modules.d
- Rearrange file list command so that gconv-modules.cache is no longer
  marked as %config

* Tue Jul 13 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-42
- Perform systemd re-exec even if glibc.i686 is installed

* Tue Jul 13 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-41
- Re-exec systemd on upgrades

* Mon Jul 12 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-40
- Merge files NSS service module into libc.
- Restore vDSO acceleration for time functions on older kernels for i686.
- Auto-sync with upstream branch master,
  commit 72e84d1db22203e01a43268de71ea8669eca2863:
- Linux: Use 32-bit vDSO for clock_gettime, gettimeofday, time (BZ# 28071)
- Reduce <limits.h> pollution due to dynamic PTHREAD_STACK_MIN
- Fix failing nss/tst-nss-files-hosts-long.
- nis: nis_local_group may read from __nisgroup[-1] (bug 28075)
- hurd _Fork: Drop duplicate malloc_fork_lock calls
- support: Replace _SC_MINSIGSTKSZ with _SC_SIGSTKSZ
- support: Replace MINSIGSTKSZ with sysconf (_SC_MINSIGSTKSZ)
- Define PTHREAD_STACK_MIN to sysconf(_SC_THREAD_STACK_MIN)
- Force building with -fno-common
- Add a generic malloc test for MALLOC_ALIGNMENT
- Properly run tst-spawn5 directly [BZ #28067]
- build-many-glibcs.py: Add glibcs-arm-linux-gnueabihf-thumb
- nptl: Use out-of-line wake function in __libc_lock_unlock slow path
- powerpc64le: Fix typo in configure
- powerpc64: Remove strcspn ifunc from the loader
- x86: Remove wcsnlen-sse4_1 from wcslen ifunc-impl-list [BZ #28064]
- x86-64: Test strlen and wcslen with 0 in the RSI register [BZ #28064]
- x86_64: Remove unneeded static PIE check for undefined weak diagnostic
- Add NT_ARM_PAC_ENABLED_KEYS to elf.h
- posix: Add posix_spawn_file_actions_addclosefrom_np
- io: Add closefrom [BZ #10353]
- linux: Add close_range
- support: Add support_stack_alloc
- _int_realloc is static
- Move mcheck symbol from stdlib to malloc
- nss: Do not install static linker input files for libnss_files
- elf/tests: Make thrlock and noload depend on libm
- Harden tcache double-free check
- nss: Access nss_files through direct references
- nss_files: Move into libc
- nss_files: Add generic code for set*ent, end*ent and file open
- nss_files: Allocate nscd file registration data on the heap
- libio: Replace internal _IO_getdelim symbol with __getdelim
- libio: Add hidden prototype for ungetc
- inet: Add hidden prototype for __inet_network
- Update MIPS libm-test-ulps
- Update powerpc-nofpu libm-test-ulps
- soft-fp: Add __extendhfsf2/__extendhfdf2, __truncsfhf2/__truncdfhf2,
  __eqhf2/__nehf2
- Update kernel version to 5.13 in tst-mman-consts.py
- tests-exclude-mcheck: Fix typo

* Wed Jul 07 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-39
- Auto-sync with upstream branch master,
  commit 7a5db2e82fbb6c3a6e3fdae02b7166c5d0e8c7a8:
- elf: Clean up GLIBC_PRIVATE exports of internal libdl symbols
- nptl: Reduce the GLIBC_PRIVATE ABI
- nptl: Remove GLIBC_2.34 versions of __pthread_mutex_lock,
  __pthread_mutex_unlock
- nptl: Use internal low-level lock type for !IS_IN (libc)
- glibc.malloc.check: Fix nit in documentation
- Exclude tst-realloc from tests-mcheck
- linux: Fix setsockopt fallback
- linux: Use the expected size for SO_TIMESTAMP{NS} convertion
- linux: Consolidate Linux setsockopt implementation
- linux: Consolidate Linux getsockopt implementation
- manual: fix description for preadv()

* Tue Jul 06 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-38
- Auto-sync with upstream branch master,
  commit 832f50be6c9c010e46180d14126bbb81f35e808c:
- linux: Check for null value msghdr struct before use
- elf: Call free from base namespace on error in dl-libc.c [BZ #27646]

* Mon Jul 05 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-37
- Move libanl.a into glibc-devel.
- Auto-sync with upstream branch master,
  commit 91fb0f17a5779da6e7877eb74119a83dbe8bf167:
- hooks.c: Remove incorrect comment
- mtrace: Add attribute nocommon to mallwatch
- Move glibc.malloc.check implementation into its own file
- mtrace: Deprecate mallwatch and tr_break
- Drop source dependencies on hooks.c and arena.c
- malloc: Initiate tcache shutdown even without allocations [BZ #28028]
- Add mcheck tests to malloc
- iconvconfig: Use the public feof_unlocked
- resolv: Move libanl into libc (if libpthread is in libc)
- powerpc: optimize strcpy/stpcpy for POWER9/10
- soft-fp: Add __extendhfxf2 and __truncxfhf2
- x86: Check RTM_ALWAYS_ABORT for RTM [BZ #28033]
- Update syscall lists for Linux 5.13
- s390: Fix MEMCHR_Z900_G5 ifunc-variant if n>=0x80000000 [BZ #28024]
- Fix extra PLT reference in libc.so due to __glob64_time64 if build with gcc 7.5 on 32bit.
- AArch64: Add hp-timing.h
- AArch64: Improve strnlen performance

* Wed Jun 30 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-36
- Auto-sync with upstream branch master,
  commit eb68d7d23cc411acdf68a60f194343a6774d6194:
- Linux: Avoid calling malloc indirectly from __get_nprocs (#1975693)
- Use Linux 5.13 in build-many-glibcs.py

* Wed Jun 30 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-35
- Drop glibc-s390x-roundeven.patch, applied upstream.
- Move libutil.a into glibc-devel.
- Auto-sync with upstream branch master,
  commit 734c60ebb607086ad6d67b2544d6b7baba72a652:
- login: Move libutil into libc
- login: Rework hidden prototypes for __setutent, __utmpname, __endutent
- login: Hidden prototypes for _getpt, __ptsname_r, grantpt, unlockpt
- nptl_db: Re-use the ELF-to-abilist converter for ABI checking
- Add RFC 8335 Definitions from Linux 5.13
- nss: Fix NSS_DECLARE_MODULE_FUNCTIONS handling of _nss_*_endnetgrent
- s390x: Update math: redirect roundeven function
- posix: Add _Fork [BZ #4737]

* Mon Jun 28 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-34
- Move librt.a to glibc-devel (#1977058)

* Mon Jun 28 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-33
- Dropped patches glibc-nosymlink-*.patch, glibc-iconvconfig-corruption.patch,
  glibc-libthread_db-dynsym-*.patch; applied upstream.
- Auto-sync with upstream branch master,
  commit dd45734e322a03287d34d8af9b7da7b35cfddb8e:
- nptl: Add glibc.pthread.stack_cache_size tunable
- nptl: Export libthread_db-used symbols under GLIBC_PRIVATE
- nptl: Rename nptl_version to __nptl_version
- nptl_db: Clean up main/rtld variable handling
- arm: align stack in clone [BZ 28020]
- Linux: Cleanups after librt move
- Linux: Move timer_settime, __timer_settime64 from librt to libc
- Linux: Move timer_gettime, __timer_gettime64 from librt to libc
- Linux: Move timer_getoverrun from librt to libc
- Linux: Move timer_create, timer_delete from librt to libc
- Linux: Define TIMER_T_WAS_INT_COMPAT in kernel-posix-timers.h
- Install shared objects under their ABI names
- elf: Generalize name-based DSO recognition in ldconfig
- Makerules: Remove lib-version, $(subdir-version)
- nptl_db: Install libthread_db under a regular implementation name
- iconvconfig: Fix multiple issues
- wordexp: handle overflow in positional parameter number (bug 28011)
- Update math: redirect roundeven function
- Use GCC builtins for roundeven functions if desired.
- x86_64: roundeven with sse4.1 support
- math: redirect roundeven function

* Mon Jun 28 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-32
- Switch to new version of libthread_db .dynsym patch

* Mon Jun 28 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-31
- Further .symtab adjustment: Keep all __GI_* symbols (#1975895)

* Mon Jun 28 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-30
- Keep most of .symtab in libc.so.6 (#1975895)

* Sun Jun 27 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-29
- Apply emergency patch to fix iconvconfig corruption

* Sun Jun 27 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-28
- Adjust glibc.req so that egrep does not cause eu-readelf to fail

* Sun Jun 27 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-27
- Drop glibc-revert-dtv-gap-reuse.patch, applied upstream.
- Auto-sync with upstream branch master,
  commit 2c16cb88a6e5ace0fb7cedca86860ea7bde522a7:
- Linux: Move timer helper routines from librt to libc
- Linux: Move mq_unlink from librt to libc
- Linux: Move mq_send, mq_timedsend, __mq_timedsend_time64 to libc
- Linux: Move mq_receive, mq_timedreceive, __mq_timedreceive_time64 to libc
- Linux: Move mq_open, __mq_open_2 from librt to libc
- Linux: Move mq_notify from librt to libc
- Linux: Move mq_getattr from librt to libc
- Linux: Move mq_setattr from librt to libc
- Linux: Move mq_close from librt to libc
- Linux: Move lio_listio, lio_listio64 from librt to libc
- rt: Rework lio_listio implementation
- Linux: Move aio_write, aio_write64 into libc
- Linux: Move aio_suspend, aio_suspend64, __aio_suspend_time64 to libc
- Linux: Move aio_return, aio_return64 into libc
- Linux: Move aio_read, aio_read64 into libc
- Linux: Move aio_fsync, aio_fsync64 into libc
- Linux: Move aio_error, aio_error64 into libc
- Linux: Move aio_cancel, aio_cancel64 into libc
- Linux: Move aio_init from librt into libc
- support: Fix xclone build failures on ia64 and hppa
- elf: Disable most of TLS modid gaps processing [BZ #27135]
- elf: Fix glibc-hwcaps priorities with cache flags mismatches [BZ #27046]
- * NEWS: Clarify _TIME_BITS change.
- x86: Remove unnecessary overflow check from wcsnlen-sse4_1.S
- String: Add three more overflow tests cases to test-strnlen.c
- Consolidate pthread_atfork
- posix: Do not clobber errno by atfork handlers
- posix: Consolidate fork implementation
- support: Add xclone
- x86: Fix tst-cpu-features-cpuinfo on Ryzen 9 (BZ #27873)
- x86: Copy IBT and SHSTK usable only if CET is enabled
- x86: Fix overflow bug in wcsnlen-sse4_1 and wcsnlen-avx2 [BZ #27974]
- x86: Fix overflow bug with wmemchr-sse2 and wmemchr-avx2 [BZ #27974]
- String: Add overflow tests for strnlen, memchr, and strncat [BZ #27974]
- x86-64: Add wcslen optimize for sse4.1
- x86-64: Move strlen.S to multiarch/strlen-vec.S
- hurd: Fix build after 52a5fe70a2
- nptl: Use SA_RESTART for SIGCANCEL handler
- doc: _TIME_BITS defaults may change
- More mcheck -> malloc-check refactoring
- Add NEWS item for gconv-modules.d change
- Handle DT_UNKNOWN in gconv-modules.d
- iconvconfig: Use common gconv module parsing function
- gconv_conf: Split out configuration file processing
- gconv_conf: Remove unused variables
- iconv: Remove alloca use in gconv-modules configuration parsing
- Remove unsused symbols from nptl/Versions
- linux: Only use 64-bit syscall if required for clock_nanosleep
- linux: Only use 64-bit syscall if required for internal futex
- linux: Only use 64-bit syscall if required for utimensat family
- linux: Only use 64-bit syscall if required for sigtimedwait
- linux: Only use 64-bit syscall if required for mq_timedsend
- linux: Only use 64-bit syscall if required for mq_timedreceive
- linux: Only use 64-bit syscall if required for timerfd_settime
- linux: Only use 64-bit syscall if required for semtimedop
- linux: timerfd_gettime minor cleanup
- linux: Remove time64-support
- linux: Remove supports_time64 () from clock_gettime
- linux: Remove supports_time64 () from clock_getres
- linux: Only use 64-bit syscall if required for select
- linux: Only use 64-bit syscall if required for pselect
- linux: Only use 64-bit syscall if required for ppoll
- support: Add support_create_timer
- Use 64 bit time_t stat internally
- malloc: Drop __malloc_initialized from Versions
- tst-mcheck: Rename to tst-malloc-check
- Add hidden prototypes for fsync, fdatasync
- nptl: Move pthreadP.h into sysdeps directory
- rt: Move generic implementation from sysdeps/pthread to rt
- rt: Move shm_unlink into libc
- rt: Move shm_open into libc
- rt: Replace generic stub of shm_unlink with the posix version
- rt: Replace generic stub of shm_open with the posix version
- Fix librt-routines-var issues for !PTHREAD_IN_LIBC
- rt: Lexicographically sort Versions file; librt-routines in Makefile
- elf: Use _dl_catch_error from base namespace in dl-libc.c [BZ #27646]
- Makeconfig: Fix time64-compat.mk target

* Sun Jun 27 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-26
- Add automatic requires if building against glibc development snapshots

* Thu Jun 24 2021 Carlos O'Donell <carlos@redhat.com> - 2.33.9000-25
- Fix thread local storage corruption (#1974970)

* Tue Jun 22 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.33.9000-24
- Strengthen dependency on glibc-gconv-extra.

* Fri Jun 18 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-23
- Make glibc-all-langpacks require glibc-gconv-extra in buildroots (#1973663)

* Thu Jun 17 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-22
- Export libthread_db symbols under GLBIC_PRIVATE (#1965374)

* Thu Jun 17 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-21
- Redo the crafted libc.so.6 symbol table for valgrind (#1965374)

* Thu Jun 17 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-20
- Remove .symtab from libc.so.6 again (#1965374)

* Thu Jun 17 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-19
- Drop glibc-rh697421.patch: The ISO-10646-UCS-2// alias for UTF-8 is incorrect
  (#1972520)

* Wed Jun 16 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-18
- Rebuild against rawhide gcc

* Tue Jun 15 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-17
- Dropped glibc-gconv-modules-revert.patch, applied upstream.
- Auto-sync with upstream branch master,
  commit aa9a7f629632c9180de89632d4f2c1e6039f7781:
- nptl: Export _pthread_cleanup_push, _pthread_cleanup_pop again
- s390x: Align child stack while clone. [BZ #27968]
- y2038: Add test coverage
- libsupport: Add 64-bit time_t support for stat functions
- libsupport: Add 64-bit time_t support for time functions
- io: Add ftw64 with 64-bit time_t support
- io: Add fts64 with 64-bit time_t support
- posix: Add glob64 with 64-bit time_t support
- y2038: Add support for 64-bit time on legacy ABIs
- time: Add 64-bit time support for getdate
- y2038: Add __USE_TIME_BITS64 support for socket-constants.h
- y2038: Use a common definition for shmid_ds
- y2038: Use a common definition for semid_ds
- y2038: Use a common definition for msqid_ds
- y2038: Use a common definition for stat
- y2038: linux: Add __USE_TIME_BITS64 support for struct timex
- y2038: Add __USE_TIME_BITS64 support for struct utimbuf
- y2038: Add __USE_TIME_BITS64 support for struct timespec
- y2038: Add __USE_TIME_BITS64 support for struct timeval
- y2038: Add __USE_TIME_BITS64 support for time_t
- linux: Add recvvmsg fallback for 64-bit time_t SO_TIMESTAMP{NS}
- linux: Add fallback for 64-bit time_t SO_TIMESTAMP{NS}
- linux: Add fallback for 64-bit time_t SO_{RCV,SND}TIMEO
- linux: s390: Add libanl.abilist in s390 and s390x
- linux: mips: Split libanl.abilist in n32 and n64
- linux: mips: Split librt.abilist in n32 and n64
- Reinstate gconv-modules as the default configuration file

* Tue Jun 15 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-16
- Preserve some symbols in libc.so.6's symtab (#1965374)

* Tue Jun 15 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-15
- Install shared objects under their ABI names, avoiding symlinks (#1652867)

* Mon Jun 14 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.33.9000-14
- Add a conditional dependency for glibc-gconv-extra.i686 in x86_64.

* Mon Jun 14 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.33.9000-13
- Auto-sync with upstream branch master,
  commit ebae2f5a6f971a8f0b6c99e00f9c45ef7433924a.
- Revert gconv configuration file name to gconv-modules.

* Thu Jun 03 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-12
- libdl is no longer  a separate shared object.
- CVE-2021-33574: Use-after-free via mq_notify (#1965410)
- Auto-sync with upstream branch master,
  commit 466c1ea15f461edb8e3ffaf5d86d708876343bbf:
- dlfcn: Rework static dlopen hooks
- dlfcn: Eliminate GLIBC_PRIVATE dependency from tststatic2
- dlfcn: Cleanups after -ldl is no longer required
- dlfcn: Move dlopen into libc
- dlfcn: Move dlvsym into libc
- dlfcn: Move dlinfo into libc
- dlfcn: Move dladdr1 into libc
- dlfcn: Move dlmopen into libc
- dlfcn: Move dlsym into libc
- dlfcn: Move dladdr into libc
- dlfcn: Move dlclose into libc
- Improve test coverage of strlen function
- fix typo
- dlfcn: Move dlerror into libc
- Add libc ABI extension kludge for baseline-violating libdl symbols
- scripts/versions.awk: Add local: * to all version nodes
- Add missing symbols to Version files
- Fix use of __pthread_attr_copy in mq_notify (bug 27896)
- Use __pthread_attr_copy in mq_notify (bug 27896)
- Update floating-point feature test macro handling for C2X
- stdio-common: Remove _IO_vfwscanf
- aarch64: align stack in clone [BZ #27939]
- powerpc: Optimized memcmp for power10
- x86-64: Align child stack to 16 bytes [BZ #27902]

* Mon May 31 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-11
- glibc-sigsetxid-sa_onstack.patch was applied upstream
- Auto-sync with upstream branch master,
  commit 271ec55d0ae795f03d92e3aa61bff69a31a19e3a:
- support: Do not build xpthread_attr_setaffinity_np for hurd
- nptl: Add pthread_attr_setaffinity_np failure test
- support: Add xpthread_attr_setaffinity_np wrapper
- nptl: Move createthread to pthread_create
- nptl: Move Linux createthread to nptl
- nptl: Install SIGSETXID handler with SA_ONSTACK [BZ #27914]
- aarch64: Added optimized memset for A64FX
- aarch64: Added optimized memcpy and memmove for A64FX
- benchtests: Fixed bench-memcpy-random: buf1: mprotect failed
- aarch64: Added Vector Length Set test helper script
- aarch64: define BTI_C and BTI_J macros as NOP unless HAVE_AARCH64_BTI
- config: Added HAVE_AARCH64_SVE_ASM for aarch64
- tst-mallinfo2.c: Use correct multiple for total variable

* Wed May 26 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-10
- nptl: Install SIGSETXID handler with SA_ONSTACK [BZ #27914]

* Tue May 25 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-9
- Auto-sync with upstream branch master,
  commit ac0353af81a23535f517586a5d04427120a157ac.
- This removes libpthread as a separate shared object.  New programs
  will depend on the GLIBC_2.34 symbol version.  Upstream development
  brings in the following noteworthy bug fixes:
- ppc64le: scv ABI error handling fails to check IS_ERR_VALUE (#1962971)
- CVE-2021-27645 glibc: Use-after-free in addgetnetgrentX function in
  netgroupcache.c (#1932590)
- Linking the main program with jemalloc causes sysconf to deadlock in
  audit mode (#1909920)

* Fri May 21 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-8
- Switch back to a unified glibc-headers package for downstream (#1940686)

* Fri May 21 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-7
- aarch64: Enable optional memory tagging support

* Tue May 11 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-6
- Use distribution mechanism for debuginfo (#1661510, #1886295, #1905611)

* Thu May  6 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-5
- Build locales in parallel again

* Tue May  4 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-4
- Various changes to get glibc building again, using selected upstream
  backports.
- Re-enable -Werror by default.
- This release introduces __libc_start_main@@GLIBC_2.34, so binaries
  are not compatible with glibc 2.33.  Building binaries against this
  glibc version is not recommended because of the partial libpthread
  transition.
- glibc-upstream-amx-detection.patch: Fix build failure after GCC 11.1 update.
- glibc-upstream-malloc-test-hang.patch: Avoid test hang due to
  annobin/binutils bug (#1951492)

* Wed Mar 03 2021 Arjun Shankar <arjun@redhat.com> - 2.33.9000-3
- Drop glibc-rh819430.patch; fixed upstream.
- Auto-sync with upstream branch master,
  commit f01a61e13872109b3b233158ab664364bd1879bc:
- i386: Regenerate ulps
- x86: Add CPU-specific diagnostics to ld.so --list-diagnostics
- x86: Automate generation of PREFERRED_FEATURE_INDEX_1 bitfield
- ld.so: Implement the --list-diagnostics option
- powerpc: Update libm-test-ulps
- tst: Add test for utimes
- tst: Add test for utime
- tst: Add test for futimens
- nptl: __libc_cleanup_push/__libc_cleanup_pop require -fexceptions
- elf: Build __dl_iterate_phdr with unwinding support [BZ #27498]
- nptl: Use <unwind-link.h> for accessing the libgcc_s unwinder
- Implement _Unwind_Resume in libc on top of <unwind-link.h>
- Move sysdeps/gnu/unwind-resume.c to sysdeps/generic/unwind-resume.c
- __frame_state_for: Use <unwind-link.h> for unwinder access
- sparc: Implement backtrace on top <unwind-link.h>
- m68k: Implement backtrace on top of <unwind-link.h>
- i386: Implement backtrace on top of <unwind-link.h>
- arm: Implement backtrace on top of <unwind-link.h>
- backtrace: Implement on top of <unwind-link.h>
- Implement <unwind-link.h> for dynamically loading the libgcc_s unwinder
- Correct buffer end pointer in IO_wdefault_doallocate (BZ #26874)
- aarch64: update ulps.
- Add inputs that generate larger error bounds
- Reduce the statically linked startup code [BZ #23323]
- posix: Falling back to non wide mode in case of encoding error [BZ #14185]
- nptl: Move elision implementations into libc
- NEWS: Add missing bug closures
- added rt to malloc/Depend [BZ #27132]
- x86: Use x86/nptl/pthreaddef.h
- nptl: Move futex-internal into libc
- nptl: Move lowlevellock into libc [BZ #15648]
- nptl: Move futex-internal.c into main nptl directory
- nptl: Reformat Versions
- nptl: Split libpthread-routines into one routine per line
- x86: Remove unused variables for raw cache sizes from cacheinfo.h
- Use Linux 5.11 in build-many-glibcs.py.
- <bits/platform/x86.h>: Correct x86_cpu_TBM
- x86_64/clone.S: Upate comments
- i386/clone.S: Remove redundant EBX load
- aarch64: Remove the unused __read_tp symbol
- build-many-glibcs.py: Use make -O for more consistent log output

* Sun Feb 21 2021 Carlos O'Donell <carlos@redhat.com> - 2.33.9000-2
- Auto-sync with upstream branch master,
  commit e9e7f24543e6d1b0a31641f144697e261df6ccd7:
- configure: Replace obsolete AC_TRY_LINK with AC_LINK_IFELSE
- configure: Remove obsolete AC_CHECK_TOOL_PREFIX
- configure: Replace obsoleted AC_HELP_STRING with AS_HELP_STRING
- Update syscall lists for Linux 5.11.
- Correct hppa EFD_NONBLOCK, IN_NONBLOCK, SFD_NONBLOCK and TFD_NONBLOCK defines.
- string: Work around GCC PR 98512 in rawmemchr
- tst: time: Provide Y2038 tests for mktime (tst-mktime4.c)
- tst: Provide test for difftime
- tst: Provide test for ctime
- tst: Provide test for sched_rr_get_interval
- S390: Add new hwcap values.
- aarch64: Fix sys/ptrace.h if linux headers are included
- elf: Do not copy vDSO soname when setting up link map
- x86: Remove the extra space between "# endif"
- hurd: Fix fstatfs build failure
- linux: Remove stat-check.c
- linux: Remove overflow.h
- linux: Consolidate internal_statvfs
- linux: Consolidate statvfs implementations
- linux: Consolidate fstatvfs implementations
- linux: Consolidate statfs implementations
- linux: Consolidate fstatfs implementations
- linux: Set LFS statfs as default
- linux: Set default kernel_stat.h to LFS
- linux: Fix STATFS_IS_STATFS64 definition

* Fri Feb 12 2021 Florian Weimer <fweimer@redhat.com> - 2.33.9000-1
- Auto-sync with upstream branch master,
  commit 228f30ab4724d4087d5f52018873fde22efea6e2:
- tunables: Disallow negative values for some tunables
- x86: Use SIZE_MAX instead of (long int)-1 for tunable range value
- tunables: Simplify TUNABLE_SET interface
- setrlimit/getrlimit: Use __nonnull to avoid null pointer
- benchtests: Updated json bench-variant attribute
- regex: stop using alloca
- regexec: remove alloca usage in build_trtable
- regex: remove alloca usage on regex set_regs
- malloc: Sync dynarray with gnulib
- misc: Sync cdefs.h with gnulib
- linux: Fix __sem_check_add_mapping search_sem
- linux: Fix __sem_check_add_mapping name length
- Add more ptrace constants for AArch64 and PowerPC.
- strchr: Add additional benchmarks and tests
- x86-64: Refactor and improve performance of strchr-avx2.S
- pthread: Remove alloca usage from __sem_check_add_mapping
- pthread: Refactor semaphore code
- linux: Require /dev/shm as the shared memory file system
- sunrpc: Fix typo in xdr_string comment
- tst: Provide test for ppoll
- tst: Provide test for timerfd related functions
- x86: Add PTWRITE feature detection [BZ #27346]
- nsswitch: return result when nss database is locked [BZ #27343]
- printf: Add smoke tests for long double
- Add NT_ARM_TAGGED_ADDR_CTRL from Linux 5.10 to elf.h.
- argp: Avoid undefined behaviour when invoking qsort().
- argp: Improve comments.
- argp: Don't pass invalid arguments to isspace, isalnum, isalpha, isdigit.
- argp: Don't rely on undefined behaviour of _tolower().
- argp: fix pointer-subtraction bug
- Use binutils 2.36 branch in build-many-glibcs.py.
- manual: Correct description of ENTRY [BZ #17183]
- nptl: Remove private futex optimization [BZ #27304]
- stdio-common: Add a few double formatting tests [BZ #27245]
-  posix/tst-rfc3484: Fix compile failure linking to local __stat64
- i686: Regenerate ULPs
- tst-rtld-list-tunables.sh: Unset glibc tunables
- linux: Remove shmmax check from tst-sysvshm-linux
- x86: Adding an upper bound for Enhanced REP MOVSB.
- Fix version.h for glibc 2.34 development
- Add MS_NOSYMFOLLOW from Linux 5.10 to <sys/mount.h>.
- Move _SC_MINSIGSTKSZ/_SC_SIGSTKSZ entry in NEWS
- libSegFault: Fix printing signal number [BZ #27249]
- hurd TIOCFLUSH: fix fixing argument
- sysconf: Add _SC_MINSIGSTKSZ/_SC_SIGSTKSZ [BZ #20305]
- hurd TIOCFLUSH: Cope BSD 4.1 semantic
- tst-mallinfo2.c: Remove useless trailing semicolon for macro
- elf: Replace a --defsym trick with an object file to be compatible with LLD
- Open master branch for glibc 2.34 development
- Prepare for glibc 2.33 release
- Update NEWS with bugs
- Update translations
- NEWS: Fix typo in CVE-2021-3326 entry
- elf: Fix tests that rely on ld.so.cache for cross-compiling
- NEWS: Mention CVE-2021-3326 (iconv assertion with ISO-20220-JP-3)
- NEWS: Add entry for glibc-hwcaps and deprecate legacy hwcaps
- x86: Properly set usable CET feature bits [BZ #26625]
- Update translations
- Update libc.pot for 2.33 release
- Update ia64 libm-test-ulps
- sh: Update libm-tests-ulps
- ia64: Fix brk call on statup
- Update sparc libm-test-ulps
- Update alpha libm-test-ulps
- powerpc64: Workaround sigtramp vdso return call
- Fix nss/tst-reload2 for systems without PATH_MAX
- nsswitch: do not reload if "/" changes
- elf: Limit tst-prelink-cmp target archs
- CVE-2021-3326: gconv: Fix assertion failure in ISO-2022-JP-3 module (#1921917)

* Wed Jan 27 2021 Arjun Shankar <arjun@redhat.com> - 2.32.9000-29
- Auto-sync with upstream branch master,
  commit df359a25ba6f6bda06104229fbfe284c1fb30915:
- Revert "Make libc symbols hidden in static PIE" [BZ #27237]
- benchtests: Do not build bench-timing-type with MODULE_NAME=libc
- aarch64: Fix the list of tested IFUNC variants [BZ #26818]
- Update INSTALL with package versions that are known to work
- aarch64: Move and update the definition of MTE_ENABLED
- Fix misplaced const
- Update C-SKY libm-test-ulps
- manual: Correct argument order in mount examples [BZ #27207]
- linux: mips: Fix getdents64 fallback on mips64-n32
- x86: Properly match CPU features in /proc/cpuinfo [BZ #27222]
- x86-64: Update tst-glibc-hwcaps-2.c for x86-64 baseline
- powerpc64: Select POWER9 machine for the scv instruction
- x86: Check ifunc resolver with CPU_FEATURE_USABLE [BZ #27072]
- Revert "linux: Move {f}xstat{at} to compat symbols" for static build
- aarch64: revert memcpy optimze for kunpeng to avoid performance degradation
- Make libc symbols hidden in static PIE
- csu: Move static pie self relocation later [BZ #27072]
- Use hidden visibility for early static PIE code
- csu: Avoid weak ref for __ehdr_start in static PIE
- configure: Check for static PIE support
- elf: Avoid RELATIVE relocs in __tunables_init
- elf: Make the tunable struct definition internal only
- <sys/platform/x86.h>: Remove the C preprocessor magic
- posix: Fix fnmatch.c on bootstrap
- stdlib: Add testcase for BZ #26241
- posix: Fix regex_internal.h on bootstrap
- Use <startup.h> in __libc_init_secure
- elf: Avoid RELATIVE relocation for _dl_sysinfo
- libmvec: Add extra-test-objs to test-extras
- Hurd: Add rtld-strncpy-c.c
- Update MIPS libm-test-ulps.
- Update arm libm-test-ulps.
- Update powerpc-nofpu libm-test-ulps.
- Update hppa libm-test-ulps
- ARC: nofpu: Regenerate ulps
- ld.so: Add --list-tunables to print tunable values
- math/test-tgmath2: Fix fabs failure when no long double
- x86: Move x86 processor cache info to cpu_features
- Fix x86 build with --enable-tunable=no
- ifuncmain6pie: Remove the circular IFUNC dependency [BZ #20019]

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.9000-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Arjun Shankar <arjun@redhat.com> - 2.32.9000-27
- Introduce new glibc-doc.noarch subpackage (#1346925)
- Move the reference manual info pages from glibc-devel to glibc-doc
- Move debugger interface documentation from glibc to glibc-doc
- Remove unnecessary README, INSTALL, NEWS files from glibc
- Remove unnecessary README.timezone and gai.conf files from glibc-common

* Thu Jan 14 2021 Arjun Shankar <arjun@redhat.com> - 2.32.9000-26
- Deprecate nscd (#1905135)
- https://fedoraproject.org/wiki/Changes/DeprecateNSCD

* Wed Jan 13 2021 Carlos O'Donell <carlos@redhat.com> - 2.32.9000-25
- Auto-sync with upstream branch master,
  commit cf1290064598def8dfeddec3d86d98495aee1fba:
- Use the right argument code in unnormal tests
- ldconfig/x86: Store ISA level in cache and aux cache
- elf: work around a gcc bug in elf_get_dynamic_info
- x86: Set header.feature_1 in TCB for always-on CET [BZ #27177]
- posix: consume less entropy on tempname
- Makerules: Do not require startup files for format.lds probe object
- install: Replace scripts/output-format.sed with objdump -f [BZ #26559]
- math: Add BZ#18980 fix back on dbl-64 cosh
- posix: Sync tempname with gnulib [BZ #26648]
- posix: Fix return value of system if shell can not be executed [BZ #27053]
- support: Add xchmod wrapper
- Update STATX_ATTR_DAX value from Linux 5.10.
- riscv: Initialize $gp before resolving the IRELATIVE relocation
- riscv: support GNU indirect function
- posix: Correct attribute access mode on readlinkat [BZ #27024].
-  Add xfchmod to libsupport
- Add xchdir to libsupport.
- POSIX locale: Fix typo in comment
- ARC: Regenerate ulps
- mntent: Use __putc_unlocked instead of fputc_unlocked
- aarch64: define PI_STATIC_AND_HIDDEN
- Update NEWS for CVE-2019-25013.
- x86: Support GNU_PROPERTY_X86_ISA_1_V[234] marker [BZ #26717]
- Remove dbl-64/wordsize-64 (part 2)
- Remove dbl-64/wordsize-64
- Add SEGV_MTEAERR and SEGV_MTESERR from Linux 5.10.
- support: Add support_small_thread_stack_size
- stdlib: Sync canonicalize with gnulib [BZ #10635] [BZ #26592] [BZ #26341] [BZ #24970]
- malloc: Add scratch_buffer_dupfree
- Import filename.h from gnulib
- Import idx.h from gnulib
- alpha: Provide wait4 for static library [BZ #27150]
- aarch64: push the set of rules before falling into slow path
- nptl: Fix comment typo in pthread_cond_wait.c
- x86: Check IFUNC definition in unrelocated executable [BZ #20019]
- hurd: Fix mmap(!MAP_FIXED) on bogus address

* Mon Jan 04 2021 Florian Weimer <fweimer@redhat.com> - 2.32.9000-24
- Drop glibc-fedora-__libc_multiple_libcs.patch.  Replaced by upstream's
  __libc_initial flag.
- Adjust glibc-rh819430.patch to upstream's gnulib merge of fnmatch.
- Disable -Werror again due to GCC PR98512.
- Auto-sync with upstream branch master,
  commit 3ec5d83d2a237d39e7fd6ef7a0bc8ac4c171a4a5:
- x86-64: Avoid rep movsb with short distance [BZ #27130]
- aarch64: fix stack missing after sp is updated
- nptl: Remove set*id, set*gid files which are not built
- Drop nan-pseudo-number.h usage from tests
- posix: Sync fnmatch with gnulib
- Sync flexmember.h with gnulib
- Sync intprops.h with gnulib
- posix: Sync glob code with gnulib
- posix: Sync regex code with gnulib
- Move generic nan-pseudo-number.h to ldbl-96
- Sync FDL from https://www.gnu.org/licenses/fdl-1.3.texi
- Sync move-if-change from Gnulib
- Update automatically-generated copyright dates
- Update copyright dates not handled by scripts/update-copyrights.
- Update copyright dates with scripts/update-copyrights
- aarch64: use PTR_ARG and SIZE_ARG instead of DELOUSE
- nonstring: Enable __FORTIFY_LEVEL=3
- string: Enable __FORTIFY_LEVEL=3
- Introduce _FORTIFY_SOURCE=3
- Warn on unsupported fortification levels
- powerpc: Use scv instruction on clone when available
- powerpc: Runtime selection between sc and scv for syscalls
- malloc: preserve errno on mcheck hooks [BZ #17924]
- x86 long double: Add tests for pseudo normal numbers
- x86 long double: Consider pseudo numbers as signaling
- io: Remove xmknod{at} implementations
- io: Remove xstat implementations
- free: preserve errno [BZ#17924]
- hurd: Accept including hurd/version.h
- hurd: Add WSTOPPED/WCONTINUED/WEXITED/WNOWAIT support [BZ #23091]
- support: Make support_process_state_wait wait less
- hurd: set sigaction for signal preemptors in arch-independent file
- hurd: Fix spawni SPAWN_XFLAGS_TRY_SHELL with empty argv
- hurd: Try shell in posix_spawn* only in compat mode
- Remove _ISOMAC check from <cpu-features.h>
- x86: Remove the duplicated CPU_FEATURE_CPU_P
- Partially revert 681900d29683722b1cb0a8e565a0585846ec5a61
- x86 long double: Support pseudo numbers in isnanl
- x86 long double: Support pseudo numbers in fpclassifyl
- MTE: Do not pad size in realloc_check
- tests-mcheck: New variable to run tests with MALLOC_CHECK_=3
- elf: Account for glibc-hwcaps/ prefix in _dl_important_hwcaps
- misc: Use __ferror_unlocked instead of ferror
- s390x: Regenerate ulps
- powerpc: Regenerate ulps
- addmntent: Remove unbounded alloca usage from getmntent [BZ#27083]
- <sys/platform/x86.h>: Add Intel LAM support
- i386: Regenerate ulps
- aarch64: update ulps.
- aarch64: Add aarch64-specific files for memory tagging support
- aarch64: Add sysv specific enabling code for memory tagging
- linux: Add compatibility definitions to sys/prctl.h for MTE
- malloc: Basic support for memory tagging in the malloc() family
- elf: Add a tunable to control use of tagged memory
- config: Allow memory tagging to be enabled when configuring glibc
- alpha: Remove anonymous union in struct stat [BZ #27042]
- add inputs to auto-libm-test-in yielding larger errors (binary64, x86_64)
- m68k: fix clobbering a5 in setjmp() [BZ #24202]
- iconv add iconv_close before the function returned with bad value.
- iconv: use iconv_close after iconv_open
- Fix buffer overrun in EUC-KR conversion module (bz #24973)
- hurd: Make trampoline fill siginfo ss_sp from sc_uesp
- Hurd: make sigstates hold a reference on thread ports
- profil-counter: Add missing SIGINFO case
- hurd: implement SA_SIGINFO signal handlers.
- hurd: Fix ELF_MACHINE_USER_ADDRESS_MASK value
- hurd: Note when the vm_map kernel bug was fixed
- hurd: Also turn KERN_INVALID_ADDRESS to EINVAL
- ieee754: Remove unused __sin32 and __cos32
- ieee754: Remove slow paths from asin and acos
- getenv: Move call to strlen to the branch it's used in.
- Update kernel version to 5.10 in tst-mman-consts.py.
- s390x: Require GCC 7.1 or later to build glibc.
- malloc: Use __libc_initial to detect an inner libc
- Replace __libc_multiple_libcs with __libc_initial flag
- {nptl,htl}/semaphoreP.h: clean up
- htl: Get sem_open/sem_close/sem_unlink support [BZ #25524]
- pthread: Move semaphore initialization for open to semaphoreP.h
- Mark __libc_freeres_fn as used [BZ #27002]
- Update syscall lists for Linux 5.10.
- htl: Add pshared semaphore support
- hurd: Add LLL_PRIVATE and LLL_SHARED
- hurd: Add __libc_open and __libc_close
- htl: Add futex-internal.h
- hurd: Add __lll_abstimed_wait_intr
- hurd: make lll_* take a variable instead of a ptr
- hurd: Rename LLL_INITIALIZER to LLL_LOCK_INITIALIZER
- Use Linux 5.10 in build-many-glibcs.py.

* Wed Dec 16 2020 DJ Delorie <dj@redhat.com> - 2.32.9000-23
- Fix conditionals for _enable_debug_packages and benchtests [BZ #1902514]

* Tue Dec 15 2020 Patsy Griffin <patsy@redhat.com> - 2.32.9000-22
- Auto-sync with upstream branch master,
  commit 4d0985543f479a6f421d4d8a9e0d1dc71c9c2c53.
- elf: Record libc.so link map when it is the main program (bug 20972)
- Use GMP 6.2.1 in build-many-glibcs.py.
- aarch64: remove the strlen_asimd symbol
- aarch64: fix static PIE start code for BTI [BZ #27068]
- elf: Fix failure handling in _dl_map_object_from_fd
- elf: inline lose for error handling
- Remove strtoimax, strtoumax, wcstoimax, wcstoumax inlines
- nsswitch: handle missing actions properly
- x86: Remove the default REP MOVSB threshold tunable value [BZ #27061]
- elf.h: Remove SHF_GNU_BUILD_NOTE.
- elf.h: fix spelling typos in comments
- Fix spelling and grammar in several comments
- malloc: Detect infinite-loop in _int_free when freeing tcache [BZ#27052]
- elf: Fix dl-load.c
- elf: Include libc.so.6 as main program in dependency sort (bug 20972)
- support: Add support_slibdir_prefix variable
- aarch64: Use mmap to add PROT_BTI instead of mprotect [BZ #26831]
- elf: Pass the fd to note processing
- elf: Move note processing after l_phdr is updated
- aarch64: align address for BTI protection [BZ #26988]
- aarch64: Fix missing BTI protection from dependencies [BZ #26926]
- Fix linknamespace errors in nss_database.c if build with -Os.
- treewide: fix incorrect spelling of indices in comments
- linux: Consolidate brk implementation
- elf: Include <sys/param.h> in cache.c
- s390x: Add glibc-hwcaps support
- elf: Fix run-time dependencies of tst-dlopen-fail-2
- Handle out-of-memory case in svc_tcp.c/svc_unix.c:rendezvous_request.
- elf: Fix incorrect comparison in sort_priorities_by_name
- S390: Derive float_t from FLT_EVAL_METHOD
- Fix parsing of /sys/devices/system/cpu/online (bug 25859)
- Make strtoimax, strtoumax, wcstoimax, wcstoumax into aliases
- Fixed typos in "NEWS for version 2.32"
- Add NEWS entry for CVE-2020-29562 (BZ #26923)
- iconv: Fix incorrect UCS4 inner loop bounds (BZ#26923)
- Drop glibc-rh1906066 and glibc-rh741105 patches fixed by sync.

* Mon Dec 14 2020 Florian Weimer <fweimer@redhat.com> - 2.32.9000-21
- Re-enable -Werror everywhere (#1888246)

* Wed Dec 09 2020 DJ Delorie <dj@redhat.com> - 2.32.9000-20
- nsswitch: handle missing actions properly (temporary fix for 1906066)

* Mon Dec 07 2020 Arjun Shankar <arjun@redhat.com> - 2.32.9000-19
- Auto-sync with upstream branch master,
  commit 088e9625378f25607acff3daf7a79cbdee497043:
- x86: Rename readelflib.c
- nsswitch: use new internal API (callers)
- nsswitch: user new internal API (tests)
- nsswitch: use new internal API (core)
- nss: Implement <nss_database.h>
- <nss_action.h>: New abstraction for combining NSS modules and NSS actions
- nss: Introduce <nss_module.h>
- Add scripts/move-symbol-to-libc.py

* Fri Dec 04 2020 Arjun Shankar <arjun@redhat.com> - 2.32.9000-18
- Drop glibc-revert-fxstat-compat.patch; applied upstream.
- Drop glibc-revert-mknod-compat.patch; applied upstream.
- Auto-sync with upstream branch master,
  commit 4c38c1a229bc3628269ad98bd7e8d31d118d91f6:
- powerpc64le: Add glibc-hwcaps support
- x86: Adjust tst-cpu-features-supports.c for GCC 11
- x86: Set RDRAND usable if CPU supports RDRAND
- elf: Add missing <stddef.h> header to elf/dl-hwcaps.h
- lowlevellock-futex: Remove not used macros
- futex: Remove not used futex_reltimed_wait{_cancelable}
- y2038: Convert gai_suspend to support 64 bit time
- symbols: Add defines for libanl's libanl_hidden_{def|proto}
- x86_64: Add glibc-hwcaps support
- elf: Add glibc-hwcaps subdirectory support to ld.so cache processing
- elf: Process glibc-hwcaps subdirectories in ldconfig
- elf: Implement tail merging of strings in ldconfig
- elf: Implement a string table for ldconfig, with tail merging
- elf: Add extension mechanism to ld.so.cache
- elf: Add endianness markup to ld.so.cache (bug 27008)
- elf: Add glibc-hwcaps support for LD_LIBRARY_PATH
- elf: Synchronize <elf.h> section header flags with binutils
- x86: Fix THREAD_SELF definition to avoid ld.so crash (bug 27004)
- htl: Add hidden def for __pthread_create/detach
- manual: Clarify File Access Modes section and add O_PATH
- htl: Add missing symbols
- Revert "linux: Move xmknod{at} to compat symbols"
- Revert "linux: Move {f}xstat{at} to compat symbols"
- elf.h: Fix spelling of EM_TILE64 comment
- nptl: Fix __futex_clocklock64 return error check [BZ #26964]
- powerpc64le: ifunc select *f128 routines in multiarch mode
- y2038: Convert aio_suspend to support 64 bit time
- Fix typo in NEWS file
- nptl: Add EOVERFLOW checks for futex calls
- nptl: Fix PTHREAD_PRIO_PROTECT timed lock
- sh: Add sh4 fpu Implies folder
- io: nftw/ftw: Fix stack overflow with large nopenfd [BZ #26353]
- elf: Introduce enum opt_format in the ldconfig implementation
- support: Add support_copy_file
- NEWS entry for commit b4f020c9b408fb3d1d3d4901c4a71839145f8791
- timezone: Change zdump installation to bin directory
- nptl: Return EINVAL for invalid clock for pthread_clockjoin_np
- nptl: Return EINVAL for pthread_mutex_clocklock/PI with CLOCK_MONOTONIC [BZ #26801]
- nptl: Replace lll_futex_wake with futex-internal.h
- nptl: Replace lll_futex_supported_clockid with futex-internal.h
- nptl: Replace lll_futex_{timed_}wait by futex-internal.h
- nptl: Replace lll_timedwait with __futex_abstimed_wait64
- nptl: Replace __futex_clocklock_wait64 with __futex_abstimed_wait64
- nptl: Remove _futex_clock_wait_bitset64
- nptl: Consolidate __futex_abstimed_wait_{cancelable}64
- nptl: Extend __futex_abstimed_wait_cancelable64 comment
- nptl: Remove clockwait_tid
- nptl: Remove futex_wait_cancelable
- nptl: Remove unused internal futex functions
- Mark mtrace tests UNSUPPORTED if bug-ga2.mtrace or tst-leaks2.mtrace are missing
- elf: Fix uninitialized variable for _dl_write
- powerpc: Make PT_THREAD_POINTER available to assembly code
- Use libnss_files.so for tests posix/bug-ga2 and resolv/tst-leaks2 [BZ #26821]
- hurd report-wait: Fix stpcpy usage
- hurd S_msg_report_wait: Fix detecting fd ports
- hurd S_msg_report_wait: Fix reporting ports
- hurd: Fix strcpy calls
- hurd: Fix _S_msg_get/set_env_variable prototype
- hurd: Enable using ifunc
- Add {,sysdep-}ld-library-path make variable
- nptl: Move stack list variables into _rtld_global
- hurd: let _dl_argv and __libc_stack_end be relro
- hurd: Remove some remnants of cthreads
- nanosleep: Pass NULL when rem == NULL on ports with __TIMESIZE != 64
- y2038: Convert thrd_sleep to support 64 bit time
- y2038: Convert mtx_timedlock to support 64 bit time
- y2038: Convert cnd_timedwait to support 64 bit time
- hurd: Drop CLOCK_MONOTONIC change which slipped in
- hurd: make ptsname fail with ENOTTY on non-master-pty
- mach: Add missing assert.h include
- hurd: break relocation loop between libc.so and lib{mach,hurd}user.so
- Remove obsolete defines for HPUX support from fcntl.h and update O_NONBLOCK.
- Remove tls.h inclusion from internal errno.h
- nptl: Eliminate <smp.h> and __is_smp
- powerpc: Eliminate UP macro conditionals
- x86: Remove UP macro.  Define LOCK_PREFIX unconditionally.
- alpha: Remove UP preprocessor conditionals
- hurd: Make sure signals get started
- hurd: initialize libpthread before starting the signal thread
- hurd: Make _hurd_libc_proc_init idempotent
- powerpc: Add optimized stpncpy for POWER9
- powerpc: Add optimized strncpy for POWER9
- Don't use nested function in test-ffs
- Use __builtin___stpncpy_chk when available
- tests: Remove NULL check for an array
- hurd: Move {,f,l}xstat{,at} and xmknod{at} to compat symbols
- hurd: Notify the proc server later during initialization
- htl: Initialize later
- htl: Keep thread signals blocked during its initialization
- htl: Fix spurious symbols in namespaces
- Use O_CLOEXEC in sysconf [BZ #26791]
- struct _Unwind_Exception alignment should not depend on compiler flags
- hurd: keep only required PLTs in ld.so
- hurd: Add missing startup calls
- riscv: Get cache information through sysconf
- RISC-V: Add _dl_start_user.

* Thu Nov 26 2020 Florian Weimer <fweimer@redhat.com> - 2.32.9000-17
- s390x: Do not rewrite program interpreter symlink (make install is enough)

* Tue Nov 10 2020 Carlos O'Donell <carlos@redhat.com> - 2.32.9000-16
- Remove the work around for systemd-nspawn (#1869030).

* Mon Nov 09 2020 DJ Delorie <dj@redhat.com> - 2.32.9000-15
- Auto-sync with upstream branch master,
  commit 75a193b7611bade31a150dfcc528b973e3d46231.
- linux: Allow adjtime with NULL argument [BZ #26833]
- aarch64: Add unwind information to _start (bug 26853)
- bsd unlockpt: unlockpt needs to fail with EINVAL, not ENOTTY
- Rearrange bsd_getpt vs bsd_openpt and implement posix_openpt on BSD
- Remove __warndecl
- Remove __warn_memset_zero_len [BZ #25399]
- iconv: Accept redundant shift sequences in IBM1364 [BZ #26224]
- msg: Remove redundant #include <sys/msg.h> header
- tst-setuid1-static-ENV: Add $(common-objpfx)nss [BZ #26820]

* Tue Nov 03 2020 Patsy Griffin <patsy@redhat.com> - 2.32.9000-14
- Auto-sync with upstream branch master,
  commit e156dabc766d6f6f99ce9402999eae380a3ec1f2.
- aarch64: Add variant PCS lazy binding test [BZ #26798]
- aarch64: Fix DT_AARCH64_VARIANT_PCS handling [BZ #26798]
- hurd: Correct 'ethenet' spelling
- Avoid -Wstringop-overflow warning in pthread_cleanup_push macros
- Disable spurious -Warray-bounds for ypclnt.c (bug 26687)
- Do not use array parameter to new_composite_name (bug 26726)
- Disable spurious -Wstringop-overflow for setjmp/longjmp (bug 26647)
- malloc debug: fix compile error when enable macro MALLOC_DEBUG > 1
- tst-tcfree2: adjust coding style.
- elf: In ldconfig, extract the new_sub_entry function from search_dir
- Use MPC 1.2.1 in build-many-glibcs.py.
- Argument Syntax: Use "option", @option, and @command.
- elf: Unify old and new format cache handling code in ld.so
- x86: Restore processing of cache size tunables in init_cacheinfo
- Make elf.h header self contained.
- x86: Optimizing memcpy for AMD Zen architecture.
- Hurd: Fix ftime build
- Add IP_RECVERR_RFC4884 and IPV6_RECVERR_RFC4884 from Linux 5.9.
- misc: Add internal __getauxval2 function
- Remove NEWS entry about ftime removal
- time: Add 64-bit time_t support for ftime
- Reinstate ftime and add deprecate message on ftime usage
- Update kernel version to 5.9 in tst-mman-consts.py.
- Amend grammar and add a description
- Fix typo in NEWS file
- Remove timing related checks of time/tst-cpuclock1
- Update syscall lists for Linux 5.9.
- Use Linux 5.9 in build-many-glibcs.py.
- Reword description of SXID_* tunable properties
- New benchtest: pthread locks
- y2038: nptl: Provide __futex_clock_wait_bitset64 to support 64 bit bitset
- C-SKY: Make dynamic linker's name compitable with the older gcc.
- Revert "C-SKY:Fix dynamic linker's name when mfloat-abi=softfp."
- Move vtimes to a compatibility symbol
- y2038: linux: Provide __time64 implementation
- rt: Fix typos in comments in <aio.h>
- C-SKY:Fix dynamic linker's name when mfloat-abi=softfp.
- Drop the glibc-revert-ftime-compat.patch.

* Thu Oct 29 2020 DJ Delorie <dj@redhat.com> - 2.32.9000-13
- Add BuildRequires for perl (malloc/mtrace) if running the testsuite.

* Wed Oct 21 2020 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.32.9000-12
- Revert __xstat64 symbol removal.
- Revert xmknod* symbol removal.
- Revert ftime symbol removal.

* Sun Oct 18 2020 Patsy Griffin <patsy@redhat.com> - 2.32.9000-11
- Auto-sync with upstream branch master,
  commit 0f09154c64005e78b61484ae87b5ea2028051ea0.
- x86: Initialize CPU info via IFUNC relocation [BZ 26203]
- Add NEWS entry for ftime compatibility move
- support: Add create_temp_file_in_dir
- linux: Add __readdir_unlocked
- linux: Simplify opendir buffer allocation
- linux: Move posix dir implementations to Linux
- linux: Add 64-bit time_t support for wait3
- Move ftime to a compatibility symbol
- linux: Fix time64 support for futimesat
- linux: Use INTERNAL_SYSCALL on fstatat{64}
- shm tests: Append PID to names passed to shm_open [BZ #26737]
- sysvipc: Fix tst-sysvshm-linux on x32
- x86/CET: Update vfork to prevent child return
- resolv: Serialize processing in resolv/tst-resolv-txnid-collision
- statfs: add missing f_flags assignment
- y2038: Remove not used __fstatat_time64 define
- y2038: nptl: Convert pthread_mutex_{clock|timed}lock to support 64 bit
- sysvipc: Return EINVAL for invalid shmctl commands
- sysvipc: Fix IPC_INFO and SHM_INFO handling [BZ #26636]
- AArch64: Use __memcpy_simd on Neoverse N2/V1
- resolv: Handle transaction ID collisions in parallel queries (bug 26600)
- support: Provide a way to clear the RA bit in DNS server responses
- support: Provide a way to reorder responses within the DNS test server
- Add missing stat/mknod symbol on libc.abilist some ABIs
- manual: correct the spelling of "MALLOC_PERTURB_" [BZ #23015]
- manual: replace an obsolete collation example with a valid one
- rtld: fix typo in comment
- elf: Add missing <dl-procinfo.h> header to elf/dl-usage.c
- hurd: support clock_gettime(CLOCK_PROCESS/THREAD_CPUTIME_ID)
- linux: Move xmknod{at} to compat symbols
- linux: Add {f}stat{at} y2038 support
- linux: Move {f}xstat{at} to compat symbols
- linux: Disentangle fstatat from fxstatat
- linux: Implement {l}fstat{at} in terms of fstatat
- linux: Move the struct stat{64} to struct_stat.h
- Remove mknod wrapper functions, move them to symbols
- Remove stat wrapper functions, move them to exported symbols
- <sys/platform/x86.h>: Add FSRCS/FSRS/FZLRM support
- <sys/platform/x86.h>: Add Intel HRESET support
- <sys/platform/x86.h>: Add AVX-VNNI support
- <sys/platform/x86.h>: Add AVX512_FP16 support
- <sys/platform/x86.h>: Add Intel UINTR support
- elf: Do not pass GLRO(dl_platform), GLRO(dl_platformlen) to _dl_important_hwcaps
- elf: Enhance ld.so --help to print HWCAP subdirectories
- elf: Add library search path information to ld.so --help
- sunrpc: Adjust RPC function declarations to match Sun's (bug 26686]
- Avoid GCC 11 -Warray-parameter warnings [BZ #26686].
- elf: Make __rtld_env_path_list and __rtld_search_dirs global variables
- elf: Print the full name of the dynamic loader in the ld.so help message
- elf: Use the term "program interpreter" in the ld.so help message
- scripts/update-copyrights: Update csu/version.c, elf/dl-usage.c
- elf: Implement ld.so --version
- nptl: Add missing cancellation flags on lockf
- Update mips64 libm-test-ulps
- Update alpha libm-test-ulps
- elf: Implement ld.so --help
- elf: Record whether paths come from LD_LIBRARY_PATH or --library-path
- elf: Move ld.so error/help output to _dl_usage
- elf: Extract command-line/environment variables state from rtld.c

* Wed Oct 14 2020 Florian Weimer <fweimer@redhat.com> - 2.32.9000-10
- Disable -Werror on ELN (#1888246)

* Wed Oct 14 2020 Florian Weimer <fweimer@redhat.com> - 2.32.9000-9
- Make glibc.spec self-contained (#1887097)

* Thu Oct 08 2020 Arjun Shankar <arjun@redhat.com> - 2.32.9000-8
- Drop glibc-fix-float128-benchtests.patch; applied upstream.
- Auto-sync with upstream branch master,
  commit 72d36ffd7db55ae599f4c77feb0eae25a0f3714e:
- elf: Implement __rtld_malloc_is_complete
- __vfscanf_internal: fix aliasing violation (bug 26690)
- Revert "Fix missing redirects in testsuite targets"
- nptl: Add missing cancellation flags on futex_internal and pselect32
- elf: Implement _dl_write
- elf: Do not search HWCAP subdirectories in statically linked binaries
- Linux: Require properly configured /dev/pts for PTYs
- Linux: unlockpt needs to fail with EINVAL, not ENOTTY (bug 26053)
- login/tst-grantpt: Convert to support framework, more error checking
- posix: Fix -Warray-bounds instances building timer_create [BZ #26687]
- Replace Minumum/minumum with Minimum/minimum
- Optimize scripts/merge-test-results.sh
- Fix GCC 11 -Warray-parameter warning for __sigsetjmp (bug 26647)
- manual: Fix typo
- y2038: nptl: Convert pthread_rwlock_{clock|timed}{rd|wr}lock to support 64
  bit time
- Y2038: nptl: Provide futex_abstimed_wait64 supporting 64 bit time
- sysvipc: Return EINVAL for invalid msgctl commands
- sysvipc: Fix IPC_INFO and MSG_INFO handling [BZ #26639]
- sysvipc: Return EINVAL for invalid semctl commands
- sysvipc: Fix SEM_STAT_ANY kernel argument pass [BZ #26637]
- aarch64: enforce >=64K guard size [BZ #26691]
- sysvipc: Fix semtimedop for Linux < 5.1 for 64-bit ABI
- nptl: futex: Move __NR_futex_time64 alias to beginning of futex-internal.h
- nptl: Provide proper spelling for 32 bit version of futex_abstimed_wait
- string: Fix strerrorname_np return value [BZ #26555]
- Set tunable value as well as min/max values
- ld.so: add an --argv0 option [BZ #16124]
- Reversing calculation of __x86_shared_non_temporal_threshold
- linux: Add time64 recvmmsg support
- linux: Add time64 support for nanosleep
- linux: Consolidate utimes
- linux: Use 64-bit time_t syscall on clock_getcputclockid
- linux: Add time64 sigtimedwait support
- linux: Add time64 select support
- nptl: Fix __futex_abstimed_wait_cancellable32
- sysvipc: Fix semtimeop for !__ASSUME_DIRECT_SYSVIPC_SYSCALLS
- hurd: add ST_RELATIME
- intl: Handle translation output codesets with suffixes [BZ #26383]
- bench-strcmp.c: Add workloads on page boundary
- bench-strncmp.c: Add workloads on page boundary
- strcmp: Add a testcase for page boundary
- strncmp: Add a testcase for page boundary [BZ #25933]
- Set locale related environment variables in debugglibc.sh
- benchtests: Run _Float128 tests only on architectures that support it
- powerpc: Protect dl_powerpc_cpu_features on INIT_ARCH() [BZ #26615]
- x86: Harden printf against non-normal long double values (bug 26649)
- x86: Use one ldbl2mpn.c file for both i386 and x86_64
- Define __THROW to noexcept for C++11 and later

* Mon Sep 21 2020 Arjun Shankar <arjun@redhat.com> - 2.32.9000-7
- Adjust glibc-rh741105.patch.
- Add glibc-fix-float128-benchtests.patch to allow building on armv7hl.
- Auto-sync with upstream branch master,
  commit cdf645427d176197b82f44308a5e131d69fb53ad:
- Update mallinfo2 ABI, and test
- Allow memset local PLT reference for RISC-V.
- powerpc: fix ifunc implementation list for POWER9 strlen and stpcpy
- nscd: bump GC cycle during cache pruning (bug 26130)
- x86: Use HAS_CPU_FEATURE with IBT and SHSTK [BZ #26625]
- <sys/platform/x86.h>: Add Intel Key Locker support
- Fix handling of collating symbols in fnmatch (bug 26620)
- pselect.c: Pass a pointer to SYSCALL_CANCEL [BZ #26606]
- y2038: nptl: Convert sem_{clock|timed}wait to support 64 bit time
- hurd: Add __x86_get_cpu_features to ld.abilist
- x86: Install <sys/platform/x86.h> [BZ #26124]
- linux: Add time64 pselect support
- linux: Add time64 semtimedop support
- linux: Add ppoll time64 optimization
- linux: Simplify clock_getres
- Update sparc libm-test-ulps
- Remove internal usage of extensible stat functions
- Linux: Consolidate xmknod
- linux: Consolidate fxstatat{64}
- linux: Consolidate fxstat{64}
- linux: Consolidate lxstat{64}
- linux: Consolidate xstat{64}
- linux: Define STAT64_IS_KERNEL_STAT64
- linux: Always define STAT_IS_KERNEL_STAT
- Update powerpc libm-test-ulps
- benchtests: Add "workload" traces for sinf128
- benchtests: Add "workload" traces for sinf
- benchtests: Add "workload" traces for sin
- benchtests: Add "workload" traces for powf128
- benchtests: Add "workload" traces for pow
- benchtests: Add "workload" traces for expf128
- benchtests: Add "workload" traces for exp
- nptl: futex: Provide correct indentation for part of
  __futex_abstimed_wait_cancelable64

* Tue Sep 08 2020 DJ Delorie <dj@redhat.com> - 2.32.9000-6
- Auto-sync with upstream branch master,
  commit e74b61c09a2a2ab52153e731225ccba5078659b1.
- Disable -Wstringop-overread for some string tests
- string: Fix GCC 11 `-Werror=stringop-overread' error
- C11 threads: Fix inaccuracies in testsuite
- elf.h: Add aarch64 bti/pac dynamic tag constants
- x86: Set CPU usable feature bits conservatively [BZ #26552]

* Wed Sep 02 2020 Patsy Griffin <patsy@redhat.com> - 2.32.9000-5
- Auto-sync with upstream branch master,
  commit 86a912c8634f581ea42ec6973553dde7f058cfbf.
- Update i686 ulps.
- Use LFS readdir in generic POSIX getcwd [BZ# 22899]
- linux: Remove __ASSUME_ATFCTS
- Sync getcwd with gnulib
- x86-64: Fix FMA4 detection in ifunc [BZ #26534]
- y2038: nptl: Convert pthread_cond_{clock|timed}wait to support 64 bit time
- malloc: Fix mallinfo deprecation declaration
- x32: Add <fixup-asm-unistd.h> and regenerate arch-syscall.h
- Add mallinfo2 function that support sizes >= 4GB.
- Remove obsolete default/nss code
- AArch64: Improve backwards memmove performance
- Add RISC-V 32-bit target to build-many-glibcs.py
- Documentation for the RISC-V 32-bit port
- RISC-V: Build infrastructure for 32-bit port
- RISC-V: Add rv32 path to RTLDLIST in ldd
- riscv32: Specify the arch_minimum_kernel as 5.4
- RISC-V: Fix llrint and llround missing exceptions on RV32
- RISC-V: Add the RV32 libm-test-ulps
- RISC-V: Add 32-bit ABI lists
- RISC-V: Add hard float support for 32-bit CPUs
- RISC-V: Support the 32-bit ABI implementation
- RISC-V: Add arch-syscall.h for RV32
- RISC-V: Add path of library directories for the 32-bit
- RISC-V: Support dynamic loader for the 32-bit
- RISC-V: Add support for 32-bit vDSO calls
- RISC-V: Use 64-bit-time syscall numbers with the 32-bit port
- RISC-V: Cleanup some of the sysdep.h code
- RISC-V: Use 64-bit time_t and off_t for RV32 and RV64
- io/lockf: Include bits/types.h before __OFF_T_MATCHES_OFF64_T check
- elf/tst-libc_dlvsym: Add a TEST_COMPAT around some symbol tests
- hurd: define BSD 4.3 ioctls only under __USE_MISC
- string: test strncasecmp and strncpy near page boundaries
- linux: Simplify utimensat
- linux: Simplify timerfd_settime
- linux: Simplify timer_gettime
- linux: Simplify sched_rr_get_interval
- linux: Simplify ppoll
- linux: Simplify mq_timedsend
- linux: Simplify mq_timedreceive
- linux: Simplify clock_settime
- linux: Simplify clock_nanosleep
- linux: Simplify clock_gettime
- linux: Simplify clock_adjtime
- linux: Add helper function to optimize 64-bit time_t fallback support
- S390: Sync HWCAP names with kernel by adding aliases [BZ #25971]
- [vcstocl] Import ProjectQuirks from its own file
- build-many-glibcs.py: Add a s390x -O3 glibc variant.
- Fix namespace violation in stdio.h and sys/stat.h if build with optimization. [BZ #26376]
- Add C2x BOOL_MAX and BOOL_WIDTH to limits.h.
- Use MPC 1.2.0 in build-many-glibcs.py.
- Add new STATX_* constants from Linux 5.8 to bits/statx-generic.h.
- Correct locking and cancellation cleanup in syslog functions (bug 26100)

* Thu Aug 20 2020 Carlos O'Donell <carlos@redhat.com> - 2.32.9000-4
- Support building glibc in a mock chroot using older systemd-nspawn (#1869030).

* Tue Aug 18 2020 Carlos O'Donell <carlos@redhat.com> - 2.32.9000-3
- Suggest installing minimal localization e.g. C, POSIX, C.UTF-8.

* Mon Aug 17 2020 DJ Delorie <dj@redhat.com> - 2.32.9000-2
- Auto-sync with upstream branch master,
  commit cb7e7a5ca1d6d25d59bc038bdc09630e507c41e5.
- nptl: Handle NULL abstime [BZ #26394]
- Update build-many-glibcs.py for binutils ia64 obsoletion.
- Update kernel version to 5.8 in tst-mman-consts.py.
- y2038: nptl: Convert pthread_{clock|timed}join_np to support 64 bit time
- aarch64: update ulps.

* Wed Aug 12 2020 Patsy Griffin <patsy@redhat.com> - 2.32.9000-1
- Auto-sync with upstream branch master,
  commit 0be0845b7a674dbfb996f66cd03d675f0f6028dc:
- S390: Regenerate ULPs.
- manual: Fix sigdescr_np and sigabbrev_np return type (BZ #26343)
- math: Update x86_64 ulps
- math: Regenerate auto-libm-test-out-j0
- manual: Put the istrerrorname_np and strerrordesc_np return type in braces
- Linux: Use faccessat2 to implement faccessat (bug 18683)
- manual: Fix strerrorname_np and strerrordesc_np return type (BZ #26343)
- math: Fix inaccuracy of j0f for x >= 2^127 when sin(x)+cos(x) is tiny
- Update syscall lists for Linux 5.8.
- Use Linux 5.8 in build-many-glibcs.py.
- htl: Enable tst-cancelx?[45]
- tst-cancel4: Make blocking on write more portable
- hurd: Add missing hidden def
- hurd: Rework sbrk
- hurd: Implement basic sched_get/setscheduler
- x86: Rename Intel CPU feature names
- manual: Fix some @code/@var formatting glitches chapter Date And Time
- Copy regex_internal.h from Gnulib
- Copy regex BITSET_WORD_BITS porting from Gnulib
- Sync regex.h from Gnulib
- Sync mktime.c from Gnulib
- Sync intprops.h from Gnulib
- Open master branch for glibc 2.33 development.

* Thu Aug 06 2020 Arjun Shankar <arjun@redhat.com> - 2.32-1
- Auto-sync with upstream branch release/2.32/master,
  commit 3de512be7ea6053255afed6154db9ee31d4e557a:
- Prepare for glibc 2.32 release.
- Regenerate configure scripts.
- Update NEWS with bugs.
- Update translations.
- Don't mix linker error messages into edited scripts
- benchtests/README update.
- RISC-V: Update lp64d libm-test-ulps according to HiFive Unleashed
- aarch64: update NEWS about branch protection
- Add NEWS entry for CVE-2016-10228 (bug 19519)
- powerpc: Fix incorrect cache line size load in memset (bug 26332)
- Update Nios II libm-test-ulps file.

* Fri Jul 31 2020 Patsy Griffin <patsy@redhat.com> - 2.31.9000-24
- Auto-sync with upstream branch master,
  commit 7f1a08cff82255cd4252a2c75fd65b80a6a170bf.
- Move NEWS entry for CVE-2020-1751 to the 2.31 section
- NEWS: Deprecate weak libpthread symbols for single-threaded checks
- NEWS: Deprecate nss_hesiod
- nptl: Zero-extend arguments to SETXID syscalls [BZ #26248]
- Use binutils 2.35 branch in build-many-glibcs.py.
- aarch64: Use future HWCAP2_MTE in ifunc resolver
- Update x86-64 libm-test-ulps
- aarch64: Respect p_flags when protecting code with PROT_BTI
- Disable warnings due to deprecated libselinux symbols used by nss and nscd
- Regenerate INSTALL for ARC port updates.
- Update libc.pot for 2.32 release.
- powerpc: Fix POWER10 selection
- powerpc64le: guarantee a .gnu.attributes section [BZ #26220]

* Wed Jul 29 2020 Florian Weimer <fweimer@redhat.com> - 2.31.9000-23
- Inherit -mbranch-protection=standard from redhat-rpm-config (for aarch64)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Carlos O'Donell <carlos@redhat.com> - 2.31.9000-21
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 21 2020 Arjun Shankar <arjun@redhat.com> - 2.31.9000-20
- Add glibc-deprecated-selinux-makedb.patch and
  glibc-deprecated-selinux-nscd.patch to work around libselinux API
  deprecations.
- Drop glibc-rseq-disable.patch; rseq support removed upstream.  (#1855729)
- Auto-sync with upstream branch master,
  commit ec2f1fddf29053957d061dfe310f106388472a4f:
- libio: Remove __libc_readline_unlocked
- shadow: Implement fgetspent_r using __nss_fgetent_r
- pwd: Implement fgetpwent_r using __nss_fgetent_r
- gshadow: Implement fgetsgent_r using __nss_fgetent_r (bug 20338)
- grp: Implement fgetgrent_r using __nss_fgetent_r
- nss: Add __nss_fgetent_r
- libio: Add fseterr_unlocked for internal use
- nss_files: Use generic result pointer in parse_line
- nss_files: Consolidate line parse declarations in <nss_files.h>
- nss_compat: Do not use mmap to read database files (bug 26258)
- nss_files: Consolidate file opening in __nss_files_fopen
- Update powerpc-nofpu libm-test-ulps.
- Use MPFR 4.1.0 in build-many-glibcs.py.
- elf: Change TLS static surplus default back to 1664
- hurd: Fix longjmp check for sigstate
- hurd: Fix longjmp early in initialization
- manual: New signal and errno string functions are AS-safe
- AArch64: Improve strlen_asimd performance (bug 25824)
- Move <rpc/netdb.h> from sunrpc to inet
- en_US: Minimize changes to date_fmt (Bug 25923)
- Linux: Remove rseq support
- manual: Use Unicode instead HTML entities for characters (bug 19737)
- Add NEWS entry for CVE-2020-6096 (bug 25620)
- arm: remove string/tst-memmove-overflow XFAIL
- AArch64: Rename IS_ARES to IS_NEOVERSE_N1
- AArch64: Add optimized Q-register memcpy
- AArch64: Align ENTRY to a cacheline
- Correct timespec implementation [BZ #26232]
- Remove --enable-obsolete-rpc configure flag
- hurd: Fix build-many-glibcs.py
- x86: Support usable check for all CPU features
- string: Make tst-strerror/tst-strsignal unsupported if msgfmt is not installed
- malloc: Deprecate more hook-related functionality
- elf: Support at least 32-byte alignment in static dlopen
- x86: Remove __ASSEMBLER__ check in init-arch.h
- x86: Remove the unused __x86_prefetchw
- Documentation for ARC port
- build-many-glibcs.py: Enable ARC builds
- ARC: Build Infrastructure
- ARC: ABI lists
- ARC: Linux Startup and Dynamic Loading
- ARC: Linux ABI
- ARC: Linux Syscall Interface
- ARC: hardware floating point support
- ARC: math soft float support
- ARC: Atomics and Locking primitives
- ARC: Thread Local Storage support
- ARC: startup and dynamic linking code
- ARC: ABI Implementation
- Fix time/tst-cpuclock1 intermitent failures
- powerpc64: Fix calls when r2 is not used [BZ #26173]
- Add NEWS entry for Update to Unicode 13.0.0 [BZ #25819]
- Update i686 libm-test-ulps
- Fix memory leak in __printf_fp_l (bug 26215).
- Fix double free in __printf_fp_l (bug 26214).
- linux: Fix syscall list generation instructions
- sysv: linux: Add 64-bit time_t variant for shmctl
- sysvipc: Remove the linux shm-pad.h file
- sysvipc: Split out linux struct shmid_ds
- sysv: linux: Add 64-bit time_t variant for msgctl
- sysvipc: Remove the linux msq-pad.h file
- sysvipc: Split out linux struct semid_ds
- sysv: linux: Add 64-bit time_t variant for semctl

* Fri Jul 10 2020 Florian Weimer <fweimer@redhat.com> - 2.31.9000-19
- Disable rseq registration by default to help Firefox (#1855729)

* Thu Jul 09 2020 Florian Weimer <fweimer@redhat.com> - 2.31.9000-18
- Auto-sync with upstream branch master,
  commit ffb17e7ba3a5ba9632cee97330b325072fbe41dd:
- rtld: Avoid using up static TLS surplus for optimizations [BZ #25051]
- rtld: Account static TLS surplus for audit modules
- rtld: Add rtld.nns tunable for the number of supported namespaces
- Remove --enable-obsolete-nsl configure flag
- Move non-deprecated RPC-related functions from sunrpc to inet
- aarch64: add NEWS entry about branch protection support
- aarch64: redefine RETURN_ADDRESS to strip PAC
- aarch64: fix pac-ret support in _mcount
- aarch64: Add pac-ret support to assembly files
- aarch64: configure check for pac-ret code generation
- aarch64: ensure objects are BTI compatible
- aarch64: enable BTI at runtime
- aarch64: fix RTLD_START for BTI
- aarch64: fix swapcontext for BTI
- aarch64: Add BTI support to assembly files
- aarch64: Rename place holder .S files to .c
- aarch64: configure test for BTI support
- Rewrite abi-note.S in C.
- rtld: Clean up PT_NOTE and add PT_GNU_PROPERTY handling
- string: Move tst-strsignal tst-strerror to tests-container
- string: Fix prototype mismatch in sigabbrev_np, __sigdescr_np
- arm: CVE-2020-6096: Fix multiarch memcpy for negative length (#1820332)
- arm: CVE-2020-6096: fix memcpy and memmove for negative length (#1820332)
- sunrpc: Remove hidden aliases for global data symbols (bug 26210)
- hurd: Fix strerror not setting errno
- tst-strsignal: fix checking for RT signals support
- hurd: Evaluate fd before entering the critical section
- CVE-2016-10228: Rewrite iconv option parsing (#1428292)
- nss: Remove cryptographic key support from nss_files, nss_nis, nss_nisplus
- sunrpc: Do not export getrpcport by default
- sunrpc: Do not export key handling hooks by default
- sunrpc: Turn clnt_sperrno into a libc_hidden_nolink_sunrpc symbol
- string: Add strerrorname_np and strerrordesc_np
- string: Add sigabbrev_np and sigdescr_np
- string: Add strerror_l on test-strerror-errno
- string: Add strerror, strerror_r, and strerror_l test
- string: Add strsignal test
- string: Simplify strerror_r
- string: Use tls-internal on strerror_l
- string: Implement strerror in terms of strerror_l
- string: Remove old TLS usage on strsignal
- linux: Fix __NSIG_WORDS and add __NSIG_BYTES
- signal: Move sys_errlist to a compat symbol
- signal: Move sys_siglist to a compat symbol
- signal: Add signum-{generic,arch}.h
- Remove most vfprintf width/precision-dependent allocations (bug 14231, bug 26211).
- elf: Do not signal LA_ACT_CONSISTENT for an empty namespace [BZ #26076]
- Fix stringop-overflow errors from gcc 10 in iconv.
- x86: Add thresholds for "rep movsb/stosb" to tunables
- Use C2x return value from getpayload of non-NaN (bug 26073).
- x86: Detect Extended Feature Disable (XFD)
- x86: Correct bit_cpu_CLFSH [BZ #26208]
- manual: Document __libc_single_threaded
- Add the __libc_single_threaded variable
- Linux: rseq registration tests
- Linux: Use rseq in sched_getcpu if available
- Linux: Perform rseq registration at C startup and thread creation
- tst-cancel4: deal with ENOSYS errors
- manual: Show copyright information not just in the printed manual


* Thu Jul 02 2020 Carlos O'Donell <carlos@redhat.com> - 2.31.9000-17
- Auto-sync with upstream branch master,
  commit c6aac3bf3663709cdefde5f5d5e9e875d607be5e.
- Fix typo in comment in bug 26137 fix.
- Fix strtod multiple-precision division bug (bug 26137).
- Linux: Fix UTC offset setting in settimeofday for __TIMESIZE != 64
- random: range is not portably RAND_MAX [BZ #7003]
- Update kernel version to 5.7 in tst-mman-consts.py.
- powerpc: Add support for POWER10
- hurd: Simplify usleep timeout computation
- htl: Enable cancel*16 an cancel*20 tests
- hurd: Add remaining cancelation points
- hurd: fix usleep(ULONG_MAX)
- hurd: Make fcntl(F_SETLKW*) cancellation points
- hurd: make wait4 a cancellation point
- hurd: Fix port definition in HURD_PORT_USE_CANCEL
- hurd: make close a cancellation point
- hurd: make open and openat cancellation points
- hurd: clean fd and port on thread cancel
- htl: Move cleanup handling to non-private libc-lock
- htl: Fix includes for lockfile
- htl: avoid cancelling threads inside critical sections
- tst-cancel4-common.c: fix calling socketpair
- x86: Detect Intel Advanced Matrix Extensions
- Set width of JUNGSEONG/JONGSEONG characters from UD7B0 to UD7FB to 0 [BZ #26120]
- S390: Optimize __memset_z196.
- S390: Optimize __memcpy_z196.
- elf: Include <stddef.h> (for size_t), <sys/stat.h> in <ldconfig.h>
- nptl: Don't madvise user provided stack
- S390: Regenerate ULPs.
- htl: Add wrapper header for <semaphore.h> with hidden __sem_post
- elf: Include <stdbool.h> in <dl-tunables.h> because bool is used
- htl: Fix case when sem_*wait is canceled while holding a token
- htl: Make sem_*wait cancellations points
- htl: Simplify non-cancel path of __pthread_cond_timedwait_internal
- htl: Enable tst-cancel25 test
- powerpc: Add new hwcap values
- aarch64: MTE compatible strncmp
- aarch64: MTE compatible strcmp
- aarch64: MTE compatible strrchr
- aarch64: MTE compatible memrchr
- aarch64: MTE compatible memchr
- aarch64: MTE compatible strcpy
- Add MREMAP_DONTUNMAP from Linux 5.7
- x86: Update CPU feature detection [BZ #26149]

* Mon Jun 22 2020 DJ Delorie <dj@redhat.com> - 2.31.9000-16
- Auto-sync with upstream branch master,
  commit ea04f0213135b13d80f568ca2c4127c2ec112537.
- aarch64: Remove fpu Makefile
- m68k: Use sqrt{f} builtin for coldfire
- arm: Use sqrt{f} builtin
- riscv: Use sqrt{f} builtin
- s390: Use sqrt{f} builtin
- sparc: Use sqrt{f} builtin
- mips: Use sqrt{f} builtin
- alpha: Use builtin sqrt{f}
- i386: Use builtin sqrtl
- x86_64: Use builtin sqrt{f,l}
- powerpc: Use sqrt{f} builtin
- s390x: Use fma{f} builtin
- aarch64: Use math-use-builtins for ceil{f}
- math: Decompose math-use-builtins.h
- hurd: Add mremap
- ia64: Use generic exp10f
- New exp10f version without SVID compat wrapper
- i386: Use generic exp10f
- math: Optimized generic exp10f with wrappers
- benchtests: Add exp10f benchmark

* Fri Jun 19 2020 Patsy Franklin <patsy@redhat.com> - 2.31.9000-15
- Auto-sync with upstream branch master,
  commit 27f8864bd41f0f1b61e8e947d9a030b1a0d23df9.
- x86: Update F16C detection [BZ #26133]
- Fix avx2 strncmp offset compare condition check [BZ #25933]
- nptl: Remove now-spurious tst-cancelx9 references
- x86_64: Use %xmmN with vpxor to clear a vector register
- x86: Correct bit_cpu_CLFLUSHOPT [BZ #26128]
- powerpc64le: refactor e_sqrtf128.c
- Update syscall-names.list for Linux 5.7.
- ieee754/dbl-64: Reduce the scope of temporary storage variables
- manual: Add pthread_attr_setsigmask_np, pthread_attr_getsigmask_np
- ld.so: Check for new cache format first and enhance corruption check
- hurd: Fix __writev_nocancel_nostatus
- hurd: Make send* cancellation points
- htl: Enable more cancellation tests
- hurd: Make write and pwrite64 cancellation points
- htl: Fix cleanup support for IO locking
- htl: Move cleanup stack to variable shared between libc and pthread
- htl: initialize first and prevent from unloading
- htl: Add noreturn attribute on __pthread_exit forward
- hurd: Make recv* cancellation points
- powerpc: Automatic CPU detection in preconfigure
- Use Linux 5.7 in build-many-glibcs.py.
- htl: Enable more cancel tests
- htl: Fix linking static tests by factorizing the symbols list
- Add "%d" support to _dl_debug_vdprintf
- aarch64: MTE compatible strlen
- aarch64: MTE compatible strchr
- aarch64: MTE compatible strchrnul
- AArch64: Merge Falkor memcpy and memmove implementations
- hurd: document that gcc&gdb look at the trampoline code
- pthread: Move back linking rules to nptl and htl
- htl: Enable more tests
- htl: Fix registration of atfork handlers in modules
- htl: Fix tls initialization for already-created threads
- hurd: Make read and pread64 cancellable
- hurd: Fix unwinding over interruptible RPC
- htl: Enable but XFAIL tst-flock2, tst-signal1, tst-signal2
- hurd: XFAIL more tests that require setpshared support
- hurd: Briefly document in xfails the topics of the bugzilla entries
- htl: Enable more tests
- htl: Add sem_clockwait support
- htl: fix register-atfork ordering
- hurd: Fix hang in _hurd_raise_signal from pthread_kill
- hurd: Reject raising invalid signals
- hurd: fix clearing SS_ONSTACK when longjmp-ing from sighandler
- hurd: Add pointer guard support
- hurd: Add stack guard support
- dl-runtime: reloc_{offset,index} now functions arch overide'able
- powerpc64le: add optimized strlen for P9
- powerpc64le: use common fmaf128 implementation

* Fri Jun 05 2020 Patsy Griffin <patsy@redhat.com> - 2.31.9000-14
- Auto-sync with upstream branch master,
  commit e52434a2e4d1105272daaef87678da950fbec73f.
- benchtests: Restore the clock_gettime option
- Update HP_TIMING_NOW for _ISOMAC in sysdeps/generic/hp-timing.h
- Replace val with __val in TUNABLE_SET_VAL_IF_VALID_RANGE
- support: Fix detecting hole support on >2KB-block filesystems
- powerpc: Fix powerpc64le due a7a3435c9a
- manual/jobs.texi: remove unused var from example code
- powerpc/fpu: use generic fma functions
- aarch/fpu: use generic builtins based math functions
- ieee754: provide gcc builtins based generic fma functions
- ieee754: provide gcc builtins based generic sqrt functions
- Linux: Use __pthread_attr_setsigmask_internal for timer helper thread
- nptl: Add pthread_attr_setsigmask_np, pthread_attr_getsigmask_np
- nptl: Make pthread_attr_t dynamically extensible
- nptl: Destroy the default thread attribute as part of freeres
- nptl: Change type of __default_pthread_attr
- nptl: Use __pthread_attr_setaffinity_np in pthread_getattr_np
- nptl: Use __pthread_getattr_default_np in pthread_create
- nptl: Add internal alias __pthread_getattr_default_np
- htl: Fix gsync_wait symbol exposition
- htl: Make pthread_cond_destroy wait for threads to be woken
- htl: Enable more cond tests
- tst-cond11: Fix build with _SC_MONOTONIC_CLOCK > 0
- mbstowcs: Document, test, and fix null pointer dst semantics (Bug 25219)
- build: Use FAIL_EXIT1 () on failure to exec child [BZ #23990]
- manual: Fix backtraces code example [BZ #10441]
- hurd: Fix fexecve
- i386: Remove unused file sysdeps/unix/i386/sysdep.S
- hurd: fix ptsname error when called on a non-tty
- hurd: Fix fdopendir checking for directory type
- i386: Remove NO_TLS_DIRECT_SEG_REFS handling
- Hurd: Move <hurd/sigpreempt.h> internals into wrapper header
- Hurd: Use __sigmask in favor of deprecated sigmask
- hurd: Fix pselect atomicity
- elf: Remove extra hwcap mechanism from ldconfig
- elf: Do not read hwcaps from the vDSO in ld.so
- linux: Use internal DIR locks when accessing filepos on telldir
- Update i386 libm-test-ulps
- htl: Add clock variants
- signal: Deprecate additional legacy signal handling functions
- elf: Turn _dl_printf, _dl_error_printf, _dl_fatal_printf into functions
- x86: Update Intel Atom processor family optimization
- elf.h: add aarch64 property definitions
- elf.h: Add PT_GNU_PROPERTY
- <libc-symbols.h>: Add libpthread hidden alias support
- nptl: Use __pthread_attr_copy in pthread_setattr_default_np
- nptl: Use __pthread_attr_copy in pthread_getattr_default_np (bug 25999)
- nptl: Add __pthread_attr_copy for copying pthread_attr_t objects
- nptl: Make __pthread_attr_init, __pthread_attr_destroy available internally
- nptl: Move pthread_gettattr_np into libc
- nptl: Move pthread_getaffinity_np into libc
- nptl: Move pthread_attr_setaffinity_np into libc
- nptl: Replace some stubs with the Linux implementation
- Linux: Add missing handling of tai field to __ntp_gettime64
- Mention GCC 10 attribute access.
- y2038: Replace __clock_gettime with __clock_gettime64
- manual: Add missing section and node for clockid_t wait functions
- y2038: linux: Provide __ntp_gettimex64 implementation
- y2038: linux: Provide __ntp_gettime64 implementation
- y2038: Provide conversion helpers for struct __ntptimeval64
- y2038: Introduce struct __ntptimeval64 - new internal glibc type
- y2038: linux: Provide __adjtime64 implementation
- y2038: linux: Provide ___adjtimex64 implementation
- y2038: linux: Provide __clock_adjtime64 implementation
- ldconfig: Default to the new format for ld.so.cache
- nss_compat: internal_end*ent may clobber errno, hiding ERANGE [BZ #25976]
- powerpc: Optimized rawmemchr for POWER9
- x86: Add --enable-cet=permissive
- Remove NO_CTORS_DTORS_SECTIONS macro
- elf: Assert that objects are relocated before their constructors run
- powerpc: Optimized stpcpy for POWER9
- powerpc: Optimized strcpy for POWER9
- x86: Move CET control to _dl_x86_feature_control [BZ #25887]
- sunrpc/tst-udp-*: Fix timeout value
- Linux: Remove remnants of the getcpu cache
- Update timezone code from tzcode 2020a
- aarch64: fix strcpy and strnlen for big-endian [BZ #25824]
- locale: Add transliteration for Geresh, Gershayim (U+05F3, U+05F4)
- string: Fix string/tst-memmove-overflow to compile with GCC 7
- Add arch-syscall.h dependency for generating sysd-syscalls file
- arm: XFAIL string/tst-memmove-overflow due to bug 25620
- elf: Remove redundant add_to_global_resize_failure  call from dl_open_args
- string: Add string/tst-memmove-overflow, a test case for bug 25620
- support: Add support_blob_repeat_allocate_shared
- nptl: wait for pending setxid request also in detached thread (bug 25942)
- aarch64: Accept PLT calls to __getauxval within libc.so
- Use unsigned constants for ICMP6 filters [BZ #22489]
- Linux: Enhance glibcsyscalls.py to support listing system calls

* Mon May 11 2020 DJ Delorie <dj@redhat.com> - 2.31.9000-13
- Auto-sync with upstream branch master,
  commit 978e8ac39f8ba2d694031e521511da1ae803ccfc.
- Suppress GCC 10 true positive warnings [BZ #25967]
- POWER: Add context-synchronizing instructions to pkey_write [BZ #25954]
- hurd: Add missing sigstate members initialization
- x86-64: Use RDX_LP on __x86_shared_non_temporal_threshold [BZ #25966]
- linux: Remove assembly umount2 implementation
- signal: Use <sigsetops.h> for sigemptyset, sigfillset
- ckb_IQ, or_IN locales: Add missing reorder-end keywords
- semaphore: consolidate arch headers into a generic one
- Use GCC 10 branch in build-many-glibcs.py.
- Document the internal _ and N_ macros
- y2038: Provide conversion helpers for struct __timex64
- y2038: Introduce struct __timex64 - new internal glibc type
- y2038: include: Move struct __timeval64 definition to a separate file
- y2038: nscd: Modify nscd_helper to use __clock_gettime64
- y2038: inet: Convert inet deadline to support 64 bit time
- y2038: hurd: Provide __clock_gettime64 function
- y2038: Export __clock_gettime64 to be usable in other libraries
- manual: Document the O_NOFOLLOW open flag
- powerpc64le/power9: guard power9 strcmp against rtld usage [BZ# 25905]
- float128: use builtin_signbitf128 always
- improve out-of-bounds checking with GCC 10 attribute access [BZ #25219]
- nios2: delete sysdeps/unix/sysv/linux/nios2/kernel-features.h
- powerpc: Rename argN to _argN in LOADARGS_N [BZ #25902]
- locale/tst-localedef-path-norm: Don't create $(complocaledir)
- support: Set errno before testing it.
- localedef: Add tests-container test for --no-hard-links.
- test-container: Support $(complocaledir) and mkdirp.
- i386: Remove unused variable in sysdeps/x86/cacheinfo.c
- Add a C wrapper for prctl [BZ #25896]
- powerpc64le: Enable support for IEEE long double
- powerpc64le: blacklist broken GCC compilers (e.g GCC 7.5.0)
- powerpc64le: bump binutils version requirement to >= 2.26
- powerpc64le: raise GCC requirement to 7.4 for long double transition
- Rename __LONG_DOUBLE_USES_FLOAT128 to __LDOUBLE_REDIRECTS_TO_FLOAT128_ABI
- ldbl-128ibm-compat: workaround GCC 9 C++ PR90731
- x86: Add the test case of __get_cpu_features support for Zhaoxin processors
- x86: Add cache information support for Zhaoxin processors
- x86: Add CPU Vendor ID detection support for Zhaoxin processors
- Update translations
- Add C wrappers for process_vm_readv/process_vm_writev [BZ #25810]
- generic/typesizes.h: Add support for 32-bit arches with 64-bit types
- semctl: Remove the sem-pad.h file
- bits/sem.h: Split out struct semid_ds
- Mark unsigned long arguments with U in more syscalls [BZ #25810]
- elf: Add initial flag argument to __libc_early_init
- Add SYSCALL_ULONG_ARG_[12] to pass long to syscall [BZ #25810]
- Makeconfig: Use $(error ...) to output error message
- manual: Fix typos in the fexecve description
- misc: Remove sstk from the autogenerated system call list
- Remove unused floating-point configuration from gmp-impl.h.
- support: Implement <support/xthread.h> key create/delete
- nptl/tst-setuid1-static: Improve isolation from system objects
- Increase the timeout of locale/tst-localedef-path-norm
- Use 2020 as copyright year.
- misc: Turn sstk into a compat symbol
- manual: Document the fexecve function
- nptl: Start new threads with all signals blocked [BZ #25098]
- localedef: Add verbose messages for failure paths.
- Remove most gmp-mparam.h headers.
- elf: Implement __libc_early_init
- elf: Introduce <elf_machine_sym_no_match.h>
- Add a syscall test for [BZ #25810]
- elf: Support lld-style link map for librtld.map
- signal: Only handle on NSIG signals on signal functions (BZ #25657)
- linux: Use pthread_sigmask on sigprocmask
- ia64: Remove sigprocmask/sigblock objects from libpthread
- nptl: Move pthread_sigmask implementation to libc
- Bug 25819: Update to Unicode 13.0.0

* Wed Apr 29 2020 Florian Weimer <fweimer@redhat.com> - 2.31.9000-12
- nss_db.x86_64 should install nss_db.i686 if glibc.i686 is installed (#1807821)
- Likewise for nss_hesiod.

* Mon Apr 27 2020 Florian Weimer <fweimer@redhat.com> - 2.31.9000-11
- Introduce glibc-headers-x86, glibc-headers-s390 packages (#1828332)
- Remove the glibc-headers package

* Mon Apr 20 2020 DJ Delorie <dj@redhat.com> - 2.31.9000-10
- Auto-sync with upstream branch master,
  commit 0798b8ecc8da8667362496c1217d18635106c609.
- ARC: Update syscall-names.list for ARC specific syscalls
- Revert "x86_64: Add SSE sfp-exceptions"
- provide y2038 safe socket constants for default/asm-generic ABI
- x86_64: Add SSE sfp-exceptions
- Remove __NO_MATH_INLINES
- i686: Add INTERNAL_SYSCALL_NCS 6 argument support
- Reset converter state after second wchar_t output (Bug 25734)
- Fix typo in posix/tst-fnmatch.input (Bug 25790)

* Wed Apr 15 2020 Patsy Griffin <patsy@redhat.com> - 2.31.9000-9
- Auto-sync with upstream branch master,
  commit 076f09afbac1aa57756faa7a8feadb7936a724e4.
- Linux: Remove <sys/sysctl.h> and the sysctl function
- posix: Add wait4 test case
- linux: wait4: Fix incorrect return value comparison
- hurd: add mach_print function
- x32: Properly pass long to syscall [BZ #25810]
- Add GRND_INSECURE from Linux 5.6 to sys/random.h
- Update kernel version to 5.6 in tst-mman-consts.py.

* Wed Apr 15 2020 Florian Weimer <fweimer@redhat.com> - 2.31.9000-8
- nsswitch.conf: don't add sss to shadow line

* Wed Apr 08 2020 Carlos O'Donell <carlos@redhat.com> - 2.31.9000-7
- Auto-sync with upstream branch master,
  commit b1caa144c74678097cada5a54eda2996bb459d8f.
- Update mips libm-test-ulps
- Update alpha libm-test-ulps
- Update ia64 libm-test-ulps
- Update sparc libm-test-ulps
- Update arm libm-test-ulps
- Update aarch64 libm-test-ulps
- Updates to the shn_MM locale [BZ #25532]
- powerpc: Update ULPs and xfail more ibm128 outputs
- i386: Remove build support for GCC older than GCC 6
- oc_FR locale: Fix spelling of April (bug 25639)
- Update hppa libm-test-ulps
- y2038: linux: Provide __mq_timedreceive_time64 implementation
- y2038: linux: Provide __mq_timedsend_time64 implementation
- y2038: include: Move struct __timespec64 definition to a separate file
- malloc: ensure set_max_fast never stores zero [BZ #25733]
- powerpc64le: enforce non-specific long double in .gnu.attributes section
- powerpc64le: workaround ieee long double / _Float128 stdc++ bug
- powerpc64le: Enforce -mabi=ibmlongdouble when -mfloat128 used
- powerpc64le/multiarch: don't generate strong aliases for fmaf128-ppc64
- ldbl-128ibm: simplify iscanonical.h
- i386: Disable check_consistency for GCC 5 and above [BZ #25788]
- Add IPPROTO_ETHERNET and IPPROTO_MPTCP from Linux 5.6 to netinet/in.h.
- Update syscall lists for Linux 5.6.
- elf: Implement DT_AUDIT, DT_DEPAUDIT support [BZ #24943]
- elf: Simplify handling of lists of audit strings
- support: Change xgetline to return 0 on EOF
- nptl: Remove x86_64 cancellation assembly implementations [BZ #25765]
- aarch64: update bits/hwcap.h
- Add tests for Safe-Linking
- S390: Regenerate ULPs.
- sysv/alpha: Use generic __timeval32 and helpers
- linux: Use long time_t for wait4/getrusage
- resource: Add a __rusage64 struct
- linux: Use long time_t __getitimer/__setitimer
- sysv: Define __KERNEL_OLD_TIMEVAL_MATCHES_TIMEVAL64
- math: Add inputs that yield larger errors for float type (x86_64)

* Tue Mar 31 2020 DJ Delorie <dj@redhat.com> - 2.31.9000-6
- Auto-sync with upstream branch master,
  commit 49c3c37651e2d2ec4ff8ce21252bbbc08a9d6639.
- Fix alignment bug in Safe-Linking
- Typo fixes and CR cleanup in Safe-Linking
- Use Linux 5.6 and GMP 6.2.0 in build-many-glibcs.py.
- Add new file missed in previous hppa commit.
- powerpc: Add support for fmaf128() in hardware
- Fix data race in setting function descriptors during lazy binding on hppa.
- sparc: Move __fenv_{ld,st}fsr to fenv-private.h
- x86: Remove feraiseexcept optimization
- math: Remove fenvinline.h
- hurd: Make O_TRUNC update mtime/ctime
- Add Safe-Linking to fastbins and tcache
- Add benchtests for roundeven and roundevenf.
- time: Add a __itimerval64 struct
- time: Add a timeval with a 32-bit tv_sec and tv_usec
- sysv/linux: Rename alpha functions to be alpha specific
- ARC: add definitions to elf/elf.h
- powerpc64: apply -mabi=ibmlongdouble to special files
- powerpc64le: add -mno-gnu-attribute to *f128 objects and difftime
- Makeconfig: sandwich gnulib-tests between libc/ld linking of tests
- powerpc64le: Ensure correct ldouble compiler flags are used
- Fix tests which expose ldbl -> _Float128 redirects
- ldbl-128ibm-compat: PLT redirects for using ldbl redirects internally

* Wed Mar 25 2020 Patsy Franklin <patsy@redhat.com> - 2.31.9000-5
- Auto-sync with upstream branch master,
  commit 4eda036f5b897fa8bc20ddd2099b5a6ed4239dc9.
- stdlib: Move tst-system to tests-container
- support/shell-container.c: Add builtin kill
- support/shell-container.c: Add builtin exit
- support/shell-container.c: Return 127 if execve fails
- Add NEWS entry for CVE-2020-1751 (bug 25423)
- posix: Fix system error return value [BZ #25715]
- y2038: fix: Add missing libc_hidden_def attribute for some syscall wrappers
- Extended Char Intro: Use getwc in example (Bug 25626)
- stdio: Add tests for printf multibyte convertion leak [BZ#25691]
- stdio: Remove memory leak from multibyte convertion [BZ#25691]
- Add NEWS entry for CVE-2020-1752 (bug 25414)
- math: Remove inline math tests
- Remove __LIBC_INTERNAL_MATH_INLINES
- math: Remove mathinline
- m68k: Remove mathinline.h
- oc_FR locale: Fix spelling of Thursday (bug 25639)
- x86: Remove ARCH_CET_LEGACY_BITMAP [BZ #25397]
- Fix build with GCC 10 when long double = double.
- nscd/cachedumper.c : fix whitespace
- Fix nscd/cachedumper.c compile errors
- manual: Fix inconsistent declaration of wcsrchr [BZ #24655]
- nscd: add cache dumper

* Fri Mar 13 2020 Patsy Franklin <patsy@redhat.com> - 2.31.9000-4
- Auto-sync with upstream branch master,
  commit 2de7fe62534b7a6461c633114f03e9dff394f5f7.
- parse_tunables: Fix typo in comment
- ldconfig: trace origin paths with -v
- test-container: print errno when execvp fails
- [AArch64] Improve integer memcpy
- Add NEWS entry for CVE-2020-10029 (bug 25487)
- gcc PR 89877: miscompilation due to missing cc clobber in longlong.h macros
- mips: Fix wrong INTERNAL_SYSCALL_ERROR_P check from bc2eb9321e
- elf: Fix wrong indentation from commit eb447b7b4b
- y2038: linux: Provide __futimesat64 implementation
- y2038: linux: Provide __lutimes64 implementation
- y2038: linux: Provide __futimes64 implementation
- y2038: fix: Add missing libc_hidden_def for __futimens64
- sparc: Move sigreturn stub to assembly 
- ldbl-128ibm: Let long double files have specific compiler flags
- ldbl-128ibm-compat: Add tests for IBM long double functions
- powerpc: Fix feraiseexcept and feclearexcept macros
- arm: Fix softp-fp Implies (BZ #25635)
- Remove reference of --without-fp on configure
- linux/sysipc: Include linux/posix_types.h for __kernel_mode_t
- Improve IFUNC check [BZ #25506]
- linux: Clear mode_t padding bits (BZ#25623)
- linux: Remove aarch64 ipc_priv.h
- Linux: Use __fstatat64 in fchmodat implementation
- Linux: Use AT_FDCWD in utime, utimes when calling utimensat
- S390: Remove backchain-based fallback and use generic backtrace.c.
- manual: Fix wrong declaration of wcschr [BZ #24654]
- manual: Fix typo in parse_printf_format example [BZ #24638]

* Thu Mar  5 2020 Florian Weimer <fweimer@redhat.com> - 2.31.9000-3
- Emergency patch for broken utimes/utime functions

* Tue Mar 03 2020 Patsy Franklin <patsy@redhat.com> - 2.31.9000-2
- Auto-sync with upstream branch master,
  commit 78c9d0c6efabe2067ef7f93cd36325f54c60adc2.
- Update translations
- Convert Python scripts to Python 3
- alpha: Do not build with -fpic
- y2038: linux: Provide __utime64 implementation
- y2038: linux: Provide __utimes64 implementation
- y2038: Introduce struct __utimbuf64 - new internal glibc type
- microblaze: vfork is always available
- m68k: getpagesize syscall number is always available
- Linux: epoll_pwait syscall number is always available
- x86_64: Do not define __NR_semtimedop in <sysdep.h>
- ia64: Do not define __NR_semtimedop in <sysdep.h>
- Linux: open_by_handle_at syscall number is always available
- Linux: set_robust_list syscall number is always available
- Linux: pciconfig_iobase syscall number is always available on alpha
- Linux: getdents64 syscall number is always available on MIPS
- Linux: Clean up preadv2, pwritev2 system call names
- Linux: exit_group syscall number is always available
- Linux: set_tid_address syscall number is always available
- Linux: pkey_mprotect syscall number is always available
- Linux: rt_sigqueueinfo syscall number is always available
- Linux: getrandom syscall number is always available
- Linux: Clean up preadv, pwritev system call names
- Linux: Clean up pread64/pwrite64 system call names
- Linux: sigaltstack syscall number is always available
- Linux: sched_getaffinity syscall number is always available
- Linux: sched_setaffinity syscall number is always available
- Linux: statx syscall number is always available
- Linux: mq_* syscall numbers are always available
- Linux: mlock2 syscall number is always available
- Linux: copy_file_range syscall number is always available
- Linux: renameat2 syscall number is always available
- build-many-glibcs.py: Add list-compilers, list-glibcs commands
- build-many-glibcs.py: Add --shallow option
- Fixed typo in run_command_array() in support/shell-container.c
- Add missing libc_hidden_def for __utimensat64
- elf: Add elf/check-wx-segment, a test for the presence of WX segments
- i386: Use comdat instead of .gnu.linkonce for i386 setup pic register (BZ #20543)
- ldbl-128ibm-compat: link tst-ldbl-efgcvt against loader too
- ldbl-128ibm-compat: enforce ibm128 on compat tests
- ldbl-128ibm-compat: Provide nexttoward functions
- ldbl-128ibm-compat: Provide a significand implementation
- ldbl-128ibm-compat: Redirect complex math functions
- ldbl-128ibm-compat: Redirect long double functions to f128/ieee128 functions
- posix: Remove posix waitid
- posix: Refactor tst-waitid (BZ #14666)
- support: Add support_process_state_wait
- malloc/tst-mallocfork2: Kill lingering process for unexpected failures

* Wed Feb 26 2020 Patsy Franklin <patsy@redhat.com> - 2.31.9000-1
- Auto-sync with upstream branch master,
  commit 758599bc9dcc5764e862bd9e1613c5d1e6efc5d3.
- elf: Apply attribute_relro to pointers in elf/dl-minimal.c
- powerpc: Refactor fenvinline.h
- nss_nis: Use NSS_DECLARE_MODULE_FUNCTIONS
- csu: Use ELF constructor instead of _init in libc.so
- ldbl-128ibm: make ieee754.h work with IEEE 128 long double
- ldbl-128ibm-compat: fixup subdir location of several funcs
- ldbl-128ibm-compat: enforce correct abi flags on internal file
- ldbl-128ibm-compat: Provide ieee128 symbols to narrow functions
- Undefine redirections after long double definition on __LDBL_COMPAT [BZ #23294]
- nios2: Fix Linux kABI for syscall return
- Fix use-after-free in glob when expanding ~user (bug 25414)
- nptl: Move pthread_setschedparam implementation into libc
- nptl: Move pthread_getschedparam implementation into libc
- Add hidden prototypes for __sched_getparam, __sched_getscheduler
- nptl: Move pthread_cond_init implementation into libc
- nptl: Move pthread_cond_destroy implementation into libc
- nptl: Move pthread_condattr_init implementation into libc
- nptl: Move pthread_condattr_destroy implementation into libc
- nptl: Move pthread_attr_setscope implementation into libc
- nptl: Move pthread_attr_getscope implementation into libc
- nptl: Move pthread_attr_setschedpolicy implementation into libc
- nptl: Move pthread_attr_getschedpolicy implementation into libc
- nptl: Sort routines list in Makefile alphabetically
- nptl: Use .NOTPARALLEL in Makefile only if actually running tests
- Block all signals on timer_create thread (BZ#10815)
- Fix tst-pkey expectations on pkey_get [BZ #23202]
- y2038: linux: Provide __gettimeofday64 implementation
- Linux: Work around kernel bugs in chmod on /proc/self/fd paths [BZ #14578]
- Introduce <elf-initfini.h> and ELF_INITFINI for all architectures
- mips: Fix bracktrace result for signal frames
- Move implementation of <file_change_detection.h> into a C file
- <fd_to_filename.h>: Add type safety and port to Hurd
- Prepare redirections for IEEE long double on powerpc64le
- conform/conformtest.py: Extend tokenizer to cover character constants
- stdlib: Reduce namespace pollution in <inttypes.h>
- x86: Avoid single-argument _Static_assert in <tls.h>
- x86 tls: Use _Static_assert for TLS access size assertion
- htl: Link internal htl tests against libpthread
- pthread: Fix building tst-robust8 with nptl
- pthread: Move robust mutex tests from nptl to sysdeps/pthread
- htl: Remove stub warning for pthread_mutexattr_setpshared
- htl: Add missing functions and defines for robust mutexes
- htl: Only check pthread_self coherency when DEBUG is set
- hurd: Add THREAD_GET/SETMEM/_NC
- hurd tls: update comment about fields at the end of tcbhead
- ld.so: Do not export free/calloc/malloc/realloc functions [BZ #25486]
- Remove weak declaration of free from <inline-hashtab.h>
- elf: Extract _dl_sym_post, _dl_sym_find_caller_map from elf/dl-sym.c
- elf: Introduce the rtld-stubbed-symbols makefile variable
- arm: fix use of INTERNAL_SYSCALL_CALL
- linux: Remove INTERNAL_SYSCALL_DECL
- nptl: Remove ununsed pthread-errnos.h rule
- linux: Consolidate INLINE_SYSCALL
- s390: Consolidate Linux syscall definition
- riscv: Avoid clobbering register parameters in syscall
- microblaze: Avoid clobbering register parameters in syscall
- nios2: Use Linux kABI for syscall return
- mips: Use Linux kABI for syscall return
- mips64: Consolidate Linux sysdep.h
- ia64: Use Linux kABI for syscall return
- alpha: Refactor syscall and Use Linux kABI for syscall return
- sparc: Avoid clobbering register parameters in syscall
- sparc: Use Linux kABI for syscall return
- powerpc: Use Linux kABI for syscall return
- powerpc: Consolidate Linux syscall definition
- i386: Enable CET support in ucontext functions
- tst-clone3: Use __NR_futex_time64 if we don't have __NR_futex
- powerpc64: Add memory protection key support [BZ #23202]
- ldbl-128ibm-compat: Provide a scalb implementation
- Add a generic scalb implementation
- Adjust thresholds in Bessel function implementations (bug 14469).
- resolv: Fix ABA race in /etc/resolv.conf change detection [BZ #25420]
- resolv: Enhance __resolv_conf_load to capture file change data
- resolv: Fix file handle leak in __resolv_conf_load [BZ #25429]
- resolv: Use <file_change_detection.h> in __resolv_conf_get_current
- Add STATX_ATTR_VERITY from Linux 5.5 to bits/statx-generic.h.
- Use gcc -finput-charset=ascii for check-installed-headers.
- math/test-sinl-pseudo: Use stack protector only if available
- alpha: Fix static gettimeofday symbol
- nss_nisplus: Use NSS_DECLARE_MODULE_FUNCTIONS
- nss_dns: Use NSS_DECLARE_MODULE_FUNCTIONS
- nss_files: Use NSS_DECLARE_MODULE_FUNCTIONS
- nss_db: Use NSS_DECLARE_MODULE_FUNCTIONS
- nss_compat: Use NSS_DECLARE_MODULE_FUNCTIONS
- nss_hesiod: Use NSS_DECLARE_MODULE_FUNCTIONS
- nss: Add function types and NSS_DECLARE_MODULE_FUNCTIONS macro to <nss.h>
- nss_compat: Do not use nss_* names for function pointers
- Avoid ldbl-96 stack corruption from range reduction of pseudo-zero (bug 25487).
- mips: Fix argument passing for inlined syscalls on Linux [BZ #25523]
- mips: Use 'long int' and 'long long int' in linux syscall code
- alpha: Use generic gettimeofday implementation
- sunrpc: Properly clean up if tst-udp-timeout fails
- elf: avoid stack allocation in dl_open_worker
- elf: avoid redundant sort in dlopen
- elf: Allow dlopen of filter object to work [BZ #16272]
- Update translations
- Rename RWF_WRITE_LIFE_NOT_SET to RWH_WRITE_LIFE_NOT_SET following Linux 5.5.
- S390: Fix non-ascii character in fenv.h.
- io: Add io/tst-lchmod covering lchmod and fchmodat
- Linux: Emulate fchmodat with AT_SYMLINK_NOFOLLOW using O_PATH [BZ #14578]
- io: Implement lchmod using fchmodat [BZ #14578]
- Add internal <file_change_detection.h> header file
- elf.h: Add R_RISCV_IRELATIVE
- Fix typo in the name for Wednesday in Kurdish [BZ #9809]
- debug: Add missing locale dependencies of fortify tests
- htl C11 threads: Avoid pthread_ symbols visibility in static library
- hurd: Add __pthread_spin_wait and use it
- ldbl-128ibm-compat: set PRINTF_CHK flag in {,v}sprintf_chk
- Use --disable-gdbserver in build-many-glibcs.py.
- Improve random memcpy benchmark
- nptl: update default pthread-offsets.h
- nptl: add missing pthread-offsets.h
- htl: Avoid a local plt for pthread_self
- pthread: Move some join tests from nptl to sysdeps/pthread
- htl: Make joining self return EDEADLK
- pthread: Move most barrier tests from nptl to sysdeps/pthread
- htl: Fix barrier_wait with one thread
- pthread: Move most sem tests from nptl to sysdeps/pthread
- htl: Make sem_wait/sem_timedwait interruptible
- htl: Make sem_open return ENOSYS
- htl: Add support for semaphore maximum value
- pthread: Move key tests from nptl to sysdeps/pthread
- hurd: Make nanosleep a cancellation point
- htl: Add support for libc cancellation points
- htl: clean __pthread_get_cleanup_stack hidden proto
- htl: XFAIL rwlock tests which need pshared support
- pthread: Move some rwlock tests from nptl to sysdeps/pthread
- pthread: Move most once tests from nptl to sysdeps/pthread
- htl: support cancellation during pthread_once
- pthread: Move most cond tests from nptl to sysdeps/pthread
- htl: make pthread_cond_destroy return EBUSY on waiters
- htl: Report missing mutex lock on pthread_cond_*wait
- htl: Fix linking static testcases
- htl: Move __register_atfork from forward to own file
- pthread: Move some attr tests from nptl to sysdeps/pthread
- htl: Fix default guard size
- pthread: Move most mutex tests from nptl to sysdeps/pthread
- pthread: Move spin tests from nptl to sysdeps/pthread
- htl: make pthread_spin_lock really spin
- htl: Avoid check-installed-headers looking at inlines
- htl: Do not put spin_lock inlines in public headers
- pthread: Move basic tests from nptl to sysdeps/pthread
- htl: Fix calling pthread_exit in the child of a fork
- x86: Remove <bits/select.h> and use the generic version
- C11 threads: Move implementation to sysdeps/pthread
- htl: Add C11 threads types definitions
- C11 threads: make thrd_join more portable
- C11 threads: Fix thrd_t / pthread_t compatibility assertion
- C11 threads: do not require PTHREAD_DESTRUCTOR_ITERATIONS
- nptl: Move nptl-specific types to separate header
- htl: Make __PTHREAD_ONCE_INIT more flexible
- htl: Add support for C11 threads behavior
- htl: Add missing internal functions declarations
- htl: Rename _pthread_mutex_init/destroy to __pthread_mutex_init/destroy
- htl: Move internal mutex/rwlock symbols to GLIBC_PRIVATE
- Linux: Add io/tst-o_path-locks test
- support: Add the xlstat function
- htl: Remove duplicate files
- htl: Remove unused files
- resolv: Fix CNAME chaining in resolv/tst-resolv-ai_idn-common.c
- Remove a comment claiming that sin/cos round correctly.
- y2038: linux: Provide __settimeofday64 implementation
- y2038: Provide conversion helpers for struct __timeval64
- y2038: alpha: Rename valid_timeval64_to_timeval to valid_timeval_to_timeval32
- y2038: alpha: Rename valid_timeval_to_timeval64 to valid_timeval32_to_timeval
- y2038: Introduce struct __timeval64 - new internal glibc type
- y2038: Define __suseconds64_t type to be used with struct __timeval64
- Update kernel version to 5.5 in tst-mman-consts.py.
- Update syscall lists for Linux 5.5.
- NEWS: Set fill-column hint to 72
- y2038: linux: Provide __timespec_get64 implementation
- Use binutils 2.34 branch in build-many-glibcs.py.
- Run nptl/tst-pthread-getattr in a container
- test-container: add exec, cwd
- Use Linux 5.5 in build-many-glibcs.py.
- rt: avoid PLT setup in timer_[sg]ettime
- Update or_IN collation [BZ #22525]
- Fix ckb_IQ [BZ #9809]
- Add new locale: ckb_IQ (Kurdish/Sorani spoken in Iraq) [BZ #9809]
- list-fixed-bugs.py: Wrap at 72 chars
- y2038: linux: Provide __sched_rr_get_interval64 implementation
- y2038: linux: Provide __timerfd_settime64 implementation
- y2038: linux: Provide __timerfd_gettime64 implementation
- i386: Remove _exit.S
- i386: Use ENTRY/END in assembly codes
- i386-mcount.S: Add _CET_ENDBR to _mcount and __fentry__
- i386/sub_n.S: Add a missing _CET_ENDBR to indirect jump target
- i386: Don't unnecessarily save and restore EAX, ECX and EDX [BZ# 25262]
- x86: Don't make 2 calls to dlerror () in a row
- Open master for 2.32 development

* Mon Feb 03 2020 DJ Delorie <dj@redhat.com> - 2.31-1
- Auto-sync with upstream branch release/2.31/master,
  commit 9ea3686266dca3f004ba874745a4087a89682617.
- glibc 2.31 release
- Generate ChangeLog.old/ChangeLog.20 for 2.31
- Add bugs fixed in 2.31 in NEWS
- Update newest tested versions of dependencies in install.texi
- Add more contributors to the manual
- Add note to NEWS about kernel headers dependency on risc-v
- Add Portuguese (Portugal) translation
- Add NEWS entry about 64-bit time_t syscall use on 32-bit targets
- nptl: Avoid using PTHREAD_MUTEX_DEFAULT in macro definition [BZ #25271]

* Thu Jan 30 2020 Patsy Franklin <patsy@redhat.com> - 2.30.9000-33
- Auto-sync with upstream branch master,
  commit 352bb99754ae7c83ff1b974f9c52244e974c9410.
- Build raise with -fasynchronous-unwind-tables.
- Fix locale/tst-locale-locpath cross-testing when sshd sets LANG.
- Fix elf/tst-rtld-preload cross-testing.
- Fix cross-testing of tst-ifunc-fault-* tests.
- gitlog-to-changelog: Drop scripts in favour of gnulib version
- Add NEWS entry about the change in handling of PT_GNU_STACK on MIPS
- Fix array overflow in backtrace on PowerPC (bug 25423)
- getaddrinfo: Fix resource leak after strdup failure in gethosts (swbz#25425)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Patsy Franklin <patsy@redhat.com> - 2.30.9000-31
- Auto-sync with upstream branch master,
  commit 92ce43eef7ac844782d50a8015d977d216fbadec.
- Run bench-timing-type with newly built libc.
- Get rid of Werror=maybe-uninitialized in res_send.c.
- translations: Update translations
- translations: Trim po files using msgattrib
- Update translations
- translations: Run msgmerge when downloading translations
- Fix maybe-uninitialized error on powerpc
- powerpc32: Fix syntax error in __GLRO macro
- Remove incorrect alloc_size attribute from pvalloc (swbz#25401)

* Fri Jan 17 2020 Florian Weimer <fweimer@redhat.com> - 2.30.9000-30
- Auto-sync with upstream branch master,
  commit 70ba28f7ab2923d4e36ffc9d5d2e32357353b25c:
- Fix tst-pkey.c pkey_alloc return checks and manual
- powerpc: Move cache line size to rtld_global_ro
- powerpc: Initialize rtld_global_ro for static dlopen (swbz#20802)
- Revert outdated translations
- vcs-to-changelog: Add quirk for __nonnull
- elf: Add elf/tst-dlopenfail-2 (swbz#25396, #1395758)
- Clear GL(dl_initfirst) when freeing its link_map (swbz#25396, #1395758)
- Update Translations
- Fix "elf: Add tst-ldconfig-ld_so_conf-update test" on 32bit.
- elf: Add tst-ldconfig-ld_so_conf-update test
- sl_SI locale: Use "." as the thousands separator (swbz#25233)

* Mon Jan 06 2020 Arjun Shankar <arjun@redhat.com> - 2.30.9000-29
- Auto-sync with upstream branch master,
  commit cbce69e70dc4b04fefcc7257e593733b8b03856c:
- Multiple locales: Add date_fmt (bug 24054)
- Update libc.pot for 2.31 release
- Add libm_alias_finite for _finite symbols
- Linux: Fix clock_nanosleep time64 check
- linux: Fix vDSO macros build with time64 interfaces
- x86: Make x32 use x86 time implementation
- Remove vDSO support from make-syscall.sh
- linux: Update x86 vDSO symbols
- linux: Update mips vDSO symbols
- linux: Consolidate Linux gettimeofday
- linux: Consolidate time implementation
- elf: Enable relro for static build
- elf: Move vDSO setup to rtld (BZ#24967)
- linux: Add support for clock_gettime64 vDSO
- linux: Optimize fallback 32-bit clock_gettime
- linux: Enable vDSO clock_gettime64 for i386
- linux: Enable vDSO clock_gettime64 for arm
- linux: Enable vDSO clock_gettime64 for mips
- linux: Add support for clock_getres64 vDSO
- linux: Optimize fallback 32-bit clock_getres
- htl: Use dso_handle.h
- htl: Drop common tcbhead_t definition
- htl: Move pthread_atfork to libc_nonshared.a
- htl: Add __errno_location and __h_errno_location
- hurd: Fix message reception for timer_thread

* Thu Jan 02 2020 Florian Weimer <fweimer@redhat.com> - 2.30.9000-28
- Auto-sync with upstream branch master,
  commit cc47d5c5f53f6d845ac54698ae8929af15662c44:
- Linux: Use built-in system call tables
- lv_LV locale: Correct the time part of d_t_fmt (swbz#25324)
- km_KH locale: Use "%M" instead of "m" in d_t_fmt (swbz#25323)
- ldbl-128ibm-compat: Do not mix -mabi=*longdouble and -mlong-double-128
- ldbl-128ibm-compat: Compiler flags for stdio functions
- Do not redirect calls to __GI_* symbols, when redirecting to *ieee128
- aarch64: add default memcpy version for kunpeng920
- aarch64: ifunc rename for kunpeng
- aarch64: Modify error-shown comments for strcpy
- linux: Consolidate sigprocmask
- Fix return code for __libc_signal_* functions
- nptl: Remove duplicate internal __SIZEOF_PTHREAD_MUTEX_T (swbz#25241)

* Thu Dec 26 2019 Carlos O'Donell <carlos@redhat.com> - 2.30.9000-27
- Auto-sync with upstream branch master,
  commit b8c210bcc74840d24c61d39bde15bea9daf3e271.
- mnw_MM, my_MM, and shn_MM locales: Do not use %Op
- Avoid compat symbols for totalorder in powerpc64le IEEE long double
- ldbl-128ibm-compat: Add *cvt functions
- Refactor *cvt functions implementation (2/2)
- Refactor *cvt functions implementation (1/2)
- Add exception-based flags for wait4
- aarch64: Optimized memset for Kunpeng processor.
- aarch64: Optimized strlen for strlen_asimd
- aarch64: Add Huawei Kunpeng to tunable cpu list
- aarch64: Optimized implementation of memrchr
- aarch64: Optimized implementation of strnlen
- aarch64: Optimized implementation of strcpy
- aarch64: Optimized implementation of memcmp
- Consolidate wait3 implementations
- Implement waitpid in terms of wait4
- linux: Use waitid on wait4 if __NR_wait4 is not defined
- Implement wait in terms of waitpid
- nptl: Move waitpid implementation to libc
- nptl: Move wait implementation to libc
- Remove __waitpid_nocancel
- Fix test isolation for elf/tst-ifunc-fault-lazy, elf/tst-ifunc-fault-bindnow
- Fix __libc_signal_block_all on sparc64
- powerpc: Do not run IFUNC resolvers for LD_DEBUG=unused [BZ #24214]

* Thu Dec 19 2019 Patsy Franklin <patsy@redhat.com> - 2.30.9000-26
- Auto-sync with upstream branch master,
  commit 3dcad8158f43d71d5b8f6f317f82952ddf3468f3.
- hurd: Do not make sigprocmask available in ld.so
- build-many-glibcs.py: Do not build C++ PCHs by default
- hurd: Make getrandom honour GRND_NONBLOCK
- tunables: report sbrk() failure
- build-many-glibcs.py: Add mipsisa64r6el-linux-gnu target
- mips: Do not include hi and lo in __SYSCALL_CLOBBERS for R6
- ldbl-128ibm-compat: Add ISO C99 versions of scanf functions
- ldbl-128ibm-compat: Fix selection of GNU and ISO C99 scanf
- hurd: Fix local PLT
- dlopen: Do not block signals
- dlopen: Rework handling of pending NODELETE status
- dlopen: Fix issues related to NODELETE handling and relocations
- hurd: Fix __close_nocancel_nostatus availability
- hurd: add getrandom and getentropy implementations
- hurd: Implement __close_nocancel_nostatus
- manual: clarify fopen with the x flag
- S390: Use sysdeps/ieee754/dbl-64/wordsize-64 on s390x.
- S390: Implement roundtoint and converttoint and define TOINT_INTRINSICS.
- S390: Implement math-barriers math_opt_barrier and math_force_eval.
- S390: Use libc_fe* macros in fe* functions.
- S390: Implement libc_fe* macros.
- S390: Use convert-to-fixed instruction for llround functions.
- S390: Use convert-to-fixed instruction for lround functions.
- S390: Use convert-to-fixed instruction for llrint functions.
- S390: Use convert-to-fixed instruction for lrint functions.
- S390: Use load-fp-integer instruction for roundeven functions.
- Adjust s_copysignl.c regarding code style.
- Adjust s_ceilf.c and s_ceill.c regarding code style.
- Adjust s_floorf.c and s_floorl.c regarding code style.
- Adjust s_rintf.c and s_rintl.c regarding code style.
- Adjust s_nearbyintf.c and s_nearbyintl.c regarding code style.
- Use GCC builtins for copysign functions if desired.
- Use GCC builtins for round functions if desired.
- Use GCC builtins for trunc functions if desired.
- Use GCC builtins for ceil functions if desired.
- Use GCC builtins for floor functions if desired.
- Use GCC builtins for rint functions if desired.
- Use GCC builtins for nearbyint functions if desired.
- Always use wordsize-64 version of s_round.c.
- Always use wordsize-64 version of s_trunc.c.
- Always use wordsize-64 version of s_ceil.c.
- Always use wordsize-64 version of s_floor.c.
- Always use wordsize-64 version of s_rint.c.
- Always use wordsize-64 version of s_nearbyint.c.
- ldconfig: Do not print a warning for a missing ld.so.conf file
- hurd: Fix using altstack while in an RPC call to be aborted
- Fix failure when CFLAGS contains -DNDEBUG (Bug 25251)

* Mon Dec 09 2019 DJ Delorie <dj@redhat.com> - 2.30.9000-25
- Auto-sync with upstream branch master,
  commit 0487ebed2278b20971af4cabf186fd3681adccf0.
- nptl: Add more missing placeholder abi symbol from nanosleep move
- sysdeps/riscv/start.S: rename .Lload_gp to load_gp (bug 24376)
- y2038: linux: Provide __timer_settime64 implementation
- y2038: linux: Provide __timer_gettime64 implementation
- timer: Decouple x86_64 specific timer_settime from generic Linux implementation
- timer: Decouple x86_64 specific timer_gettime from generic Linux implementation
- time: Introduce glibc's internal struct __itimerspec64
- Correct range checking in mallopt/mxfast/tcache [BZ #25194]
- misc/test-errno-linux: Handle EINVAL from quotactl
- <string.h>: Define __CORRECT_ISO_CPP_STRING_H_PROTO for Clang [BZ #25232]
- build-many-glibcs.py: Move sparcv8 to extra_glibcs

* Thu Dec  5 2019 Florian Weimer <fweimer@redhat.com> - 2.30.9000-24
- Upstream patches for fallout from dlopen NODELETE changes (#1778344, #1778366)

* Wed Dec 04 2019 Patsy Franklin <patsy@redhat.com> - 2.30.9000-23
- Auto-sync with upstream branch master,
  commit ec138c67cbda8b5826a0a2a7ba456408117996dc.
- sysdeps: Add clock_gettime64 vDSO
- Do not use ld.so to open statically linked programs in debugglibc.sh
- Attach to test in container from debugglibc.sh
- Expand $(as-needed) and $(no-as-needed) throughout the build system
- x86: Assume --enable-cet if GCC defaults to CET [BZ #25225]
- ldbl-128ibm-compat: Add tests for strfroml, strtold, and wcstold
- ldbl-128ibm-compat: Add tests for strfmon and strfmon_l
- ldbl-128ibm-compat: Add strfmon_l with IEEE long double format
- ldbl-128ibm-compat: Replace http with https in new files
- elf: Do not run IFUNC resolvers for LD_DEBUG=unused [BZ #24214]
- elf/tst-dlopenfail: Disable --no-as-needed for tst-dlopenfailmod1.so
- hurd: Fix ld.so __access override from libc
- hurd: Fix ld.so __getcwd override from libc
- hurd: Make __sigprocmask GLIBC_PRIVATE
- hurd: Fix renameat2 error
- hurd: make strerror(0) coherent with other ports
- hurd: Fix ld.so link
- Update kernel version to 5.4 in tst-mman-consts.py.
- Update SOMAXCONN value from Linux 5.4.
- Update syscall-names.list for Linux 5.4.
- Fix syntax error in build-many-glibcs.py.
- Define MADV_COLD and MADV_PAGEOUT from Linux 5.4.

* Mon Dec  2 2019 Florian Weimer <fweimer@redhat.com> - 2.30.9000-22
- dlopen: Remove incorrect assert in activate_nodelete (#1778344)

* Thu Nov 28 2019 Florian Weimer <fweimer@redhat.com> - 2.30.9000-21
- Auto-sync with upstream branch master,
  commit e37c2cf299b61ce18f62852f6c5624c27829b610:
- Move _dl_open_check to its original place in dl_open_worker
- Block signals during the initial part of dlopen
- Remove all loaded objects if dlopen fails, ignoring NODELETE (#1395758)
- Avoid late dlopen failure due to scope, TLS slotinfo updates (swbz#25112)
- Avoid late failure in dlopen in global scope update (swbz#25112)
- Lazy binding failures during dlopen/dlclose must be fatal (swbz#24304)
- resolv: Implement trust-ad option for /etc/resolv.conf (#1164339)
- dlsym: Do not determine caller link map if not needed
- libio: Disable vtable validation for pre-2.1 interposed handles (swbz#25203)
- ldbl-128ibm-compat: Add syslog functions
- ldbl-128ibm-compat: Add obstack printing functions
- ldbl-128ibm-compat: Reuse tests for err.h and error.h functions
- ldbl-128ibm-compat: Add error.h functions
- ldbl-128ibm-compat: Add err.h functions
- ldbl-128ibm-compat: Add argp_error and argp_failure
- sparc: Use atomic compiler builtins on sparc
- Remove 32 bit sparc v7 support

* Wed Nov 27 2019 Arjun Shankar <arjun@redhat.com> - 2.30.9000-20
- Auto-sync with upstream branch master,
  commit bfdb731438206b0f70fe7afa890681155c30b419:
- rtld: Check __libc_enable_secure for LD_PREFER_MAP_32BIT_EXEC (CVE-2019-19126)
- Introduce DL_LOOKUP_FOR_RELOCATE flag for _dl_lookup_symbol_x
- Enable inlining issignalingf within glibc
- Don't use a custom wrapper macro around __has_include (bug 25189).
- Remove duplicate inline implementation of issignalingf
- misc: Set generic pselect as ENOSYS
- Use DEPRECATED_SCANF macro for remaining C99-compliant scanf functions
- ldbl-128ibm-compat: Add regular/wide character printing printing functions
- ldbl-128ibm-compat: Test double values and positional arguments
- ldbl-128ibm-compat: Add regular/wide character scanning functions
- arm: Fix armv7 selection after 'Split BE/LE abilist'
- Use Linux 5.4 in build-many-glibcs.py.
- sysdeps/posix: Simplify if expression in getaddrinfo
- sysdeps/posix/getaddrinfo: Return early on invalid address family
- ru_UA locale: use copy "ru_RU" in LC_TIME (bug 25044)
- locale: Greek -> ASCII transliteration table [BZ #12031]
- nptl: Cleanup mutex internal offset tests
- nptl: Add tests for internal pthread_rwlock_t offsets
- nptl: Remove rwlock elision definitions
- nptl: Add struct_mutex.h and struct_rwlock.h
- nptl: Add default pthreadtypes-arch.h and pthread-offsets.h
- Compile elf/rtld.c with -fno-tree-loop-distribute-patterns.
- nptl: Fix __PTHREAD_MUTEX_INITIALIZER for !__PTHREAD_MUTEX_HAVE_PREV
- S390: Fix handling of needles crossing a page in strstr z15 ifunc [BZ #25226]

* Mon Nov 18 2019 Patsy Griffin <patsy@redhat.com> - 2.30.9000-19
- Auto-sync with upstream branch master,
  commit 2a764c6ee848dfe92cb2921ed3b14085f15d9e79.
- Enhance _dl_catch_exception to allow disabling exception handling
- hurd: Suppress GCC 10 -Warray-bounds warning in init-first.c [BZ #25097]
- linux: Add comment on affinity set sizes to tst-skeleton-affinity.c
- Avoid zero-length array at the end of struct link_map [BZ #25097]
- Introduce link_map_audit_state accessor function
- Properly initialize audit cookie for the dynamic loader [BZ #25157]
- nios2: Work around backend bug triggered by csu/libc-tls.c (GCC PR 92499)
- Redefine _IO_iconv_t to store a single gconv step pointer [BZ #25097]
- Add new script for plotting string benchmark JSON output
- support: Fix support_set_small_thread_stack_size to build on Hurd
- login: Use pread64 in utmp implementation
- Clarify purpose of assert in _dl_lookup_symbol_x
- aarch64: Increase small and medium cases for __memcpy_generic
- login: Introduce matches_last_entry to utmp processing

* Tue Nov 12 2019 Arjun Shankar <arjun@redhat.com> - 2.30.9000-18
- Auto-sync with upstream branch master,
  commit cba932a5a9e91cffd7f4172d7e91f9b2efb1f84b:
- nptl: Move nanosleep implementation to libc
- Refactor nanosleep in terms of clock_nanosleep
- nptl: Refactor thrd_sleep in terms of clock_nanosleep
- math: enhance the endloop condition of function handle_input_flag
- hurd: Remove lingering references to the time function
- hurd: Use __clock_gettime in _hurd_select
- login: Remove double-assignment of fl.l_whence in try_file_lock
- nptl: Add missing placeholder abi symbol from nanosleep move
- login: Acquire write lock early in pututline [BZ #24882]
- Remove hppa pthreadP.h
- sysdeps/clock_nanosleep: Use clock_nanosleep_time64 if avaliable
- Fix array bounds violation in regex matcher (bug 25149)
- support: Add support_set_small_thread_stack_size
- linux: Reduce stack size for nptl/tst-thread-affinity-pthread
- y2038: linux: Provide __ppoll64 implementation
- Declare asctime_r, ctime_r, gmtime_r, localtime_r for C2X.
- support: Add xsetlocale function
- libio/tst-fopenloc: Use xsetlocale, xfopen, and xfclose
- Fix clock_nanosleep when interrupted by a signal
- slotinfo in struct dtv_slotinfo_list should be flexible array [BZ #25097]

* Wed Nov 06 2019 Patsy Franklin <patsy@redhat.com> - 2.30.9000-17
- Auto-sync with upstream branch master,
  commit 2a0356e1191804d57005e1cfe2a72f019b7a8cce.
- posix: Sync regex with gnulib
- Add mnw language code [BZ #25139]
- Add new locale: mnw_MM (Mon language spoken in Myanmar) [BZ #25139]
- S390: Fp comparison are now raising FE_INVALID with gcc 10.
- linux: pselect: Remove CALL_PSELECT6 macro
- Fix run-one-test so that it runs elf tests
- nptl: Fix niggles with pthread_clockjoin_np
- hppa: Align __clone stack argument to 8 bytes (Bug 25066)
- y2038: linux: Provide __futimens64 implementation
- y2038: linux: Provide __utimensat64 implementation
- nptl: Add pthread_timedjoin_np, pthread_clockjoin_np NULL timeout test
- nptl: Add pthread_clockjoin_np
- manual: Add documentation for pthread_tryjoin_np and pthread_timedjoin_np
- nptl: Convert tst-join3 to use libsupport
- Sync time/mktime.c with gnulib
- Sync timespec-{add,sub} with gnulib
- Sync intprops.h with gnulib
- Refactor adjtimex based on clock_adjtime
- Refactor PI mutexes internal definitions
- Remove pause and nanosleep not cancel wrappers
- nptl: Replace non cancellable pause/nanosleep with futex
- Consolidate lowlevellock-futex.h
- Consolidate futex-internal.h
- Base max_fast on alignment, not width, of bins (Bug 24903)
- Revise the documentation of simple calendar time.
- Make second argument of gettimeofday as 'void *'
- Use clock_gettime to implement gettimeofday.
- Use clock_gettime to implement timespec_get.
- Consolidate and deprecate ftime
- Change most internal uses of time to __clock_gettime.
- Use clock_gettime to implement time.
- Use clock_settime to implement settimeofday.
- Use clock_settime to implement stime; withdraw stime.
- Change most internal uses of __gettimeofday to __clock_gettime.
- Linux/Alpha: don't use timeval32 system calls.
- resolv/tst-idna_name_classify: Isolate from system libraries
- hurd: Support for file record locking
- Comment out initgroups from example nsswitch.conf (Bug 25146)

* Mon Oct 28 2019 DJ Delorie <dj@redhat.com> - 2.30.9000-16
- Auto-sync with upstream branch master,
  commit 177a3d48a1c74d7b2cd6bfd48901519d25a5ecad.
- y2038: linux: Provide __clock_getres64 implementation
- time: Introduce function to check correctness of nanoseconds value
- Add Transliterations for Unicode Misc. Mathematical Symbols-A/B [BZ #23132]
- Install charmaps uncompressed in testroot
- Add wait-for-debugger test harness hooks
- Define __STATFS_MATCHES_STATFS64
- hurd: Fix build after __pread64 usage in the dynamic loader
- sysdeps/stat: Handle 64-bit ino_t types on 32-bit hosts
- S390: Remove not needed stack frame in syscall function.

* Fri Oct 25 2019 DJ Delorie <dj@redhat.com> - 2.30.9000-15
- Add *.mo files to all-langpacks (#1624528)

* Thu Oct 24 2019 DJ Delorie <dj@redhat.com> - 2.30.9000-14
- Add Requires on basesystem for main package (#1757267)
- Add Requires on coreutils for glibc-headers (uses rm)

* Wed Oct 23 2019 Arjun Shankar <arjun@redhat.com> - 2.30.9000-13
- Auto-sync with upstream branch master,
  commit 7db1fe38de21831d53ceab9ae83493d8d1aec601:
- Include <kernel-features.h> explicitly in Linux clock_settime.c
- Remove math-finite.h
- Remove finite-math tests
- Remove x64 _finite tests and references
- Fix testroot.pristine creation copying dynamic linker

* Fri Oct 18 2019 Patsy Franklin <patsy@redhat.com> - 2.30.9000-12
- Auto-sync with upstream branch master,
  commit ef21bd2d8c6805c0c186a01f7c5039189f51b8c4.
- loadarchive: guard against locale-archive corruption (Bug #25115)
- Undo accidental commit to ChangeLog.19.
- nptl: Document AS-safe functions in cancellation.c.
- elf: Use nocancel pread64() instead of lseek()+read()
- Add nocancel version of pread64()
- Add run-one-test convenience target and makefile help text
- Update sysvipc kernel-features.h files for Linux 5.1
- S390: Add new s390 platform z15.
- nptl: SIGCANCEL, SIGTIMER, SIGSETXID are always defined
- nptl/tst-cancel25 needs to be an internal test
- Remove libc_hidden_def from __semtimedop stub
- sysvipc: Implement semop based on semtimedop
- ipc: Refactor sysvipc internal definitions
- Rename and split elf/tst-dlopen-aout collection of tests
- dlfcn: Remove remnants of caller sensitivity from dlinfo
- ldconfig: handle .dynstr located in separate segment (bug 25087)
- ldd: Print "not a dynamic executable" on standard error [BZ #24150]
- Add PTRACE_GET_SYSCALL_INFO from Linux 5.3 to sys/ptrace.h.
- Move ChangeLog to ChangeLog.old/ChangeLog.19
- manual: Remove warning in the documentation of the abort function
- sysvipc: Set ipc_perm mode as mode_t (BZ#18231)
- Simplify note processing
- syscall-names.list: fix typos in comment
- y2038: linux: Provide __clock_settime64 implementation
- posix: Use posix_spawn for wordexp
- mips: Do not malloc on getdents64 fallback
- sparc: Assume GOTDATA support in the toolchain
- <dirent.h>: Remove wrong comment about getdents64 declaration
- ChangeLog: Remove leading spaces before tabs and trailing whitespace
- Make tst-strftime2 and tst-strftime3 depend on locale generation
- posix/tst-wordexp-nocmd: Fix diagnostics output in test
- wordexp: Split out command execution tests from posix/wordexp-test

* Tue Oct 08 2019 Arjun Shankar <arjun@redhat.com> - 2.30.9000-11
- Adjust glibc-rh741105.patch.
- Auto-sync with upstream branch master,
  commit ca602c1536ce2777f95c07525f3c42d78812e665:
- Add TCP_TX_DELAY from Linux 5.3 to netinet/tcp.h
- [powerpc] fenv_private.h clean up
- [powerpc] libc_feupdateenv_test: optimize FPSCR access
- [powerpc] __fesetround_inline optimizations
- [powerpc] Rename fegetenv_status to fegetenv_control
- [powerpc] libc_feholdsetround_noex_ppc_ctx: optimize FPSCR write
- [powerpc] Rename fesetenv_mode to fesetenv_control
- Add helper script for glibc debugging
- Update bits/mman.h constants and tst-mman-consts.py for Linux 5.3.
- y2038: Provide conversion helpers for struct __timespec64
- Use binutils 2.33 branch in build-many-glibcs.py.
- Sync "language", "lang_name", "territory", "country_name" with CLDR/langtable
- Split up endian.h to minimize exposure of BYTE_ORDER.
- time: Add padding for the timespec if required
- Enable passing arguments to the inferior in debugglibc.sh
- [powerpc] No need to enter "Ignore Exceptions Mode"
- Y2038: Include proper header to provide support for struct timeval on HURD
- Disable warnings in string/tester.c at top level.
- string/endian.h: Restore the __USE_MISC conditionals
- Disable -Wmaybe-uninitialized for total_deadline in sunrpc/clnt_udp.c.
- ChangeLog update from my last commit
- nptl: Move pthread_attr_setinheritsched implementation into libc.
- elf: Never use the file ID of the main executable [BZ #24900]
- elf: Assign TLS modid later during dlopen [BZ #24930]
- nptl: Move pthread_attr_getschedparam implementation into libc
- riscv: Remove support for variable page sizes
- nptl: Move pthread_attr_setschedparam implementation into libc

* Fri Sep 27 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.30.9000-10
- Use full locale names in langpack descriptions (#1651375)

* Thu Sep 26 2019 Patsy Franklin <patsy@redhat.com> - 2.30.9000-9
- Auto-sync with upstream branch master,
  commit 464cd3a9d5f505d92bae9a941bb75b0d91ac14ee.
- y2038: Introduce struct __timespec64 - new internal glibc type
- auto-changelog: Remove latin1 from codecs
- Set the expects flags to clock_nanosleep
- Fix tst-sigcontext-get_pc rule name from a43565ac447b1
- inet/net-internal.h: Fix uninitalised clntudp_call() variable
- Fix vDSO initialization on arm and mips
- Script to generate ChangeLog-like output from git log
- [powerpc] SET_RESTORE_ROUND optimizations and bug fix
- Fix building support_ptrace.c on i686-gnu.
- S390: Use _HP_TIMING_S390_H instead of _HP_TIMING_H.
- Update syscall-names.list for Linux 5.3.
- Use Linux 5.3 in build-many-glibcs.py.
- S390: Add support for HP_TIMING_NOW.
- Fix RISC-V vfork build with Linux 5.3 kernel headers.
- Add UNSUPPORTED check in elf/tst-pldd.
- sparc64: Use linux generic time implementation
- mips: Consolidate INTERNAL_VSYSCALL_CALL
- powerpc: Simplify vsyscall internal macros
- Refactor vDSO initialization code
- Remove PREPARE_VERSION and PREPARE_VERSION_KNOW
- Fix small error in HP_TIMING_PRINT trailing null char setting

* Mon Sep 16 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.30.9000-8
- Change Supplements "langpacks-" to "langpacks-core-" (#1729992)

* Mon Sep 16 2019 DJ Delorie <dj@redhat.com> - 2.30.9000-7
- Auto-sync with upstream branch master,
  commit 1a6566094d3097f4a3037ab5555cddc6cb11c3a3.
- alpha: force old OSF1 syscalls for getegid, geteuid and getppid [BZ #24986]
- Fix http: URL in 'configure'
- Regenerate charmap-kw.h, locfile-kw.h
- Fix three GNU license URLs, along with trailing-newline issues.
- Prefer https to http for gnu.org and fsf.org URLs

* Fri Sep 06 2019 Patsy Franklin <patsy@redhat.com> - 2.30.9000-6
- Auto-sync with upstream branch master,
  commit 1b7f04070bd94f259e2ed24d6fb76309d64fb164.
- locale: Avoid zero-length array in _nl_category_names [BZ #24962]
- math: Replace const attribute with pure in totalorder* functions
- y2038: Introduce the __ASSUME_TIME64_SYSCALLS define
- Finish move of clock_* functions to libc. [BZ #24959]
- Update Alpha libm-test-ulps
- localedef: Use initializer for flexible array member [BZ #24950]
- Add misc/tst-mntent-autofs, testing autofs "ignore" filtering
- Use autofs "ignore" mount hint in getmntent_r/getmntent
- hurd: Fix build
- Use generic memset/memcpy/memmove in benchtests
- nptl: Move pthread_attr_getinheritsched implementation into libc
- hurd: Fix SS_ONSTACK support
- hurd: Remove optimizing anonymous maps as __vm_allocate.
- hurd: Fix poll and select POSIX compliancy details about errors
- hurd: Fix timeout handling in _hurd_select
- hurd getcwd: Allow unknown root directory
- hurd: Fix implementation of setitimer.
- hurd: Fix _hurd_select for single fd sets
- MIPS support for GNU hash
- sh: Split BE/LE abilist
- microblaze: Split BE/LE abilist
- arm: Split BE/LE abilist
- Correct the spelling of more contributors
- Fix posix/tst-regex by using UTF-8 and own test input
- [powerpc] fegetenv_status: simplify instruction generation
- [powerpc] fesetenv: optimize FPSCR access
- [powerpc] SET_RESTORE_ROUND improvements
- [powerpc] fe{en,dis}ableexcept, fesetmode: optimize FPSCR accesses
- [powerpc] fe{en,dis}ableexcept optimize bit translations
- misc: Use allocate_once in getmntent
- nptl: Move pthread_attr_setdetachstate implementation into libc
- login: pututxline could fail to overwrite existing entries [BZ #24902]
- Fix posix/tst-regex by using a dedicated input-file.

* Tue Aug 27 2019 DJ Delorie <dj@redhat.com> - 2.30.9000-5
- Move makedb from glibc-common to nss_db (#1704334)

* Mon Aug 26 2019 DJ Delorie <dj@redhat.com> - 2.30.9000-4
- Auto-sync with upstream branch master,
  commit 1bced8cadc82077f0201801239e89eb24b68e9aa.
- Don't put non-ASCII into installed headers
- Fix spellings of contributor names in comments and doc
- [MIPS] Raise highest supported EI_ABIVERSION value [SWBZ #24916]
- mips: Force RWX stack for hard-float builds that can run on pre-4.8 kernels
- linux: Make profil_counter a compat_symbol (SWBZ#17726)
- Refactor sigcontextinfo.h
- Add RTLD_SINGLE_THREAD_P on generic single-thread.h
- Chinese locales: Set first_weekday to 2 (swbug 24682).
- powerpc: Fix typos and field name in comments
- Mark IDN tests unsupported with libidn2 before 2.0.5.
- Document strftime %Ob and %OB as C2X features.
- Remove dead regex code
- Fix bad pointer / leak in regex code
- Don't use the argument to time.
- Add tgmath.h macros for narrowing functions.
- Update i386 libm-test-ulps

* Mon Aug 19 2019 Carlos O'Donell <carlos@redhat.com> - 2.30.9000-3
- Drop glibc-fedora-nscd-warnings.patch; applied upstream.
- Drop Source7: nsswitch.conf; applying patch to upstream.
- Add glibc-fedora-nsswitch.patch for Fedora customizations.
- Auto-sync with upstream branch master,
  commit d34d4c80226b3f5a1b51a8e5b005a52fba07d7ba:
- Do not print backtraces on fatal glibc errors.
- elf: Self-dlopen failure with explict loader invocation (swbz#24900)
- login: Add nonstring attributes to struct utmp, struct utmpx (swbz#24899)
- login: Use struct flock64 in utmp (swbz#24880)
- login: Disarm timer after utmp lock acquisition (swbz#24879)

* Fri Aug 16 2019 Carlos O'Donell <carlos@redhat.com> - 2.30.9000-2
- Fix C.UTF-8 to use full code ranges.

* Thu Aug 15 2019 Florian Weimer <fweimer@redhat.com> - 2.30.9000-1
- Auto-sync with upstream branch master,
  commit 341da5b4b6253de9a7581a066f33f89cacb44dec.

* Fri Aug 02 2019 Florian Weimer <fweimer@redhat.com> - 2.30-1
- Drop glibc-rh1734680.patch, applied upstream.
- Auto-sync with upstream branch release/2.30/master,
  commit be9a328c93834648e0bec106a1f86357d1a8c7e1:
- malloc: Remove unwanted leading whitespace in malloc_info (swbz#24867)
- glibc 2.30 release
- iconv: Revert steps array reference counting changes (#1734680)
- Restore r31 setting in powerpc32 swapcontext

* Wed Jul 31 2019 Florian Weimer <fweimer@redhat.com> - 2.29.9000-37
- Fix memory leak in iconv_open (#1734680)

* Tue Jul 30 2019 Florian Weimer <fweimer@redhat.com> - 2.29.9000-36
- Drop glibc-rh1732406.patch, fix for the regression applied upstream.
- Auto-sync with upstream branch master,
  commit 8a814e20d443adc460a1030fa1a66aa9ae817483:
- nptl: Use uintptr_t for address diagnostic in nptl/tst-pthread-getattr
- Linux: Move getdents64 to <dirent.h>
- test-container: Install with $(sorted-subdirs) (swbz#24794)
- gconv: Check reference count in __gconv_release_cache (#1732406)
- x86-64: Compile branred.c with -mprefer-vector-width=128 (swbz#24603)
- build-many-glibcs.py: Use Linux 5.2 by default
- Linux: Use in-tree copy of SO_ constants for !__USE_MISC (swbz#24532)
- test-container: Avoid copying unintended system libraries

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Florian Weimer <fweimer@redhat.com> - 2.29.9000-34
- Revert libio change that causes crashes (#1732406)

* Mon Jul 22 2019 DJ Delorie <dj@redhat.com> - 2.29.9000-33
- Auto-sync with upstream branch master,
  commit dcf36bcad3f283f77893d3b157ef7bb2c99419f2.
- Add NEWS entry about the new AArch64 IFUNC resolver call ABI
- locale/C-translit.h.in: Cyrillic -> ASCII transliteration [BZ #2872]
- Linux: Update syscall-names.list to Linux 5.2

* Thu Jul 18 2019 DJ Delorie <dj@redhat.com> - 2.29.9000-32
- Auto-sync with upstream branch master,
  commit 3556658c5b8765480711b265abc901c67d5fc060.
- Regenerate po/libc.pot for 2.30 release.
- nptl: Add POSIX-proposed _clock functions to hppa pthread.h
- nptl: Remove unnecessary forwarding of pthread_cond_clockwait from libc
- Afar locales: Months and days updated from CLDR (bug 21897).
- nl_BE locale: Use "copy "nl_NL"" in LC_NAME (bug 23996).
- nl_BE and nl_NL locales: Dutch salutations (bug 23996).
- ga_IE and en_IE locales: Revert first_weekday removal (bug 24200).
- nptl: Remove futex_supports_exact_relative_timeouts
- Update NEWS for new _clockwait and _clocklock functions
- nptl: Add POSIX-proposed pthread_mutex_clocklock
- nptl: Rename lll_timedlock to lll_clocklock and add clockid parameter
- nptl: Add POSIX-proposed pthread_rwlock_clockrdlock & pthread_rwlock_clockwrlock
- nptl: pthread_rwlock: Move timeout validation into _full functions
- nptl: Add POSIX-proposed pthread_cond_clockwait
- nptl: Add POSIX-proposed sem_clockwait
- nptl: Add clockid parameter to futex timed wait calls
- posix: Fix large mmap64 offset for mips64n32 (BZ#24699)
- nss_db: fix endent wrt NULL mappings [BZ #24695] [BZ #24696]

* Wed Jul 10 2019 Carlos O'Donell <carlos@redhat.com> - 2.29.9000-31
- Auto-sync with upstream branch master,
  commit 30ba0375464f34e4bf8129f3d3dc14d0c09add17.
- Don't declare __malloc_check_init in <malloc.h> (bug 23352)
- nftw: fill in stat buf for dangling links [BZ #23501]
- dl-vdso: Add LINUX_4 HASH CODE to support nds32 vdso mechanism
- riscv: restore ABI compatibility (bug 24484)
- aarch64: new ifunc resolver ABI
- nptl: Remove vfork IFUNC-based forwarder from libpthread [BZ #20188]
- malloc: Add nptl, htl dependency for the subdirectory [BZ #24757]
- Call _dl_open_check after relocation [BZ #24259]
- Linux: Use mmap instead of malloc in dirent/tst-getdents64
- ld.so: Support moving versioned symbols between sonames [BZ #24741]
- io: Remove copy_file_range emulation [BZ #24744]
- Linux: Adjust gedents64 buffer size to int range [BZ #24740]
- powerpc: Use generic e_expf
- Linux: Add nds32 specific syscalls to syscall-names.list
- szl_PL locale: Fix a typo in the previous commit (bug 24652).
