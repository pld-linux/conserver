# TODO: smart .init/.sysconfig, maybe a default configuration
#
Summary:	Console server
Summary(pl):	Serwer konsoli
Name:		conserver
Version:	8.1.9
Release:	1
License:	BSD-like
Group:		Daemons
Source0:	http://www.conserver.com/%{name}-%{version}.tar.gz
# Source0-md5:	7f4e613cbe5ebdd61ef9c01d7e8a05b8
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
URL:		http://www.conserver.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel
BuildRequires:	libwrap-devel
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Conserver is an application that allows multiple users to watch a
serial console at the same time.  It can log the data, allows users
to take write-access of a console (one at a time), and has a
variety of bells and whistles to accentuate that basic
functionality.

%description -l pl
Conserver jest aplikacj±, która umo¿liwia kilku u¿ytkownikom naraz
ogl±daæ logi na konsoli szeregowej. Mo¿e zapisywaæ zebrane dane,
pozwalaæ u¿ytkownikom na pe³ne korzystanie z konsoli (ale tylko
jednemu naraz), oraz posiada mnóstwo dodatków rozszerzaj±cych tê
podstawow± funkcjonalno¶æ.

%prep
%setup -q

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
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d} \
	$RPM_BUILD_ROOT/var/log/{conserver.d,archiv/conserver.d}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/examples/conserver examples
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
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/*
%attr(750,root,root) %dir /var/log/conserver.d
%attr(750,root,root) %dir /var/log/archiv/conserver.d
%{_mandir}/man*/*
