#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	doc	# Build API documentation
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	pep8
Summary:	Python style guide checker
Name:		python-%{module}
Version:	1.5.7
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/pep8/%{module}-%{version}.tar.gz
# Source0-md5:	f6adbdd69365ecca20513c709f9b7c93
URL:		https://pypi.python.org/pypi/pep8
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-Sphinx
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-distribute
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pep8 is a tool to check your Python code against some of the style
conventions in PEP 8.

%package -n python3-%{module}
Summary:	Python style guide checker
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
pep8 is a tool to check your Python code against some of the style
conventions in PEP 8.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.rst
%attr(755,root,root) %{_bindir}/pep8
%{py_sitescriptdir}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/pep8-*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt README.rst
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}.cpython-*.py[co]
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
