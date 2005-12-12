# TODO: smart .init/.sysconfig, maybe a default configuration
#
Summary:	Console server
Summary(pl):	Serwer konsoli
Name:		conserver
Version:	8.1.12
Release:	1
License:	BSD-like
Group:		Daemons
Source0:	http://www.conserver.com/%{name}-%{version}.tar.gz
# Source0-md5:	1fb356224f018625be5c3d35529a4ac6
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-locks.patch
URL:		http://www.conserver.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libwrap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/conserver

%description
Conserver is an application that allows multiple users to watch a
serial console at the same time. It can log the data, allows users to
take write-access of a console (one at a time), and has a variety of
bells and whistles to accentuate that basic functionality.

%description -l pl
Conserver jest aplikacj�, kt�ra umo�liwia kilku u�ytkownikom naraz
ogl�da� logi na konsoli szeregowej. Mo�e zapisywa� zebrane dane,
pozwala� u�ytkownikom na pe�ne korzystanie z konsoli (ale tylko
jednemu naraz), oraz posiada mn�stwo dodatk�w rozszerzaj�cych t�
podstawow� funkcjonalno��.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-master=localhost \
	--with-extmsgs \
	--with-libwrap \
	--with-openssl \
	--with-pam
#	--with-uds
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d,conserver} \
	$RPM_BUILD_ROOT/var/log/{conserver.d,archiv/conserver.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/examples/conserver examples

install examples/conserver.cf $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/conserver.passwd
touch $RPM_BUILD_ROOT%{_sysconfdir}/console.cf

rm -f examples/conserver.rc
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/conserver
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/conserver
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/conserver

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add conserver
if [ -f /var/lock/subsys/conserver ]; then
	/etc/rc.d/init.d/conserver restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/conserver start\" to start conserver daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/conserver ]; then
		/etc/rc.d/init.d/conserver stop 1>&2
	fi
	/sbin/chkconfig --del conserver
fi

%files
%defattr(644,root,root,755)
%doc CHANGES FAQ README TODO examples LICENSE
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/conserver
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(750,root,root) %dir /var/log/conserver.d
%attr(750,root,root) %dir /var/log/archiv/conserver.d
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_mandir}/man*/*
