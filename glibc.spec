%define glibcsrcdir glibc-2.12-2-gc4ccff1
%define glibcversion 2.12
%define glibcrelease 1.212%{?dist}.3
%define run_glibc_tests 1
%define auxarches athlon sparcv9v sparc64v alphaev6
%define xenarches i686 athlon
%ifarch %{xenarches}
%define buildxen 1
%define xenpackage 0
%else
%define buildxen 0
%define xenpackage 0
%endif
%ifarch ppc ppc64
%define buildpower6 1
%else
%define buildpower6 0
%endif
%define rtkaioarches %{ix86} x86_64 ppc ppc64 s390 s390x
%define biarcharches %{ix86} x86_64 ppc ppc64 s390 s390x
%define debuginfocommonarches %{biarcharches} alpha alphaev6 sparc sparcv9 sparcv9v sparc64 sparc64v
%define multiarcharches ppc ppc64 %{ix86} x86_64
%define systemtaparches %{ix86} x86_64 ppc ppc64 s390 s390x

Summary: The GNU libc libraries
Name: glibc
Version: %{glibcversion}
Release: %{glibcrelease}
# GPLv2+ is used in a bunch of programs, LGPLv2+ is used for libraries.
# Things that are linked directly into dynamically linked programs
# and shared libraries (e.g. crt files, lib*_nonshared.a) have an additional
# exception which allows linking it into any kind of programs or shared
# libraries without restrictions.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System Environment/Libraries
URL: http://sources.redhat.com/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.bz2
Source1: %{glibcsrcdir}-releng.tar.bz2
Patch0: glibc-fedora.patch
Patch2: glibc-rh587360.patch
Patch3: glibc-rh582738.patch
Patch4: glibc-getlogin-r.patch
Patch5: glibc-localedata.patch
Patch6: glibc-rh593396.patch
Patch7: glibc-recvmmsg.patch
Patch8: glibc-aliasing.patch
Patch9: glibc-rh593686.patch
Patch10: glibc-rh607461.patch
Patch11: glibc-rh621959.patch
Patch12: glibc-rh607010.patch
Patch13: glibc-rh630801.patch
Patch14: glibc-rh631011.patch
Patch15: glibc-rh641128.patch
Patch16: glibc-rh642584.patch
Patch17: glibc-rh643822.patch
Patch18: glibc-rh645672.patch
Patch19: glibc-rh580498.patch
Patch20: glibc-rh615090.patch
Patch21: glibc-rh623187.patch
Patch22: glibc-rh646954.patch
Patch23: glibc-rh647448.patch
Patch24: glibc-rh615701.patch
Patch25: glibc-rh652661.patch
Patch26: glibc-rh656530.patch
Patch27: glibc-rh656014.patch
Patch28: glibc-rh661982.patch
Patch29: glibc-rh601686.patch
Patch30: glibc-rh676076.patch
Patch31: glibc-rh667974.patch
Patch32: glibc-rh625893.patch
Patch33: glibc-rh681054.patch
Patch34: glibc-rh689471.patch
Patch35: glibc-rh692177.patch
Patch36: glibc-rh692838.patch
Patch37: glibc-rh703480.patch
Patch38: glibc-rh705465.patch
Patch39: glibc-rh703481.patch
Patch40: glibc-rh694386.patch
Patch41: glibc-rh676591.patch
Patch42: glibc-rh711987.patch
Patch43: glibc-rh695595.patch
Patch45: glibc-rh695963.patch
Patch46: glibc-rh713134.patch
Patch47: glibc-rh714823.patch
Patch48: glibc-rh718057.patch
Patch49: glibc-rh688980.patch
Patch50: glibc-rh712248.patch
Patch51: glibc-rh731042.patch
Patch52: glibc-rh730379.patch
Patch53: glibc-rh700507.patch
Patch54: glibc-rh699724.patch
Patch55: glibc-rh736346.patch
Patch56: glibc-rh737778.patch
Patch57: glibc-rh738665.patch
Patch58: glibc-rh738763.patch
Patch59: glibc-rh739184.patch
Patch60: glibc-rh711927.patch
Patch61: glibc-rh688720.patch
Patch62: glibc-rh726517.patch
Patch63: glibc-rh752122.patch
Patch64: glibc-rh739971.patch
Patch65: glibc-rh751750.patch
Patch66: glibc-rh740506.patch
Patch67: glibc-rh757888.patch
Patch68: glibc-rh750531.patch
Patch69: glibc-rh749188.patch
Patch70: glibc-rh767746.patch
Patch72: glibc-rh767693.patch
Patch73: glibc-rh740506-2.patch
Patch74: glibc-rh696472.patch
Patch75: glibc-rh771342.patch
Patch76: glibc-rh657572.patch
Patch77: glibc-rh767693-2.patch
Patch78: glibc-rh782585.patch
Patch79: glibc-rh784402.patch
Patch80: glibc-rh697421.patch
Patch81: glibc-rh785984.patch
Patch82: glibc-rh767146.patch
Patch83: glibc-rh766513.patch
Patch84: glibc-rh789209.patch
Patch85: glibc-rh788959.patch
Patch86: glibc-rh789189.patch
Patch88: glibc-rh789238.patch
Patch89: glibc-rh794817.patch
Patch90: glibc-rh797094-1.patch
Patch91: glibc-rh797094-2.patch
Patch92: glibc-rh789238-2.patch
Patch93: glibc-rh795498.patch
Patch94: glibc-rh794817-2.patch
Patch95: glibc-rh804689.patch
Patch96: glibc-rh809602.patch
Patch97: glibc-rh808337.patch
Patch99: glibc-rh788959-2.patch
Patch100: glibc-rh808545.patch
Patch101: glibc-rh833717.patch
Patch103: glibc-rh823909.patch
Patch104: glibc-rh826149.patch
Patch105: glibc-rh841787.patch
Patch106: glibc-rh809726.patch
Patch107: glibc-rh806404.patch
Patch108: glibc-rh832516.patch
Patch109: glibc-rh830127.patch
Patch110: glibc-rh832694.patch
Patch111: glibc-rh843673.patch
Patch112: glibc-rh847932.patch
Patch113: glibc-rh837918.patch
Patch114: glibc-rh849203.patch
Patch115: glibc-rh849651.patch
Patch116: glibc-rh827362.patch
Patch117: glibc-rh837695.patch
Patch118: glibc-rh804686.patch
Patch119: glibc-rh848082.patch
Patch120: glibc-rh846342.patch
Patch121: glibc-rh852445.patch
Patch122: glibc-rh861167.patch
Patch123: glibc-rh863453.patch
Patch124: glibc-rh864322.patch
Patch125: glibc-rh929388.patch
Patch126: glibc-rh919562.patch
Patch127: glibc-rh886968.patch
Patch128: glibc-rh966775.patch
Patch129: glibc-rh834386.patch
Patch130: glibc-rh834386-2.patch
Patch131: glibc-rh862094.patch
Patch132: glibc-rh851470.patch
Patch133: glibc-rh868808.patch
Patch134: glibc-rh552960.patch
Patch135: glibc-rh663641.patch
Patch136: glibc-rh663641-2.patch
Patch137: glibc-rh848748.patch
Patch138: glibc-rh952422.patch
Patch139: glibc-rh663641-3.patch
Patch140: glibc-rh916986.patch
Patch141: glibc-rh970776.patch
Patch142: glibc-rh966778.patch
Patch143: glibc-rh863384.patch
Patch144: glibc-rh629823.patch
Patch145: glibc-rh629823-2.patch
Patch146: glibc-rh947882.patch
Patch147: glibc-rh905874.patch
Patch148: glibc-rh929302.patch
Patch150: glibc-rh928318.patch
Patch151: glibc-rh905575.patch
Patch152: glibc-rh988931.patch
Patch153: glibc-rh970090.patch
Patch154: glibc-rh1008310.patch
Patch155: glibc-rh1022022.patch
Patch156: glibc-rh1043557.patch
Patch157: glibc-rh1039988.patch
Patch158: glibc-rh995972.patch
Patch159: glibc-rh981942.patch
Patch160: glibc-rh1032628.patch
Patch161: glibc-rh1027101.patch
Patch162: glibc-rh1025933.patch
Patch163: glibc-rh845218.patch
Patch164: glibc-rh1044628.patch
Patch165: glibc-rh1085273.patch
Patch166: glibc-rh1074342.patch
Patch167: glibc-rh1085289.patch
Patch168: glibc-rh1082379.patch
Patch169: glibc-rh1074353.patch
Patch170: glibc-rh1019916.patch
Patch171: glibc-rh1028285.patch
Patch172: glibc-rh1099025.patch
Patch173: glibc-rh1087833.patch
Patch174: glibc-rh1027261.patch
Patch175: glibc-rh905941.patch
Patch176: glibc-rh1054846.patch
Patch177: glibc-rh1111460.patch
Patch178: glibc-rh1099025-2.patch
Patch179: glibc-rh1133810-1.patch
Patch180: glibc-rh1133810-2.patch
Patch181: glibc-rh1138769.patch
Patch182: glibc-rh1171296.patch
Patch183: glibc-rh1172044.patch
Patch184: glibc-rh1154563.patch
Patch185: glibc-rh1125307.patch
Patch186: glibc-rh1176907.patch
Patch187: glibc-rh1183534.patch
Patch188: glibc-rh1159167.patch
Patch189: glibc-rh1023306.patch
Patch190: glibc-rh1085312.patch
Patch191: glibc-rh1091915.patch
Patch192: glibc-rh859965.patch
Patch193: glibc-rh1124204.patch
Patch194: glibc-rh978098.patch
Patch195: glibc-rh1144019.patch
Patch196: glibc-rh1053178.patch
Patch197: glibc-rh1144132.patch
Patch198: glibc-rh1116050.patch
Patch199: glibc-rh1116050-1.patch
Patch200: glibc-rh867679.patch
Patch201: glibc-rh1088301.patch
Patch202: glibc-rh1195453-avx512.patch
Patch203: glibc-rh1066724.patch
Patch204: glibc-rh1209376.patch
Patch205: glibc-rh1207236.patch
Patch206: glibc-rh1217186.patch
Patch207: glibc-rh1245731.patch
Patch208: glibc-rh1245731-2.patch
Patch209: glibc-rh1245731-3.patch
Patch210: glibc-rh1245731-4.patch
Patch211: glibc-rh1246656.patch
Patch212: glibc-rh1246660.patch
Patch213: glibc-rh1264189.patch
Patch214: glibc-rh1244585.patch
Patch215: glibc-rh1211098.patch
Patch216: glibc-rh1192621.patch
Patch217: glibc-rh1091334.patch
Patch218: glibc-rh1211748.patch
Patch219: glibc-rh1011900.patch
Patch220: glibc-rh1186104.patch
Patch221: glibc-rh1198802.patch
Patch222: glibc-rh1275384.patch
Patch223: glibc-rh1020263.patch
Patch224: glibc-rh1200555.patch
Patch225: glibc-rh1293464.patch
Patch226: glibc-rh1280058.patch
Patch227: glibc-rh1296031.patch
Patch228: glibc-rh1296031-0.patch
Patch229: glibc-rh1299319-0.patch
Patch230: glibc-rh1299319-1.patch
Patch231: glibc-rh1223095.patch
Patch232: glibc-rh1358014.patch
Patch233: glibc-rh1373646.patch
Patch234: glibc-rh1358011.patch
Patch235: glibc-rh1358013.patch
Patch236: glibc-rh1270950.patch
Patch237: glibc-rh1331304.patch
Patch238: glibc-rh1318380.patch
Patch239: glibc-rh1101858.patch
Patch240: glibc-rh1384281.patch
Patch241: glibc-rh1338673.patch
Patch242: glibc-rh1358015.patch
Patch243: glibc-rh1012343.patch
Patch244: glibc-rh1452717-1.patch
Patch245: glibc-rh1452717-2.patch
Patch246: glibc-rh1452717-3.patch
Patch247: glibc-rh1452717-4.patch
Patch248: glibc-rh1504810-1.patch
Patch249: glibc-rh1504810-2.patch
Patch250: glibc-rh1668169.patch
Patch251: glibc-rh1555930-1.patch
Patch252: glibc-rh1555930-2.patch
Patch253: glibc-rh1577437.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: glibc-profile < 2.4
Provides: ldconfig
# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)
Requires: glibc-common = %{version}-%{release}
# Require libgcc in case some program calls pthread_cancel in its %%post
Requires(pre): basesystem, libgcc
# This is for building auxiliary programs like memusage, nscd
# For initial glibc bootstraps it can be commented out
BuildRequires: gd-devel libpng-devel zlib-devel texinfo, libselinux-devel >= 1.33.4-3
BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext, nss-devel
BuildRequires: /bin/ps, /bin/kill, /bin/awk
%ifarch %{systemtaparches}
BuildRequires: systemtap-sdt-devel
%endif
# This is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildRequires: gcc >= 3.2
%define enablekernel 2.6.18
%ifarch i386
%define nptl_target_cpu i486
%else
%define nptl_target_cpu %{_target_cpu}
%endif
%ifarch %{multiarcharches}
# Need STT_IFUNC support
%ifarch ppc ppc64
BuildRequires: binutils >= 2.20.51.0.2
Conflicts: binutils < 2.20.51.0.2
%else
BuildRequires: binutils >= 2.19.51.0.10
Conflicts: binutils < 2.19.51.0.10
%endif
# Earlier releases have broken support for IRELATIVE relocations
Conflicts: prelink < 0.4.2
%else
# Need AS_NEEDED directive
# Need --hash-style=* support
BuildRequires: binutils >= 2.17.50.0.2-5
%endif
BuildRequires: gcc >= 3.2.1-5
%ifarch ppc s390 s390x
BuildRequires: gcc >= 4.1.0-0.17
%endif
%if 0%{?_enable_debug_packages}
BuildRequires: elfutils >= 0.72
BuildRequires: rpm >= 4.2-0.56
%endif
%define __find_provides %{_builddir}/%{glibcsrcdir}/find_provides.sh
%define _filter_GLIBC_PRIVATE 1

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

%if %{xenpackage}
%package xen
Summary: The GNU libc libraries (optimized for running under Xen)
Group: System Environment/Libraries
Requires: glibc = %{version}-%{release}, glibc-utils = %{version}-%{release}

%description xen
The standard glibc package is optimized for native kernels and does not
perform as well under the Xen hypervisor.  This package provides alternative
library binaries that will be selected instead when running under Xen.

Install glibc-xen if you might run your system under the Xen hypervisor.
%endif

%package devel
Summary: Object files for development using standard C libraries.
Group: Development/Libraries
Requires(pre): /sbin/install-info
Requires(pre): %{name}-headers
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

%package static
Summary: C library static libraries for -static linking.
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

%package headers
Summary: Header files for development using standard C libraries.
Group: Development/Libraries
Provides: %{name}-headers(%{_target_cpu})
%ifarch x86_64
# If both -m32 and -m64 is to be supported on AMD64, x86_64 glibc-headers
# have to be installed, not i586 ones.
Obsoletes: %{name}-headers(i586)
Obsoletes: %{name}-headers(i686)
%endif
Requires(pre): kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}-%{release}
BuildRequires: kernel-headers >= 2.6.22

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2015g-4
Group: System Environment/Base

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

%package -n nscd
Summary: A Name Service Caching Daemon (nscd).
Group: System Environment/Daemons
Requires: libselinux >= 1.17.10-1, audit-libs >= 1.1.3
Requires: %{name} = %{version}-%{release}
Requires(pre): /sbin/chkconfig, /usr/sbin/useradd, /usr/sbin/userdel, sh-utils

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well.

%package utils
Summary: Development utilities from GNU C library
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%define __debug_install_post %{nil}
%global __debug_package 1

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: no
%ifarch %{debuginfocommonarches}
Requires: glibc-debuginfo-common = %{version}-%{release}
%else
%ifarch %{ix86}
Obsoletes: glibc-debuginfo-common
%endif
%endif

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

This package also contains static standard C libraries with
debugging information.  You need this only if you want to step into
C library routines during debugging programs statically linked against
one or more of the standard C libraries.
To use this debugging information, you need to link binaries
with -static -L%{_prefix}/lib/debug%{_prefix}/%{_lib} compiler options.

%ifarch %{debuginfocommonarches}

%package debuginfo-common
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: no

%description debuginfo-common
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%endif
%endif

%prep
%setup -q -n %{glibcsrcdir} -b1
%patch0 -E -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch95 -p1
%patch96 -p1
%patch97 -p1
%patch99 -p1
%patch100 -p1
%patch101 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1
%patch137 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch145 -p1
%patch146 -p1
%patch147 -p1
%patch148 -p1
%patch150 -p1
%patch151 -p1
%patch152 -p1
%patch153 -p1
%patch154 -p1
%patch155 -p1
%patch156 -p1
%patch157 -p1
%patch158 -p1
%patch159 -p1
%patch160 -p1
%patch161 -p1
%patch162 -p1
%patch163 -p1
%patch164 -p1
%patch165 -p1
%patch166 -p1
%patch167 -p1
%patch168 -p1
%patch169 -p1
%patch170 -p1
%patch171 -p1
%patch172 -p1
%patch173 -p1
%patch174 -p1
%patch175 -p1
%patch176 -p1
%patch177 -p1
%patch178 -p1
%patch179 -p1
%patch180 -p1
%patch181 -p1
%patch182 -p1
%patch183 -p1
%patch184 -p1
%patch185 -p1
%patch186 -p1
%patch187 -p1
%patch188 -p1
%patch189 -p1
%patch190 -p1
%patch191 -p1
%patch192 -p1
%patch193 -p1
%patch194 -p1
%patch195 -p1
%patch196 -p1
%patch197 -p1
%patch198 -p1
%patch199 -p1
%patch200 -p1
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1
%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
%patch209 -p1
%patch210 -p1
%patch211 -p1
%patch212 -p1
%patch213 -p1
%patch214 -p1
%patch215 -p1
%patch216 -p1
%patch217 -p1
%patch218 -p1
%patch219 -p1
%patch220 -p1
%patch221 -p1
%patch222 -p1
%patch223 -p1
%patch224 -p1
%patch225 -p1
%patch226 -p1
%patch227 -p1
%patch228 -p1
%patch229 -p1
%patch230 -p1
%patch231 -p1
%patch232 -p1
%patch233 -p1
%patch234 -p1
%patch235 -p1
%patch236 -p1
%patch237 -p1
%patch238 -p1
%patch239 -p1
%patch240 -p1
%patch241 -p1
%patch242 -p1
%patch243 -p1
%patch244 -p1
%patch245 -p1
%patch246 -p1
%patch247 -p1
%patch248 -p1
%patch249 -p1
%patch250 -p1
%patch251 -p1
%patch252 -p1
%patch253 -p1

# A lot of programs still misuse memcpy when they have to use
# memmove. The memcpy implementation below is not tolerant at
# all.
rm -f sysdeps/alpha/alphaev6/memcpy.S
%if %{buildpower6}
# On powerpc32, hp timing is only available in power4/power6
# libs, not in base, so pre-power4 dynamic linker is incompatible
# with power6 libs.
rm -f sysdeps/powerpc/powerpc32/power4/hp-timing.[ch]
%endif

find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;
cat > find_provides.sh <<EOF
#!/bin/sh
/usr/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
exit 0
EOF
chmod +x find_provides.sh
touch `find . -name configure`
touch locale/programs/*-kw.h

%build
# Log system information
uname -a
cat /proc/cpuinfo
cat /proc/meminfo
df || true

GCC=gcc
GXX=g++
%ifarch %{ix86}
BuildFlags="-march=%{nptl_target_cpu} -mtune=generic"
%endif
%ifarch i686
BuildFlags="-march=i686 -mtune=generic"
%endif
%ifarch i386 i486 i586
BuildFlags="$BuildFlags -mno-tls-direct-seg-refs"
%endif
%ifarch x86_64
BuildFlags="-mtune=generic"
%endif
%ifarch alphaev6
BuildFlags="-mcpu=ev6"
%endif
%ifarch sparc
BuildFlags="-fcall-used-g6"
GCC="gcc -m32"
GXX="g++ -m32"
%endif
%ifarch sparcv9
BuildFlags="-mcpu=ultrasparc -fcall-used-g6"
GCC="gcc -m32"
GXX="g++ -m32"
%endif
%ifarch sparcv9v
BuildFlags="-mcpu=niagara -fcall-used-g6"
GCC="gcc -m32"
GXX="g++ -m32"
%endif
%ifarch sparc64
BuildFlags="-mcpu=ultrasparc -mvis -fcall-used-g6"
GCC="gcc -m64"
GXX="g++ -m64"
%endif
%ifarch sparc64v
BuildFlags="-mcpu=niagara -mvis -fcall-used-g6"
GCC="gcc -m64"
GXX="g++ -m64"
%endif
%ifarch ppc64
BuildFlags="-mno-minimal-toc"
GCC="gcc -m64"
GXX="g++ -m64"
%endif

BuildFlags="$BuildFlags -fasynchronous-unwind-tables"
# Add -DNDEBUG unless using a prerelease
case %{version} in
  *.*.9[0-9]*) ;;
  *)
     BuildFlags="$BuildFlags -DNDEBUG"
     ;;
esac
EnableKernel="--enable-kernel=%{enablekernel}"
echo "$GCC" > Gcc
AddOns=`echo */configure | sed -e 's!/configure!!g;s!\(linuxthreads\|nptl\|rtkaio\|powerpc-cpu\)\( \|$\)!!g;s! \+$!!;s! !,!g;s!^!,!;/^,\*$/d'`
%ifarch %{rtkaioarches}
AddOns=,rtkaio$AddOns
%endif

build_nptl()
{
builddir=build-%{nptl_target_cpu}-$1
shift
rm -rf $builddir
mkdir $builddir ; cd $builddir
build_CFLAGS="$BuildFlags -g -O3 $*"
../configure CC="$GCC" CXX="$GXX" CFLAGS="$build_CFLAGS" \
	--prefix=%{_prefix} \
	--enable-add-ons=nptl$AddOns --without-cvs $EnableKernel \
	--with-headers=%{_prefix}/include --enable-bind-now \
	--with-tls --with-__thread --build %{nptl_target_cpu}-redhat-linux \
	--host %{nptl_target_cpu}-redhat-linux \
%ifarch %{multiarcharches}
	--enable-multi-arch \
%endif
%ifarch %{systemtaparches}
	--enable-systemtap \
%endif
	--disable-profile --enable-experimental-malloc --enable-nss-crypt

make %{?_smp_mflags} -r CFLAGS="$build_CFLAGS"

cd ..
}

build_nptl linuxnptl

%if %{buildxen}
build_nptl linuxnptl-nosegneg -mno-tls-direct-seg-refs
%endif

%if %{buildpower6}
(
platform=`LD_SHOW_AUXV=1 /bin/true | sed -n 's/^AT_PLATFORM:[[:blank:]]*//p'`
if [ "$platform" != power6 ]; then
  mkdir -p power6emul/{lib,lib64}
  $GCC -shared -O2 -fpic -o power6emul/%{_lib}/power6emul.so releng/power6emul.c -Wl,-z,initfirst
%ifarch ppc
  gcc -shared -nostdlib -O2 -fpic -m64 -o power6emul/lib64/power6emul.so -xc - </dev/null
%endif
%ifarch ppc64
  gcc -shared -nostdlib -O2 -fpic -m32 -o power6emul/lib/power6emul.so -xc - < /dev/null
%endif
  export LD_PRELOAD=`pwd`/power6emul/\$LIB/power6emul.so
fi
AddOns="$AddOns --with-cpu=power6"
GCC="$GCC -mcpu=power6"
GXX="$GXX -mcpu=power6"
build_nptl linuxnptl-power6
)
%endif

cd build-%{nptl_target_cpu}-linuxnptl
$GCC -static -L. -Os -g ../releng/glibc_post_upgrade.c -o glibc_post_upgrade.%{_target_cpu} \
  -DNO_SIZE_OPTIMIZATION \
%ifarch i386 i486 i586
  -DARCH_386 \
%endif
  '-DLIBTLS="/%{_lib}/tls/"' \
  '-DGCONV_MODULES_DIR="%{_prefix}/%{_lib}/gconv"' \
  '-DLD_SO_CONF="/etc/ld.so.conf"' \
  '-DICONVCONFIG="%{_sbindir}/iconvconfig.%{_target_cpu}"'
cd ..

%install
GCC=`cat Gcc`

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make -j1 install_root=$RPM_BUILD_ROOT install -C build-%{nptl_target_cpu}-linuxnptl
chmod +x $RPM_BUILD_ROOT%{_prefix}/libexec/pt_chown
%ifnarch %{auxarches}
cd build-%{nptl_target_cpu}-linuxnptl && \
  make %{?_smp_mflags} install_root=$RPM_BUILD_ROOT install-locales -C ../localedata objdir=`pwd` && \
  cd ..
%endif

librtso=`basename $RPM_BUILD_ROOT/%{_lib}/librt.so.*`

%ifarch %{rtkaioarches}
rm -f $RPM_BUILD_ROOT{,%{_prefix}}/%{_lib}/librtkaio.*
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/librt.so.*
mkdir -p $RPM_BUILD_ROOT/%{_lib}/rtkaio
mv $RPM_BUILD_ROOT/%{_lib}/librtkaio-*.so $RPM_BUILD_ROOT/%{_lib}/rtkaio/
rm -f $RPM_BUILD_ROOT/%{_lib}/$librtso
ln -sf `basename $RPM_BUILD_ROOT/%{_lib}/librt-*.so` $RPM_BUILD_ROOT/%{_lib}/$librtso
ln -sf `basename $RPM_BUILD_ROOT/%{_lib}/rtkaio/librtkaio-*.so` $RPM_BUILD_ROOT/%{_lib}/rtkaio/$librtso
%endif

%if %{buildxen}
%define nosegneg_subdir_base i686
%define nosegneg_subdir i686/nosegneg
%define nosegneg_subdir_up ../..
cd build-%{nptl_target_cpu}-linuxnptl-nosegneg
destdir=$RPM_BUILD_ROOT/%{_lib}/%{nosegneg_subdir}
mkdir -p $destdir
for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
do
  libbase=${lib#*/}
  libbaseso=$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}-*.so)
  # Only install if different from base lib
  if cmp -s ${lib}.so ../build-%{nptl_target_cpu}-linuxnptl/${lib}.so; then
    ln -sf %{nosegneg_subdir_up}/$libbaseso $destdir/$libbaseso
  else
    cp -a ${lib}.so $destdir/$libbaseso
  fi
  ln -sf $libbaseso $destdir/$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}.so.*)
done
%ifarch %{rtkaioarches}
destdir=$RPM_BUILD_ROOT/%{_lib}/rtkaio/%{nosegneg_subdir}
mkdir -p $destdir
librtkaioso=$(basename $RPM_BUILD_ROOT/%{_lib}/librt-*.so | sed s/librt-/librtkaio-/)
if cmp -s rtkaio/librtkaio.so ../build-%{nptl_target_cpu}-linuxnptl/rtkaio/librtkaio.so; then
  ln -s %{nosegneg_subdir_up}/$librtkaioso $destdir/$librtkaioso
else
  cp -a rtkaio/librtkaio.so $destdir/$librtkaioso
fi
ln -sf $librtkaioso $destdir/$librtso
%endif
cd ..
%endif

%if %{buildpower6}
cd build-%{nptl_target_cpu}-linuxnptl-power6
destdir=$RPM_BUILD_ROOT/%{_lib}/power6
mkdir -p ${destdir}
for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
do
  libbase=${lib#*/}
  libbaseso=$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}-*.so)
  cp -a ${lib}.so $destdir/$libbaseso
  ln -sf $libbaseso $destdir/$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}.so.*)
done
mkdir -p ${destdir}x
pushd ${destdir}x
ln -sf ../power6/*.so .
cp -a ../power6/*.so.* .
popd
%ifarch %{rtkaioarches}
destdir=$RPM_BUILD_ROOT/%{_lib}/rtkaio/power6
mkdir -p $destdir
librtkaioso=$(basename $RPM_BUILD_ROOT/%{_lib}/librt-*.so | sed s/librt-/librtkaio-/)
cp -a rtkaio/librtkaio.so $destdir/$librtkaioso
ln -sf $librtkaioso $destdir/$librtso
mkdir -p ${destdir}x
pushd ${destdir}x
ln -sf ../power6/*.so .
cp -a ../power6/*.so.* .
popd
%endif
cd ..
%endif

# Remove the files we don't want to distribute
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libNoVersion*
rm -f $RPM_BUILD_ROOT/%{_lib}/libNoVersion*

# NPTL <bits/stdio-lock.h> is not usable outside of glibc, so include
# the generic one (#162634)
cp -a bits/stdio-lock.h $RPM_BUILD_ROOT%{_prefix}/include/bits/stdio-lock.h
# And <bits/libc-lock.h> needs sanitizing as well.
cp -a releng/libc-lock.h $RPM_BUILD_ROOT%{_prefix}/include/bits/libc-lock.h

if [ -d $RPM_BUILD_ROOT%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p $RPM_BUILD_ROOT%{_infodir}
  mv -f $RPM_BUILD_ROOT%{_prefix}/info/* $RPM_BUILD_ROOT%{_infodir}
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info
fi

gzip -9nvf $RPM_BUILD_ROOT%{_infodir}/libc*

ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libbsd.a

install -p -m 644 releng/nsswitch.conf $RPM_BUILD_ROOT/etc/nsswitch.conf

mkdir -p $RPM_BUILD_ROOT/etc/default
install -p -m 644 nis/nss $RPM_BUILD_ROOT/etc/default/nss

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 nscd/nscd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd

# Don't include ld.so.cache
rm -f $RPM_BUILD_ROOT/etc/ld.so.cache

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
> $RPM_BUILD_ROOT/etc/ld.so.cache
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
> $RPM_BUILD_ROOT/etc/sysconfig/nscd
> $RPM_BUILD_ROOT/etc/gai.conf

# Include %{_prefix}/%{_lib}/gconv/gconv-modules.cache
> $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache

# Install the upgrade program
install -m 700 build-%{nptl_target_cpu}-linuxnptl/glibc_post_upgrade.%{_target_cpu} \
  $RPM_BUILD_ROOT/usr/sbin/glibc_post_upgrade.%{_target_cpu}

strip -g $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.o

%if 0%{?_enable_debug_packages}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}
cp -a $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.a \
  $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}/
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/%{_lib}/*_p.a
%endif

# rquota.x and rquota.h are now provided by quota
rm -f $RPM_BUILD_ROOT%{_prefix}/include/rpcsvc/rquota.[hx]

# Create archive of locale files
%ifnarch %{auxarches}
olddir=`pwd`
pushd ${RPM_BUILD_ROOT}%{_prefix}/lib/locale
rm locale-archive || :
# Intentionally we do not pass --alias-file=, aliases will be added
# by build-locale-archive.
$olddir/build-%{nptl_target_cpu}-linuxnptl/elf/ld.so \
  --library-path $olddir/build-%{nptl_target_cpu}-linuxnptl/ \
  $olddir/build-%{nptl_target_cpu}-linuxnptl/locale/localedef \
    --prefix ${RPM_BUILD_ROOT} --add-to-archive \
    *_*
rm -rf *_*
mv locale-archive{,.tmpl}
popd
%endif

rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss-*.so.1

# Ugly hack for buggy rpm
ln -f ${RPM_BUILD_ROOT}%{_sbindir}/iconvconfig{,.%{_target_cpu}}

# In F7+ this is provided by rpcbind rpm
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# BUILD THE FILE LIST
{
  find $RPM_BUILD_ROOT \( -type f -o -type l \) \
       \( \
	 -name etc -printf "%%%%config " -o \
	 -name gconv-modules \
	 -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " -o \
	 -name gconv-modules.cache \
	 -printf "%%%%verify(not md5 size mtime) " \
	 , \
	 ! -path "*/lib/debug/*" -printf "/%%P\n" \)
  find $RPM_BUILD_ROOT -type d \
       \( -path '*%{_prefix}/share/*' ! -path '*%{_infodir}' -o \
	  -path "*%{_prefix}/include/*" \
       \) -printf "%%%%dir /%%P\n"
} | {

  # primary filelist
  SHARE_LANG='s|.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo|%lang(\1) &|'
  LIB_LANG='s|.*/lib/locale/\([^/_]\+\)|%lang(\1) &|'
  # rpm does not handle %lang() tagged files hardlinked together accross
  # languages very well, temporarily disable
  LIB_LANG=''
  sed -e "$LIB_LANG" -e "$SHARE_LANG" \
      -e '\,/etc/\(localtime\|gai\.conf\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\),d' \
      -e '\,/%{_lib}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > rpm.filelist

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}
mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}
for i in $RPM_BUILD_ROOT%{_prefix}/bin/{xtrace,memusage}; do
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_prefix}/%{_lib}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_prefix}/%{_lib}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
      -i $i
done

grep '%{_infodir}' < rpm.filelist | grep -v '%{_infodir}/dir' > devel.filelist
grep '%{_prefix}/include/gnu/stubs-[32164]\+\.h' < rpm.filelist >> devel.filelist || :

grep '%{_prefix}/include' < rpm.filelist |
  egrep -v '%{_prefix}/include/(linuxthreads|gnu/stubs-[32164]+\.h)' \
	> headers.filelist

sed -i -e '\|%{_prefix}/%{_lib}/lib.*_p.a|d' \
       -e '\|%{_prefix}/include|d' \
       -e '\|%{_infodir}|d' rpm.filelist

grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist \
  | grep '/lib\(\(c\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  > static.filelist
grep '%{_prefix}/%{_lib}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.so' < rpm.filelist >> devel.filelist

sed -i -e '\|%{_prefix}/%{_lib}/lib.*\.a|d' \
       -e '\|%{_prefix}/%{_lib}/.*\.o|d' \
       -e '\|%{_prefix}/%{_lib}/lib.*\.so|d' \
       -e '\|%{_prefix}/%{_lib}/linuxthreads|d' \
       -e '\|nscd|d' rpm.filelist

grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
#grep '%{_prefix}/lib/locale' < rpm.filelist | grep -v /locale-archive.tmpl >> common.filelist
#grep '%{_prefix}/libexec/pt_chown' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
grep '%{_prefix}/share' < rpm.filelist | \
  grep -v -e '%{_prefix}/share/zoneinfo' -e '%%dir %{prefix}/share' \
       >> common.filelist

sed -i -e '\|%{_prefix}/bin|d' \
       -e '\|%{_prefix}/lib/locale|d' \
       -e '\|%{_prefix}/libexec/pt_chown|d' \
       -e '\|%{_prefix}/sbin/[^gi]|d' \
       -e '\|%{_prefix}/share|d' rpm.filelist

> nosegneg.filelist
%if %{xenpackage}
grep '/%{_lib}/%{nosegneg_subdir}' < rpm.filelist >> nosegneg.filelist
sed -i -e '\|/%{_lib}/%{nosegneg_subdir}|d' rpm.filelist
%endif

echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist
echo '%{_prefix}/sbin/nscd' > nscd.filelist

cat >> rpm.filelist <<EOF
%{_prefix}/%{_lib}/libmemusage.so
%{_prefix}/%{_lib}/libpcprofile.so
EOF

cat > utils.filelist <<EOF
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp
touch -r releng/glibc.spec.in $RPM_BUILD_ROOT/etc/ld.so.conf
touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT/etc/rpc

cd releng
$GCC -Os -g -static -o build-locale-archive build-locale-archive.c \
  ../build-%{nptl_target_cpu}-linuxnptl/locale/locarchive.o \
  ../build-%{nptl_target_cpu}-linuxnptl/locale/md5.o \
  -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
  -L../build-%{nptl_target_cpu}-linuxnptl
install -m 700 build-locale-archive $RPM_BUILD_ROOT/usr/sbin/build-locale-archive
cd ..

# the last bit: more documentation
rm -rf documentation
mkdir documentation
cp crypt/README.ufc-crypt documentation/README.ufc-crypt
cp timezone/README documentation/README.timezone
cp ChangeLog{,.15,.16} documentation
bzip2 -9 documentation/ChangeLog*
cp posix/gai.conf documentation/

%ifarch s390x
# Compatibility symlink
mkdir -p $RPM_BUILD_ROOT/lib
ln -sf /%{_lib}/ld64.so.1 $RPM_BUILD_ROOT/lib/ld64.so.1
%endif

%if %{run_glibc_tests}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================
cd build-%{nptl_target_cpu}-linuxnptl
( make %{?_smp_mflags} -k check 2>&1
  sleep 10s
  teepid="`ps -eo ppid,pid,command | awk '($1 == '${parent}' && $3 ~ /^tee/) { print $2 }'`"
  [ -n "$teepid" ] && kill $teepid
) | tee check.log || :
cd ..
%if %{buildxen}
echo ====================TESTING -mno-tls-direct-seg-refs=============
cd build-%{nptl_target_cpu}-linuxnptl-nosegneg
( make %{?_smp_mflags} -k check 2>&1
  sleep 10s
  teepid="`ps -eo ppid,pid,command | awk '($1 == '${parent}' && $3 ~ /^tee/) { print $2 }'`"
  [ -n "$teepid" ] && kill $teepid
) | tee check.log || :
cd ..
%endif
%if %{buildpower6}
echo ====================TESTING -mcpu=power6=============
cd build-%{nptl_target_cpu}-linuxnptl-power6
( if [ -d ../power6emul ]; then
    export LD_PRELOAD=`cd ../power6emul; pwd`/\$LIB/power6emul.so
  fi
  make %{?_smp_mflags} -k check 2>&1
  sleep 10s
  teepid="`ps -eo ppid,pid,command | awk '($1 == '${parent}' && $3 ~ /^tee/) { print $2 }'`"
  [ -n "$teepid" ] && kill $teepid
) | tee check.log || :
cd ..
%endif
echo ====================TESTING DETAILS=================
for i in `sed -n 's|^.*\*\*\* \[\([^]]*\.out\)\].*$|\1|p' build-*-linux*/check.log`; do
  echo =====$i=====
  cat $i || :
  echo ============
done
echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

%endif

pushd $RPM_BUILD_ROOT/usr/%{_lib}/
$GCC -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
rm libpthread.a
ar rcs libpthread.a libpthread.o
rm libpthread.o
popd

%if 0%{?_enable_debug_packages}

# The #line directives gperf generates do not give the proper
# file name relative to the build directory.
(cd locale; ln -s programs/*.gperf .)
(cd iconv; ln -s ../locale/programs/charmap-kw.gperf .)

ls -l $RPM_BUILD_ROOT/usr/bin/getconf
ls -l $RPM_BUILD_ROOT/usr/libexec/getconf
eu-readelf -hS $RPM_BUILD_ROOT/usr/bin/getconf $RPM_BUILD_ROOT/usr/libexec/getconf/*

find_debuginfo_args='--strict-build-id -g'
%ifarch %{debuginfocommonarches}
echo %{_prefix}/libexec/pt_chown > workaround.filelist
find_debuginfo_args="$find_debuginfo_args \
  -l common.filelist -l utils.filelist -l nscd.filelist -l workaround.filelist \
  -p '.*/(sbin|libexec)/.*' \
  -o debuginfocommon.filelist \
  -l rpm.filelist -l nosegneg.filelist \
"
%endif
eval /usr/lib/rpm/find-debuginfo.sh "$find_debuginfo_args" -o debuginfo.filelist

list_debug_archives()
{
  local dir=%{_prefix}/lib/debug%{_prefix}/%{_lib}
  find $RPM_BUILD_ROOT$dir -name "*.a" -printf "$dir/%%P\n"
}

%ifarch %{debuginfocommonarches}

sed -i '\#^%{_prefix}/src/debug/#d' debuginfocommon.filelist
find $RPM_BUILD_ROOT%{_prefix}/src/debug \
     \( -type d -printf '%%%%dir ' \) , \
     -printf '%{_prefix}/src/debug/%%P\n' > debuginfocommon.sources

%ifarch %{biarcharches}

cat debuginfocommon.sources >> debuginfo.filelist

%else

%ifarch %{ix86}
%define basearch i686
%endif
%ifarch alpha alphaev6
%define basearch alpha
%endif
%ifarch sparc sparcv9
%define basearch sparc
%endif

# auxarches get only these few source files
auxarches_debugsources=\
'/(generic|linux|%{basearch}|nptl(_db)?)/|/%{glibcsrcdir}/build|/dl-osinfo\.h'

egrep "$auxarches_debugsources" debuginfocommon.sources >> debuginfo.filelist

egrep -v "$auxarches_debugsources" \
  debuginfocommon.sources >> debuginfocommon.filelist
%ifnarch %{auxarches}
# non-aux arches when there is a debuginfo-common
# all the sources go into debuginfo-common
#cat debuginfocommon.sources >> debuginfocommon.filelist
%endif

%endif

list_debug_archives >> debuginfocommon.filelist

%else

# already found by find-debuginfo
#list_debug_archives >> debuginfo.filelist

%endif

%endif

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%ifarch %{auxarches}

echo Cutting down the list of unpackaged files
>> debuginfocommon.filelist
sed -e '/%%dir/d;/%%config/d;/%%verify/d;s/%%lang([^)]*) //;s#^/*##' \
    common.filelist devel.filelist static.filelist headers.filelist \
    utils.filelist nscd.filelist debuginfocommon.filelist |
(cd $RPM_BUILD_ROOT; xargs --no-run-if-empty rm -f 2> /dev/null || :)

%else

mkdir -p $RPM_BUILD_ROOT/var/{db,run}/nscd
touch $RPM_BUILD_ROOT/var/{db,run}/nscd/{passwd,group,hosts,services}
touch $RPM_BUILD_ROOT/var/run/nscd/{socket,nscd.pid}
%endif

%ifnarch %{auxarches}
> $RPM_BUILD_ROOT/%{_prefix}/lib/locale/locale-archive
%endif

mkdir -p $RPM_BUILD_ROOT/var/cache/ldconfig
> $RPM_BUILD_ROOT/var/cache/ldconfig/aux-cache

%post -p /usr/sbin/glibc_post_upgrade.%{_target_cpu}

%postun -p /sbin/ldconfig

%post common -p /usr/sbin/build-locale-archive

%post devel
/sbin/install-info %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
fi

%post utils -p /sbin/ldconfig

%postun utils -p /sbin/ldconfig

%pre -n nscd
getent group nscd >/dev/null || /usr/sbin/groupadd -g 28 -r nscd
getent passwd nscd >/dev/null ||
  /usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
		    -c "NSCD Daemon" -u 28 -g nscd nscd

%post -n nscd
/sbin/chkconfig --add nscd

%preun -n nscd
if [ $1 = 0 ] ; then
  service nscd stop > /dev/null 2>&1
  /sbin/chkconfig --del nscd
fi

%postun -n nscd
if [ $1 = 0 ] ; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
if [ "$1" -ge "1" ]; then
  service nscd condrestart > /dev/null 2>&1 || :
fi

%if %{xenpackage}
%post xen -p /sbin/ldconfig
%postun xen -p /sbin/ldconfig
%endif

%clean
rm -rf "$RPM_BUILD_ROOT"
rm -f *.filelist*

%files -f rpm.filelist
%defattr(-,root,root)
%ifarch %{rtkaioarches}
%dir /%{_lib}/rtkaio
%endif
%if %{buildxen} && !%{xenpackage}
%dir /%{_lib}/%{nosegneg_subdir_base}
%dir /%{_lib}/%{nosegneg_subdir}
%ifarch %{rtkaioarches}
%dir /%{_lib}/rtkaio/%{nosegneg_subdir_base}
%dir /%{_lib}/rtkaio/%{nosegneg_subdir}
%endif
%endif
%if %{buildpower6}
%dir /%{_lib}/power6
%dir /%{_lib}/power6x
%ifarch %{rtkaioarches}
%dir /%{_lib}/rtkaio/power6
%dir /%{_lib}/rtkaio/power6x
%endif
%endif
%ifarch s390x
/lib/ld64.so.1
%endif
%verify(not md5 size mtime) %config(noreplace) /etc/rpc
%verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/localtime
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_prefix}/%{_lib}/gconv
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS CONFORMANCE
%doc COPYING COPYING.LIB README.libm LICENSES
%doc hesiod/README.hesiod
%attr(0644,root,root) %verify(not md5 size mtime) %config(missingok,noreplace) /etc/gai.conf

%if %{xenpackage}
%files -f nosegneg.filelist xen
%defattr(-,root,root)
%dir /%{_lib}/%{nosegneg_subdir_base}
%dir /%{_lib}/%{nosegneg_subdir}
%endif

%ifnarch %{auxarches}
%files -f common.filelist common
%defattr(-,root,root)
%attr(0644,root,root) %verify(not md5 size mtime) %{_prefix}/lib/locale/locale-archive.tmpl
%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/lib/locale/locale-archive
%dir %attr(755,root,root) /etc/default
%verify(not md5 size mtime) %config(noreplace) /etc/default/nss
%attr(4711,root,root) %{_prefix}/libexec/pt_chown
%doc documentation/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f static.filelist static
%defattr(-,root,root)

%files -f headers.filelist headers
%defattr(-,root,root)

%files -f utils.filelist utils
%defattr(-,root,root)

%files -f nscd.filelist -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%config /etc/rc.d/init.d/nscd
%dir %attr(0755,root,root) /var/run/nscd
%dir %attr(0755,root,root) /var/db/nscd
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
%endif

%if 0%{?_enable_debug_packages}
%files debuginfo -f debuginfo.filelist
%defattr(-,root,root)
%ifarch %{debuginfocommonarches}
%ifnarch %{auxarches}
%files debuginfo-common -f debuginfocommon.filelist
%defattr(-,root,root)
%endif
%endif
%endif

%changelog
* Mon Apr  1 2019 Florian Weimer <fweimer@redhat.com> - 2.12-1.212.3
- Remove abort() warning in manual (#1577437)

* Mon Apr  1 2019 Florian Weimer <fweimer@redhat.com> - 2.12-1.212.2
- ja_JP: Add new Japanese Era name (#1555930)

* Mon Apr  1 2019 Florian Weimer <fweimer@redhat.com> - 2.12-1.212.1
- regex: Fix false match in trailing characters (#1668169)

* Fri Nov 17 2017 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.212
- CVE-2017-15670: glob: Fix one-byte overflow with GLOB_TILDE (#1504810)
- CVE-2017-15804: glob: Fix buffer overflow in GLOB_TILDE unescaping (#1504810)

* Mon Jun 19 2017 Florian Weimer <fweimer@redhat.com> - 2.12-1.211
- Avoid large allocas in the dynamic linker (#1452717)

* Wed Mar 29 2017 Carlos O'Donell <carlos@redhat.com> - 2.12-1.210
- Fix thread cancellation issues for setmntent() and others (#1437147).

* Wed Jan 25 2017 Florian Weimer <fweimer@redhat.com> - 2.12-1.209
- Fix AF_INET6 getaddrinfo with nscd (#1416496)

* Tue Oct 18 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.208
- Update tests for struct sockaddr_storage changes (#1338673)

* Mon Oct 17 2016 Martin Sebor <msebor@redhat.com> - 2.12-1.207
- Use FL_CLOEXEC in internal calls to fopen (#1012343).

* Mon Oct 17 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.206
- Fix CVE-2015-8779 glibc: Unbounded stack allocation in catopen function
  (#1358015).

* Mon Oct 17 2016 DJ Delorie <dj@redhat.com> - 2.12-1.205
- Make padding in struct sockaddr_storage explicit (#1338673)

* Thu Oct 13 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.204
- Fix detection of Intel FMA hardware (#1384281).

* Tue Oct 11 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.203
- Add support for el_GR@euro, ur_IN, and wal_ET locales (#1101858).

* Tue Oct 11 2016 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.202
- Change malloc/tst-malloc-thread-exit.c to use fewer threads and 
  avoid timeout (#1318380).

* Tue Oct 11 2016 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.201
- df can fail on some systems (#1307029).

* Wed Sep 21 2016 DJ Delorie <dj@redhat.com> - 2.12-1.200
- Log uname, cpuinfo, meminfo during build (#1307029).

* Mon Sep 12 2016 DJ Delorie <dj@redhat.com> - 2.12-1.199
- Draw graphs for heap and stack only if MAXSIZE_HEAP and MAXSIZE_STACK
  are non-zero (#1331304).

* Mon Sep 12 2016 DJ Delorie <dj@redhat.com> - 2.12-1.198
- Avoid unneeded calls to __check_pf in getadddrinfo (#1270950)

* Mon Sep 12 2016 Martin Sebor <msebor@redhat.com> - 2.12-1.197
- Fix CVE-2015-8778 glibc: Integer overflow in hcreate and hcreate_r
  (#1358013).

* Mon Sep 12 2016 Martin Sebor <msebor@redhat.com> - 2.12-1.196
- Fix CVE-2015-8776 glibc: Segmentation fault caused by passing
  out-of-range data to strftime() (#1358011).

* Mon Sep 12 2016 Florian Weimer <fweimer@redhat.com> - 2.12-1.195
- tzdata-update: Ignore umask setting (#1373646)

* Thu Sep  8 2016 Florian Weimer <fweimer@redhat.com> - 2.12-1.194
- CVE-2014-9761: Fix unbounded stack allocation in nan* (#1358014)

* Thu Feb  4 2016 Florian Weimer <fweimer@redhat.com> - 2.12-1.193
- Avoid using uninitialized data in getaddrinfo (#1223095)

* Thu Jan 28 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.192
- Update fix for CVE-2015-7547 (#1296029).

* Sat Jan 23 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.191
- Create helper threads with enough stack for POSIX AIO and timers (#1299319).

* Thu Jan 14 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.190
- Fix CVE-2015-7547: getaddrinfo() stack-based buffer overflow (#1296029).
- Update malloc free_list cyclic fix (#1264189).
- Update tzdata-update changes (#1200555).

* Wed Jan 13 2016 Carlos O'Donell <carlos@redhat.com> - 2.12-1.189
- Avoid redundant shift character in iconv output at block boundary (#1293914).

* Tue Dec 22 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.188
- Clean up testsuite results when testing with newer kernels (#1293464).

* Tue Dec 22 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.187
- Do not rewrite /etc/localtime if it is a symbolic link.  (#1200555)

* Mon Dec 21 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.186
- Support long lines in /etc/hosts (#1020263).

* Mon Dec 21 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.185
- Avoid aliasing warning in tst-rec-dlopen (#1291444)

* Mon Dec 14 2015 Marek Polacek <polacek@redhat.com> - 2.12-1.184
- Don't touch user-controlled stdio locks in forked child (#1275384).

* Mon Dec 14 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.183
- Increase the limit of shared libraries that can use static TLS (#1198802).

* Mon Dec 14 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.182
- Avoid PLT in libm for feupdateenv (#1186104).
- Allow PLT entry in libc for _Unwind_Find_FDE on s390/s390x (#1186104).

* Fri Dec 11 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.181
- Provide /etc/gai.conf only in the glibc package.  (#1223818)

* Fri Dec 11 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.180
- Change first day of the week to Monday for the ca_ES locale.  (#1011900)

* Fri Dec 11 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.179
- Update BIG5-HKSCS charmap to HKSCS-2008.  (#1211748)

* Fri Dec 11 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.178
- Rename Oriya locale to Odia.  (#1091334)

* Fri Dec 11 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.177
- Avoid hang in gethostbyname_r due to missing mutex unlocking (#1192621)

* Fri Dec 11 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.176
- Avoid ld.so crash when audit modules provide path (#1211098)

* Fri Dec 11 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.175
- Suppress expected backtrace in tst-malloc-backtrace (#1276633)

* Mon Dec  7 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.174
- Avoid PLT for memmem (#1186104).

* Fri Nov  6 2015 Marek Polacek <polacek@redhat.com> - 2.12-1.173
- Fix up a missing dependency in the Makefile (#1219627).

* Fri Nov  6 2015 Marek Polacek <polacek@redhat.com> - 2.12-1.172
- Reduce lock contention in __tz_convert (#1244585).

* Fri Oct 30 2015 Florian Weimer <fweimer@redhat.com> - 2.12-1.171
- Prevent the malloc arena free list from becoming cyclic (#1264189)

* Thu Sep 17 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.170
- Remove legacy IA64 support (#1246145).

* Tue Aug 25 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.169
- Check for NULL arena pointer in _int_pvalloc (#1246656).
- Don't change no_dyn_threshold on mallopt failure (#1246660).

* Tue Aug 25 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.168
- Unlock main arena after allocation in calloc (#1245731).
- Enable robust malloc change again (#1245731).
- Fix perturbing in malloc on free and simply perturb_byte (#1245731).
- Don't fall back to mmap prematurely (#1245731).

* Thu Jul 16 2015 Carlos O'Donell <carlos@redhat.com> -2.12-1.167
- The malloc deadlock avoidance support has been temporarily removed since it
  triggers deadlocks in certain applications (#1243824).

* Wed May 20 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.166
- Fix ruserok() check to reject, not skip, negative user checks (#1217186).

* Thu May  7 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.165
- Optimize ruserok() function for large ~/.rhosts (#1217186).

* Mon Apr 20 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.164
- Fix crash in valloc due to the backtrace deadlock fix (#1207236).

* Tue Apr  7 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.163
- Fix buffer overflow in gethostbyname_r with misaligned buffer
  (#1209376, CVE-2015-1781).

* Wed Mar  4 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.162
- Avoid deadlock in malloc on backtrace (#1066724).

* Wed Mar  4 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.161
- Support running applications that use Intel AVX-512 (#1195453).

* Thu Feb 19 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.160
- Silence logging of record type mismatch for DNSSEC records (#1088301).

* Thu Feb 19 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.159
- Shrink heap on free when vm.overcommit_memory == 2 (#867679).

* Wed Feb 18 2015 Carlos O'Donell <carlos@redhat.com> - 2.12-1.158
- Enhance nscd to detect any configuration file changes (#859965).
- Fix __times() handling of EFAULT when buf is NULL (#1124204).
- Fix memory leak with dlopen() and thread-local storage variables (#978098).
- Prevent getaddrinfo from writing DNS queries to random fd (CVE-2013-7423,
  #1144019).
- Implement userspace half of in6.h header coordination (#1053178).
- Correctely size relocation cache used by profiler (#1144132).
- Fix reuse of cached stack leading to bounds overrun of DTV (#1116050).

* Fri Jan 30 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.157
- Return failure in getnetgrent only when all netgroups have been searched
  (#1085312).
- Fix valgrind warning in nscd_stats (#1091915).

* Tue Jan 27 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.156
- Initialize xports array (#1159167).
- Fix tst-default-attr test to not fail on powerpc (#1023306).

* Mon Jan 19 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.155
- Fix parsing of numeric hosts in gethostbyname_r (CVE-2015-0235, #1183534).

* Tue Jan 13 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.154
- Fix typo in nscd/selinux.c (#1125307).
- Actually run test-iconv modules (#1176907).

* Thu Dec 11 2014 Carlos O'Donell <carlos@redhat.com> - 2.12-1.153
- Fix recursive dlopen() (#1154563).

* Tue Dec 09 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.152
- Fix crashes on invalid input in IBM gconv modules (CVE-2014-6040, #1172044).

* Tue Dec 09 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.151
- Fix wordexp() to honour WRDE_NOCMD (CVE-2014-7817, #1171296).

* Tue Dec 09 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.150
- Fix typo in res_send and res_query (#rh1138769).

* Tue Aug 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.149
- Remove gconv transliteration loadable modules support (CVE-2014-5119,
  #1133810).
- _nl_find_locale: Improve handling of crafted locale names (CVE-2014-0475,
  #1133810).

* Wed Jul 30 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.148
- Switch gettimeofday from INTUSE to libc_hidden_proto (#1099025).

* Fri Jun 20 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.147
- Fix stack overflow due to large AF_INET6 requests (CVE-2013-4458, #1111460).
- Fix buffer overflow in readdir_r (CVE-2013-4237, #1111460).

* Tue Jun  3 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.146
- Fix memory order when reading libgcc handle (#905941).
- Fix format specifier in malloc_info output (#1027261).
- Fix nscd lookup for innetgr when netgroup has wildcards (#1054846).

* Mon Jun  2 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.145
- Add mmap usage to malloc_info output (#1027261).

* Mon May 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.144
- Use NSS_STATUS_TRYAGAIN to indicate insufficient buffer (#1087833).

* Tue May 20 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.143
- [ppc] Add VDSO IFUNC for gettimeofday (#1028285).
- [ppc] Fix ftime gettimeofday internal call returning bogus data (#1099025).

* Mon May 19 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.142
- Also relocate in dependency order when doing symbol dependency testing
  (#1019916).

* Fri May 16 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.141
- Fix infinite loop in nscd when netgroup is empty (#1085273).
- Provide correct buffer length to netgroup queries in nscd (#1074342).
- Return NULL for wildcard values in getnetgrent from nscd (#1085289).
- Avoid overlapping addresses to stpcpy calls in nscd (#1082379).
- Initialize all of datahead structure in nscd (#1074353).

* Thu May 15 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.140
- Return EAI_AGAIN for AF_UNSPEC when herrno is TRY_AGAIN (#1044628).

* Wed Apr 30 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.139
- Do not fail if one of the two responses to AF_UNSPEC fails (#845218).

* Fri Apr 18 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.138
- nscd: Make SELinux checks dynamic (#1025933).

* Mon Apr 14 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.137
- Fix race in free() of fastbin chunk (#1027101).

* Fri Apr 11 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.136
- Fix copy relocations handling of unique objects (#1032628).

* Thu Apr 10 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.135
- Fix encoding name for IDN in getaddrinfo (#981942).

* Wed Apr  9 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.134
- Fix return code from getent netgroup when the netgroup is not found (#1039988).
- Fix handling of static TLS in dlopen'ed objects (#995972).

* Wed Apr  9 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.133
- Don't use alloca in addgetnetgrentX (#1043557).
- Adjust pointers to triplets in netgroup query data (#1043557).

* Mon Nov  4 2013 Carlos O'Donell <carlos@redhat.com> - 2.12-1.132
- Revert the addition of gettimeofday vDSO function for ppc and ppc64 until
  OPD VDSO function call issues are resolved (#1026533).

* Wed Oct 23 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.131
- Call gethostbyname4_r only for PF_UNSPEC (#1022022).

* Mon Sep 23 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.130
- Fix integer overflows in *valloc and memalign. (#1008310).

* Mon Aug 26 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.129
- Initialize res_hconf in nscd (#970090).

* Thu Aug  1 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.128
- Update previous patch for dcigettext.c and loadmsgcat.c (#834386).

* Fri Jul 26 2013 Siddhesh Poyarekar <sidhesh@redhat.com> - 2.12-1.127
- Save search paths before performing relro protection (#988931).

* Thu Jul 25 2013 Carlos O'Donell <codonell@redhat.com> - 2.12-1.126
- Correctly name the 240-bit slow path sytemtap probe slowpow_p10 for slowpow (#905575).

* Thu Jul 25 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.125
- Align value of stacksize in nptl-init (#663641).

* Thu Jul 25 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.124
- Renamed release engineering directory from 'fedora' to `releng' (#903754).

* Thu Jul 25 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.123
- Backport GLIBC sched_getcpu and gettimeofday vDSO functions for ppc (#929302).
- Fall back to local DNS if resolv.conf does not define nameservers (#928318).
- Add systemtap probes to slowexp and slowpow (#905575).

* Wed Jul 24 2013 Carlos O'Donell <codonell@redhat.com> - 2.12-1.122
- Fix getaddrinfo stack overflow resulting in application crash (CVE-2013-1914, #951213).
- Fix multibyte character processing crash in regexp (CVE-2013-0242, #951213).

* Wed Jul 24 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.121
- Add netgroup cache support for nscd (#629823).

* Wed Jul 24 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.120
- Fix multiple nss_compat initgroups() bugs (#966778).
- Don't use simple lookup for AF_INET when AI_CANONNAME is set (#863384).

* Tue Jul 23 2013 Alexandre Oliva <aoliva@redhat.com> - 2.12-1.119
- Add MAP_HUGETLB and MAP_STACK support (#916986).
- Update translation for stale file handle error (#970776).

* Tue Jul 23 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.118
- Improve performance of _SC_NPROCESSORS_ONLN (#rh952422).
- Fix up _init in pt-initfini to accept arguments (#663641).

* Thu Jul 18 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.117
- Set reasonable limits on xdr requests to prevent memory leaks (#848748).

* Thu Jul 11 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.116
- Fix mutex locking for PI mutexes on spurious wake-ups on pthread condvars
  (#552960).
- New environment variable GLIBC_PTHREAD_STACKSIZE to set thread stack size
  (#663641).

* Tue Jul  9 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.115
- Improved handling of recursive calls in backtrace (#868808).

* Tue Jul  2 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.114
- The ttyname and ttyname_r functions on Linux now fall back to searching for
  the tty file descriptor in /dev/pts or /dev if /proc is not available.  This
  allows creation of chroots without the procfs mounted on /proc.  (#851470)

* Mon Jul  1 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.113
- Don't free rpath strings allocated during startup until after
  ld.so is re-relocated. (#862094)

* Thu Jun 20 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.112
- Consistantly MANGLE/DEMANGLE function pointers.
  Fix use after free in dcigettext.c (#834386).

* Wed Jun 19 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.111
- Change rounding mode only when necessary (#966775).

* Thu Jun  6 2013 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.110
- Backport of code to allow incremental loading of library list (#886968).

* Tue Jun  4 2013 Carlos O'Donell <codonell@redhat.com> - 2.12-1.109
- Fix loading of audit libraries when TLS is in use (#919562)

* Wed May 15 2013 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.12-1.108
- Fix application of SIMD FP exception mask (#929388).

* Tue Nov 20 2012 Jeff Law <law@redhat.com> - 2.12-1.107
- Simplify test for magic file to change memcpy behaviour
  and correctly handle encoded return value from inlined
  syscall (#846342, #874642)

* Wed Oct 17 2012 Jeff Law <law@redhat.com> - 2.12-1.106
- Fix typo in inlined open syscall for #846342/#865375 hack (#866798)

* Sun Oct 14 2012 Jeff Law <law@redhat.com> - 2.12-1.105
- Inline open/close syscalls in #846342/865375 hack (#846342, #865375).

* Fri Oct 12 2012 Jeff Law <law@redhat.com> - 2.12-1.104
- Change from magic environment variable to existance of
  magic file /etc/sysconfig/32bit_ssse3_mempy_via_32bit_ssse3_memmove
  to trigger change in memcpy behavior. (#846342, #865375)
- Fix IPTOS_CLASS #define. (#864322)

* Mon Oct 8 2012 Jeff Law <law@redhat.com> - 2.12-1.103
- Don't free memory allocated by mempool allocator (#863453)

* Mon Oct 1 2012 Jeff Law <law@redhat.com> - 2.12-1.102
- Add MADV_DONTDUMP/MADV_DODUMP to mman.h (#861167)

* Mon Sep 17 2012 Jeff Law <law@redhat.com> - 2.12-1.101
- Use __GI_getenv rather than getenv in memcpy ifunc handler (#846342)

* Wed Sep 12 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.100
- Fix gcc_asset failure in _Unwind_SetSpColumn() on ppc64.  (BZ852445)

* Tue Sep 11 2012 Jeff Law <law@redhat.com> - 2.12-1.99
- Allow broken code to avoid the 32 bit SSSE3 memcpy implementations
  by setting the environment variable
  32BIT_SSSE3_MEMCPY_VIA_32BIT_SSSE3_MEMMOVE to any value (#846342)

* Thu Sep  6 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.98
- Backport upstream glibc 4f031072a5055abd83717820b59efdaa463d5853
  locale/findlocale.c (_nl_find_locale): Return right away if
  _nl_explode_name failed.
  locale/programs/locarchive.c (add_locale_to_archive): Likewise. (#848082)

* Tue Sep  4 2012 Jeff Law <law@redhat.com> - 2.12-1.97
- Fix handling of variable length characters in recent fseek
  fseek changes.  Fix testcase to include string.h which
  avoids failures on s390[x] and ppc (#827362).

* Tue Sep  4 2012 Jeff Law <law@redhat.com> - 2.12-1.96
- Increase size of temporary buffers to avoid unnecessary DNS
  lookups (#837695)
- Properly handle case where server rejects query (#804686)

* Tue Sep  4 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.95
- Change _IO_wfile_seekoff to properly set buffer and read ptr for wide chars. (#827362)

* Tue Aug 21 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.94
- Add hand optimized assembly version of expf for x86_64. (#849651)

* Fri Aug 17 2012 Jeff Law <law@redhat.com> - 2.12-1.93
- Fix race in intl/* testsuite (#849203)

* Thu Aug 16 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.92
- Mark /etc/rpc as a configuration file in glibc.spec. (#829222)
- Fix for unpredictable results with some non-default
  floating point rounding modes.. (#837918)

* Wed Aug 15 2012 Jeff Law <law@redhat.com> - 2.12-1.91
- Fix integer overflow leading to buffer overflow in strto*
  and related out of bounds array index (#847930)

* Mon Aug  6 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.90
- Make qsort() thread safe. (#843673)
- Change error text for ESTALE (#832694)

* Sun Aug  5 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.89
- Delay setting file->decided until we have successfully loaded the file's data. (#832516)
- FIX vfprintf() to return EOVERFLOW (not ERANGE) when the (INT_MAX/4)th or larger argument
  is specified in the format string. (#830127)

* Fri Aug  3 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.88
- Fix unchecked malloc and incorrect loop in getent() (#806404)

* Fri Aug  3 2012 Jeff Law <law@redhat.com> - 2.12-1.87
- Update Finnish locale collation rules (#809726)

* Thu Jul 26 2012 Jeff Law <law@redhat.com> - 2.12-1.86
- Pack IPv4 servers at the start of nsaddr_list and
  only track the number of IPV4 servers in EXT(statp)->nscount
  Thanks to Michael Chapman (#841787)

* Wed Jul 25 2012 Jeff Law <law@redhat.com> - 2.12-1.85
- Revert recent changes to res_send (#804630, #835090).
- Fix memcpy args in res_send (#841787).

* Wed Jul 18 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.84
- Fix fnmatch() failure when '*' wildcard was applied on a file name
  containing multi-byte character(s) (#826149)

* Mon Jul 16 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.83
- Fix for iconv() segfault when the invalid multibyte character 0xffff is input while
  converting from IBM930 (#823909).

* Mon Jul 2 2012 Jeff Law <law@redhat.com> - 2.12-1.82
- Fix regression after patch for BZ804630 (#835090).

* Fri Jun 22 2012 Patsy Franklin <pfrankli@redhat.com> - 2.12-1.81
- Fixes an unbounded alloca and related problems. (#833717)

* Wed Apr 18 2012 Jeff Law <law@redhat.com> - 2.12-1.80
- Do not override TTL of CNAME with TTL of its alias (#808545)

* Wed Apr 11 2012 Jeff Law <law@redhat.com> - 2.12-1.79
- Fix unbound alloca usage in cache_addgr (#788959)

* Thu Apr 5 2012 Jeff Law <law@redhat.com> - 2.12-1.78
- Fix option rotate with single IPV6 server (#804630)
- Fix loading first object along a path when tracing (#808337)
- Don't free non-malloced memory.  (#809602)

* Thu Mar 22 2012 Jeff Law <law@redhat.com> - 2.12-1.77
- Fix regression caused by changes for 797094 (#804689).

* Mon Mar 5 2012 Jeff Law <law@redhat.com> - 2.12-1.77
- Properly set errno in vfprintf (#794817)

* Fri Mar 2 2012 Jeff Law <law@redhat.com> - 2.12-1.75
- Enable fix for 771342 (#771342).

* Fri Mar 2 2012 Jeff Law <law@redhat.com> - 2.12-1.74
- Correctly handle large response to AF_UNSPEC dns lookup (#795498)
- Always use another area after a failed allocation in the
 main arena (#795328)

* Wed Feb 29 2012 Jeff Law <law@redhat.com> - 2.12-1.73
- Remove sse3 memcpy (#695812) changes (#781646)

* Tue Feb 28 2012 Jeff Law <law@redhat.com> - 2.12-1.72
- Avoid unbound alloca use in various routines (#797094)

* Wed Feb 22 2012 Jeff Law <law@redhat.com> - 2.12-1.71
- Fix case where nss_compat_initgroups_dyn always returned failure (#788959)

* Mon Feb 20 2012 Jeff Law <law@redhat.com> - 2.12-1.70
- Avoid "nargs" integer overflow which could be used to bypass FORTIFY_SOURCE (#794817)

* Mon Feb 20 2012 Jeff Law <law@redhat.com> - 2.12-1.69
- Fix memory leak on error path (#788959)

* Fri Feb 17 2012 Jeff Law <law@redhat.com> - 2.12-1.68
- Disable 552960 changes again, they're still not right.
- Fix locking on malloc family retry paths (#789238)

* Fri Feb 10 2012 Jeff Law <law@redhat.com> - 2.12-1.66
- Fix lost wakeups in pthread_cond_*, reenable 552960 patch (#552960)
- Fix resolv.conf parsing for ipv6 (#789189)
- Fix nscd crash when group has many members (#788959)
- Fix Ukrainian currency symbol (#789209)

* Thu Feb 9 2012 Jeff Law <law@redhat.com> - 2.12-1.65
- Fix Japanese translation of getopt error (#766513)

* Fri Feb 3 2012 Jeff Law <law@redhat.com> - 2.12-1.64
- From lxo: Avoid mapping past end of shared object (#741105)

* Wed Feb 1 2012 Jeff Law <law@redhat.com> - 2.12-1.63
- Fix month abbreviations for zh_CN locale (#785984)

* Thu Jan 26 2012 Jeff Law <law@redhat.com> - 2.12-1.62
- Add aliases for ISO-10646-UCS-2 (#697421)

* Tue Jan 24 2012 Jeff Law <law@redhat.com> - 2.12-1.61
- Do not cache negative results in nscd if these are transient (#784402)

* Fri Jan 20 2012 Jeff Law <law@redhat.com> - 2.12-1.60
- Fix cycle detection in dynamic loader (#782585)

* Thu Jan 19 2012 Jeff Law <law@redhat.com> - 2.12-1.59
- Avoid high cpu usage when accept fails with EMFILE (#767693)

* Wed Jan 11 2012 Jeff Law <law@redhat.com> - 2.12-1.58
- Temporarily disable 771342.

* Mon Jan 09 2012 Jeff Law <law@redhat.com> - 2.12-1.57
- Fix problems with Finnish locale (#657572)

* Wed Jan 04 2012 Jeff Law <law@redhat.com> - 2.12-1.56
- Workaround kernel clobbering robust list (#771342)

* Tue Jan 03 2012 Jeff Law <law@redhat.com> - 2.12-1.55
- Assume Intel Core i3/i5/i7 processor if AVX is available (#696472)

* Thu Dec 22 2011 Jeff Law <law@redhat.com> - 2.12-1.54
- Disable #552960 patch, it's causing multiple problems in Fedora
  and Debian.

* Tue Dec 20 2011 Jeff Law <law@redhat.com> - 2.12-1.53
- Make implementation of ARENAS_TEST and ARENAS_MAX match
  documentation (#740506)

* Sun Dec 18 2011 Jeff Law <law@redhat.com> - 2.12-1.52
- Include stdint.h in tzfile.c (#767693)
- Check values from TZ file header (#767693)

* Mon Dec 12 2011 Jeff Law <law@redhat.com> - 2.12-1.50
- Handle EAGAIN from FUTEX_WAIT_REQUEUE_PI (#552960)
- Fix return value from pthread_create if stack allocation for new thread fails
  (#767746)
- Move libmemusage.so and libpcprofile.so into base RPM (#752123)
- Remove .UTF-8 suffix from locale names when it is the only supported codeset
  (#749188)
- Fix warnings in __bswap_16. (#750531)
- Fix access after end of search string in regex matcher (#757887)
- Fix locking in _IO_flush_all_lockp (#751750)
- Check malloc arena atomically  (#740506)
- Don't call reused_arena when _int_new_arena failed

* Wed Dec 7 2011 Jeff Law <law@redhat.com> - 2.12-1.49
- Correctly reparse group line after enlarging the buffer
  (#739971, #757665, #759274)

* Thu Nov 17 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.48
- Fix grouping and reuse other locales in various locales (#688720)
- Drop lock before calling malloc_printerr (#726517)
- More complete check for AVX enablement (#752122)

* Thu Nov  3 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.47
- Don't start AVC thread until credentials are installed (#700507)

* Wed Oct 26 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.46
- Update systemtaparches

* Mon Oct 17 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.45
- Update configure script

* Fri Sep 30 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.44
- Add gdb hooks (#711927)

* Mon Sep 19 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.43
- Don't assume AT_PAGESIZE is always available (#739184)
- Define IP_MULTICAST_ALL (#738763)

* Thu Sep 15 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.42
- Avoid race between {,__de}allocate_stack and __reclaim_stacks during
  fork (#738665)

* Tue Sep 13 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.41
- Locale-independent parsing in libintl (#737778)

* Wed Sep  7 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.40
- Change setgroups to affect all the threads in the process (#736346)

* Fri Sep  2 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.39
- Make sure AVC thread has capabilities (#700507)
- Fix memory leak in dlopen with RTLD_NOLOAD (#699724)

* Thu Aug 18 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.38
- Build libresolv with stack protector (#730379)

* Tue Aug 16 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.37
- Maintain stack alignment when cancelling threads (#731042)

* Fri Aug 12 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.36
- Fix missing debuginfo (#729036)

* Mon Jul 11 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.35
- Report write error in addmnt even for cached streams (#688980,
  CVE-2011-1089)
- Handle Lustre filesystem (#712248)

* Mon Jul  4 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.34
- Query NIS domain only when needed (#718057)
- Update: Use mmap for allocation of buffers used for __abort_msg
  (#676591)

* Wed Jun 29 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.33
- Don't use gethostbyaddr to determine canonical name (#714823)

* Wed Jun 15 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.32
- ldd: never run file directly (#713134)

* Tue Jun 14 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.31
- Support Intel processor model 6 and model 0x2c (#695595)
- Optimize memcpy for SSSE3 (#695812)
- Optimize strlen for SSE2 (#695963)

* Thu Jun  9 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.30
- Support f_flags in Linux statfs implementation (#711987)

* Thu May 26 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.29
- Avoid overriding CFLAGS (#706903)

* Tue May 24 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.28
- Use mmap for allocation of buffers used for __abort_msg (#676591)

* Thu May 19 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.27
- Fix PLT use due to __libc_alloca_cutoff
- Schedule nscd cache pruning more accurately from re-added values
  (#703481)
- Fix POWER4 optimized strncmp to not read past differing bytes
  (#694386)

* Tue May 17 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.26
- Create debuginfo-common on biarch platforms (#676467)
- Use Rupee sign in Indian locales (#692838)
- Signal temporary host lookup errors in nscd as such to the requester
  (#703480)
- Define initgroups callback for nss_files (#705465)

* Thu Mar 31 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.25
- Implement x86 cpuid handling of leaf4 for cache information
  (#692177)

* Mon Mar 21 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.24.1
- Handle page boundaries in x86 SSE4.2 strncmp (#689471)

* Fri Mar 18 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.23
- Check size of pattern in wide character representation in fnmatch
  (#681054)

* Thu Mar 17 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.22.1
- Avoid too much stack use in fnmatch (#681054, CVE-2011-1071)
- Properly quote output of locale (#625893, CVE-2011-1095)
- Don't leave empty element in rpath when skipping the first element,
  ignore rpath elements containing non-isolated use of $ORIGIN when
  privileged (#667974, CVE-2011-0536)

* Fri Mar 11 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.21.1
- Revert "Optimize memcpy, mempcpy and memmove" to let broken software
  continue to be broken (#676065)
- Optimize memset (#676076)

* Thu Feb 10 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.20
- Optimize memcpy, mempcpy and memmove (#676065)

* Wed Feb  9 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.19
- Optimize strcasestr, strcasecmp, strnlen (#601686)

* Wed Feb  2 2011 Andreas Schwab <schwab@redhat.com> - 2.12-1.18
- Don't expand DST twice in dl_open (#643822)

* Wed Dec 15 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.17
- Fix use of restrict in string.h and wchar.h (#661982)

* Fri Dec 10 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.16
- Don't ignore $ORIGIN in libraries (#643822)

* Fri Nov 26 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.15
- Don't ignore zero TTL in DNS answers (#656014)

* Wed Nov 24 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.14
- Fix comparison in sqrtl for IBM long double 128 (#656530)

* Mon Nov 22 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.13
- Make <sys/timex.h> compatible with C++ (#652661)
- Avoid unpackaged files (#653905)

* Tue Nov 16 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.12
- Fix vDSO synthetic hwcap handling so they are not masked out from
  ld.so.cache matching (#615701)

* Tue Nov  2 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.11
- Work around kernel rejecting valid absolute timestamps (#580498)
- Document M_PERTURB (#615090)
- Fix x86 pthread_cond_signal FUTEX_WAKE_OP fallback (#623187)
- Fix concurrency problem between dl_open and dl_iterate_phdr (#646954)
- Fix x86-64 strchr propagation of search byte into all bytes of SSE
  register (#647448)

* Fri Oct 22 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.10
- Require suid bit on audit objects in privileged programs (#645680,
  CVE-2010-3856)

* Mon Oct 18 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.9
- Never expand $ORIGIN in privileged programs (#643822)

* Fri Oct 15 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.8
- Fix bug in generic strstr/memmem implementation handling certain
  repeated patterns (#641128)
- Correctly align TCB for AVX (#642584)

* Tue Sep  7 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.7
- Round cache sizes to handle odd sizes (#607010)
- Fix initializsation of cpu features (#630801)
- Fix ifunc thunk for strspn on x86 in static libc (#631011)

* Fri Aug 20 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.6
- Fix error handling in getlogin_r (#621959)

* Tue Aug 10 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.5
- Fix use of extend_alloca (#621959)

* Tue Jun 29 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.4
- Fix setxid race handing exiting threads (#607461)

* Tue Jun  1 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.3
- Implement recvmmsg on all archs (#594194)
- Avoid strict aliasing issues (#594194)
- Fix nscd user creation (#594256)
- Fix access outside of red zone on ppc (#593771)
- Fix scope handling during dl_close (#593686)

* Wed May 19 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.2
- Fix race in free sanity check (#593396)

* Thu May  6 2010 Andreas Schwab <schwab@redhat.com> - 2.12-1.1
- Fix exit codes in nscd start script (#582738)
- Fix lookup of collation sequence value during regexp matching (#587360)
- Handle too-small buffers in Linux getlogin_r (BZ#11571)
- Fix name of tt_RU.UTF-8@iqtelif locale (#589138)

* Tue May  4 2010 Roland McGrath <roland@redhat.com> - 2.12-1
- Update to 2.12 release.
  - Fix ldconfig chroot handling.
  - Don't deadlock in __dl_iterate_phdr while (un)loading objects.
  - Fix handling of newline in addmntent.
  - Fix AIO when thread creation failed.

* Fri Apr 16 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-20
- Update from master
  - Fix bugs in x86-32 strcmp-sse4.S and strcmp-ssse3.S
  - Add x86-32 FMA support
  - Don't crash in trace mode when dependencies are missing
  - x86-64 SSE4 optimized memcmp
  - Fix makecontext on s390/s390x

* Tue Apr 13 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-19
- Avoid multiarch memcmp in tzdata-update (#581677)

* Mon Apr 12 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-18
- Update from master
  - Implement interfaces to set and get names of threads (BZ#11390)
  - Locale data updates (BZ#10824, BZ#10936, BZ#11470, BZ#11471)
  - Print reload count in nscd statistics (BZ#10915)
  - Fix reading loginuid file in getlogin{,_r}
  - Fix fallocate error return on i386
  - Fix cproj implmentation (BZ#10401)
  - Fix getopt handing (BZ#11039, BZ#11040, BZ#11041)
  - Implement new mode for NIS passwd.adjunct.byname table (BZ#11134)
  - Obey LD_HWCAP_MASK in ld.so.cache lookups

* Tue Apr  6 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-17
- Update from master
  - Locale data updates (BZ#11007, BZ#11258, BZ#11272, BZ#10554)
  - Handle DNS timeouts in old-style lookup code (BZ#11010)
  - Fix aux cache handling in ldconfig with chroot (BZ#11149)
  - Fix printing error messages in getopt (BZ#11043)
  - Declare iruserok and iruserok_af (BZ#11070)
  - Fix option aliasing in argp (BZ#11254)
  - Handle POSIX-compliant errno value of unlink in remove (BZ#11276)
  - Fix definition and testing of S_ISSOCK (BZ#11279)
  - Fix retrieving of kernel header version (BZ#11287)
  - Fix concurrent handling of __cpu_features (BZ#11292)
  - Handle unnecessary padding in getdents64 (BZ#11333)
  - Fix changes to interface list during getifaddrs calls (BZ#11387)
  - Missing memory barrier in DES initialization (BZ#11449)
  - Fix spurious UNAVAIL status is getaddrinfo
  - Add support for new clocks (BZ#11389)
  - Fix Linux getlogin{_r,} implementation
  - Fix missing zero-termination in cuserid (BZ#11397)
  - Fix glob with empty pattern
  - Fix handling of STB_GNU_UNIQUE in LD_TRACE_PRELINKING
  - Unify wint_t handling in wchar.h and wctype.h (BZ#11410)
  - Implement handling of libc ABI in ELF header
  - Don't underestimate length of DST substitution in rpath
  - Power7-optimized 64-bit and 32-bit memcpy
- Assign global scope to RFC 1918 addresses (#577626)

* Thu Mar 18 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-16
- Fix SSSE3 memcmp (#574210)

* Tue Mar  9 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-15
- Update from master
  - sparc64: Fix handling of R_SPARC_TLS_LE_* relocations (#571551)
  - Handle ext4 and logfs in statvfs functions
  - Fix setxid race with thread creation
  - Pass -mtune=i686 to assembler when compiling for i686
  - Fix R_X86_64_PC32 overflow detection
  - Fix msgrcv on sparc64
  - Fix unwind info in x86 strcmp-sse4.S (BZ#11332)
  - sparc: Add multiarch support for memset/bzero/memcpy
- Remove directories owned by filesystem (#569414)
- Add %%ghost /etc/gai.conf to glibc-common (#567748)

* Tue Feb 23 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-14
- Update from master
  - Sparc updates
- Fix SSSE3 memcpy (#556584)

* Mon Feb 22 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-13
- Update from master
  - Use CPUID_OFFSET instead of FEATURE_OFFSET
  - Add 32bit memcmp/strcmp/strncmp optimized for SSSE3/SSS4.2
  - Fix file descriotor leak in nftw with FTW_CHDIR (BZ#11271)
  - Add Sparc STT_GNU_IFUNC support
  - Add power7-optimized classification functions
- Reapply "Optimize 32bit memset/memcpy with SSE2/SSSE3."
- Use unsigned comparison in sse memcpy/memset

* Mon Feb  8 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-12
- Update from master
  - Update constants in <sys/mount.h> for current kernels (#11235)
  - Fix endless loop with invalid /etc/shells file (#11242)
  - Fix sorting of malayalam letter 'na' (#10414)
  - Add kok_IN locale
  - Use common collation data in as_IN locale
  - Avoid alloca in setenv for long strings
- Use shared mapping to reserve memory when creating locale archive (#10855)
- Fix fstat on Linux/sparc64 (#11155)

* Mon Feb  1 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-11
- Update from master
  - Fix error checking in iconv (#558053)
  - Don't map U00DF to U1E9E in toupper table
  - _nl_load_locale() incorrectly handles mmap() failures (BZ#11200)
  - Fix various issues in regex matcher (BZ#11183, BZ#11184, BZ#11185,
    BZ#11186, BZ#11187, BZ#11188, BZ#11189, BZ#11190, BZ#11191,
    BZ#11192, BZ#11193)

* Tue Jan 19 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-10
- Update from master
  - Fix ____longjmp_chk for s390/s390x
  - Remove duplicate definitions of O_DSYNC and O_RSYNC for Linux/sparc
  - Ignore negative dynamic entry types (#546890)
  - Fix pthread_cond_*wait with requeue-PI on i386 (#548989)
  - Fix _XOPEN_SOURCE_EXTENDED handling
- Revert "Optimize 32bit memset/memcpy with SSE2/SSSE3."

* Fri Jan 15 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-9
- Update from master.
  - Define IPTOS_CLASS_* macros according to RFC 2474 (BZ#11027)
  - Always use IPv4 sockets for IPv4 addresses (BZ#11141)
  - regcomp.c: do not ignore memory allocation failure (BZ#11127)
  - Fix malloc_info without prior allocations (BZ#11126)
  - Optimize 32bit memset/memcpy with SSE2/SSSE3
  - Relax feature tests in headers

* Tue Jan 12 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-8
- Update from master.
  - More POSIX conformance fixes.

* Mon Jan 11 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-7
- Fix build failure.

* Mon Jan 11 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-6
- Update from master.
  - POSIX conformance fixes (BZ#11125).

* Mon Jan  4 2010 Andreas Schwab <schwab@redhat.com> - 2.11.90-5
- Update from master.
  - Additional setcontext(), etc. conformance tests (BZ#11115).
  - Handle AT_FDCWD in futimens (BZ#10992).
  - Update poll.h header for POSIX 2008 (BZ#11093).
  - Avoid ELF lookup race.

* Mon Dec 14 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-4
- Update from master.
  - Add Requeue-PI support for x86 arch.
  - Redefine O_SYNC and O_DSYNC to match 2.6.33+ kernels.
  - Fix a few error cases in *name4_r lookup handling (BZ#11000).
  - Fix kernel version check in recent ptsname change (BZ#11046).
  - Add more warnings to exec functions (BZ#11056).
  - Add recvmmsg interface.
  - Define SCHED_IDLE and SCHED_RESET_ON_FORK for Linux.

* Mon Nov 30 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-3
- Update from master.
  - Fix infloop in __pthread_disable_asynccancel on x86_64 (#537690).
  - Prevent unintended file desriptor leak in grantpt (#530558).
  - Fix startup to security-relevant statically linked binaries (#528631).
- Re-install CFI in x86/x86_64 clone (#491542).

* Tue Nov 24 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-2
- Update from master.
  - Define week, first_weekday, and first_workday for en_DK locale (#525126).
  - Use struct timespec for timestamps in struct stat also if
    __USE_XOPEN2K8 (#539870).
  - Fix week information for nl_NL locale (#499748).
  - Update ntp_gettime for Linux (#479558).
  - Fix getwc* and putwc* on non-wide streams (BZ#10958).
  - Avoid warnings in CPU_* macros when using const bitsets (BZ#10918).
  - Handle LC_GLOBAL_LOCALE in duplocale (BZ#10969).
  - Fix _NC_LOCALE_NAME definition (BZ#10968).
  - Add missing Linux MADV_* definitions (BZ#10972).
  - Add support for new Linux error ERFKILL (BZ#10939).
- Enable multi-arch support on ppc and ppc64.

* Thu Nov 12 2009 Andreas Schwab <schwab@redhat.com> - 2.11.90-1
- Update from master.

* Thu Nov  5 2009 Andreas Schwab <schwab@redhat.com> - 2.11-2
- Fix readahead on powerpc32.
- Fix R_PPC64_{JMP_IREL,IRELATIVE} handling.
- Fix preadv, pwritev and fallocate for -D_FILE_OFFSET_BITS=64 (#533063).

* Mon Nov  2 2009 Andreas Schwab <schwab@redhat.com> - 2.11-1
- Update to 2.11 release.
- Disable multi-arch support on PowerPC again since binutils is too old.
- Fix crash in tzdata-update due to use of multi-arch symbol (#532128).

* Fri Oct 30 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-27
- Update from master.
  - Fix races in setXid implementation (BZ#3270).
  - Implement IFUNC for PPC and enable multi-arch support.
  - Implement mkstemps/mkstemps64 and mkostemps/mkostemps64 (BZ#10349).
  - Fix IA-64 and S390 sigevent definitions (BZ#10446).
  - Fix memory leak in NIS grp database handling (BZ#10713).
  - Print timestamp in nscd debug messages (BZ#10742).
  - Fix mixing IPv4 and IPv6 name server in resolv.conf.
  - Fix range checks in coshl.
  - Implement SSE4.2 optimized strchr and strrchr.
  - Handle IFUNC symbols in dlsym (#529965).
  - Misc fixes (BZ#10312, BZ#10315, BZ#10319, BZ#10391, BZ#10425,
    BZ#10540, BZ#10553, BZ#10564, BZ#10609, BZ#10692, BZ#10780,
    BZ#10717, BZ#10784, BZ#10789, BZ#10847
- No longer build with -fno-var-tracking-assignments.

* Mon Oct 19 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-26
- Update from master.
  - Add ____longjmp_chk for sparc.
- Avoid installing the same libraries twice.

* Mon Oct 12 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-25
- Update from master
  - Fix descriptor leak when calling dlopen with RTLD_NOLOAD (#527409).
  - Fix week-1stday in C locale.
  - Check for integer overflows in formatting functions.
  - Fix locale program error handling (#525363).

* Mon Sep 28 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-24
- Update from master.
  - Fix missing reloc dependency (#517001).

* Mon Sep 21 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-23
- Update from master.

* Mon Sep 14 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-22
- Update from master.
  - Fix endless loop in localedef.
  - Fix __longjmp_chk on s390/s390x.
- Fix exit codes in nscd start script (#521848).
- Build with -fno-var-tracking-assignments for now (#523172).

* Mon Sep  7 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-21
- Update from master.
  - Fix strstr/strcasestr on i386 (#519226).

* Thu Sep  3 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-20
- Update from master.
  - Fix strstr/strcasestr/fma/fmaf on x86_64 (#519226).
  - Fix lookup of group names in hesiod initgroups (#520472).

* Wed Sep  2 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-19
- Update from master.
  - Fix x86_64 bits/mathinline.h for -m32 compilation.

* Tue Sep  1 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-18
- Update from master.
  - fix parse error in <bits/mathinline.h> (#520209).

* Thu Aug 27 2009 Roland McGrath <roland@redhat.com> - 2.10.90-17
- Update from master.

* Wed Aug 26 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-16
- Update from master.
  - handle AVX saving on x86-64 in interrupted symbol lookups (#519081).

* Mon Aug 24 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-15
- Update from master.
  - fix fortify failure with longjmp from alternate stack (#512103).
- Add conflict with prelink (#509655).

* Mon Aug 17 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-14
- Update from master.
  - fix pthread_cond_signal (#516469)

* Mon Aug 10 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-13
- Update from master.
  - fix rehashing of unique symbols (#515677)
- Fix spurious messages with --excludedocs (#515948)

* Mon Aug  3 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-12
- Update from master.
  - fix fortify failure with longjmp from alternate stack (#512103)

* Thu Jul 30 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-11
- Update from master.
- Don't package debuginfo files in glibc-devel.

* Tue Jul 28 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-10
- Update from master.
  * fix memory ordering in pthread_mutex_unlock (BZ#10418)
  * implement RES_USE_DNSSEC option in resolver (#205842)
  * fix hang in ldd -r (#513945)

* Mon Jul 27 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-9
- Update from master.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.90-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Jakub Jelinek <jakub@redhat.com> - 2.10.90-7.1
- Fix up pthread_cond_timedwait on x86_64 with old kernels.

* Thu Jul 23 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-7
- Update from master.
- Build with -DNDEBUG unless using a prerelease.

* Thu Jul 23 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-6
- Rebuilt with binutils-2.19.51.0.14-29.fc12 to fix static binaries

* Wed Jul 22 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-5
- Update from master.
- Undefine __i686 on x86 to fix build.

* Mon Jul 20 2009 Andreas Schwab <schwab@redhat.com> - 2.10.90-4
- Update from master.
- Don't build separate i686 package.

* Wed Jul  8 2009 Andreas Schwab <schwab@redhat.com> 2.10.90-3
- Reenable setuid on pt_chown.

* Thu Jul  2 2009 Andreas Schwab <aschwab@redhat.com> 2.10.90-2
- Update from master.

* Fri Jun 26 2009 Andreas Schwab <aschwab@redhat.com> 2.10.90-1
- Update from master.
- Enable multi-arch support on x86/x86-64.
- Add requires glibc-headers to glibc-devel (#476295).
- Implement second fallback mode for DNS requests (#505105).
- Don't generate invalid POSIX TZ string for Asia/Dhaka timezone (#506941).
- Allow backtrace through __longjmp_chk on powerpc.

* Fri May 22 2009 Jakub Jelinek <jakub@redhat.com> 2.10.1-2
- fix accept4 on architectures other than i?86/x86_64
- robustify nscd client code during server GC
- fix up nscd segfaults during daemon shutdown
- fix memchr on ia64 (BZ#10162)
- replace the Sun RPC license with the BSD license, with the explicit
  permission of Sun Microsystems
- fix up powerpc long double errno reporting

* Sun May 10 2009 Jakub Jelinek <jakub@redhat.com> 2.10.1-1
- fix up getsgent_r and getsgnam_r exports on i?86 and ppc

* Sat May  9 2009 Jakub Jelinek <jakub@redhat.com> 2.10-2
- update from trunk
  - glibc 2.10 release
  - fix memchr on x86_64 (#499689)

* Mon Apr 27 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-22
- update from trunk
  - further localedef fixes
- fix build-locale-archive

* Fri Apr 24 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-21
- update from trunk
  - fix localedef
  - fix SHIFT_JIS iconv EILSEQ handling (#497267)
  - misc fixes (BZ#10093, BZ#10100)

* Fri Apr 24 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-20
- update from trunk
  - fix p{read,write}v{,64} (#497429, #497434)
  - fix strfmon (#496386)

* Thu Apr 16 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-19
- update from trunk
  - fix dlopen from statically linked binaries (#495830)

* Thu Apr 16 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-18
- update from trunk
  - fix fallocate

* Wed Apr 15 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-17
- update from trunk
  - if threads have very small stack sizes, use much smaller buffer
    in __get_nprocs when called from within malloc (#494631)

* Tue Apr 14 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-16
- update from trunk

* Thu Apr  9 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-15
- rebuilt with fixed gcc to avoid miscompilation of i586 memmove
- reenable experimental malloc again

* Wed Apr  8 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-14
- update from trunk
- temporarily disable experimental malloc

* Tue Apr  7 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-13
- update from trunk
  - fix strverscmp (#494457)
- configure with --enable-nss-crypt

* Wed Apr  1 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-12
- update from trunk
- configure with --enable-experimental-malloc

* Fri Mar 20 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-11
- update from trunk
  - POSIX 2008 prototype adjustments for scandir{,64}, alphasort{,64} and
    versionsort{,64}
  - fix libthread_db (#491197)

* Tue Mar 10 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-10
- update from trunk
  - fix atexit/__cxa_atexit

* Mon Mar  9 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-9
- update from trunk
  - POSIX 2008 support: -D_XOPEN_SOURCE=700 and -D_POSIX_C_SOURCE=200809L
- move libnldbl_nonshared.a on ppc*/s390*/sparc* back to glibc-devel

* Fri Feb 27 2009 Roland McGrath <roland@redhat.com> - 2.9.90-8.1
- fix libthread_db (#487212)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.90-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-7
- update from trunk
- adjust for i586 + i686 from i386 + i686 build
- split static libraries into glibc-static subpackage
- ld -r the whole libpthread.a together to avoid endless issues with
  -static ... -lpthread
- require 2.6.18 and later kernel

* Wed Feb  4 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-3
- update from trunk
  - ISO C++ compliant strchr etc. with GCC 4.4+
  - AT_RANDOM support

* Thu Jan  8 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-2
- update from trunk

* Fri Jan  2 2009 Jakub Jelinek <jakub@redhat.com> 2.9.90-1
- update from trunk (#478314)

* Mon Dec  8 2008 Jakub Jelinek <jakub@redhat.com> 2.9-3
- temporarily disable _nss_dns_gethostbyname4_r (#459756)
- NIS hostname lookup fixes (#473073, #474800, BZ#7058)
- fix unsetenv (#472941)

* Thu Nov 13 2008 Jakub Jelinek <jakub@redhat.com> 2.9-2
- glibc 2.9 release
- fix CPU_ALLOC_SIZE on 32-bit arches (BZ#7029)

* Wed Nov 12 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-17
- update from trunk
  - don't abort on broken DNS replies (#469299, BZ#7009)
  - misc fixes (BZ#6966, BZ#7008, BZ#6955, BZ#6843)

* Fri Oct 31 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-16
- update from trunk
  - further resolver fixes
  - another dynamic TLS handling fix (#469263)
  - misc fixes (BZ#6867, BZ#6875, BZ#6919, BZ#6920, BZ#6942, BZ#6947,
		BZ#6968, BZ#6974, BZ#6980, BZ#6995)
- rebuild with newer rpm to avoid stripping
  shared libraries when they shouldn't be (#468129)

* Tue Oct 28 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-15
- update from trunk
  - __libc_res_nquery fixes (#466786)

* Sun Oct 19 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-14
- update from trunk
  - fix dynamic TLS handling (#467309)
  - fix sys/signalfd.h for C++ (#467172)
  - fix sprof (#458861)
  - fix _mcount and socket syscalls on s390x (#464146)
  - try harder to allocate memory in valloc and pvalloc (#461481)
- fix power6 32-bit libs (#467311)

* Fri Oct 10 2008 Dennis Gilmore <dennis@ausil.us> 2.8.90-13
- apply sparcv9v memset patch from jakub and davem

* Fri Aug 29 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-12
- update from trunk
  - revert origin changes (#457849)
  - use MAP_STACK for thread stacks
  - misc fixes (BZ#6845, BZ#6544, BZ#6634, BZ#6589, BZ#6790, BZ#6791,
    BZ#6824)
  - power7 bits (BZ#6817)
  - fix expm1 on i?86/x86_64 (#43354, BZ#5794)

* Sat Aug  2 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-11
- update from trunk
  - fix non-absolute $ORIGIN handling (#457560)
  - exported some further libresolv APIs (#453325)
  - misc fixes

* Tue Jul 29 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-10
- update from trunk
  - resolver fixes
  - misc fixes (BZ#6771, BZ#6763, BZ#6698, BZ#6712)
  - s390{,x} utmp/utmpx bi-arch support (BZ#6724)
  - popen "e" flag
- fr_FR locale changes reenabled

* Wed Jul 16 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-9
- update from trunk
  - fix unbuffered vfprintf if writing to the stream fails (#455360)
  - remove useless "malloc: using debugging hooks" message (#455355)
  - nscd fixes
  - fix resolver alignment issues (#454500)
  - fix setvbuf (BZ#6719)

* Thu Jul  3 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-8
- update from trunk
  - watch even resolv.conf in nscd using inotify
  - some nscd fixes

* Fri Jun 13 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-7
- update from trunk
  - avoid *lround* on ppc* clobbering cr3/cr4 registers (#450790)
  - further nscd fixes (#450704)
  - use inotify in nscd to watch files

* Thu Jun 12 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-6
- update from trunk
  - nscd fixes (#450704)
  - fix getservbyport (#449358)
  - fix regexp.h (#446406)
  - avoid crashing on T_DNAME in DNS responses (#450766)

* Sun May 25 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-5
- update from trunk

* Tue May 20 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-4
- further getaddrinfo and nscd fixes

* Sun May 18 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-3
- getaddrinfo and nscd fixes
- reenable assertion checking in rawhide

* Fri May 16 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-2
- fix getaddrinfo (#446801, #446808)

* Thu May 15 2008 Jakub Jelinek <jakub@redhat.com> 2.8.90-1
- update to trunk
  - O(n) memmem/strstr/strcasestr
  - i386/x86_64 TLS descriptors support
  - concurrent IPv4 and IPv6 DNS lookups by getaddrinfo

* Mon May  5 2008 Jakub Jelinek <jakub@redhat.com> 2.8-3
- don't run telinit u in %post if both /dev/initctl and
  /sbin/initctl exist (#444978)
- workaround GCC ppc64 miscompilation of c{log{,10},acosh,atan}l
  (#444996)

* Wed Apr 30 2008 Jakub Jelinek <jakub@redhat.com> 2.8-2
- fix nscd races during GC (BZ#5381)
- rebuilt with fixed GCC to fix regex miscompilation on power6
- SPARC fixes

* Sat Apr 12 2008 Jakub Jelinek <jakub@redhat.com> 2.8-1
- 2.8 release

* Fri Apr 11 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-16
- update to trunk
  - misc fixes (BZ#4997, BZ#5741)
  - make sure all users of __libc_setlocale_lock know it is
    now a rwlock
  - fix ppc/ppc64 compatibility _sys_errlist and _sys_siglist
    symbols

* Thu Apr 10 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-15
- update to trunk
  - misc fixes (BZ#4314, BZ#4407, BZ#5209, BZ#5436, BZ#5768, BZ#5998,
		BZ#6024)
- restart sshd in %post when upstart is used - it doesn't have
  /dev/initctl (#441763)
- disable assert checking again

* Tue Apr  8 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-14
- update to trunk
  - misc fixes (BZ#5443, BZ#5475, BZ#5478, BZ#5939, BZ#5979, BZ#5995,
		BZ#6004, BZ#6007, BZ#6020, BZ#6021, BZ#6042)
  - change mtrace to keep perl 5.10 quiet (#441082)
  - don't share conversion state between mbtowc and wctomb (#438687)
  - if st_blksize is too large and malloc fails, retry with smaller
    buffer in opendir (#430768)
  - correct *printf overflow test (#358111)

* Fri Mar 28 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-13
- update to trunk
  - don't define ARG_MAX in <limits.h>, as it is no longer
    constant - use sysconf (_SC_ARG_MAX) to get the current
    argument size limit
  - fix build on sparc64
- only service sshd condrestart if /etc/rc.d/init.d/sshd exists
  (#428859)

* Wed Mar 26 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-12
- update to trunk
  - new CLONE_* flags in <sched.h> (#438542)
  - nis+ errno clobbering fix (#437945)
  - fix adjtime (#437974)

* Fri Mar 14 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-11
- update to trunk
- remove <stropts.h>, define _XOPEN_STREAMS -1 (#436349)

* Wed Mar  5 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-8
- update to trunk
  - {,v}{as,d}printf and obstack_{,v}printf fortification (#435905)
  - fix getnameinfo/gethostbyaddr (#428067, BZ#5790)
  - fix yp_order (#435519, BZ#5854)
  - misc fixes (BZ#5779, BZ#5736, BZ#5627, BZ#5818, BZ#5012)
- merge review cleanup (Tom Callaway, #225806)

* Sat Feb 16 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-7
- update to trunk
  - make NI_MAXHOST and NI_MAXSERV available even in BSDish
    namespaces (BZ#5737)
  - timerfd_* syscalls

* Fri Feb  1 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-6
- fix build

* Thu Jan 31 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-5
- update to trunk
- rebuild with gcc 4.3

* Fri Jan 11 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-4
- update to trunk
  - misc fixes (BZ#5541, BZ#5545, BZ#5553, BZ#5112, BZ#5520)
  - getaddrinfo fixes
  - signalize EOVERFLOW from sem_post instead of overflowing
    the counter
  - fix i?86 makecontext
  - fix iconv for iso-2022-jp//translit (#397021)

* Thu Jan  3 2008 Jakub Jelinek <jakub@redhat.com> 2.7.90-3
- update to trunk
  - fix recognition of interface family (#425768)
  - add __THROW to __ctype_{b,tolower,toupper}_loc prototypes

* Thu Dec 27 2007 Jakub Jelinek <jakub@redhat.com> 2.7.90-2
- update to trunk
  - nsswitch fix (#425768)
- temporarily enable assert checking

* Wed Dec 12 2007 Jakub Jelinek <jakub@redhat.com> 2.7.90-1
- update to trunk
  - fix __USE_STRING_INLINES on i?86 (#408731, #371711)
  - fix *scanf (#388751)

* Wed Oct 17 2007 Jakub Jelinek <jakub@redhat.com> 2.7-1
- glibc 2.7 release
- fix tzfile.c for times after last transition (#333561)
- fix sem_post@GLIBC_2.0 on i?86
- appease valgrind in libpthread.so initialization
- misc fixes (BZ#3425, BZ#5184, BZ#5186)

* Mon Oct 15 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-21
- fix getgr{name,gid}{,_r} with nscd

* Sun Oct 14 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-20
- install <bits/error.h> (#330031)
- disable -D_FORTIFY_SOURCE{,=2} support (with a warning) for
  GCC 3.4.x and earlier(#327641)
- pl_PL locale changes (BZ#4098, #242296)
- misc fixes (BZ#1140, BZ#3195, BZ#3242, BZ#4359)

* Thu Oct 11 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-19
- fix <netinet/tcp.h>
- simple preprocessor in localedef, fix de_DE collation with it

* Wed Oct 10 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-18
- add signalfd, eventfd, eventfd_read, eventfd_write
- qsort speedups
- workaround for cpuid bugs (#324081)
- make sure gettext's conversion_lock is initialized even if
  program isn't linked against libpthread.so.0, only dlopens it (#321761)
- misc fixes (BZ#5112, BZ#5113, BZ#5104, BZ#5063, BZ#5010, BZ#4407,
  BZ#3924, BZ#5103, BZ#2633, BZ#181, BZ#73, #321901)

* Wed Oct  3 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-17
- fix {,v}swprintf with -D_FORTIFY_SOURCE=1 -mlong-double-64 on ppc*/s390*/sparc*
- strcoll fixes
- misc fixes (BZ#645, BZ#5071)
- locale fixes (BZ#4941, #299321, #203364, #196711, #236212)

* Sat Sep 29 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-16
- misc fixes (BZ#4963, BZ#4972, BZ#5028, BZ#5043, BZ#5058)
- improve -D_FORTIFY_SOURCE{,=2} diagnostic through warning/error
  attributes
- fix wcscpy, wcpcpy, fgetws, fgetws_unlocked, swprintf and vswprintf
  fortification inlines
- fix a scalability issue with lazy binding in heavily multithreaded
  programs

* Thu Sep 20 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-15
- $5$ (SHA-256) and $6$ (SHA-512) support in crypt
  (#228697, #249477, #173834)

* Tue Sep 18 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-14
- -D_FORTIFY_SOURCE{,=2} support for C++
- fortification of fread{,_unlocked}
- support *scanf m allocation modifier (%ms, %mls, %mc, ...)
- in -std=c99 or -D_XOPEN_SOURCE=600 mode don't recognize
  %as, %aS and %a[ as a GNU extension for *scanf
- fix splice, vmsplice, tee return value, make them cancellation
  points
- mq_open checking
- use inline function rather than function-like macro
  for open{,at}{,64} checking
- IFA_F_OPTIMISTIC handling in getaddrinfo (#259681)
- fix an ABBA deadlock in ld.so (#284171)
- remove sparc{32,64} unwind info from _start and clone

* Mon Aug 27 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-13
- fix personality on x86_64/ppc/ppc64 (#256281)

* Sat Aug 25 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-12
- readd x86_64 gettimeofday stuff, initialize it earlier
- nis_list fix (#254115)
- workaround for bugs in ia64 silly /emul/ia32-linux hack (#253961)
- misc fixes (BZ#3924, BZ#4566, BZ#4582, BZ#4588, BZ#4726, BZ#4946,
  BZ#4905, BZ#4814, BZ#4925, BZ#4936, BZ#4896, BZ#4937, BZ#3842,
  BZ#4554, BZ#4557, BZ#4938)

* Fri Aug 17 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-11
- remove __strtold_internal and __wcstold_internal from ppc*/s390*/sparc*
  *-ldbl.h headers
- temporarily backout x86_64 gettimeofday.S changes (#252453)
- some further sparc, sparc64 and alpha fixes

* Wed Aug 15 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-10
- don't open /etc/ld.so.{cache,preload} with O_NOATIME (#252146)
- s390{,x}, alpha and sparc fixes
- sparcv9 is no longer an aux arch, as we expect
  to not build sparc.rpm glibc any longer, only sparcv9.rpm,
  sparc64.rpm and new two aux arches sparcv9v.rpm and sparc64v.rpm

* Tue Aug 14 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-9
- private futex even for mutexes and condvars
- some further O_CLOEXEC changes
- use vDSO on x86_64 if available
- ia64 build fixes (#251983)

* Fri Aug 10 2007 Roland McGrath <roland@redhat.com> 2.6.90-8
- update to trunk
  - fix missing strtold_l export on ppc64

* Thu Aug  9 2007 Roland McGrath <roland@redhat.com> 2.6.90-6
- update to trunk
  - fix local PLT regressions
- spec file revamp for new find-debuginfo.sh

* Sun Aug  5 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-4
- fix librt.so and librtkaio.so on ppc32, so that it is not using
  bss PLT

* Sat Aug  4 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-3
- fix open{,at}{,64} macro for -pedantic (#250897)
- add transliteration for l with stroke (#250492)
- fix strtod ("-0", NULL)
- update License tag

* Wed Aug  1 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-2
- make aux-cache purely optional performance optimization in ldconfig,
  don't issue any errors if it can't be created (#250430)
- remove override_headers hack, BuildRequire >= 2.6.22 kernel-headers
  and rely on its content

* Tue Jul 31 2007 Jakub Jelinek <jakub@redhat.com> 2.6.90-1
- update to trunk
  - private futex optimizations
  - open{,at}{,64} argument checking
- ldconfig speedups

* Sun Jul  8 2007 Jakub Jelinek <jakub@redhat.com> 2.6-4
- filter <built-in> pseudo-files from debuginfo source lists (#245714)
- fix sscanf when errno is EINTR before the call (BZ#4745)
- save/restore errno around reading /etc/default/nss (BZ#4702)
- fix LD_HWCAP_MASK handling
- disable workaround for #210748, instead backport
  ld.so locking fixes from the trunk (#235026)
- new x86_64 memcpy
- don't write uninitialized padding bytes to nscd socket
- fix dl{,v}sym, dl_iterate_phdr and dlopen if some library is
  mapped into ld.so's inter-segment hole on x86_64 (#245035, #244545)
- fix LD_AUDIT=a:b program (#180432)
- don't crash on pseudo-zero long double values passed to
  *printf on i?86/x86_64/ia64 (BZ#4586)
- fix *printf %La and strtold with some hexadecimal floating point
  constants on ppc/ppc64
- fix nextafterl on ppc/ppc64
- fix sem_timedwait on i?86 and x86_64

* Thu May 24 2007 Jakub Jelinek <jakub@redhat.com> 2.6-3
- don't use %%config(missingok) for locale-archive.tmpl,
  instead of removing it altogether truncate it to zero
  size (#240697)
- add a workaround for #210748

* Mon May 21 2007 Jakub Jelinek <jakub@redhat.com> 2.6-2
- restore malloc_set_state backwards compatibility (#239344)
- fix epoll_pwait (BZ#4525)
- fix printf with unknown format spec or positional arguments
  and large width and/or precision (BZ#4514)
- robust mutexes fix (BZ#4512)

* Tue May 15 2007 Roland McGrath <roland@redhat.com> 2.6-1
- glibc 2.6 release

* Fri May 11 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-24
- utimensat, futimens and lutimes support

* Thu May 10 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-23
- use madvise MADV_DONTNEED in malloc
- fix ia64 feraiseexcept
- fix s390{,x} feholdexcept (BZ#3427)
- ppc fenv fixes
- make fdatasync a cancellation point (BZ#4465)
- fix *printf for huge precisions with wide char code and multi-byte
  strings
- fix dladdr (#232224, BZ#4131)

* Fri May  4 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-22
- add transliteration for <U2044> (BZ#3213)
- fix *scanf with %f on hexadecimal floats without exponent (BZ#4342)
- fix *printf with very large precisions for %s (#238406, BZ#4438)
- fix inet_ntop size checking for AF_INET (BZ#4439)
- for *printf %e avoid 1.000e-00, for exponent 0 always use + sign (#238431)
- fix a regression introduced in #223467 changes
- gethostby*_r alignment fixes (BZ#4381)
- fix ifaddrs error handling

* Mon Apr 16 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-21
- don't include individual locale files in glibc-common,
  rather include prepared locale-archive template and let
  build-locale-archive create locale-archive from the template
  and any user supplied /usr/lib/locale/*_* directories,
  then unlink the locale-archive template - this should save
  > 80MB of glibc-common occupied disk space
- fix _XOPEN_VERSION (BZ#4364)
- fix printf with %g and values tiny bit smaller than 1.e-4 (#235864,
  BZ#4362)
- fix NIS+ __nisfind_server (#235229)

* Sat Mar 31 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-20
- assorted NIS+ speedups (#223467)
- fix HAVE_LIBCAP configure detection (#178934)
- remove %{_prefix}/sbin/rpcinfo from glibc-common (#228894)
- nexttoward*/nextafter* fixes (BZ#3306)
- feholdexcept/feupdateenv fixes (BZ#3427)
- speed up fnmatch with two or more * in the pattern

* Sat Mar 17 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-19
- fix power6 libm compat symbols on ppc32 (#232633)
- fix child refcntr in NPTL fork (#230198)
- fix ifaddrs with many net devices on > 4KB page size arches (#230151)
- fix pthread_mutex_timedlock on x86_64 (#228103)
- various fixes (BZ#3919, BZ#4101, BZ#4130, BZ#4181, BZ#4069, BZ#3458)

* Wed Feb 21 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-18
- fix nftw with FTW_CHDIR on / (BZ#4076)
- nscd fixes (BZ#4074)
- fix fmod{,f,l} on i?86 (BZ#3325)
- support localized digits for fp values in *scanf (BZ#2211)
- namespaces fixes (BZ#2633)
- fix euidaccess (BZ#3842)
- glob fixes (BZ#3996)
- assorted locale data fixes (BZ#1430, BZ#672, BZ#58, BZ#3156,
  BZ#2692, BZ#2648, BZ#3363, BZ#3334, BZ#3326, BZ#3322, BZ#3995,
  BZ#3885, BZ#3884, BZ#3851)

* Sun Feb 11 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-17
- RFC2671 support in resolver (#205842)
- fix strptime (BZ#3944)
- fix regcomp with REG_NEWLINE (BZ#3957)
- fix pthread_mutex_timedlock on x86_64 (#228103)

* Fri Feb  2 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-16
- add strerror_l
- fix application crashes when doing NSS lookups through nscd
  mmapped databases and nscd decides to start garbage collection
  during the lookups (#219145, #225315)
- fix %0lld printing of 0LL on 32-bit architectures (BZ#3902)
- ignore errors from install-info in glibc-devel scriptlets
  (#223691)

* Wed Jan 17 2007 Jakub Jelinek <jakub@redhat.com> 2.5.90-15
- fix NIS getservbyname when proto is NULL
- fix nss_compat +group handling (#220658)
- cache services in nscd
- fix double free in fts_close (#222089)
- fix vfork+execvp memory leak (#221187)
- soft-fp fixes (BZ#2749)
- further strtod fixes (BZ#3855)
- make sure pthread_kill doesn't return EINVAL even if
  the target thread exits in between pthread_kill ESRCH check
  and the actual tgkill syscall (#220420)
- fix ABBA deadlock possibility in ld.so scope locking code

* Tue Dec 19 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-14
- fix {j,m}rand48{,_r} on 64-bit arches (BZ#3747)
- handle power6x AT_PLATFORM (#216970)
- fix a race condition in getXXbyYY_r (#219145)
- fix tst-pselect testcase

* Thu Dec 14 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-13
- fix setcontext on ppc32 (#219107)
- fix wide stdio after setvbuf (#217064, BZ#2337)
- handle relatime mount option in statvfs
- revert i?86/x86_64 clone CFI temporarily

* Sun Dec 10 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-12
- fix hasmntopt (#218802)
- fix setusershell and getusershell (#218782)
- strtod fixes (BZ#3664, BZ#3673, BZ#3674)
- fix memusage with realloc (x, 0)

* Tue Dec  5 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-11
- allow suid apps to setenv NIS_PATH and influence through that
  nis_list and nis_lookup (#209155)
- fix ttyname and ttyname_r with invalid file descriptor (#218276)
- cs_CZ LC_TIME fixes (#218438)
- fix build with 2.6.19+ headers (#217723)

* Fri Dec  1 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-10
- fix x86-64 restore_rt unwind info

* Thu Nov 30 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-9
- fix last svc_run change (#217850)
- on ppc64 build __libc_start_main without unwind info,
  as it breaks MD_FROB_UPDATE_CONTEXT (#217729, #217775; in the
  future that could be fixable just by providing .cfi_undefined r2
  in __libc_start_main instead)
- add unwind info for x86-64 restore_rt signal return landing pad
  (#217087)
- add power6x subdir to /%{_lib}/ and /%{_lib}/rtkaio/,
  link all libs from ../power6/* into them

* Tue Nov 28 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-8
- fix svc_run (#216834, BZ#3559)
- add -fasynchronous-unwind-tables to CFLAGS (#216518)
- make sure there is consistent timestamp for /etc/ld.so.conf,
  /etc/localtime and /etc/rpc between multilib glibc rpms

* Mon Nov 20 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-7
- handle IPv6 addresses in /etc/hosts that are mappable to
  IPv4 addresses in IPv4 host lookups (#215283)
- fix :include: /etc/alias handling (#215572)
- handle new tzdata format to cope with year > 2037 transitions
  on 64-bit architectures

* Fri Nov 10 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-6
- fix strxfrm fix
- fix i?86 floor and ceil inlines (BZ#3451)

* Thu Nov  9 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-5
- fix sysconf (_SC_LEVEL{2,3}_CACHE_SIZE) on Intel Core Duo
  CPUs
- fix libthread_db.so on TLS_DTV_AT_TP architectures
- fix --inhibit-rpath (#214569)
- fix _r_debug content when prelinked ld.so executes
  a program as its argument
- fix strxfrm
- powerpc-cpu add-on updates

* Fri Nov  3 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-4
- fix atexit backwards compatibility (#213388)
- add mai_IN locale (#213415)
- remove bogus %{_libdir}/librt.so.1 symlink (#213555)
- fix memusage (#213656)
- change libc.info category (#209493)

* Sun Oct 29 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-3
- fix suid/sgid binaries on i?86/x86_64 (#212723)

* Fri Oct 27 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-2
- fix ia64 build
- don't call _dl_close outside of dl_load_lock critical section
  if dlopen failed (BZ#3426)
- add rtld scope locking (#211133)

* Wed Oct 25 2006 Jakub Jelinek <jakub@redhat.com> 2.5.90-1
- fix i?86 6 argument syscalls (e.g. splice)
- fix rtld minimal realloc (BZ#3352)
- fix RFC3484 getaddrinfo sorting according to rules 4 and 7 (BZ#3369)
- fix xdrmem_setpos (#211452)
- bump __GLIBC_MINOR__
- increase PTHREAD_STACK_MIN on ppc{,64} to 128K to allow
  64K pagesize kernels (#209877)
- speed up initgroups on NIS+ (#208203)

* Mon Oct  2 2006 Jakub Jelinek <jakub@redhat.com> 2.5-2
- fix nscd database growing (#207928)
- bypass prelinking when LD_DYNAMIC_WEAK=1 is in the environment

* Fri Sep 29 2006 Jakub Jelinek <jakub@redhat.com> 2.5-1
- glibc 2.5 release

* Wed Sep 27 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-36
- rebuilt with gcc-4.1.1-26 to fix unwind info

* Mon Sep 25 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-35
- fix glob with large number of matches (BZ#3253)
- fix fchownat on kernels that don't support that syscall (BZ#3252)
- fix lrintl on s390{,64}

* Sat Sep 23 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-34
- fix ppc{32,64} longjmp (BZ#3225)
- fix user visible spelling errors (BZ#3137)
- fix l{,l}rint{,f,l} around zero (BZ#2592)
- avoid stack trampoline in s390{,x} makecontext

* Fri Sep 15 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-33
- fix dlclose (#206639)
- don't load platform optimized libraries if kernel doesn't set
  AT_PLATFORM
- fix ppc{32,64} libSegFault.so
- use -mtune=generic even for glibc-devel.i386 (#206437)
- fix /%{_lib}/librt.so.1 symlink

* Fri Sep 15 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-32
- on ppc* use just AT_PLATFORM and altivec AT_HWCAP bit for library selection
- fix lrintl and lroundl on ppc{,64}
- use hidden visibility on fstatat{,64} and mknodat in libc_nonshared.a

* Sun Sep 10 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-31
- fix pthread_cond_{,timed}wait cancellation (BZ#3123)
- fix lrint on ppc32 (BZ#3155)
- fix malloc allocating more than half of address space (BZ#2775)
- fix mktime on 32-bit arches a few years after 2038 (BZ#2821)

* Thu Sep  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-30
- add librtkaio, to use it add /%{lib}/rtkaio to your
  LD_LIBRARY_PATH or /etc/ld.so.conf
- fix or_IN February name (#204730)
- fix pthread_create called from cancellation handlers (BZ#3124)
- fix regex case insensitive searches with characters where upper
  and lower case multibyte representations have different length
  (e.g. I and dotless i, #202991)

* Tue Sep  5 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-29
- randomize resolver query ids before use instead after use (#205113)
- fix resolver symver checking with DT_GNU_HASH (#204909)
- put .hash section in glibc libraries at the end of RO segment
  when .gnu.hash is present

* Thu Aug 31 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-28
- another malloc doubly linked list corruption problem fix (#204653)

* Thu Aug 31 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-27
- allow $LIB and $PLATFORM in dlopen parameters even in suid/sgid (#204399)
- handle $LIB/$PLATFORM in LD_LIBRARY_PATH
- fix splice prototype (#204530)

* Mon Aug 28 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-26
- real fix for the doubly linked list corruption problem
- try harder in realloc to allocate memory (BZ#2684)
- fix getnameinfo error reporting (#204122)
- make localedef more robust on invalid input (#203728)

* Fri Aug 25 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-25
- temporarily back out code to limit number of unsorted block
  sort iterations (#203735, #204027)
- handle PLT symbols in dladdr properly (BZ#2683)
- avoid malloc infinite looping for allocations larger than
  the system can allocate (#203915)

* Tue Aug 22 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-23
- malloc fixes, especially for 32-bit arches (#202309)
- further *_IN locale fixes (#200230)
- fix get{serv,rpc}ent{,_r} if NIS map is empty (#203237)
- fix /usr/bin/iconv (#203400)

* Fri Aug 18 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-22
- rebuilt with latest binutils to pick up 64K -z commonpagesize
  on ppc/ppc64 (#203001)

* Tue Aug 15 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-21
- if some test gets stuck, kill the tee process after make check
  finishes
- build with -mtune=generic on i686 and x86_64

* Tue Aug 15 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-20
- PTHREAD_PRIO_PROTECT support
- fix errno if nice() fails (#201826)

* Thu Aug 10 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-19
- adaptive malloc brk/mmap threshold
- fix fchownat to use kernel syscall (if available) on many arches (#201870)
- only define O_DIRECT with -D_GNU_SOURCE on ia64 to match all
  other arches (#201748)

* Mon Aug  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-18
- NIS+ fixes
- fix memusage and xtrace scripts (#200736)
- redirect /sbin/service sshd condrestart std{out,err} to /dev/null
  when executed from glibc_post_upgrade

* Wed Aug  2 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-17
- typo fix for the dladdr patch
- build i?86 glibc with -mno-tls-direct-seg-refs (#200469)

* Wed Aug  2 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-16
- fix dladdr on binaries/libraries with only DT_GNU_HASH and no
  DT_HASH (#200635)
- fix early timeout of initgroups data in nscd (#173019)
- add am/pm display to es_PE and es_NI locales (#167101)
- fix nss_compat failures when nis/nis+ unavailable (#192072)

* Mon Jul 31 2006 Roland McGrath <roland@redhat.com> 2.4.90-15
- fix missing destructor calls in dlclose (#197932)
- enable transliteration support in all locales (#196713)
- disallow RTLD_GLOBAL flag for dlmopen in secondary namespaces (#197462)
- PI mutex support

* Mon Jul 10 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-13
- DT_GNU_HASH support

* Fri Jun 30 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-12
- buildrequire gettext
- enable fstatat64/newfstatat syscalls even on ppc*/s390*/ia64 (#196494)
- fix out of memory behavior in gettext (#194321)
- fix regex on multi-byte non-UTF-8 charsets (#193873)
- minor NIS+ fixes (#190803)
- don't use cancellable calls in posix_spawn* and only set{u,g}id
  current thread if requested (#193631)

* Wed May 31 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-11
- don't exit from nscd -i <database> before the database is
  actually invalidated, add locking to prune_cache (#191464)
- build glibc-devel.i386 static libraries with
  -mno-tls-direct-seg-refs -DNO_TLS_DIRECT_SEG_REFS
- RFC3542 support (advanced API for IPv6; #191001, BZ##2693)

* Wed May 24 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-10
- on i686 make glibc owner of /lib/i686 directory (#192597)
- search parent NIS+ domains (#190803)

* Sun May 21 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-9
- update from CVS
  - big NIS+ changes

* Fri May 19 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-8
- update from CVS
  - fix nss_compat when SETENT_BATCH_READ=TRUE is in /etc/default/nss
  - fix RFC3484 precedence table for site-local and ULA addresses (#188364)
  - fix a sunrpc memory leak

* Thu May 11 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-7
- update from CVS
  - fix tcgetattr (#177965)
  - fix <sys/queue.h> (#191264)

* Fri May  5 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-6
- update from CVS
- rebuilt using fixed rpm

* Fri May  5 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-5
- update from CVS
  - some NIS+ fixes
  - allow overriding rfc3484 address sorting tables for getaddrinfo
    through /etc/gai.conf (sample config file included in %%doc directory)

* Mon May  1 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-4
- update from CVS
  - SETENT_BATCH_READ /etc/default/nss option for speeding up
    some usages of NIS+ (#188246)
  - move debug state change notification (#179208)
  - fix ldd script if one of the dynamic linkers is not installed (#190259)

* Thu Apr 27 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-3
- update from CVS
  - fix a typo in nscd.conf (#190085)
  - fix handling of SIGHUP in nscd when some caches are disabled (#189978)
  - make nscd paranoia mode working with non-root server-user (#189779)

* Wed Apr 26 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-2
- update from CVS
  - fix getaddrinfo (#190002)
  - add auto-propagate nscd.conf options (#177154)
  - fix nscd auditing (#169148)

* Tue Apr 25 2006 Jakub Jelinek <jakub@redhat.com> 2.4.90-1
- update from CVS

* Mon Apr 24 2006 Jakub Jelinek <jakub@redhat.com> 2.4-6
- update from CVS
  - NIS+ fixes
  - don't segfault on too large argp key values (#189545)
  - getaddrinfo fixes for RFC3484 (#188364)

* Tue Mar 28 2006 Jakub Jelinek <jakub@redhat.com> 2.4-5
- update from CVS
  - pshared robust mutex support
  - fix btowc and bwtoc in C++ (#186410)
  - fix NIS+ (#186592)
  - don't declare __wcsto*l_internal for non-GCC or if not -O1+ (#185667)
- don't mention nscd failures on 2.0 kernels (#185335)

* Tue Mar  7 2006 Roland McGrath <roland@redhat.com> 2.4-4
- back up %%{ix86} gdb conflicts to < 6.3.0.0-1.111

* Tue Mar  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4-3
- really fix rintl on ppc64

* Tue Mar  7 2006 Jakub Jelinek <jakub@redhat.com> 2.4-2
- accurate unwind info for lowlevellock.h stubs on %%{ix86}
- fix ppc/ppc64 ceill, floorl, rintl, roundl and truncl (BZ#2423)

* Mon Mar  6 2006 Jakub Jelinek <jakub@redhat.com> 2.4-1
- update from CVS
  - glibc 2.4 release

* Mon Mar  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.91-2
- update from CVS
  - fix sYSMALLOc for MALLOC_ALIGNMENT > 2 * SIZE_SZ (#183895)
  - revert ppc32 malloc alignment patch, it breaks malloc_set_state
    and needs some further thoughts and time (#183894)
- provide accurate unwind info for lowlevellock.h stubs on x86_64

* Thu Mar  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.91-1
- update from CVS
  - fixes for various arches
- ensure malloc returns pointers aligned to at least
  MIN (2 * sizeof (size_t), __alignof__ (long double))
  (only on ppc32 this has not been the case lately with addition
   of 128-bit long double, #182742)

* Wed Mar  1 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-39
- update from CVS

* Fri Feb 17 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-38
- update from CVS
  - robust mutexes rewrite

* Mon Feb 13 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-37
- update from CVS
  - *at fixes
  - unshare syscall wrapper

* Sat Feb  4 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-36
- update from CVS
  - fix frequency setting for ITIMER_PROF (#179938, BZ#2268)
  - fix powerpc inline fegetround ()
  - fix nptl_db (#179946)

* Fri Feb  3 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-35
- update from CVS
  - handle futimesat (fd, NULL, tvp) as futimes (fd, tvp)
- fix <stdlib.h> q{e,f,g}cvt{,_r} for -mlong-double-64

* Thu Feb  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-34
- fix <math.h> with C++ and -mlong-double-64 (#179742)
- add nexttowardl redirect for -mlong-double-64

* Thu Feb  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-33
- update from CVS
  - long double support fixes

* Wed Feb  1 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-32
- update from CVS
  - 128-bit long double fixes for ppc{,64}, s390{,x} and sparc{,v9},
    alpha 128-bit long double support
- add inotify syscall numbers to the override <asm/unistd.h> headers
  (#179366)

* Mon Jan 30 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-31
- update from CVS
  - 128-bit long double on ppc, ppc64, s390, s390x and sparc{,v9}
- add some new syscall numbers to the override <asm/unistd.h>
  headers

* Mon Jan  9 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-30
- update from CVS
  - <pthread.h> initializer fixes for -std=c{8,9}9 on 32-bit
    arches
- avoid writable .rodata (#177121)

* Fri Jan  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-29
- update from CVS
  - make pthread_mutex_t an unnamed union again, as it affects
    libstdc++ ABI mangling

* Fri Jan  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-28
- update from CVS
  - make aio_suspend interruptible by signals (#171968)

* Fri Jan  6 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-27
- only rely on d_type in 32-bit getdents on s390 for 2.6.11+

* Wed Jan  4 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-26
- update from CVS
  - for newly linked lio_listio* callers, send per request
    notifications (#170116)
  - fixup nscd -S option removal changes (#176860)
  - remove nonnull attribute from ctermid (#176753)
  - fix PTHREAD_*_INITIALIZER{,_NP} on 64-bit arches
  - SPARC NPTL support for pre-v9 CPUs
- drop support for 2.4.xx and < 2.6.9 kernels

* Mon Jan  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-25
- update from CVS
  - s390{,x} and sparc{,64} pointer mangling fixes
- install a sanitized LinuxThreads <bits/libc-lock.h>

* Mon Jan  2 2006 Jakub Jelinek <jakub@redhat.com> 2.3.90-24
- update from CVS
  - nscd audit changes (#174422)
  - ppc{32,64} vDSO support and ppc32 hp-timing

* Tue Dec 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-23
- update from CVS
  - robust mutexes
- fix transliteration segfaults (#176573, #176583)
- ignore prelink temporaries in ldconfig (#176570)

* Wed Dec 21 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-22
- update from CVS
  - minor fts fixes
- revert broken _Pragma () workaround
- fix ldconfig on bi-arch architectures (#176316)

* Tue Dec 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-21
- update from CVS
  - fix pointer (de)mangling in gconv_cache.c

* Tue Dec 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-20
- update from CVS
  - time ((void *) 1) should segfault, not return -EFAULT (#174856, BZ#1952)
  - fix errlist generation
- update ulps for GCC 4.1 on IA-64

* Mon Dec 19 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-19
- update from CVS
  - sysdeps/generic reorg
  - setjmp/longjmp jump pointer mangling
- rebuilt with GCC 4.1-RH prerelease, worked around broken _Pragma ()
  handling in it
- remove glibc-profile subpackage
- use non-PLT calls for malloc/free/realloc/memalign invocations in
  mtrace and mcheck hooks (#175261)
- setjmp/longjmp jump pointer mangling on ppc{,64}/ia64/s390{,x}

* Sat Nov 19 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-18
- update from CVS
  - change <sys/stat.h> for broken apps that #define const /**/,
    handle non-GCC compilers
  - fix ppc{32,64} strncmp (BZ#1877, #173643, IT#83510)
  - provide shmatt_t typedef in ia64 <sys/shm.h (#173680)
  - support 2nd arg to futimesat being NULL (#173581)

* Wed Nov 16 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-17
- update from CVS
  - fix <sys/stat.h> in C++
  - {fstat,fchown,rename,unlink}at fixes
  - epoll_wait is now a cancellation point

* Tue Nov 15 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-16
- update from CVS
- make sure waitid syscall is used on ppc*/s390*

* Thu Oct 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-15
- update from CVS
  - be permissive in %n check because of kernel bug #165351 (#171240)
  - don't misalign stack in pthread_once on x86_64 (#170786, IT#81521)
  - many locale fixes

* Mon Oct 10 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-14
- update from CVS
  - fix malloc bug after fork introduced in the last update
  - fix getent hosts IP for IPv4 IPs (#169831)

* Mon Oct  3 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-13
- update from CVS
  - fix setuid etc. hangs if some thread exits during the call (#167766)
  - fix innetgr memory leak (#169051)
  - support > 2GB nscd log files (#168851)
  - too many other changes to list here
- include errno in nscd message if audit_open failed (#169148)

* Mon Sep 12 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-12
- update from CVS
  - netgrp handling fixes (#167728)
  - fix memory leak in setlocale (BZ#1318)
  - fix hwcaps computation
  - several regex portability improvements (#167019)
  - hypotf fix
  - fix *printf return code if underlying write fails (BZ#1146)
  - PPC64 dl{,v}sym fixes for new ABI .opd symbols
- fix calloc with MALLOC_PERTURB_ in environment on 64-bit architectures
  (#166719)
- source /etc/sysconfig/nscd (if it exists) in /etc/rc.d/init.d/nscd
  (#167083)
- add %%triggerin for tzdata to glibc-common, so that tzdata updates
  update /etc/localtime and /var/spool/postfix/etc/localtime if they
  exist (#167787)

* Mon Aug 29 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-11
- FUTEX_WAKE_OP support to speed up pthread_cond_signal

* Wed Aug 24 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-10
- update from CVS
  - fix growing of nscd persistent database (BZ#1204)
  - fix _FORTIFY_SOURCE mbstowcs and wcstombs if destination size
    is known at compile time, but length argument is not

* Mon Aug 22 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-9
- update from CVS
  - fix resolving over TCP (#161181, #165802)
  - on ia64 don't abort on unhandled math function exception codes
    (#165693)

* Mon Aug  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-8
- update from CVS
  - nscd persistent database verifier (#164001)
  - cleanup _FORTIFY_SOURCE bits/*.h headers (#165000)
  - handle EINTR in sigwait properly
- make sure poor man's stack guard randomization keeps first
  byte 0 even on big-endian 32-bit arches
- fix {elf,nptl}/tst-stackguard1
- obsolete linuxthreads-devel in glibc-devel

* Fri Jul 29 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-7
- update from CVS
- do some poor man's stack guard randomization even without
  the costly --enable-stackguard-randomization
- rebuilt with new GCC to make it use -msecure-plt on PPC32

* Mon Jul 25 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-6
- update from CVS
  - fix execvp if PATH is not in environment and the call is going
    to fail (BZ#1125)
  - another bits/wchar2.h fix (#163990)

* Fri Jul 22 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-5
- update from CVS
  - fix stubs.h generation
- don't use _G_va_list in bits/wchar2.h

* Fri Jul 22 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-4
- update from CVS
  - make sure bits/wchar2.h header is installed
  - fix __getgroups_chk return type

* Thu Jul 21 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-3
- update from CVS
  - make sure nscd cmsg buffers aren't misaligned, handle EINTR from
    poll when contacting nscd more gracefully
  - remove malloc attribute from posix_memalign
  - correctly size nscd buffer for grpcache key (#163538)
  - fix atan2f
  - fix error memory leaks
  - some more _FORTIFY_SOURCE protection

* Fri Jul  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-2
- update from CVS
  - ia64 stack protector support
  - handle DNS referral results as server errors (#162625)
  - ctan{,h}{,f,l} fixes (#160759)
  - pass argc, argv and envp also to executable's *ni_array
    functions (BZ#974)
  - add ellipsis to clone prototype (#161593)
  - fix glibc-profile (#162601)
  - nss_compat fixes
- use sysdeps/generic version of <bits/stdio-lock.h> in installed
  headers instead of NPTL version (#162634)

* Mon Jun 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.90-1
- update from CVS
  - stack protector support
  - fix xdr_{,u_}{longlong_t,hyper} on 64-bit arches (#161583)
- enable @GLIBC_2.4 symbols
- remove linuxthreads

* Mon Jun 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-11
- update from CVS
  - PPC32 -msecure-plt support
  - support classes keyword in /etc/hesiod.conf (#150350)
  - add RLIMIT_NICE and RLIMIT_RTPRIO to <sys/resources.h> (#157049)
  - decrease number of .plt relocations in libc.so
  - use -laudit in nscd (#159217)
  - handle big amounts of networking interfaces in getifaddrs/if_nameindex
    (#159399)
  - fix pa_IN locale's am_pm (#158715, BZ#622)
  - fix debugging of PIEs

* Mon May 30 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-10
- fix LD_ASSUME_KERNEL (since 2.3.5-8 GLRO(dl_osversion)
  has been always overwritten with the version of currently
  running kernel)
- remove linuxthreads man pages other than those covered in
  3p section, as 3p man pages are far better quality and describe
  POSIX behaviour that NPTL implements (#159084)

* Tue May 24 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-9
- update from CVS
  - increase bindresvport's LOWPORT to 512, apparently some
    broken daemons don't think 0 .. 511 ports are reserved

* Mon May 23 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-8
- update from CVS
  - fix kernel version check in ld.so
- fix sendfile{,64} prototypes (BZ#961)
- try more ports in bindresvport if all 600..1023 are
  used, don't use priviledged ports when talking to portmap
  (#141773)

* Fri May 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-7
- update from CVS
  - make regexec thread safe (BZ#934)
- fix statically linked programs on i?86, x86_64, s390* and
  sparc* (#158027)
- fix IBM939 iconv module (BZ#955)

* Wed May  4 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-6
- update from CVS
  - fix cancellation on i?86
  - add call frame information to i?86 assembly

* Tue May  3 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-5
- update from CVS
  - add some more UTF-8 locales (#156115)
- clean up /lib64/tls instead of /lib/tls on x86-64, s390x and
  ppc64 in glibc_post_upgrade (#156656)
- fix posix_fallocate{,64} (#156289)

* Thu Apr 28 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-4
- update from CVS
  - fix nscd cache pruning (#150748)

* Wed Apr 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-3
- update from CVS
  - fix linuxthreads clocks
- put xen libs into the glibc-2*.i686 package instead of a separate one
- fix librt.so symlink in linuxthreads-devel
- do not include linuxthreads-devel on %{auxarches},
  just on the base architectures

* Wed Apr 27 2005 Jakub Jelinek <jakub@redhat.com> 2.3.5-2
- update from CVS
  - with MALLOC_CHECK_=N N>0 (#153003)
  - fix recursive dlclose (#154641)
  - handle %z in strptime (#154804)
  - automatically append /%{_lib}/obsolete/linuxthreads/
    to standard library search path if LD_ASSUME_KERNEL=N N <= 2.4.19
    or for glibc 2.0 binaries (or broken ones that don't use errno/h_errno
    properly).  Warning: all those will stop working when LinuxThreads
    is finally nuked, which is not very far away
  - remove nonnull attribute from acct prototype (BZ#877)
  - kernel CPU clocks support
  - fix *scanf in locales with multi-byte decimal point

* Wed Apr 27 2005 Roland McGrath <roland@redhat.com>
- glibc-xen subpackage for i686

* Fri Apr 15 2005 Roland McGrath <roland@redhat.com> 2.3.5-1
- update from CVS
  - fix execvp regression (BZ#851)
  - ia64 libm updates
  - sparc updates
  - fix initstate{,_r}/strfry (#154504)
  - grok PT_NOTE in vDSO for kernel version and extra hwcap dirs,
    support "hwcap" keyword in ld.so.conf files

* Mon Apr  4 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-21
- update from CVS
  - fix xdr_rmtcall_args on 64-bit arches (#151686)
- fix <pthread.h> and <bits/libc-lock.h> with -std=c89 -fexceptions (#153774)

* Mon Apr  4 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-20
- move LinuxThreads libraries to /%{_lib}/obsolete/linuxthreads/
  and NPTL libraries to /%{_lib}.  To run a program against LinuxThreads,
  LD_ASSUME_KERNEL=2.4.xx LD_LIBRARY_PATH=/%{_lib}/obsolete/linuxthreads/
  is now needed
- bzip2 ChangeLog* files instead of gzipping them

* Sat Apr  2 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-19
- update from CVS
  - fix nextafterl and several other libm routines on ia64
  - fix initgroups (BZ#661)
- kill nptl-devel subpackage, add linuxthreads-devel,
  compile and link by default against NPTL and only with
  -I/usr/include/linuxthreads -L/usr/%{_lib}/linuxthreads
  against LinuxThreads
- package /usr/lib/debug/%{_lib}/tls/i{5,6}86 symlinks in
  i386 glibc-debuginfo
- limit number of ChangeLog* files in glibc-common %%doc
  to last 2.5 years of changes only to save space

* Fri Mar 25 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-18
- fix build on 64-bit arches with new GCC

* Thu Mar 24 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-17
- update from CVS
  - fix LD_AUDIT in LinuxThreads ld.so
  - fix calloc with M_PERTURB
  - fix error handling in pthread_create with PTHREAD_EXPLICIT_SCHED
    on ppc*/ia64/alpha/mips (BZ#801)
  - fix a typo in WINDOWS-31J charmap (#151739)
  - fix NIS ypprot_err (#151469)

* Sun Mar 20 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-16
- fix pread with -D_FILE_OFFSET_BITS=64 (#151573)

* Sat Mar 19 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-15
- update from CVS
  - better fix for the dlclose bug (#145810, #150414)
  - fix regex crash on case insensitive search in zh_CN locale
    (#151215)
  - fix malloc_trim (BZ#779)
  - with -D_FORTIFY_SOURCE=*, avoid defining read and a bunch of others
    as function-like macros, there are too many broken programs
    out there
- add %%dir %{_prefix}/%{_lib}/gconv to glibc's file list (#151372)

* Sun Mar  6 2005 Roland McGrath <roland@redhat.com> 2.3.4-14
- fix bits/socket2.h macro typos

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-12
- fix tst-chk{2,3}
- fix up AS_NEEDED directive in /usr/%{_lib}/libc.so
- BuildReq binutils >= 2.15.94.0.2-1 for AS_NEEDED, in
  glibc-devel Conflict with binutils < 2.15.94.0.2-1

* Thu Mar  3 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-11
- update from CVS
  - fix execvp (#149290)
  - fix dlclose (#145810)
  - clear padding in gconv-modules.cache (#146614, BZ#776)
- rebuilt with GCC4
- changed __GLIBC_MINOR__ for now back to 3
- back out the newly added GLIBC_2.4 *_chk routines, instead
  do the checking in macros

* Sat Feb 12 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-10
- hopefully fix interaction with prelink (#147655)

* Fri Feb 11 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-9
- update from CVS
  - bi-arch <gnu/stubs.h> (BZ#715)

* Fri Feb 11 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-8
- update from CVS
  - bi-arch <gnu/lib-names.h> (BZ#632)
  - fix libdl on s390 and maybe other platforms
  - fix initstate{,_r} (BZ#710)
  - fix <gnu/stubs.h> generation (BZ#157)
- define CMSPAR in bits/termios.h (#147533)

* Tue Feb  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-7
- update from CVS
  - fix TLS handling in linuxthreads

* Tue Feb  8 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-6
- update from CVS
  - ld.so auditing
  - fix segfault if chrooted app attempts to dlopen a library
    and no standard library directory exists at all (#147067, #144303)
  - fix initgroups when nscd is running, but has group caching disabled
    (#146588)
  - fix pthread_key_{create,destroy} in LinuxThreads when pthread_create
    has not been called yet (#146710)
  - fix ppc64 swapcontext and setcontext (#146736, BZ#700)
  - service nscd cosmetic fixes (#146776)
  - fix IA-32 and x86-64 stack alignment in DSO constructors (#145689)
  - fix zdump -v segfaults on x86-64 (#146210)
  - avoid calling sigaction (SIGPIPE, ...) inside syslog (#146021, IT#56686)
  - fix errno values for futimes (BZ#633)
  - unconditionally include <features.h> in malloc.h (BZ#650)
  - change regex \B handling to match old GNU regex as well as perl/grep's dfa
    (from empty string inside of word to empty string not at a word boundary,
     BZ#693)
  - slightly optimize i686 TLS accesses, use direct TLS %gs access in sem_*
    and allow building -mno-tls-direct-seg-refs glibc that is free of direct TLS
    %gs access with negative offsets
  - fix addseverity
  - fix fmemopen
  - fix rewinddir
  - increase svc{tcp,unix}_create listen backlog

* Thu Jan  6 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-5
- update from CVS
  - add some warn_unused_result marking
  - make ftruncate available even for just -D_POSIX_C_SOURCE=200112L
    (BZ#640)

* Thu Jan  6 2005 Jakub Jelinek <jakub@redhat.com> 2.3.4-4
- update from CVS
  - fix IA-32 stack alignment for LinuxThreads thread functions
    and functions passed to clone(2) directly
  - fix ecvt{,_r} on denormals (#143279)
  - fix __tls_get_addr typo
  - fix rounding in IA-64 alarm (#143710)
  - don't reinitialize __environ in __libc_start_main, so that
    effects of setenv/putenv done in DSO initializers are preserved
    (#144037, IT#57403)
  - fix fmemopen
  - fix vDSO l_map_end and l_text_end values
  - IA64 libm update (#142494)
- fix ppc rint/ceil etc. (BZ#602)

* Tue Dec 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.4-3
- rebuilt

* Mon Dec 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.4-2
- work around rpm bug some more, this time by copying
  iconvconfig to iconvconfig.%%{_target_cpu}.

* Mon Dec 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.4-1
- update from CVS
  - glibc 2.3.4 release
  - add -o and --nostdlib options to iconvconfig
- if /sbin/ldconfig doesn't exist when running
  glibc_post_upgrade.%%{_target_cpu}, just don't attempt to run it.
  This can happen during first install of bi-arch glibc and the
  other arch glibc's %post wil run /sbin/ldconfig (#143326)
- use -o and --nostdlib options to create all needed
  gconv-modules.cache files on bi-arch setups

* Sun Dec 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-99
- rebuilt

* Sat Dec 18 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-98
- add .%%{_target_cpu} to glibc_post_upgrade, only run telinit u
  if /sbin/init is the same ELF class and machine as
  glibc_post_upgrade.%%{_target_cpu} and similarly with
  condrestarting sshd (#143046)

* Fri Dec 17 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-97
- update from CVS
  - fix ppc64 getcontext and swapcontext (BZ#610)
  - sparc/sparc64 fixes

* Wed Dec 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-96
- update from CVS
  - fix i686 __USE_STRING_INLINES strncat
  - make sure ppc/ppc64 maintain correct stack alignment
    across clone

* Wed Dec 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-95
- export nis_domain_of_r from libnsl.so again which was
  unintentionally lost

* Wed Dec 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-93
- update from CVS
  - ppc/ppc64 clone without CLONE_THREAD getpid () adjustement
  - fix MALLOC_CHECK_={1,2,3} for non-contiguous main arena
    (BZ#457)
  - fix sysconf (_POSIX_V6_*) for other ABI environments in
    bi-arch setups
- s390/s390x clone without CLONE_THREAD getpid () adjustement

* Tue Dec 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-92
- update from CVS
- fix %{_prefix}/libexec/getconf filenames generation

* Tue Dec 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-91
- update from CVS
  - double buffer size in getXXbyYY or getXXent on ERANGE
    instead of adding BUFLEN (#142617)
  - avoid busy loop in malloc if another thread is doing fork
    (#142214)
  - some more realloc corruption checks
  - fix getconf _POSIX_V6_WIDTH_RESTRICTED_ENVS output,
    tweak %{_prefix}/libexec/getconf/ filenames

* Fri Dec 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-90
- update from CVS
  - regex speedups
  - use | cat in ldd if running under bash3+ to allow running
    it on binaries that are not through SELinux allowed to access
    console or tty
- add __NR_waitid defines for alpha and ia64

* Wed Dec  8 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-89
- update from CVS
  - fix clone2 on ia64
  - avoid tst-timer5 failing with linuxthreads implementation
- if __libc_enable_secure, disallow mode != normal
- change ldd script to imply -r when -u is used, properly
  propagate return value and handle suid binaries

* Tue Dec  7 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-88
- update from CVS
  - disregard LD_SHOW_AUXV and LD_DYNAMIC_WEAK if __libc_enable_secure
  - disregard LD_DEBUG if __libc_enable_secure in normal mode
    if /suid-debug doesn't exist
  - fix fseekpos after ungetc
  - avoid reading bytes before start of buffers in regex's
    check_dst_limits_calc_pos_1 (#142060)
  - make getpid () working with clone/clone2 without CLONE_THREAD
    (so far on i386/x86_64/ia64 only)
- move %{_prefix}/libexec/getconf/* to glibc from glibc-common
- make %{_prefix}/libexec/getconf directory owned by glibc package

* Fri Dec  3 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-87
- update from CVS
  - build libpthread_nonshared.a objects with -fPIC on s390/s390x
  - fix mktime with < 0 or > 59 tm_sec on entry
  - remove nonnull attribute for realpath
  - add $(make-target-directory) for errlist-compat.c rule
    (hopefully fix #141404)
- add testcase for ungetc bug
- define _POSIX_{,THREAD_}CPUTIME to 0 on all Linux arches

* Tue Nov 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-86
- update from CVS
  - some posix_opt.h fixes
- fix strtold use of unitialized memory (#141000)
- some more bugfixes for bugs detected by valgrind
- rebuilt with GCC >= 3.4.3-5 to avoid packed stack layout
  on s390{,x} (#139678)

* Fri Nov 26 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-85
- update from CVS
  - support -v specification in getconf
  - fix sysconf (_SC_LFS64_CFLAGS) etc.
  - avoid thread stack aliasing issues on EM64T (#140803)
- move %{_prefix}/include/nptl headers from nptl-devel
  to glibc-headers, so that even NPTL specific programs
  can be built bi-arch without problems

* Wed Nov 24 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-84
- update from CVS
  - fix memory leak in getaddrinfo if using nscd (#139559)
  - handle large lines in /etc/hosts and /etc/networks
    (#140378)
  - add nonnull attributes to selected dirent.h and dlfcn.h
    functions

* Sun Nov 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-83
- update from CVS
  - add deprecated and/or nonnull attribute to some signal.h
    functions
  - speed up tzset () by only using stat instead of open/fstat
    when calling tzset for the second and following time if
    /etc/localtime has not changed
- fix tgamma (BZ #552)

* Sat Nov 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-82
- update from CVS
  - some malloc () checking
  - libpthread.a object dependency cleanups (#115157)
  - <bits/socket.h> fix for -std=c89 -pedantic-errors (#140132)

* Fri Nov 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-81
- don't use chunksize in <= 2 * SIZE_SZ free () checks

* Fri Nov 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-80
- update from CVS
  - with -D_FORTIFY_SOURCE=2, prevent missing %N$ formats
  - for -D_FORTIFY_SOURCE=2 and %n in writable format string,
    issue special error message instead of using the buffer overflow
    detected one
  - speedup regex searching with REG_NOSUB, add RE_NO_SUB,
    speedup searching with nested subexps (BZ #544)
  - block SIGCANCEL in NPTL timer_* helper thread
- further free () checking

* Tue Nov 16 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-79
- update from CVS
- fix free () checking
- move /etc/default/nss into glibc-common (hopefully fix #132392)

* Mon Nov 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-78
- update from CVS
  - fix LD_DEBUG=statistics
  - issue error message before aborting in __chk_fail ()
- some more free () checking

* Fri Nov 12 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-77
- update from CVS
  - speedup regex on palindromes (BZ #429)
  - fix NPTL set{,e,re,res}[ug]id, so that even if making process
    less priviledged all threads change their credentials successfully

* Wed Nov 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-76
- update from CVS
  - fix regcomp crash (#138439)
  - fix ftell{,o,o64} (#137885)
  - robustification of nscd to cope with corrupt databases (#137140)
  - fix NPTL with pthread_exit immediately after pthread_create (BZ #530)
  - some regex optimizations

* Tue Nov  2 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-75
- update from CVS
  - mktime cleanups (BZ #487, #473)
  - unique comments in free(3) check error messages
- adjust some x86_64 headers for -m32 (#129712)
- object size checking support even with GCC-3.4.2-RH >= 3.4.2-8

* Wed Oct 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-74
- fix <netinet/udp.h> header
- fix globfree (#137176)
- fix exiting if there are dlmopened libraries in namespaces
  other than main one not closed yet
- export again _res_opcodes and __p_{class,type}_syms from
  libresolv.so that were lost in -69

* Thu Oct 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-73
- remove setaltroot and key{_add,_request,ctl} also from Versions
- back out _sys_errlist changes

* Thu Oct 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-72
- back out setaltroot and key{_add,_request,ctl} addition
- fix severe x86-64 symbol versioning regressions that breaks
  e.g. java binaries

* Wed Oct 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-71
- update from CVS
  - fix minor catchsegv temp file handling vulnerability
    (CAN-2004-0968, #136319)
  - add 4 new errno codes
  - setaltroot, key{_add,_request,ctl} syscalls on some arches
  - export _dl_debug_state@GLIBC_PRIVATE from ld.so again for
    gdb purpose
  - use inet_pton to decide what is address and what is hostname
    in getent (#135422)
  - change dladdr/dladdr1, so that dli_saddr is the same kind
    of value as dlsym/dlvsym return (makes difference on ia64/hppa only)
  - fix catchsegv script so that it works with both 32-bit and 64-bit
    programs on multi-arch platforms

* Tue Oct 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-70
- update from CVS
- require newer selinux-policy (#135978)
- add %%dir for /var/run/nscd and /var/db/nscd and %%ghost
  files in it
- conflict with gcc4 4.0.0-0.6 and earlier (needs __builtin_object_size)

* Mon Oct 18 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-69
- update from CVS
  - object size checking support (-D_FORTIFY_SOURCE={1,2})

* Thu Oct 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-68
- update from CVS
  - support for namespaces in the dynamic linker
  - fix dlclose (BZ #77)
  - libSegFault.so uses now backtrace() to work on IA-64, x86-64
    and s390 (#130254)

* Tue Oct 12 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-67
- update from CVS
  - use non-blocking sockets in resolver (#135234)
  - reset pd->res options on thread exit, so that threads
    reusing cached stacks get resolver state properly initialized
    (BZ #434)

* Wed Oct  6 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-66
- update from CVS
- avoid using perl in the spec file, buildrequire sed >= 3.95
  (#127671)
- export TIMEOUTFACTOR=16
- fix _JMPBUF_CFA_UNWINDS_ADJ on s390{,x}

* Tue Oct  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-65
- update from CVS
  - define _POSIX_THREAD_PROCESS_SHARED and _POSIX_CLOCK_SELECTION
    to -1 in LinuxThreads
  - define _POSIX_CPUTIME and _POSIX_THREAD_CPUTIME to 0
    on i?86/ia64 and make sure sysconf (_SC_{,THREAD_}CPUTIME)
    returns correct value
- if _POSIX_CLOCK_SELECTION == -1 in nscd, still try
  sysconf (_SC_CLOCK_SELECTION) and if it returns true,
  dlopen libpthread.so and dlsym pthread_condattr_setclock
- build nscd with -z relro and -z now

* Mon Oct  4 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-64
- update from CVS
  - stop using __builtin_expect in assert and assert_perror
    (#127606)
  - try to avoid too much VA fragmentation with malloc
    on flexmap layout (#118574)
  - nscd robustification
  - change valloc to use debugging hooks (#134385)
- make glibc_post_upgrade more verbose on errors (Fergal Daly,
  #125700)

* Fri Oct  1 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-63
- update from CVS
  - fix __nscd_getgrouplist
  - fix a typo in x86_64 pthread_mutex_timedwait fix

* Fri Oct  1 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-62
- update from CVS
  - fix NPTL pthread_mutex_timedwait on i386/x86_64 (BZ #417)

* Thu Sep 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-61
- update from CVS
  - some nscd fixes (#134193)
  - cache initgroups in nscd (#132850)
  - reread /etc/localtime in tzset () even if just mtime changed
    (#133481)
  - fix glob (#126460)
  - another get_myaddress fix

* Wed Sep 29 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-60
- update from CVS
  - fix get_myaddress (#133982)
  - remove nonnull attribute from second utime argument (#133866)
  - handle SIGSETXID the same way as SIGCANCEL in
    sigaction/pthread_kill/sigwait/sigwaitinfo etc.
  - add __extension__ to long long types in NPTL <bits/pthreadtypes.h>

* Mon Sep 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-59
- update from CVS
  - fix BZ #151, #362, #381, #407
  - fdim fix for +inf/+inf (BZ #376)

* Sun Sep 26 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-58
- update from CVS
  - vasprintf fix (BZ #346)
  - gettext locking (BZ #322)
- change linuxthreads useldt.h inclusion login again, the last
  one failed all linuxthreads FLOATING_STACKS tests

* Sat Sep 25 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-57
- update from CVS
  - fix setuid in LD_ASSUME_KERNEL=2.2.5 libc (#133558)
  - fix nis locking (#132204)
  - RTLD_DEEPBIND support
  - fix pthread_create bugs (BZ #401, #405)

* Wed Sep 22 2004 Roland McGrath <roland@redhat.com> 2.3.3-56
- migrated CVS to fedora-branch in sources.redhat.com glibc repository
  - source tarballs renamed
  - redhat/ moved to fedora/, some old cruft removed
- update from trunk
  - some __nonnull annotations

* Wed Sep 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-55
- update from CVS
  - set{re,e,res}[ug]id now affect the whole process in NPTL
  - return EAGAIN instead of ENOMEM when not enough memory
    in pthread_create

* Fri Sep 17 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-54
- update from CVS
  - nscd getaddrinfo caching

* Tue Sep 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-53
- restore temporarily old definition of __P()/__PMT()
  for third party apps

* Tue Sep 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-52
- update from CVS
  - nscd bi-arch fix
  - remove all uses of __P()/__PMT() from glibc headers
- update and reenable nscd SELinux patch
- remove libnss1* and libnss*.so.1 compatibility NSS modules
  on IA-32, SPARC and Alpha

* Fri Sep 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-51
- update from CVS
  - disable one of the malloc double free checks for non-contiguous
    arenas where it doesn't have to be true even for non-broken
    apps

* Thu Sep  9 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-50
- update from CVS
  - pwd/grp/host loops with nscd speed up by sharing the
    nscd cache r/o with applications
  - inexpensive double free check in free(3)
  - make NPTL pthread.h initializers usable even from C++
    (BZ #375)
- use atomic instructions even in i386 nscd on i486+ CPUs
  (conditionally)

* Fri Sep  3 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-49
- update from CVS
- fix linuxthreads tst-cancel{[45],-static}

* Fri Sep  3 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-48
- update from CVS
  - fix pthread_cond_destroy (BZ #342)
  - fix fnmatch without FNM_NOESCAPE (BZ #361)
  - fix ppc32 setcontext (BZ #357)
- add NPTL support for i386 glibc (only if run on i486 or higher CPU)
- add __NR_waitid defines for i386, x86_64 and sparc*

* Tue Aug 31 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-47
- update from CVS
  - persistent nscd caching
  - ppc64 32-bit atomicity fix
  - fix x86-64 nptl-devel headers for -m32 compilation
- %%ghost /etc/ld.so.cache (#130597)
- edit /etc/ld.so.conf in glibc_post_upgrade if
  include ld.so.conf.d/*.conf line is missing (#120588)
- ugly hacks for the IA-64 /emul braindamage (#124996, #128267)

* Sat Aug 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-46
- update from CVS

* Thu Aug 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-45
- update from CVS
  - fix nss_compat's initgroups handling (#130363)
  - fix getaddrinfo ai_canonname setting

* Thu Aug 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-44
- update from CVS
  - add ip6-dotint resolv.conf option, make
    no-ip6-dotint the default
- BuildPrereq libselinux-devel (#129946)
- on ppc64, build without dot symbols

* Thu Aug 12 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-43
- update from CVS
  - remove debugging printout (#129747)
  - make <sys/shm.h> usable in C++ (IT#45148)
- update RLIMIT_* constants in <bits/resource.h>, make
  <sys/resource.h> POSIX compliant (#129740)

* Wed Aug 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-42
- fix last tzset () fixes, disable rereading of /etc/localtime
  every time for now
- really enable SELinux support for NSCD

* Wed Aug 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-41
- update from CVS
  - fread_unlocked/fwrite_unlocked macro fixes (BZ #309, #316)
  - tzset () fixes (BZ #154)
- speed up pthread_rwlock_unlock on arches other than i386 and
  x86_64 (#129455)
- fix compilation with -ansi (resp. -std=c89 or -std=c99) and
  -D_XOPEN_SOURCE=[56]00 but no -D_POSIX_SOURCE* or -D_POSIX_C_SOURCE*
  (BZ #284)
- add SELinux support for NSCD

* Fri Aug  6 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-40
- update from CVS
  - change res_init to force all threads to re-initialize
    resolver before they use it next time (#125712)
  - various getaddrinfo and related fixes (BZ #295, #296)
  - fix IBM{932,943} iconv modules (#128674)
  - some nscd fixes (e.g. BZ #292)
  - RFC 3678 support (Multicast Source Filters)
- handle /lib/i686/librtkaio-* in i386 glibc_post_upgrade
  the same as /lib/i686/librt-*

* Fri Jul 23 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-39
- update from CVS
  - conformance related changes in headers
- remove -finline-limit=2000 for GCC 3.4.x+

* Thu Jul 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-38
- update from CVS
  - fix res_init leaks
  - fix newlocale races
  - fix ppc64 setjmp
- fix strtold (BZ #274)

* Fri Jul 16 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-37
- update from CVS
  - allow pthread_cancel in DSO destructors run at exit time
- fix pow{f,,l} on IA-32 and powl on x86-64
- allow PIEs on IA-32 to have main in a shared library they depend on

* Mon Jul  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-36
- s390* .plt slot reduction
- fix pthread_rwlock_timedrdlock on x86_64

* Wed Jun 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-35
- tweak spec file for the libpthread-0.61.so -> libpthread-2.3.3.so
  NPTL changes

* Wed Jun 30 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-34
- update from CVS
  - if_nameindex using preferably netlink
  - printf_parsemb initialization fix
  - NPTL version is now the same as glibc version

* Mon Jun 28 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-33
- update from CVS
  - reread resolv.conf for nscd --invalidate=hosts
  - fix F_GETLK/F_SETLK/F_SETLKW constants on x86_64 for
    -m32 -D_FILE_OFFSET_BITS=64 compilations
  - avoid calling non-existing fcntl64 syscall on ppc64

* Mon Jun 14 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-32
- update from CVS
  - FUTEX_CMP_REQUEUE support (fix pthread_cond_* deadlocks)
  - fix backtrace in statically linked programs
- rebuilt with GCC 3.4, adjusted ulps and i386 <bits/string.h>

* Fri May 28 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-31
- update from CVS
- <bits/string2.h> and <bits/mathinline.h> changes for GCC 3.{2,4,5}+
- make c_stubs buildable even with GCC 3.2.x (#123042)

* Fri May 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-30
- fix pthread_cond_wait on architectures other than IA-32 and
  x86_64

* Thu May 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-29
- use lib64 instead of lib on ia64 if %%{_lib} is defined to lib64

* Wed May 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-28
- update from CVS
  - FUTEX_REQUEUE fixes (#115349)
  - SPARC GCC 3.4 build fix
  - fix handling of undefined TLS symbols on IA32 (RELA only),
    SPARC and SH
  - regex translate fix
  - speed up sprintf
  - x86_64 makecontext alignment fix
  - make POSIX sigpause the default sigpause, unless BSD sigpause
    requested

* Tue May 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-27
- remove /lib64/tls/librtkaio-2.3.[23].so in glibc_post_upgrade
  on x86-64, s390x and ppc64 instead of /lib/tls/librtkaio-2.3.[23].so
- build mq_{send,receive} with -fexceptions

* Fri May  7 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-26
- update from CVS
  - fix <tgmath.h>
  - fix memory leaks in nis, getifaddrs, etc. caused by incorrect
    use of realloc
- remove /lib/{tls,i686}/librtkaio-2.3.[23].so in glibc_post_upgrade
  and rerun ldconfig if needed, otherwise after glibc upgrade librt.so.1
  might be a stale symlink

* Wed May  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-25
- update from CVS
- disable FUTEX_REQUEUE (work around #115349)
- mq for sparc/sparc64/ia64

* Tue May  4 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-24
- update from CVS
  - define S_ISSOCK in -D_XOPEN_SOURCE=600 and S_I[FS]SOCK
    plus F_[SG]ETOWN also in -D_XOPEN_SOURCE=500 (both
    included already in XNS5)
  - reorder dlopen checks, so that dlopening ET_REL objects
    complains about != ET_DYN != ET_EXEC, not about phentsize
    (#121606)
  - fix strpbrk macro for GCC 3.4+ (BZ #130)
  - fix <sys/sysctl.h> (BZ #140)
  - sched_[gs]etaffinity documentation fix (BZ #131)
  - fix sparc64 build (BZ #139)
  - change linuxthreads back to use non-cancellable writes
    to manager pipes etc.
  - fix sem_timedwait return value in linuxthreads (BZ #133)
  - ia64 unnecessary PLT relocs removal

* Thu Apr 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-23
- update from CVS
  - fix *scanf
  - fix shm_unlink, sem_unlink and mq_unlink errno values
  - avoid memory leaks in error
  - execstack fixes on s390

* Mon Apr 19 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-22
- update from CVS
  - mq and timer fixes
- rebuilt with binutils >= 2.15.90.0.3-2 to fix IA-64 statically
  linked binaries
- fix linuxthreads librt.so on s390{,x}, so it is no longer DT_TEXTREL

* Sat Apr 17 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-21
- disable rtkaio
- update from CVS
  - POSIX message passing support
  - fixed SIGEV_THREAD support for POSIX timers
  - fix free on non-malloced memory in syslog
  - fix ffsl on some 64-bit arches
  - fix sched_setaffinity on x86-64, ia64
  - fix ppc64 umount
  - NETID_AUTHORITATIVE, SERVICES_AUTHORITATIVE support
  - various NIS speedups
  - fix fwrite with > 2GB sizes on 64-bit arches
  - fix pthread_getattr_np guardsize reporting in NPTL
- report PLT relocations in ld.so and libc.so during the build

* Thu Mar 25 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-20
- update from CVS
  - change NPTL PTHREAD_MUTEX_ADAPTIVE_NP mutexes to spin on SMP
  - strtol speed optimization
  - don't try to use certainly unimplemented syscalls on ppc64
- kill -debug subpackage, move the libs to glibc-debuginfo{,-common}
  into /usr/lib/debug/usr/%{_lib}/ directory
- fix c_stubs with gcc 3.4
- move all the up to 3 builds into %%build scriptlet and
  leave only installation in the %%install scriptlet

* Mon Mar 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-19
- update from CVS
  - affinity API changes

* Thu Mar 18 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-18
- update from CVS
  - fix ia64 iopl (#118591)
  - add support for /etc/ld.so.conf.d/*.conf
  - fix x86-64 LD_DEBUG=statistics
- fix hwcap handling when using ld.so.cache (#118518)

* Mon Mar 15 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-17
- update from CVS
  - implement non-_l function on top of _l functions

* Thu Mar 11 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-16
- update from CVS
- fix s390{,x} TLS handling

* Wed Mar 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-15
- update from CVS
  - special section for compatibility code
  - make getpid () work even in vfork () child
- configure with --enable-bind-now to avoid lazy binding in ld.so
  and libc.so

* Fri Mar  5 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-14
- update from CVS
  - fix iconv -c (#117021)
  - fix PIEs on sparc/sparc64
  - fix posix_fadvise on 64-bit architectures
- add locale-archive as %%ghost file (#117014)

* Mon Mar  1 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-13
- update from CVS

* Fri Feb 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-12
- update from CVS

* Fri Feb 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-11
- update from CVS
  - fix ld.so when vDSO is randomized

* Fri Feb 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-10
- update from CVS

* Fri Feb 20 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-9
- update from CVS

* Tue Feb 10 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-8
- update from CVS

* Tue Jan 27 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-7
- update from CVS
  - dl_iterate_phdr extension to signal number of added/removed
    libraries
- fix PT_GNU_RELRO support on ppc* with prelinking

* Fri Jan 23 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-6
- rebuilt with fixed GCC on IA-64

* Thu Jan 22 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-5
- fix PT_GNU_RELRO support

* Wed Jan 21 2004 Jakub Jelinek <jakub@redhat.com> 2.3.3-4
- update from CVS
  - some further regex speedups
  - fix re.translate handling in regex (#112869)
  - change regfree to match old regex behaviour (what is freed
    and clearing of freed pointers)
  - fix accesses to unitialized memory in regex (#113507, #113425,
    #113421)
  - PT_GNU_RELRO support

* Tue Dec 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.3-3
- update from CVS
  - fix pmap_set fd and memory leak (#112726)
- fix backreference handling in regex
- rebuilt under glibc without the above bug to fix
  libc.so linker script (#112738)

* Mon Dec 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.3-2
- update from CVS
  - faster getpid () in NPTL builds
  - fix to make pthread_setcancelstate (PTHREAD_CANCEL_DISABLE, )
    really disable cancellation (#112512)
  - more regex fixes and speedups
  - fix nextafter*/nexttoward*
  - handle 6th syscall(3) argument on AMD64
  - handle memalign/posix_memalign in mtrace
  - fix linuxthreads memory leak (#112208)
  - remove throw () from cancellation points in linuxthreads (#112602)
  - fix NPTL unregister_atfork
  - fix unwinding through alternate signal stacks

* Mon Dec  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.3-1
- update from CVS
  - 2.3.3 release
  - lots of regex fixes and speedups (#110401)
  - fix atan2
  - fix pshared condvars in NPTL
  - fix pthread_attr_destroy for attributes created with
    pthread_attr_init@GLIBC_2.0
- for the time being, include both nb_NO* and no_NO* as locales
  so that the distribution can catch up with the no_NO->nb_NO
  transition
- add BuildPrereq texinfo (#110252)

* Tue Nov 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-102
- update from CVS
  - fix getifaddrs (CAN-2003-0859)
  - fix ftw fd leak
  - fix linuxthreads sigaction (#108634)
  - fix glibc 2.0 stdio compatibility
  - fix uselocale (LC_GLOBAL_LOCALE)
  - speed up stdio locking in non-threaded programs on IA-32
  - try to maintain correct order of cleanups between those
    registered with __attribute__((cleanup))
    and with LinuxThreads style pthread_cleanup_push/pop (#108631)
  - fix segfault in regex (#109606)
  - fix RE_ICASE multi-byte handling in regex
  - fix pthread_exit in libpthread.a (#109790)
  - FTW_ACTIONRETVAL support
  - lots of regex fixes and speedups
  - fix ceill/floorl on AMD64

* Mon Oct 27 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-101
- update from CVS
  - fix ld.so --verify (and ldd)

* Mon Oct 27 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-100
- update from CVS
  - fix sprof (#103727)
  - avoid infinite loops in {,f}statvfs{,64} with hosed mounts file
  - prevent dlopening of executables
  - fix glob with GLOB_BRACE and without GLOB_NOESCAPE
  - fix locale printing of word values on 64-bit big-endian arches
    (#107846)
  - fix getnameinfo and getaddrinfo with reverse IPv6 lookups
    (#101261)

* Wed Oct 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-99
- update from CVS
  - dl_iterate_phdr in libc.a on arches other than IA-64
  - LD_DEBUG=statistics prints number of relative relocations
  - fix hwcap computation
- NPTL is now part of upstream glibc CVS
- include {st,xh,zu}_ZA{,.UTF-8} locales

* Sat Oct  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-98
- update from CVS
  - fix close, pause and fsync (#105348)
  - fix pthread_once on IA-32
- implement backtrace () on IA-64, handle -fomit-frame-pointer
  in AMD64 backtrace () (#90402)

* Tue Sep 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-97
- update from CVS
  - fix <sys/sysmacros.h> with C++ or -ansi or -pedantic C
  - fix mknod/ustat return value when given bogus device number (#105768)

* Fri Sep 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-96
- rebuilt

* Fri Sep 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-95
- fix IA-64 getcontext

* Thu Sep 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-94
- update from CVS
- fix syslog with non-C non-en_* locales (#61296, #104979)
- filter GLIBC_PRIVATE symbols from glibc provides
- fix NIS+

* Thu Sep 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-93
- update from CVS
- assume 2.4.21 kernel features on RHEL/ppc*, so that
  {make,set,get,swap}context works
- backout execstack support for RHEL
- build rtkaio on amd64 too

* Wed Sep 24 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-92
- update from CVS
  - execstack/noexecstack support
  - build nscd as PIE
- move __libc_stack_end back to @GLIBC_2.1
- build against elfutils >= 0.86 to fix stripping on s390x

* Mon Sep 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-91
- rebuilt

* Mon Sep 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-90
- update from CVS
  - NPTL locking change (#102682)
- don't jump around lock on amd64

* Thu Sep 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-89
- fix open_memstream/syslog (#104661)

* Thu Sep 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-88
- update from CVS
  - retrieve affinity in pthread_getattr_np
  - fix pthread_attr_[gs]etaffinity_np
  - handle hex and octal in wordexp

* Wed Sep 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-87
- update from CVS
  - truncate instead of round in utimes when utimes syscall is not available
  - don't align stack in every glibc function unnecessarily on IA-32
  - make sure threads have their stack 16 byte aligned on IA-32
  - move sched_[sg]etaffinity to GLIBC_2.3.3 symbol version (#103231)
  - fix pthread_getattr_np for the initial thread (#102683)
  - avoid linuxthreads signal race (#104368)
- ensure all gzip invocations are done with -n option

* Fri Sep 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-86
- update from CVS
- avoid linking in libgcc_eh.a unnecessarily
- change ssize_t back to long int on s390 -m31, unless
  gcc 2.95.x is used

* Wed Sep 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-85
- update from CVS
  - fix IA-64 memccpy (#104114)

* Tue Sep  9 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-84
- update from CVS
  - undo broken amd64 signal context changes

* Tue Sep  9 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-83
- update from CVS
- change *nlink_t, *ssize_t and *intptr_t types on s390 -m31 to
  {unsigned,} int
- change *u_quad_t, *quad_t, *qaddr_t, *dev_t, *ino64_t, *loff_t,
  *off64_t, *rlim64_t, *blkcnt64_t, *fsblkcnt64_t, *fsfilcnt64_t
  on 64-bit arches from {unsigned,} long long int {,*} to
  {unsigned,} long int {,*} to restore binary compatibility
  for C++ functions using these types as arguments

* Sun Sep  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-82
- rebuilt

* Sat Sep  6 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-81
- update from CVS
  - fix tc[gs]etattr/cf[gs]et[io]speed on ppc (#102732)
  - libio fixes

* Thu Sep  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-80
- update from CVS
  - fix IA-64 cancellation when mixing __attribute__((cleanup ()))
    and old-style pthread_cleanup_push cleanups

* Tue Sep  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-79
- updated from CVS
  - lots of cancellation fixes
  - fix posix_fadvise* on ppc32
  - TLS layout fix
  - optimize stdio cleanups (#103354)
  - sparcv9 NPTL
  - include sigset, sighold, sigrelse, sigpause and sigignore prototypes
    in signal.h even if -D_XOPEN_SOURCE_EXTENDED (#103269)
  - fix svc_getreqset on 64-bit big-endian arches
  - return ENOSYS in linuxthreads pthread_barrierattr_setpshared for
    PTHREAD_PROCESS_SHARED
  - add pthread_cond_timedwait stubs to libc.so (#102709)
- split glibc-devel into glibc-devel and glibc-headers to ensure
  amd64 /usr/include always wins on amd64/i386 bi-arch installs
- increase PTHREAD_STACK_MIN on alpha, ia64 and sparc*
- get rid of __syscall_* prototypes and stubs in sysdeps/unix/sysv/linux
- run make check also with linuxthreads (on IA-32 non-FLOATING_STACKS)
  ld.so and NPTL (on IA-32 also FLOATING_STACKS linuxthreads) libraries
  and tests

* Mon Aug 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-78
- include dl-osinfo.h only in glibc-debuginfo-2*.rpm, not
  in glibc-debuginfo-common*

* Mon Aug 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-77
- update from CVS
  - fix glibc 2.0 libio compatibility (#101385)
  - fix ldconfig with /usr/lib/lib*.so symlinks (#102853)
  - fix assert.h (#102916, #103017)
  - make ld.so.cache identical between IA-32 and AMD64 (#102887)
  - fix static linking of large IA-64 binaries (#102586)
- avoid using floating point regs in lazy binding code on ppc64 (#102763)

* Fri Aug 22 2003 Roland McGrath <roland@redhat.com> 2.3.2-76
- add td_thr_tls_get_addr changes missed in initial nptl_db rewrite

* Sun Aug 17 2003 Roland McGrath <roland@redhat.com> 2.3.2-74
- nptl_db rewrite not yet in CVS

* Thu Aug 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-72
- update from CVS
  - fix rtkaio aio_fsync{,64}
  - update rtkaio for !BROKEN_THREAD_SIGNALS
  - fix assert macro when used on pointers

* Wed Aug 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-71
- update from CVS

* Tue Aug 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-70
- update from CVS
- disable CLONE_STOPPED for now until it is resolved
- strip crt files
- fix libio on arches with no < GLIBC_2.2 support (#102102, #102105)
- fix glibc-debuginfo to include all nptl and nptl_db sources

* Thu Aug  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-69
- update from CVS
  - fix pthread_create@GLIBC_2.0 (#101767)
- __ASSUME_CLONE_STOPPED on all arches but s390* in RHEL

* Sun Aug  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-68
- update from CVS
  - only use CLONE_STOPPED if kernel supports it, fix setting of thread
    explicit scheduling (#101457)

* Fri Aug  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-67
- update from CVS
  - fix utimes and futimes if kernel doesn't support utimes syscall
  - fix s390 ssize_t type
  - fix dlerror when called before any dlopen/dlsym
  - update IA-64 bits/sigcontext.h (#101344)
  - various warning fixes
  - fix pthread.h comment typos (#101363)

* Wed Jul 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-66
- update from CVS
- fix dlopen of libraries using TLS IE/LE models

* Tue Jul 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-65
- update from CVS
  - fix timer_create
  - use __extension__ before long long typedefs in <bits/types.h> (#100718)

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-64
- update from CVS
  - fix wcpncpy (#99462)
  - export _res@GLIBC_2.0 even from NPTL libc.so (__res_state ()
    unlike __errno_location () or __h_errno_location () was introduced
    in glibc 2.2)
  - fix zic bug on 64-bit platforms
  - some TLS handling fixes
  - make ldconfig look into alternate ABI dirs by default (#99402)
- move %{_datadir}/zoneinfo to tzdata package, so that it can be
  errataed separately from glibc
- new add-on - rtkaio
- prereq libgcc, as glibc now relies on libgcc_s.so.1 for pthread_cancel

* Tue Jul 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-63
- fix thread cancellation on ppc64

* Sat Jul 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-62
- update from CVS
  - fix thread cancellation on ppc32, s390 and s390x

* Thu Jul 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-61
- update from CVS
  - build libc_nonshared.a with -fPIC instead of -fpic
- fix ppc64 PIE support
- add cfi directives to NPTL sysdep-cancel.h on ppc/ppc64/s390/s390x

* Tue Jul  8 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-60
- update from CVS

* Thu Jul  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-59
- update from CVS
- on IA-64 use different symbols for cancellation portion of syscall
  handlers to make gdb happier

* Thu Jun 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-58
- update from CVS
  - nss_compat supporting LDAP etc.

* Tue Jun 24 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-57
- update from CVS

* Thu Jun 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-56
- fix condvars and semaphores in ppc* NPTL
- fix test-skeleton.c reporting of timed-out tests (#91269)
- increase timeouts for tests during make check

* Wed Jun 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-55
- make ldconfig default to both /lib+/usr/lib and /lib64+/usr/lib64
  on bi-ABI architectures (#97557)
- disable FUTEX_REQUEUE on ppc* temporarily

* Wed Jun 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-54
- update from CVS
- fix glibc_post_upgrade on ppc

* Tue Jun 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-53
- update from CVS
- fix localedef (#90659)
- tweak linuxthreads for librt cancellation

* Mon Jun 16 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-52
- update from CVS

* Thu Jun 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-51
- update from CVS
- fix <gnu/stubs.h> (#97169)

* Wed Jun 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-50
- update from CVS

* Tue Jun 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-49
- update from CVS
  - fix pthread_cond_signal on IA-32 (#92080, #92253)
  - fix setegid (#91567)
- don't prelink -R libc.so on any architecture, it prohibits
  address randomization

* Thu Jun  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-48
- update from CVS
  - fix IA-64 NPTL build

* Thu Jun  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-47
- update from CVS
- PT_GNU_STACK segment in binaries/executables and .note.GNU-stack
  section in *.[oa]

* Sun Jun  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-46
- update from CVS
- enable NPTL on AMD64
- avoid using trampolines in localedef

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-45
- enable NPTL on IA-64

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-44
- update from CVS
- enable NPTL on s390 and s390x
- make __init_array_start etc. symbols in elf-init.oS hidden undefined

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-43
- update from CVS

* Fri May 23 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-42
- update from CVS

* Tue May 20 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-41
- update from CVS
- use NPTL libs if uname -r contains nptl substring or is >= 2.5.69
  or set_tid_address syscall is available instead of checking
  AT_SYSINFO dynamic tag

* Thu May 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-40
- update from CVS

* Wed May 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-39
- update from CVS
  - fix for prelinking of libraries with no dependencies

* Tue May 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-38
- update from CVS
- enable NPTL on ppc and ppc64

* Tue May  6 2003 Matt Wilson <msw@redhat.com> 2.3.2-37
- rebuild

* Sun May  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-36
- update from CVS

* Sat May  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-35
- update from CVS
  - make -jN build fixes

* Fri May  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-34
- update from CVS
- avoid using trampolines in iconvconfig for now

* Sat Apr 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-33
- update from CVS

* Fri Apr 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-32
- update from CVS
- more ppc TLS fixes

* Wed Apr 23 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-31
- update from CVS
  - nscd fixes
  - fix Bahrain spelling (#56298)
  - fix Ukrainian collation (#83973)
  - accept trailing spaces in /etc/ld.so.conf (#86032)
  - perror fix (#85994)
  - fix localedef (#88978)
  - fix getifaddrs (#89026)
  - fix strxfrm (#88409)
- fix ppc TLS
- fix getaddrinfo (#89448)
- don't print warning about errno, h_errno or _res if
  LD_ASSUME_KERNEL=2.4.1 or earlier

* Tue Apr 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-30
- update from CVS
- fix prelink on ppc32
- add TLS support on ppc32 and ppc64
- make sure on -m64 arches all helper binaries are built with this
  option

* Mon Apr 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-29
- update from CVS
  - fix strxfrm (#88409)
- use -m64 -mno-minimal-toc on ppc64
- conflict with kernels < 2.4.20 on ppc64 and < 2.4.0 on x86_64
- link glibc_post_upgrade against newly built libc.a

* Sun Apr 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-28
- update from CVS
  - fix NPTL pthread_detach and already terminated, but not yet
    joined thread (#88219)
  - fix bug-regex4 testcase (#88118)
  - reenable prelink support broken in 2.3.2-13
  - fix register_printf_function (#88052)
  - fix double free with fopen using ccs= (#88056)
  - fix potential access below $esp in {set,swap}context (#88093)
  - fix buffer underrun in gencat -H (#88099)
  - avoid using unitialized variable in tst-tgmath (#88101)
  - fix gammal (#88104)
  - fix iconv -c
  - fix xdr_string (PR libc/4999)
  - fix /usr/lib/nptl/librt.so symlink
  - avoid running NPTL cleanups twice in some cases
  - unblock __pthread_signal_cancel in linuxthreads, so that
    linuxthreads threaded programs work correctly if spawned
    from NPTL threaded programs
  - fix sysconf _SC_{NPROCESSORS_{CONF,ONLN},{,AV}PHYS_PAGES}
- remove /lib/i686 directory before running ldconfig in glibc post
  during i686 -> i386 glibc "upgrades" (#88456)

* Wed Apr  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-22
- update from CVS
  - add pthread_atfork to libpthread.a

* Tue Apr  1 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-21
- update from CVS
- make sure linuxthreads pthread_mutex_lock etc. is not a cancellation
  point

* Sat Mar 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-20
- update from CVS
- if kernel >= 2.4.1 doesn't support NPTL, fall back to
  /lib/i686 libs on i686, not stright to /lib

* Fri Mar 28 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-19
- update from CVS
  - timers fixes

* Thu Mar 27 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-18
- update from CVS
- fix NPTL pthread_cond_timedwait
- fix sysconf (_SC_MONOTONIC_CLOCK)
- use /%%{_lib}/tls instead of /lib/tls on x86-64
- add /%{_lib}/tls/librt*so* and /%{_lib}/i686/librt*so*
- display content of .out files for all make check failures

* Wed Mar 26 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-17
- update from CVS
  - kernel POSIX timers support

* Sat Mar 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-16
- update from CVS
  - export __fork from glibc again
- fix glibc-compat build in NPTL
- fix c_stubs
- fix some more atomic.h problems
- don't check abi in glibc-compat libs

* Fri Mar 21 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-15
- update from CVS
- build glibc-compat (for glibc 2.0 compatibility) and c_stubs add-ons
- condrestart sshd in glibc_post_upgrade so that the user can
  log in remotely and handle the rest (#86339)
- fix a typo in glibc_post_upgrade on sparc

* Tue Mar 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-14
- update from CVS
- change i686/athlon libc.so.6 base to 0x00e80000

* Mon Mar 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-13
- update from CVS
  - hopefully last fix for condvar problems

* Fri Mar 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-12
- fix bits/syscall.h creation on x86-64

* Thu Mar 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-11
- update from CVS

* Wed Mar 12 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-10
- update from CVS

* Tue Mar 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-9
- update from CVS
- fix glibc-debug description (#85111)
- make librt.so a symlink again, not linker script

* Tue Mar  4 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-8
- update from CVS
- remove the workarounds for broken software accessing GLIBC_PRIVATE
  symbols

* Mon Mar  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-7
- update from CVS

* Sun Mar  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-6
- fix TLS IE/LE model handling in dlopened libraries
  on TCB_AT_TP arches

* Tue Feb 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-5
- update from CVS

* Tue Feb 25 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-4
- update from CVS

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-3
- update from CVS
- only warn about errno, h_errno or _res for binaries, never
  libraries
- rebuilt with gcc-3.2.2-4 to use direct %gs TLS access insn sequences

* Sun Feb 23 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-2
- update from CVS

* Sat Feb 22 2003 Jakub Jelinek <jakub@redhat.com> 2.3.2-1
- update from CVS

* Thu Feb 20 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-51
- update from CVS

* Wed Feb 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-50
- update from CVS

* Wed Feb 19 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-49
- update from CVS
- remove nisplus and nis from the default nsswitch.conf (#67401, #9952)

* Tue Feb 18 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-48
- update from CVS

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-47
- update from CVS

* Fri Feb 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-46
- update from CVS
  - pthread_cond* NPTL fixes, new NPTL testcases

* Thu Feb 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-45
- update from CVS
- include also linuxthreads FLOATING_STACKS libs on i686 and athlon:
  LD_ASSUME_KERNEL=2.2.5 to LD_ASSUME_KERNEL=2.4.0 is non-FLOATING_STACKS lt,
  LD_ASSUME_KERNEL=2.4.1 to LD_ASSUME_KERNEL=2.4.19 is FLOATING_STACKS lt,
  later is NPTL
- enable TLS on alpha/alphaev6
- add BuildPreReq: /usr/bin/readlink

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-44
- update from CVS
  - pthread_once fix

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-43
- update from CVS
- vfork fix on s390
- rebuilt with binutils 2.13.90.0.18-5 so that accesses to errno
  don't bind locally (#83325)

* Thu Feb 06 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-42
- update from CVS
- fix pthread_create after vfork+exec in linuxthreads

* Wed Feb 05 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-41
- update from CVS

* Thu Jan 30 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-40
- update from CVS

* Wed Jan 29 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-39
- update from CVS
- enable TLS on s390{,x} and sparc{,v9}

* Fri Jan 17 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-38
- update from CVS
- initialize __environ in glibc_post_upgrade to empty array,
  so that it is not NULL
- compat symlink for s390x /lib/ld64.so.1
- enable glibc-profile on x86-64
- only include libNoVersion.so on IA-32, Alpha and Sparc 32-bit

* Thu Jan 16 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-37
- update from CVS
  - nscd fixes, *scanf fix
- fix %%nptlarches noarch build (#81909)
- IA-64 TLS fixes

* Tue Jan 14 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-36
- update from CVS
- rework -debuginfo subpackage, add -debuginfo-common
  subpackage on IA-32, Alpha and Sparc (ie. auxiliary arches)
- fix vfork in libc.a on PPC32, Alpha, Sparc
- fix libio locks in linuxthreads libc.so if libpthread.so
  is dlopened later (#81374)

* Mon Jan 13 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-35
- update from CVS
  - dlclose bugfixes
- fix NPTL libpthread.a
- fix glibc_post_upgrade on several arches

* Sat Jan 11 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-34
- update from CVS
- TLS support on IA-64

* Wed Jan  8 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-33
- fix vfork in linuxthreads (#81377, #81363)

* Tue Jan  7 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-32
- update from CVS
- don't use TLS libs if kernel doesn't set AT_SYSINFO
  (#80921, #81212)
- add ntp_adjtime on alpha (#79996)
- fix nptl_db (#81116)

* Sun Jan  5 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-31
- update from CVS
- support all architectures again

* Fri Jan  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-30
- fix condvar compatibility wrappers
- add ugly hack to use non-TLS libs if a binary is seen
  to have errno, h_errno or _res symbols in .dynsym

* Fri Jan  3 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-29
- update from CVS
  - fixes for new condvar

* Thu Jan  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-28
- new NPTL condvar implementation plus related linuxthreads
  symbol versioning updates

* Thu Jan  2 2003 Jakub Jelinek <jakub@redhat.com> 2.3.1-27
- update from CVS
- fix #include <sys/stat.h> with -D_BSD_SOURCE or without
  feature set macros
- make *sigaction, sigwait and raise the same between
  -lpthread -lc and -lc -lpthread in linuxthreads builds

* Tue Dec 31 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-26
- fix dlclose

* Sun Dec 29 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-25
- enable sysenter by default for now
- fix endless loop in ldconfig

* Sat Dec 28 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-24
- update from CVS

* Fri Dec 27 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-23
- update from CVS
  - fix ptmalloc_init after clearenv (#80370)

* Sun Dec 22 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-22
- update from CVS
- add IA-64 back
- move TLS libraries from /lib/i686 to /lib/tls

* Thu Dec 19 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-21
- system(3) fix for linuxthreads
- don't segfault in pthread_attr_init from libc.so
- add cancellation tests from nptl to linuxthreads

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-20
- fix up lists of exported symbols + their versions
  from the libraries

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-19
- fix --with-tls --enable-kernel=2.2.5 libc on IA-32

* Wed Dec 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-18
- update from CVS
  - fix NPTL hanging mozilla
  - initialize malloc in mALLOPt (fixes problems with squid, #79957)
  - make linuxthreads work with dl_dynamic_weak 0
  - clear dl_dynamic_weak everywhere

* Tue Dec 17 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-17
- update from CVS
  - NPTL socket fixes, flockfile/ftrylockfile/funlockfile fix
  - kill -debug sub-package, rename -debug-static to -debug
  - clear dl_dynamic_weak for NPTL

* Mon Dec 16 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-16
- fix <bits/mathinline.h> and <bits/nan.h> for C++
- automatically generate NPTL libpthread wrappers

* Mon Dec 16 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-15
- update from CVS
  - all functions which need cancellation should now be cancellable
    both in libpthread.so and libc.so
  - removed @@GLIBC_2.3.2 cancellation wrappers

* Fri Dec 13 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-14
- update from CVS
  - replace __libc_lock_needed@GOTOFF(%ebx) with
    %gs:offsetof(tcbhead_t, multiple_threads)
  - start of new NPTL cancellation wrappers

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-13
- update from CVS
- use inline locks in malloc

* Tue Dec 10 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-12
- update from CVS
  - support LD_ASSUME_KERNEL=2.2.5 in statically linked programs

* Mon Dec  9 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-11
- update from CVS
- rebuilt with gcc-3.2.1-2

* Fri Dec  6 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-10
- update from CVS
- non-nptl --with-tls --without-__thread FLOATING_STACKS libpthread
  should work now
- faster libc locking when using nptl
- add OUTPUT_FORMAT to linker scripts
- fix x86_64 sendfile (#79111)

* Wed Dec  4 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-9
- update from CVS
  - RUSCII support (#78906)
- for nptl builds add BuildRequires
- fix byteswap.h for non-gcc (#77689)
- add nptl-devel package

* Tue Dec  3 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-8
- update from CVS
  - make --enable-kernel=2.2.5 --with-tls --without-__thread
    ld.so load nptl and other --with-__thread libs
- disable nptl by default for now

* Wed Nov 27 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-7
- update from CVS
- restructured redhat/Makefile and spec, so that src.rpm contains
  glibc-<date>.tar.bz2, glibc-redhat-<date>.tar.bz2 and glibc-redhat.patch
- added nptl

* Fri Nov  8 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-6
- update from CVS
  - even more regex fixes
- run sed testsuite to check glibc regex

* Thu Oct 24 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-5
- fix LD_DEBUG=statistics and LD_TRACE_PRELINKING in programs
  using libpthread.so.

* Thu Oct 24 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-4
- update from CVS
  - fixed %a and %A in *printf (#75821)
  - fix re_comp memory leaking (#76594)

* Tue Oct 22 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-3
- update from CVS
  - some more regex fixes
- fix libpthread.a (#76484)
- fix locale-archive enlarging

* Fri Oct 18 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-2
- update from CVS
  - don't need to use 128K of stacks for DNS lookups
  - regex fixes
  - updated timezone data e.g. for this year's Brasil DST
    changes
  - expand ${LIB} in RPATH/RUNPATH/dlopen filenames

* Fri Oct 11 2002 Jakub Jelinek <jakub@redhat.com> 2.3.1-1
- update to 2.3.1 final
  - support really low thread stack sizes (#74073)
- tzdata update

* Wed Oct  9 2002 Jakub Jelinek <jakub@redhat.com> 2.3-2
- update from CVS
  - handle low stack limits
  - move s390x into */lib64

* Thu Oct  3 2002 Jakub Jelinek <jakub@redhat.com> 2.3-1
- update to 2.3 final
  - fix freopen on libstdc++ <= 2.96 stdin/stdout/stderr (#74800)

* Sun Sep 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-3
- don't prelink -r libc.so on ppc/x86-64/sparc*, it doesn't
  speed things up, because they are neither REL arches, nor
  ELF_MACHINE_REL_RELATIVE
- fix sparc64 build

* Sun Sep 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-2
- update from CVS

* Sat Sep 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.94-1
- update from CVS
- prelink on ppc and x86-64 too
- don't remove ppc memset
- instead of listing on which arches to remove glibc-compat
  list where it should stay

* Fri Sep  6 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-5
- fix wcsmbs functions with invalid character sets (or malloc
  failures)
- make sure __ctype_b etc. compat vars are updated even if
  they are copy relocs in the main program

* Thu Sep  5 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-4
- fix /lib/libnss1_dns.so.1 (missing __set_h_errno definition
  leading to unresolved __set_h_errno symbol)

* Wed Sep  4 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-3
- security fix - increase dns-network.c MAXPACKET to at least
  65536 to avoid buffer overrun. Likewise glibc-compat
  dns-{host,network}.c.

* Tue Sep  3 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-2
- temporarily add back __ctype_b, __ctype_tolower and __ctype_toupper to
  libc.a and export them as @@GLIBC_2.0 symbols, not @GLIBC_2.0
  from libc.so - we have still lots of .a libraries referencing
  __ctype_{b,tolower,toupper} out there...

* Tue Sep  3 2002 Jakub Jelinek <jakub@redhat.com> 2.2.93-1
- update from CVS
  - 2.2.93 release
  - use double instead of single indirection in isXXX macros
  - per-locale wcsmbs conversion state

* Sat Aug 31 2002 Jakub Jelinek <jakub@redhat.com> 2.2.92-2
- update from CVS
  - fix newlocale/duplocale/uselocale
- disable profile on x86_64 for now

* Sat Aug 31 2002 Jakub Jelinek <jakub@redhat.com> 2.2.92-1
- update from CVS
  - 2.2.92 release
  - fix gettext after uselocale
  - fix locales in statically linked threaded programs
  - fix NSS

* Thu Aug 29 2002 Jakub Jelinek <jakub@redhat.com> 2.2.91-1
- update from CVS
  - 2.2.91 release
  - fix fd leaks in locale-archive reader (#72043)
- handle EROFS in build-locale-archive gracefully (#71665)

* Wed Aug 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-27
- update from CVS
  - fix re_match (#72312)
- support more than 1024 threads

* Fri Aug 23 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-26
- update from CVS
  - fix i386 build

* Thu Aug 22 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-25
- update from CVS
  - fix locale-archive loading hang on some (non-primary) locales
    (#72122, #71878)
  - fix umount problems with locale-archives when /usr is a separate
    partition (#72043)
- add LICENSES file

* Fri Aug 16 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-24
- update from CVS
  - only mmap up to 2MB of locale-archive on 32-bit machines
    initially
  - fix fseek past end + fread segfault with mmaped stdio
- include <sys/debugreg.h> which is mistakenly not included
  in glibc-devel on IA-32

* Fri Aug 16 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-23
- don't return normalized locale name in setlocale when using
  locale-archive

* Thu Aug 15 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-22
- update from CVS
  - optimize for primary system locale
- localedef fixes (#71552, #67705)

* Wed Aug 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-21
- fix path to locale-archive in libc reader
- build locale archive at glibc-common %post time
- export __strtold_internal and __wcstold_internal on Alpha again
- workaround some localedata problems

* Tue Aug 13 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-20
- update from CVS
- patch out set_thread_area for now

* Fri Aug  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-19
- update from CVS
- GB18030 patch from Yu Shao
- applied Debian patch for getaddrinfo IPv4 vs. IPv6
- fix regcomp (#71039)

* Sun Aug  4 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-18
- update from CVS
- use /usr/sbin/prelink, not prelink (#70376)

* Thu Jul 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-17
- update from CVS

* Thu Jul 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-16
- update from CVS
  - ungetc fix (#69586)
  - fseek errno fix (#69589)
  - change *etrlimit prototypes for C++ (#68588)
- use --without-tls instead of --disable-tls

* Thu Jul 11 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-15
- set nscd user's shell to /sbin/nologin (#68369)
- fix glibc-compat buffer overflows (security)
- buildrequire prelink, don't build glibc's own copy of it (#67567)
- update from CVS
  - regex fix (#67734)
  - fix unused warnings (#67706)
  - fix freopen with mmap stdio (#67552)
  - fix realloc (#68499)

* Tue Jun 25 2002 Bill Nottingham <notting@redhat.com> 2.2.90-14
- update from CVS
  - fix argp on long words
  - update atime in libio

* Sat Jun 22 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-13
- update from CVS
  - a thread race fix
  - fix readdir on invalid dirp

* Wed Jun 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-12
- update from CVS
  - don't use __thread in headers
- fix system(3) in threaded apps
- update prelink, so that it is possible to prelink -u libc.so.6.1
  on Alpha

* Fri Jun  7 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-11
- update from CVS
  - fix __moddi3 (#65612, #65695)
  - fix ether_line (#64427)
- fix setvbuf with mmap stdio (#65864)
- --disable-tls for now, waiting for kernel
- avoid duplication of __divtf3 etc. on IA-64
- make sure get*ent_r and _IO_wfile_jumps are exported (#62278)

* Tue May 21 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-10
- update from CVS
  - fix Alpha pthread bug with gcc 3.1

* Fri Apr 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-35
- fix nice

* Mon Apr 15 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-34
- add relocation dependencies even for weak symbols (#63422)
- stricter check_fds check for suid/sgid binaries
- run make check at %%install time

* Sat Apr 13 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-33
- handle Dec 31 1969 in mktime for timezones west of GMT (#63369)
- back out do-lookup.h change (#63261, #63305)
- use "memory" clobber instead all the fancy stuff in i386/i686/bits/string.h
  since lots of compilers break on it
- fix sparc build with gcc 3.1
- fix spec file for athlon

* Tue Apr  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-32
- fix debugging of threaded apps (#62804)
- fix DST for Estonia (#61494)
- document that pthread_mutexattr_?etkind_np are deprecated
  and pthread_mutexattr_?ettype should be used instead in man
  pages (#61485)
- fix libSegFault.so undefined externals

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-31
- temporarily disable prelinking ld.so, as some statically linked
  binaries linked against debugging versions of old glibcs die on it
  (#62352)
- fix <semaphore.h> for -std=c99 (#62516)
- fix ether_ntohost segfault (#62397)
- remove in glibc_post_upgrade on i386 all /lib/i686/libc-*.so,
  /lib/i686/libm-*.so and /lib/i686/libpthread-*.so, not just current
  version (#61633)
- prelink -r on alpha too

* Thu Mar 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-30
- update GB18030 iconv module (Yu Shao)

* Tue Mar 26 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-29
- features.h fix

* Tue Mar 26 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-28
- update from CVS
  - fix nscd with huge groups
  - fix nis to not close fds it shouldn't
- rebuilt against newer glibc-kernheaders to use the correct
  PATH_MAX
- handle .athlon.rpm glibc the same way as .i686.rpm
- add a couple of .ISO-8859-15 locales (#61922)
- readd temporarily currencies which were superceeded by Euro
  into the list of accepted currencies by localedef to make
  standard conformance testsuites happy
- temporarily moved __libc_waitpid back to make Sun JDK happy
- use old malloc code
- prelink i686/athlon ld.so and prelink -r i686/athlon libc.so

* Thu Mar 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-27
- update from CVS
  - fix DST handling for southern hemisphere (#60747)
  - fix daylight setting for tzset (#59951)
  - fix ftime (#60350)
  - fix nice return value
  - fix a malloc segfault
- temporarily moved __libc_wait, __libc_fork and __libc_stack_end
  back to what they used to be exported at
- censorship (#60758)

* Thu Feb 28 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-26
- update from CVS
- use __attribute__((visibility(...))) if supported, use _rtld_local
  for ld.so only objects
- provide libc's own __{,u}{div,mod}di3

* Wed Feb 27 2002 Jakub Jelinek <jakub@redhat.com> 2.2.5-25
- switch back to 2.2.5, mmap stdio needs work

* Mon Feb 25 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-8
- fix two other mmap stdio bugs (#60228)

* Thu Feb 21 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-7
- fix yet another mmap stdio bug (#60145)

* Tue Feb 19 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-6
- fix mmap stdio bug (seen on ld as File truncated error, #60043)
- apply Andreas Schwab's fix for pthread sigwait
- remove /lib/i686/ libraries in glibc_post_upgrade when
  performing i386 glibc install

* Thu Feb 14 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-5
- update to CVS
- added glibc-utils subpackage
- disable autoreq in glibc-debug
- readd %%lang() to locale files

* Thu Feb  7 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-4
- update to CVS
- move glibc private symbols to GLIBC_PRIVATE symbol version

* Wed Jan  9 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-3
- fix a sqrt bug on alpha which caused SHN_UNDEF $__full_ieee754_sqrt..ng
  symbol in libm

* Tue Jan  8 2002 Jakub Jelinek <jakub@redhat.com> 2.2.90-2
- add debug-static package

* Mon Dec 31 2001 Jakub Jelinek <jakub@redhat.com> 2.2.90-1
- update from CVS
- remove -D__USE_STRING_INLINES
- add debug subpackage to trim glibc and glibc-devel size

* Wed Oct  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-19
- fix strsep

* Fri Sep 28 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-18
- fix a ld.so bug with duplicate searchlists in l_scope
- fix erfcl(-inf)
- turn /usr/lib/librt.so into linker script

* Wed Sep 26 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-17
- fix a ld.so lookup bug after lots of dlopen calls
- fix CMSG_DATA for non-gcc non-ISOC99 compilers (#53984)
- prelinking support for Sparc64

* Fri Sep 21 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-16
- update from CVS to fix DT_SYMBOLIC
- prelinking support for Alpha and Sparc

* Tue Sep 18 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-15
- update from CVS
  - linuxthreads now retries if -1/EINTR is returned from
    reading or writing to thread manager pipe (#43742)
- use DT_FILTER in librt.so (#53394)
  - update glibc prelink patch so that it handles filters
- fix timer_* with SIGEV_NONE (#53494)
- make glibc_post_upgrade work on PPC (patch from Franz Sirl)

* Mon Sep 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-14
- fix build on sparc32
- 2.2.4-13 build for some reason missed some locales
  on alpha/ia64

* Mon Sep  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-13
- fix iconvconfig

* Mon Sep  3 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-12
- add fam to /etc/rpc (#52863)
- fix <inttypes.h> for C++ (#52960)
- fix perror

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-11
- fix strnlen(x, -1)

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-10
- doh, <bits/libc-lock.h> should only define __libc_rwlock_t
  if __USE_UNIX98.

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-9
- fix bits/libc-lock.h so that gcc can compile
- fix s390 build

* Fri Aug 24 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-8
- kill stale library symlinks in ldconfig (#52350)
- fix inttypes.h for G++ < 3.0
- use DT_REL*COUNT

* Wed Aug 22 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-7
- fix strnlen on IA-64 (#50077)

* Thu Aug 16 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-6
- glibc 2.2.4 final
- fix -lpthread -static (#51672)

* Fri Aug 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-5
- doh, include libio/tst-swscanf.c

* Fri Aug 10 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-4
- don't crash on catclose(-1)
- fix wscanf %[] handling
- fix return value from swprintf
- handle year + %U/%W week + week day in strptime

* Thu Aug  9 2001 Jakub Jelinek <jakub@redhat.com> 2.2.4-3
- update from CVS to
  - fix strcoll (#50548)
  - fix seekdir (#51132)
  - fix memusage (#50606)
- don't make gconv-modules.cache %%config file, just don't verify
  its content.

* Mon Aug  6 2001 Jakub Jelinek <jakub@redhat.com>
- fix strtod and *scanf (#50723, #50724)

* Sat Aug  4 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix iconv cache handling
- glibc should not own %{_infodir}, %{_mandir} nor %{_mandir}/man3 (#50673)
- add gconv-modules.cache as emtpy config file (#50699)
- only run iconvconfig if /usr is mounted read-write (#50667)

* Wed Jul 25 2001 Jakub Jelinek <jakub@redhat.com>
- move iconvconfig from glibc-common into glibc subpackage,
  call it from glibc_post_upgrade instead of common's post.

* Tue Jul 24 2001 Jakub Jelinek <jakub@redhat.com>
- turn off debugging printouts in iconvconfig

* Tue Jul 24 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix IA-32 makecontext
  - make fflush(0) thread-safe (#46446)

* Mon Jul 23 2001 Jakub Jelinek <jakub@redhat.com>
- adjust prelinking DT_* and SHT_* values in elf.h
- update from CVS
  - iconv cache
  - make iconv work in SUID/SGID programs (#34611)

* Fri Jul 20 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - kill non-pic code in libm.so
  - fix getdate
  - fix some locales (#49402)
- rebuilt with binutils-2.11.90.0.8-5 to place .interp section
  properly in libBrokenLocale.so, libNoVersion.so and libanl.so
- add floating stacks on IA-64, Alpha, Sparc (#49308)

* Mon Jul 16 2001 Jakub Jelinek <jakub@redhat.com>
- make /lib/i686 directory owned by glibc*.i686.rpm

* Mon Jul  9 2001 Jakub Jelinek <jakub@redhat.com>
- remove rquota.[hx] headers which are now provided by quota (#47141)
- add prelinking patch

* Thu Jul  5 2001 Jakub Jelinek <jakub@redhat.com>
- require sh-utils for nscd

* Mon Jun 25 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS (#43681, #43350, #44663, #45685)
- fix ro_RO bug (#44644)

* Wed Jun  6 2001 Jakub Jelinek <jakub@redhat.com>
- fix a bunch of math bugs (#43210, #43345, #43346, #43347, #43348, #43355)
- make rpc headers -ansi compilable (#42390)
- remove alphaev6 optimized memcpy, since there are still far too many
  broken apps which call memcpy where they should call memmove
- update from CVS to (among other things):
  - fix tanhl bug (#43352)

* Tue May 22 2001 Jakub Jelinek <jakub@redhat.com>
- fix #include <signal.h> with -D_XOPEN_SOURCE=500 on ia64 (#35968)
- fix a dlclose reldeps handling bug
- some more profiling fixes
- fix tgmath.h

* Thu May 17 2001 Jakub Jelinek <jakub@redhat.com>
- make ldconfig more quiet
- fix LD_PROFILE on i686 (#41030)

* Wed May 16 2001 Jakub Jelinek <jakub@redhat.com>
- fix the hardlink program, so that it really catches all files with
  identical content
- add a s390x clone fix

* Wed May 16 2001 Jakub Jelinek <jakub@redhat.com>
- fix rpc for non-threaded apps using svc_fdset and similar variables (#40409)
- fix nss compatibility DSO versions for alphaev6
- add a hardlink program instead of the shell 3x for plus cmp -s/link
  which takes a lot of time during build
- rework BuildPreReq and Conflicts with gcc, so that
  it applies only where it has to

* Fri May 11 2001 Jakub Jelinek <jakub@redhat.com>
- fix locale name of ja_JP in UTF-8 (#39783)
- fix re_search_2 (#40244)
- fix memusage script (#39138, #39823)
- fix dlsym(RTLD_NEXT, ) from main program (#39803)
- fix xtrace script (#39609)
- make glibc conflict with glibc-devel 2.2.2 and below (to make sure
  libc_nonshared.a has atexit)
- fix getconf LFS_CFLAGS on 64bitters
- recompile with gcc-2.96-84 or above to fix binary compatibility problem
  with __frame_state_for function (#37933)

* Fri Apr 27 2001 Jakub Jelinek <jakub@redhat.com>
- glibc 2.2.3 release
  - fix strcoll (#36539)
- add BuildPreReqs (#36378)

* Wed Apr 25 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Fri Apr 20 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix sparc64, ia64
  - fix some locale syntax errors (#35982)

* Wed Apr 18 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Wed Apr 11 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS

* Fri Apr  6 2001 Jakub Jelinek <jakub@redhat.com>
- support even 2.4.0 kernels on ia64, sparc64 and s390x
- include UTF-8 locales
- make gconv-modules %%config(noreplace)

* Fri Mar 23 2001 Jakub Jelinek <jakub@redhat.com>
- back out sunrpc changes

* Wed Mar 21 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix ia64 build
  - fix pthread_getattr_np

* Fri Mar 16 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - run atexit() registered functions at dlclose time if they are in shared
    libraries (#28625)
  - add pthread_getattr_np API to make JVM folks happy

* Wed Mar 14 2001 Jakub Jelinek <jakub@redhat.com>
- require 2.4.1 instead of 2.4.0 on platforms where it required 2.4 kernel
- fix ldd behaviour on unresolved symbols
- remove nonsensical ldconfig warning, update osversion for the most
  recent library with the same soname in the same directory instead (#31703)
- apply selected patches from CVS
- s390x spec file changes from Florian La Roche

* Wed Mar  7 2001 Jakub Jelinek <jakub@redhat.com>
- fix gencat (#30894)
- fix ldconfig changes from yesterday, fix LD_ASSUME_KERNEL handling

* Tue Mar  6 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
- make pthread_attr_setstacksize consistent before and after pthread manager
  is started (#28194)
- pass back struct sigcontext from pthread signal wrapper (on ia32 only so
  far, #28493)
- on i686 ship both --enable-kernel 2.2.5 and 2.4.0 libc/libm/libpthread,
  make ld.so pick the right one

* Sat Feb 17 2001 Preston Brown <pbrown@redhat.com>
- glib-common doesn't require glibc, until we can figure out how to get out of dependency hell.

* Sat Feb 17 2001 Jakub Jelinek <jakub@redhat.com>
- make glibc require particular version of glibc-common
  and glibc-common prerequire glibc.

* Fri Feb 16 2001 Jakub Jelinek <jakub@redhat.com>
- glibc 2.2.2 release
  - fix regex REG_ICASE bug seen in ksymoops

* Sat Feb 10 2001 Jakub Jelinek <jakub@redhat.com>
- fix regexec leaking memory (#26864)

* Fri Feb  9 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix ia64 build with gnupro
  - make regex 64bit clean
  - fix tgmath make check failures on alpha

* Tue Feb  6 2001 Jakub Jelinek <jakub@redhat.com>
- update again for ia64 DF_1_INITFIRST

* Fri Feb  2 2001 Jakub Jelinek <jakub@redhat.com>
- update from CVS
  - fix getaddrinfo (#25437)
  - support DF_1_INITFIRST (#25029)

* Wed Jan 24 2001 Jakub Jelinek <jakub@redhat.com>
- build all auxiliary arches with --enablekernel 2.4.0, those wanting
  to run 2.2 kernels can downgrade to the base architecture glibc.

* Sat Jan 20 2001 Jakub Jelinek <jakub@redhat.com>
- remove %%lang() flags from %%{_prefix}/lib/locale files temporarily

* Sun Jan 14 2001 Jakub Jelinek <jakub@redhat.com>
- update to 2.2.1 final
  - fix a pthread_kill_other_threads_np breakage (#23966)
  - make static binaries using dlopen work on ia64 again
- fix a typo in glibc-common group

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- devel requires glibc = %%{version}
- noreplace /etc/nscd.conf

* Wed Jan 10 2001 Jakub Jelinek <jakub@redhat.com>
- some more security fixes:
  - don't look up LD_PRELOAD libs in cache for SUID apps
    (because that bypasses SUID bit checking on the library)
  - place output files for profiling SUID apps into /var/profile,
    use O_NOFOLLOW for them
  - add checks for $MEMUSAGE_OUTPUT and $SEGFAULT_OUTPUT_NAME
- hardlink identical locale files together
- add %%lang() tags to locale stuff
- remove ko_KR.utf8 for now, it is provided by locale-utf8 package

* Mon Jan  8 2001 Jakub Jelinek <jakub@redhat.com>
- add glibc-common subpackage
- fix alphaev6 memcpy (#22494)
- fix sys/cdefs.h (#22908)
- don't define stdin/stdout/stderr as macros for -traditional (#22913)
- work around a bug in IBM JDK (#22932, #23012)
- fix pmap_unset when network is down (#23176)
- move nscd in rc.d before netfs on shutdown
- fix $RESOLV_HOST_CONF in SUID apps (#23562)

* Fri Dec 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix ftw and nftw

* Wed Dec 13 2000 Jakub Jelinek <jakub@redhat.com>
- fix fcvt (#22184)
- ldd /lib/ld-linux.so.2 is not crashing any longer again (#22197)
- fix gencat

* Mon Dec 11 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha htonl and alphaev6 stpcpy

* Sat Dec  9 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to:
  - fix getnameinfo (#21934)
  - don't stomp on memory in rpath handling (#21544)
  - fix setlocale (#21507)
- fix libNoVersion.so.1 loading code (#21579)
- use auxarches define in spec file for auxiliary
  architectures (#21219)
- remove /usr/share directory from filelist (#21218)

* Sun Nov 19 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix getaddrinfo

* Fri Nov 17 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix freopen
- remove all alpha workarounds, not needed anymore

* Wed Nov 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix dladdr bug on alpha/sparc32/sparc64
- fix Makefiles so that they run static tests properly

* Tue Nov 14 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to fix ldconfig

* Thu Nov  9 2000 Jakub Jelinek <jakub@redhat.com>
- update to glibc 2.2 release

* Mon Nov  6 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS to:
  - export __sysconf@@GLIBC_2.2 (#20417)

* Fri Nov  3 2000 Jakub Jelinek <jakub@redhat.com>
- merge to 2.1.97

* Mon Oct 30 2000 Jakub Jelinek <jakub@redhat.com>
- update to CVS, including:
  - fix WORD_BIT/LONG_BIT definition in limits.h (#19088)
  - fix hesiod (#19375)
  - set LC_MESSAGES in zic/zdump for proper error message output (#19495)
  - fix LFS fcntl when used with non-LFS aware kernels (#19730)

* Thu Oct 19 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha semctl (#19199)
- update to CVS, including:
  - fix glibc headers for Compaq non-gcc compilers
  - fix locale alias handling code (#18832)
  - fix rexec on little endian machines (#18886)
- started writing changelog again

* Thu Aug 10 2000 Adrian Havill <havill@redhat.com>
- added ja ujis alias for backwards compatibility
