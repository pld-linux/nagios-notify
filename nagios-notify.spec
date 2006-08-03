Summary:	Nagios Notify Script
Name:		nagios-notify
Version:	0.9
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	%{name}.sh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/templates

%description
nagios-notify is template based notify script for Nagios.

%prep
%setup -qcT
install %{SOURCE0} %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}
install %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%attr(755,root,root) %{_sbindir}/nagios-notify
