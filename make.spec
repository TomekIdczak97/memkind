#  FILE LICENSE TAG: intel
#
#  Copyright (2014) Intel Corporation All Rights Reserved.
#
#  This software is supplied under the terms of a license
#  agreement or nondisclosure agreement with Intel Corp.
#  and may not be copied or disclosed except in accordance
#  with the terms of that agreement.
#

define make_spec

Summary: Extention to libnuma for kinds of memory
Name: $(name)
Version: $(version)
Release: $(release)
License: See COPYING
Group: System Environment/Libraries
Vendor: Intel Corporation
URL: http://www.intel.com
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: numactl
BuildRequires: numactl-devel
BuildRequires: doxygen
BuildRequires: texlive-latex
%if ! %{defined jemalloc_prefix}
BuildRequires: jemalloc
%endif


%description
The numakind library extends libnuma with the ability to categorize
groups of numa nodes into different "kinds" of memory. It provides a
low level interface for generating inputs to mbind() and mmap(), and a
high level interface for heap management.  The heap management is
implemented with an extension to the jemalloc library which dedicates
"arenas" to each node and kind of memory.  To use numakind, jemalloc
must be compiled with the --enable-numakind option.

%prep
%setup -D -q -c -T -a 0

%build
%if ! %{defined jemalloc_prefix}
$(make_prefix) $(MAKE) $(make_postfix)
%else
$(make_prefix) $(MAKE) JEMALLOC_PREFIX=%{jemalloc_prefix} $(make_postfix)
%endif

%install
make DESTDIR=%{buildroot} VERSION=%{version} install
$(extra_install)

%clean

%post
/sbin/ldconfig
/sbin/chkconfig --add numakind
/sbin/service numakind force-reload >/dev/null 2>&1

%preun
if [ -z "$1" ] || [ "$1" == 0 ]
then
    /sbin/service numakind stop >/dev/null 2>&1
    /sbin/chkconfig --del numakind
fi

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_includedir}/numakind.h
%{_includedir}/hbwmalloc.h
%{_libdir}/libnumakind.so.0.0
%{_libdir}/libnumakind.so.0
%{_libdir}/libnumakind.so
%{_sbindir}/numakind-pmtt
%{_initddir}/numakind
%doc %{_docdir}/numakind-%{version}/README.txt
%doc %{_docdir}/numakind-%{version}/numakind_refman.pdf
%doc %{_datarootdir}/man/man3/hbwmalloc.3.gz
%doc %{_datarootdir}/man/man3/numakind.3.gz
$(extra_files)

%changelog
* Mon Mar 24 2014 mic <mic@localhost> - 
- Initial build.
endef

export make_spec
