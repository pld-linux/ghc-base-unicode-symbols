#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	base-unicode-symbols
Summary:	New symbols for a number of functions, operators and types
Summary(pl.UTF-8):	Nowe symbole dla wielu funkcji, operatorów i typów
Name:		ghc-%{pkgname}
Version:	0.2.2.4
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/base-unicode-symbols
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	7faf43a94a0082ee2fe7971fabd9be21
URL:		http://hackage.haskell.org/package/base-unicode-symbols
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3.0
BuildRequires:	ghc-base < 5
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3.0
BuildRequires:	ghc-base-prof < 5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3.0
Requires:	ghc-base < 5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package defines new symbols for a number of functions, operators
and types in the base package.

All symbols are documented with their actual definition and
information regarding their Unicode code point. They should be
completely interchangeable with their definitions.

For further Unicode goodness you can enable the UnicodeSyntax language
extension. This extension enables Unicode characters to be used to
stand for certain ASCII character sequences, i.e. U+2192 instead of
->, U+2200 instead of forall and many others.

%description -l en.UTF-8
This package defines new symbols for a number of functions, operators
and types in the base package.

All symbols are documented with their actual definition and
information regarding their Unicode code point. They should be
completely interchangeable with their definitions.

For further Unicode goodness you can enable the UnicodeSyntax language
extension. This extension enables Unicode characters to be used to
stand for certain ASCII character sequences, i.e. → instead of ->, ∀
instead of forall and many others.

%description -l pl.UTF-8
Ten pakiet definiuje nowe symbole dla wielu funkcji, operatorów i
typów z pakietu base.

Wszystkie symbole są udokumentowane wraz z ich definicją i informacją
o ich kodzie Unicode. Powinny być całkowicie wymienne z ich
definicjami.

W celu jeszcze większego wykorzystania zalet Unicode, można włączyć
rozszerzenie języka UnicodeSyntax. Pozwala ono na używanie znaków
Unicode dla różnych sekwencji znaków ASCII, np. → zamiast ->, ∀
zamiast forall itd.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3.0
Requires:	ghc-base-prof < 5

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSbase-unicode-symbols-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbase-unicode-symbols-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Applicative
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Applicative/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Arrow
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Arrow/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Category
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Category/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Bool
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Bool/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Eq
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Eq/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Foldable
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Foldable/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Function
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Function/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Monoid
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Monoid/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Ord
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Ord/Unicode.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Prelude
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Prelude/Unicode.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSbase-unicode-symbols-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Applicative/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Arrow/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Category/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Bool/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Eq/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Foldable/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Function/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/List/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Monoid/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Ord/Unicode.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Prelude/Unicode.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
