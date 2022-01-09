#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Syntax extension for writing in-line benchmarks in OCaml code
Summary(pl.UTF-8):	Rozszerzenie składni do pisania testów wydajności wewnątrz kodu w OCamlu
Name:		ocaml-ppx_bench
Version:	0.14.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/janestreet/ppx_bench/tags
Source0:	https://github.com/janestreet/ppx_bench/archive/v%{version}/ppx_bench-%{version}.tar.gz
# Source0-md5:	f2852170a6396d60d4fc1c156be1ec62
URL:		https://github.com/janestreet/ppx_bench
BuildRequires:	ocaml >= 1:4.04.2
BuildRequires:	ocaml-dune >= 2.0.0
BuildRequires:	ocaml-ppx_inline_test-devel >= 0.14
BuildRequires:	ocaml-ppx_inline_test-devel < 0.15
BuildRequires:	ocaml-ppxlib-devel >= 0.14.0
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
Syntax extension for writing in-line benchmarks in OCaml code.

This package contains files needed to run bytecode executables using
ppx_bench library.

%description -l pl.UTF-8
Rozszerzenie składni do pisania testów wydajności wewnątrz kodu w
OCamlu.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki ppx_bench.

%package devel
Summary:	Syntax extension for writing in-line benchmarks in OCaml code - development part
Summary(pl.UTF-8):	Rozszerzenie składni do pisania testów wydajności wewnątrz kodu w OCamlu - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
Requires:	ocaml-ppx_inline_test-devel >= 0.14
Requires:	ocaml-ppxlib-devel >= 0.14.0

%description devel
This package contains files needed to develop OCaml programs using
ppx_bench library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki ppx_bench.

%prep
%setup -q -n ppx_bench-%{version}

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr example/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/ppx_bench/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/ppx_bench/*/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/ppx_bench

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md
%dir %{_libdir}/ocaml/ppx_bench
%attr(755,root,root) %{_libdir}/ocaml/ppx_bench/ppx.exe
%{_libdir}/ocaml/ppx_bench/META
%{_libdir}/ocaml/ppx_bench/*.cma
%dir %{_libdir}/ocaml/ppx_bench/runtime-lib
%{_libdir}/ocaml/ppx_bench/runtime-lib/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/ppx_bench/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/ppx_bench/runtime-lib/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/ppx_bench/*.cmi
%{_libdir}/ocaml/ppx_bench/*.cmt
%{_libdir}/ocaml/ppx_bench/*.cmti
%{_libdir}/ocaml/ppx_bench/*.mli
%{_libdir}/ocaml/ppx_bench/runtime-lib/*.cmi
%{_libdir}/ocaml/ppx_bench/runtime-lib/*.cmt
%{_libdir}/ocaml/ppx_bench/runtime-lib/*.cmti
%{_libdir}/ocaml/ppx_bench/runtime-lib/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/ppx_bench/ppx_bench.a
%{_libdir}/ocaml/ppx_bench/*.cmx
%{_libdir}/ocaml/ppx_bench/*.cmxa
%{_libdir}/ocaml/ppx_bench/runtime-lib/ppx_bench_lib.a
%{_libdir}/ocaml/ppx_bench/runtime-lib/*.cmx
%{_libdir}/ocaml/ppx_bench/runtime-lib/*.cmxa
%endif
%{_libdir}/ocaml/ppx_bench/dune-package
%{_libdir}/ocaml/ppx_bench/opam
%{_examplesdir}/%{name}-%{version}
