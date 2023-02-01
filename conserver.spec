# TODO: smart .init/.sysconfig, maybe a default configuration
#
Summary:	Console server
Summary(pl.UTF-8):	Serwer konsoli
Name:		conserver
Version:	8.2.6
Release:	2
License:	BSD-like
Group:		Daemons
Source0:	https://github.com/bstansell/conserver/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f04d6ab6172d81db24886b12f224940c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}.pam
Source5:	%{name}.service
URL:		http://www.conserver.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libwrap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.644
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	systemd-units >= 38
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/conserver

%description
Conserver is an application that allows multiple users to watch a
serial console at the same time. It can log the data, allows users to
take write-access of a console (one at a time), and has a variety of
bells and whistles to accentuate that basic functionality.

%description -l pl.UTF-8
Conserver jest aplikacją, która umożliwia kilku użytkownikom naraz
oglądać logi na konsoli szeregowej. Może zapisywać zebrane dane,
pozwalać użytkownikom na pełne korzystanie z konsoli (ale tylko
jednemu naraz), oraz posiada mnóstwo dodatków rozszerzających tę
podstawową funkcjonalność.

%prep
%setup -q

%build
%configure \
	--with-master=localhost \
	--with-port=782 \
	--with-extmsgs \
	--with-libwrap \
	--with-openssl \
	--with-pam
#	--with-uds
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d,conserver,pam.d} \
	$RPM_BUILD_ROOT/var/log/{conserver.d,archive/conserver.d} \
	$RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/examples/conserver examples

cp -p examples/conserver.cf $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/conserver.passwd
touch $RPM_BUILD_ROOT%{_sysconfdir}/console.cf

rm -f examples/conserver.rc
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/conserver
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/conserver
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/conserver
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/conserver
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add conserver
%service conserver restart "conserver daemon"
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service conserver stop
	/sbin/chkconfig --del conserver
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc CHANGES FAQ README.md TODO examples LICENSES
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/conserver
%attr(755,root,root) %{_libdir}/conserver/convert
%attr(754,root,root) /etc/rc.d/init.d/conserver
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/conserver
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(750,root,root) %dir /var/log/conserver.d
%attr(750,root,root) %dir /var/log/archive/conserver.d
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_mandir}/man*/*
%{systemdunitdir}/%{name}.service
