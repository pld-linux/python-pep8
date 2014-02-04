#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	doc	# Build API documentation

%define		module	pep8
Summary:	Python style guide checker
Name:		python-%{module}
Version:	1.4.6
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/pep8/%{module}-%{version}.tar.gz
# Source0-md5:	a03bb494859e87b42601b61b1b043a0c
URL:		https://pypi.python.org/pypi/pep8
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	python-Sphinx
BuildRequires:	python-distribute
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
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
%{__python} setup.py build --build-base build-2 %{?with_tests:test}

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.rst
%attr(755,root,root) %{_bindir}/pep8
%{py_sitescriptdir}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/pep8-*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
