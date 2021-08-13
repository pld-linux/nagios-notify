Summary:	Nagios Notify Script
Summary(pl.UTF-8):	Skrypt powiadamiający dla Nagiosa
Name:		nagios-notify
Version:	0.14
Release:	4
License:	GPL v2
Group:		Applications
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	47c06d14e2944f222fe08298a62ef607
Patch0:		headers.patch
Patch1:		duration.patch
Patch2:		off-by.patch
URL:		http://glen.alkohol.ee/nagios-notify/
Requires:	awk
Requires:	nagios-common
# notify via emails
Suggests:	/usr/lib/sendmail
# notify via jabber
Suggests:	nagios-alert-jabber
# notify to eggdrop bot (irc)
Suggests:	t0xirc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios
%define		_sbindir	/usr/lib/nagios

%description
nagios-notify is template based notify script for Nagios.

You should use this script because:
- the templates are easily edited in text editor
- you won't be worried about if the command definition contains shell
  syntax errors (which Nagios happily discards without any trace in logs
  :/)
- you can change templates without restarting Nagios
- with advanced templates you can send richtext (even images!) over
  jabber if you use nagios-notify-jabber
- minimal dependency (just coreutils and awk that you most likely
  already have installed)

%description -l pl.UTF-8
nagios-notify to oparty na szablonach skrypt powiadamiający dla
Nagiosa.

Powody, dla których dobrze jest używać tego skryptu:
- szablony można łatwo modyfikować w edytorze tekstu,
- nie trzeba się zbytnio martwić jeśli definicje poleceń zawierają
  błędy składni powłoki (które Nagios ucina bez żadnego śladu w logach)
- można zmieniać szablony bez restartu Nagiosa
- przy użyciu zaawansowanych szablonów można wysyłać tekst wzbogacony
  (nawet z obrazkami) przez jabbera w przypadku używania pakietu
  nagios-notify-jabber
- minimalne zależności (tylko coreutils i awk, które zwykle i tak są
  zainstalowane)

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%dir %{_sysconfdir}/templates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/templates/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugins/%{name}.cfg
%attr(755,root,root) %{_sbindir}/nagios-notify
