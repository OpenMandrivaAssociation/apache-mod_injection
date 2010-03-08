#Module-Specific definitions
%define mod_name mod_injection
%define mod_conf 23_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.3.1
Release:	%mkrel 12
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%{_sbindir}/apxs -c mod_injection.c

pushd docs/manual
    make html
popd    

mv docs/manual/one-html/manual.html index.html

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README INSTALL docs/CREDITS index.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


