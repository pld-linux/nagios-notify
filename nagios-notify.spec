# TODO:
# - move script to _libdir somewhere
Summary:	Nagios Notify Script
Summary(pl.UTF-8):	Skrypt powiadamiający dla Nagiosa
Name:		nagios-notify
Version:	0.9.5
Release:	2
License:	GPL v2
Group:		Applications
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	523e7ab6209b7ef5b386670cb7c1f08e
Patch0:		%{name}-statusfile.patch
URL:		http://glen.alkohol.ee/nagios-notify/
Requires:	awk
Requires:	nagios-common
Requires:	sed
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios

%description
nagios-notify is template based notify script for Nagios.

%description -l pl.UTF-8
nagios-notify to oparty na szablonach skrypt powiadamiający dla
Nagiosa.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/templates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/templates/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugins/*
%attr(755,root,root) %{_sbindir}/nagios-notify
