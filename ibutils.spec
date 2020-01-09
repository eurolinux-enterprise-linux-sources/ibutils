#
# Copyright (c) 2006 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
#
#
#  $Id: ibutils.spec.in 7656 2006-06-04 09:38:34Z vlad $
#

Summary: OpenIB Mellanox InfiniBand Diagnostic Tools
Name: ibutils
Version: 1.5.7
Release: 10%{?dist}
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Group: System Environment/Libraries
Source: http://www.openfabrics.org/downloads/%{name}/%{name}-%{version}-0.2.gbd7e502.tar.gz
Patch1: ibutils-1.5.7-output.patch
Patch2: add-ibdev2netdev.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: tcl, tk, swig, graphviz-tcl
Requires: ibutils-libs = %{version}-%{release}
BuildRequires: libibverbs-devel >= 1.1.8, opensm-devel >= 3.3.17, tcl-devel, swig, tk-devel, libibumad-devel, autoconf, graphviz-tcl, chrpath
ExcludeArch: s390 s390x
%description 
ibutils provides IB network and path diagnostics.

%package libs
Summary: Shared libraries used by ibutils binaries
Group: System Environment/Libraries
%description libs
Shared libraries used by the Mellanox Infiniband diagnostic utilities

%package devel
Summary: Development files to use the ibutils shared libraries
Group: System Environment/Libraries
Requires: ibutils-libs = %{version}-%{release}
%description devel
Headers and static libraries needed to develop applications that use
the Mellanox Infiniband diagnostic utilities libraries

%prep
%setup -q
%patch1 -p1
%patch2
#./autogen.sh
%configure --with-osm=%{_prefix} --enable-ibmgtsim --disable-rpath CXXFLAGS="$CXXFLAGS -fno-strict-aliasing -fPIC"

%build
# The build isn't smp safe, so no %{?_smp_mflags}
export CXXFLAGS="$CXXFLAGS -fno-strict-aliasing -fPIC"
make

%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_bindir}/git_version.tcl
# None of these files are scripts, but because in the tarball some have
# execute privs, that gets copied on install and rpmlint doesn't like them
chmod -x %{buildroot}%{_libdir}/ibdm1.5.7/ibnl/*
find %{buildroot} -name \*.la -delete
chrpath -d %{buildroot}%{_bindir}/ib{mssh,nlparse,dmsh,topodiff,is,msquit,dmtr,dmchk}
chrpath -d %{buildroot}%{_libdir}/libib{sysapi,dm}.so.1.[01].[01]
chrpath -d %{buildroot}%{_libdir}/*/libib{dm,is}.so.1.5.7
mkdir -p %{buildroot}/var/cache/ibutils
install -m 0755 ibdev2netdev %{buildroot}%{_bindir}

%clean
[ ! -z "%{buildroot}" ] && rm -fr %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/dump2psl.pl
%{_bindir}/dump2slvl.pl
%{_bindir}/ibis
%{_bindir}/ibdmsh
%{_bindir}/ibtopodiff
%{_bindir}/ibnlparse
%{_bindir}/ibdmtr
%{_bindir}/ibdmchk
%{_bindir}/ibdiagnet
%{_bindir}/ibdiagpath
%{_bindir}/ibdiagui
%{_bindir}/mkSimNodeDir
%{_bindir}/ibmssh
%{_bindir}/ibmsquit
%{_bindir}/RunSimTest
%{_bindir}/IBMgtSim
%{_bindir}/ibdev2netdev
%{_datadir}/ibmgtsim
%{_mandir}/*/*

%files libs
%defattr(-,root,root)
%dir /var/cache/ibutils
%{_libdir}/libibdmcom.so.*
%{_libdir}/libibdm.so.*
%{_libdir}/libibmscli.so.*
%{_libdir}/libibsysapi.so.*
%dir %{_libdir}/ibis%{version}
%dir %{_libdir}/ibdm%{version}
%dir %{_libdir}/ibdiagnet%{version}
%dir %{_libdir}/ibdiagpath%{version}
%dir %{_libdir}/ibdiagui%{version}
%{_libdir}/ibis%{version}/*
%{_libdir}/ibdm%{version}/*
%{_libdir}/ibdiagnet%{version}/*
%{_libdir}/ibdiagpath%{version}/*
%{_libdir}/ibdiagui%{version}/*

%files devel
%defattr(-,root,root)
%{_libdir}/libibdmcom.so
%{_libdir}/libibdm.so
%{_libdir}/libibmscli.so
%{_libdir}/libibsysapi.so
%{_libdir}/libibdmcom.a
%{_libdir}/libibdm.a
%{_libdir}/libibmscli.a
%{_libdir}/libibsysapi.a
%{_includedir}/ibdm
%{_includedir}/ibmgtsim

%changelog
* Fri Oct  7 2016 Honggang Li <honli@redhat.com> - 1.5.7-10
- Add script ibdev2netdev
- Resolves: bz1238969

* Wed Jun 18 2014 Doug Ledford <dledford@redhat.com> - 1.5.7-9
- We built a new opensm against a new libibumad and libibmad
  to resolve a bug.  So we need to rebuild this to be against
  the new libs.  Updated to latest upstream since we had to
  rebuild anyway and it's often needed to make it compatible
  with the minor changes in libibumad and libibmad and
  opensm-libs
- Related: bz1082730

* Wed Aug 28 2013 Jay Fenlason <fenlason@redhat.com> 1.5.7-8
- Add the -output patch to have programs use /var/cache/ibutils
  instead of /tmp
  Resolves: bz958569

* Mon Oct 15 2012 Doug Ledford <dledford@redhat.com> - 1.5.7-7
- Bump and rebuild against latest opensm
- Related: bz756396

* Wed Feb 29 2012 Doug Ledford <dledford@redhat.com> - 1.5.7-6
- Bump and rebuild against updated opensm
- Related: bz754196

* Tue Jan 31 2012 Doug Ledford <dledford@redhat.com> - 1.5.7-5
- Bump and rebuild against updated opensm
- Related: bz750609

* Fri Sep 02 2011 Doug Ledford <dledford@redhat.com> - 1.5.7-4
- Add a Requires for ibutils-libs to base ibutils package (found by rpmdiff)

* Thu Sep 01 2011 Doug Ledford <dledford@redhat.com> - 1.5.7-3
- Add a Requires on graphviz-tcl
- Resolves: bz734979

* Mon Aug 08 2011 Doug Ledford <dledford@redhat.com> - 1.5.7-2
- Fix the build so it generates proper debuginfo files
- Resolves: bz729019
- Related: bz725016

* Thu Aug 04 2011 Doug Ledford <dledford@redhat.com> - 1.5.7-1
- Update to latest upstream release
- Related: bz725016

* Thu Apr 28 2011 Doug Ledford <dledford@redhat.com> - 1.5.4-3.el6
- Build for i686 too
- Related: bz695204

* Tue Apr 19 2011 Dennis Gregorovic <dgregor@redhat.com> - 1.5.4-2.el6
- Build for ppc64
- Resolves: bz695204

* Mon Mar 08 2010 Doug Ledford <dledford@redhat.com> - 1.5.4-1.el6
- Update to latest upstream version, which cleans up some licensing issues
  found in the previous versions during review
- Related: bz555835

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2-12.el6
- Update license for pkgwranger approval
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 1.2-11.el5
- Update to latest compatible upstream version
- Related: bz518218

* Fri Apr 17 2009 Doug Ledford <dledford@redhat.com> - 1.2-10
- Update to ofed 1.4.1-rc3 version
- Related: bz459652

* Tue Nov 11 2008 Doug Ledford <dledford@redhat.com> - 1.2-9
- Oops, forgot to remove the man page for ibdiagui, fix that
- Related: bz468122

* Mon Nov 10 2008 Doug Ledford <dledford@redhat.com> - 1.2-8
- Remove ibdiagui from the package entirely since it still doesn't work
  without graphviz-tcl
- Related: bz468122

* Thu Oct 23 2008 Doug Ledford <dledford@redhat.com> - 1.2-7
- Grab the upstream ibutils git repo, find a checkout that supports the
  recent opensm library versions and yet doesn't require graphviz-tcl,
  export that tree to a tarball with a git designation, build from it.
- Resolves: bz468122

* Thu Sep 18 2008 Doug Ledford <dledford@redhat.com> - 1.2-6
- Add a build flag to silence some compile warnings

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 1.2-4
- Upstream has updated the tarball without changing the version number,
  grab the tarball from the OFED-1.4-beta1 tarball and use it.
- Resolves: bz451467

* Tue Jan 29 2008 Doug Ledford <dledford@redhat.com> - 1.2-3
- Bump and rebuild against OFED 1.3 libraries
- Resolves: bz428198

* Wed Jun 27 2007 Doug Ledford <dledford@redhat.com> - 1.2-2
- Bump and rebuild against openib-1.2 libraries

* Mon Jun 25 2007 Doug Ledford <dledford@redhat.com> - 1.2-1
- Update to OFED 1.2 released package
- Related: bz245817

* Wed Oct 25 2006 Tim Powers <timp@redhat.com> - 1.0-3
- rebuild against openib package set due to soname change

* Fri Oct 20 2006 Doug Ledford <dledford@redhat.com>
- Bump and rebuild against latest openib packages
- Disable ibmgtsim until I can figure out why it's failing to wrap a
  perfectly existent library function (I hate c++)

* Mon Jul 31 2006 Doug Ledford <dledford@redhat.com> 1.0-2
- Make spec file name convention/multilib compliant
- Move all the files to FHS compliant locations for a distributor

* Tue May 16 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added ibutils sh, csh and conf to update environment

* Sun Apr  2 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Initial packaging for openib gen2 stack
