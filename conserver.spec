Summary:	Console server
Summary(pl):	Serwer konsoli
Name:		conserver
Version:	8.1.0
Release:	0.1
License:	BSD-like
Group:		Daemons
Source0:	http://www.conserver.com/%{name}-%{version}.tar.gz
# Source0-md5:	-
URL:		http://www.conserver.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Conserver is an application that allows multiple users to watch a
serial console at the same time.  It can log the data, allows users
to take write-access of a console (one at a time), and has a
variety of bells and whistles to accentuate that basic
functionality.

%description -l pl
Conserver jest aplikacj± która umo¿liwia kilku u¿ytkownikom naraz
ogl±daæ logi na konsoli szeregowej. Mo¿e zapisywaæ zebrane dane, pozwalaæ
u¿ytkownikom na pe³ne korzystanie z konsoli (ale tylko jednemu naraz),
oraz posiada mnóstwo dodatków rozszerzaj±cych tê podstawow±
funkcjonalno¶æ.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_datadir}/examples/conserver examples

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc CHANGES FAQ README TODO
%doc examples LICENSE
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
