Summary:	Nagios Notify Script
Name:		nagios-notify
Version:	0.9.1
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	9de77442cc2a101f9a3ac67f48f1c87a
URL:		http://svn.pld-linux.org/cgi-bin/viewsvn/nagios-notify/
Requires:	awk
Requires:	nagios-common
Requires:	sed
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/templates

%description
nagios-notify is template based notify script for Nagios.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/nagios-notify
