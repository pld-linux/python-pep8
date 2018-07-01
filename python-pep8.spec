#
# Conditional build:
%bcond_without	tests	# test target
%bcond_without	doc	# Build API documentation
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	pep8
Summary:	Python style guide checker
Summary(pl.UTF-8):	Sprawdzanie zgodności z poradnikiem stylu kodowania w Pythonie
Name:		python-%{module}
Version:	1.7.0
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/pep8/
Source0:	https://pypi.python.org/packages/source/p/pep8/%{module}-%{version}.tar.gz
# Source0-md5:	2b03109b0618afe3b04b3e63b334ac9d
URL:		https://pypi.python.org/pypi/pep8
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%endif
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pep8 is a tool to check your Python code against some of the style
conventions in PEP 8.

%description -l pl.UTF-8
pep8 to narzędzie do sprawdzania kodu w Pythonie względem niektórych
konwencji stylistycznych opisanych w PEP 8.

%package -n python3-%{module}
Summary:	Python style guide checker
Summary(pl.UTF-8):	Sprawdzanie zgodności z poradnikiem stylu kodowania w Pythonie
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
pep8 is a tool to check your Python code against some of the style
conventions in PEP 8.

%description -n python3-%{module} -l pl.UTF-8
pep8 to narzędzie do sprawdzania kodu w Pythonie względem niektórych
konwencji stylistycznych opisanych w PEP 8.

%package apidocs
Summary:	API documentation for pep8 module
Summary(pl.UTF-8):	Dokumentacja API modułu pep8
Group:		Documentation

%description apidocs
API documentation for pep8 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu pep8.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
%{__rm} -r _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pep8{,-2}
%py_postclean
%endif

%if %{with python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pep8{,-3}
%endif

%if %{with python2}
ln -s pep8-2 $RPM_BUILD_ROOT%{_bindir}/pep8
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.rst
%attr(755,root,root) %{_bindir}/pep8
%attr(755,root,root) %{_bindir}/pep8-2
%{py_sitescriptdir}/pep8.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/pep8-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt README.rst
%attr(755,root,root) %{_bindir}/pep8-3
%{py3_sitescriptdir}/pep8.py
%{py3_sitescriptdir}/__pycache__/pep8.cpython-*.py[co]
%{py3_sitescriptdir}/pep8-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
