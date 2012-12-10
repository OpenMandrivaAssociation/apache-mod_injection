#Module-Specific definitions
%define mod_name mod_injection
%define mod_conf 23_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.3.1
Release:	15
Group:		System/Servers
License:	BSD
URL:		http://pmade.org/pjones/software/mod_injection/download.html
Source0: 	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		%{mod_name}-0.3.0-register.patch
Patch1:		mod_injection-0.3.1-apache220.diff
Patch2:		mod_injection-0.3.1-manual.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	openjade
BuildRequires:	docbook-style-dsssl
Epoch:		1

%description
mod_injection is an Apache 2.0.X filter module. It allows you to
inject text in the HTTP response after a HTML tag or after any
given text string. The main intention of this module is to add a
banner to several HTML pages on the fly.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p1
%patch1 -p0
%patch2 -p0

# fix strange permissions
find docs/manual/ -name "*.xml" | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
cp src/mod_injection.c .
%{_bindir}/apxs -c mod_injection.c

pushd docs/manual
    make html
popd    

mv docs/manual/one-html/manual.html index.html

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

# make the example work... (ugly, but it works...)
NEW_URL=%{_docdir}/%{name}-%{version}/
perl -pi -e "s|_REPLACE_ME_|$NEW_URL|g" %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc README INSTALL docs/CREDITS index.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-15mdv2012.0
+ Revision: 772668
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-14
+ Revision: 678327
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-13mdv2011.0
+ Revision: 588011
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-12mdv2010.1
+ Revision: 516129
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-11mdv2010.0
+ Revision: 406598
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-10mdv2009.1
+ Revision: 325778
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-9mdv2009.0
+ Revision: 234962
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-8mdv2009.0
+ Revision: 215590
- fix rebuild

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-7mdv2008.1
+ Revision: 182826
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.3.1-6mdv2008.1
+ Revision: 170728
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-5mdv2008.0
+ Revision: 82597
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3.1-4mdv2007.1
+ Revision: 140700
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-3mdv2007.1
+ Revision: 79441
- Import apache-mod_injection

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-3mdv2007.0
- rebuild

* Sun Dec 18 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-2mdk
- rebuilt against apache-2.2.0 (P1)
- make the html manual (P2)

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.3.1-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.3.1-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.3.1-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3.1-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3.1-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3.1-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3.1-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.3.1-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.3.1-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.3.1-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.3.1-1mdk
- built for apache 2.0.49

