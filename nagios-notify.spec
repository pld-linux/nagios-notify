Summary:	Nagios Notify Script
Summary(pl.UTF-8):	Skrypt powiadamiający dla Nagiosa
Name:		nagios-notify
Version:	0.12
Release:	1
License:	GPL v2
Group:		Applications
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	8a77b70ad8bd47183e24f14c5b0c97ac
URL:		http://glen.alkohol.ee/nagios-notify/
Requires:	awk
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios
%define		_sbindir	/usr/lib/nagios

%description
nagios-notify is template based notify script for Nagios.

You should use this script because:
- the templates are easily edited in text editor
- you won't be worried about if the command definition contains shell
  syntax errors (which Nagios happily discards without any trace in
  logs :/)
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
  błędy składni powłoki (które Nagios ucina bez żadnego śladu w
  logach)
- można zmieniać szablony bez restartu Nagiosa
- przy użyciu zaawansowanych szablonów można wysyłać tekst
  wzbogacony (nawet z obrazkami) przez jabbera w przypadku używania
  pakietu nagios-notify-jabber
- minimalne zależności (tylko coreutils i awk, które zwykle i tak
  są zainstalowane)

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- %{name} < 0.10
%{__sed} -i -e 's,/usr/sbin/%{name},%{_sbindir}/%{name},' %{_sysconfdir}/plugins/%{name}.cfg
if [ -f /etc/rc.d/init.d/nagios ]; then
	%service -q nagios reload
fi

%triggerpostun -- %{name} < 0.12-0.7
# recover renamed configs
for a in %{_sysconfdir}/templates/*.rpmsave; do
	[ -f $a ] || continue
	f=${a%%.rpmsave}
	[ -f $f ] && cp -f $f{,.rpmnew}
	mv -f $f{.rpmsave,}
done
# copy from new files if originals weren't modified but removed by upgrade
for a in eggdrop jabber sms; do
	o=%{_sysconfdir}/templates/host-notify-by-$a.tmpl
	f=%{_sysconfdir}/templates/notify-host-by-$a.tmpl
	if [ ! -f $o ]; then
		cp -a $f $o
	fi
done
for a in eggdrop email jabber-embedimage jabber-richtext jabber sms; do
	o=%{_sysconfdir}/templates/notify-by-$a.tmpl
	f=%{_sysconfdir}/templates/notify-service-by-$a.tmpl
	if [ ! -f $o ]; then
		cp -a $f $o
	fi
done
%banner -e %{name}-0.12 <<'EOF'
Templates have been renamed to follow Nagios 3.0 naming.

They have been recovered by rpm trigger, but if you want to use new style
naming these commands might help you out quickly:

# grep -r host-notify-by- /etc/nagios -l | xargs sed -i -e 's,host-notify-by-,notify-host-by-,g'
# grep -r notify-by- /etc/nagios -l | xargs sed -i -e 's,notify-by-,notify-service-by-,g'

EOF

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/templates
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/templates/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugins/%{name}.cfg
%attr(755,root,root) %{_sbindir}/nagios-notify
