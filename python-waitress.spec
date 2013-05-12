Name:           python-waitress
Version:        0.8.3
Release:        1%{?dist}
Summary:        Waitress WSGI server

License:        ZPLv2.1
URL:            https://github.com/Pylons/waitress
Source0:        http://pypi.python.org/packages/source/w/waitress/waitress-%{version}.tar.gz
#md5=42715620040cdde68c467ed29bb50516

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose
BuildRequires:  python-coverage
BuildRequires:  python-sphinx

%description
Waitress is meant to be a production-quality pure-Python WSGI server with
very acceptable performance. It has no dependencies except ones which live
in the Python standard library. It runs on CPython on Unix and Windows under
Python 2.6+ and Python 3.2. It is also known to run on PyPy 1.6.0 on UNIX.
It supports HTTP/1.0 and HTTP/1.1.

For more information, see %{_docdir}/%{name}-%{version}/docs or
http://docs.pylonsproject.org/projects/waitress/en/latest/ .

%package -n python3-waitress
Summary:        Waitress WSGI server
Requires:       python3
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-coverage
BuildRequires:  python3-sphinx

%description -n python3-waitress
Waitress is meant to be a production-quality pure-Python WSGI server with
very acceptable performance. It has no dependencies except ones which live
in the Python standard library. It runs on CPython on Unix and Windows under
Python 2.6+ and Python 3.2. It is also known to run on PyPy 1.6.0 on UNIX.
It supports HTTP/1.0 and HTTP/1.1.

For more information, see %{_docdir}/%{name}-%{version}/docs or
http://docs.pylonsproject.org/projects/waitress/en/latest/ .

%prep
%setup -q -n waitress-%{version}
rm -rf waitress.egg-info
rm -f .gitignore docs/.gitignore
# this script has devel paths, not useful in a user system
rm -f docs/rebuild

rm -rf %{py3dir}
cp -a . %{py3dir}


%build
%{__python} setup.py build

pushd %{py3dir}
%{__python3} setup.py build
popd

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd


%check
# by setting the PYTHONPATH to the current dir
# we make the package waitress importable
# Usually the testsuite is run after installing
# the package in develop mode but we can't install
# in develop mode here.
PYTHONPATH=. %{__python} setup.py test -q

pushd %{py3dir}
PYTHONPATH=. %{__python3} setup.py test -q
popd

 
%files
%doc README.rst CHANGES.txt COPYRIGHT.txt LICENSE.txt docs
%{python_sitelib}/waitress
%{python_sitelib}/waitress-%{version}-py2.?.egg-info

%files -n python3-waitress
%doc README.rst CHANGES.txt COPYRIGHT.txt LICENSE.txt docs
%{python3_sitelib}/waitress
%{python3_sitelib}/waitress-%{version}-py3.?.egg-info


%changelog
* Sun May 12 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.3-1
- Update to upstream

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.2-3
- Use %{version} in the Source0 to avoid duplicates
* Sat Nov 24 2012 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.2-2
- Point to the local docs directory in the description for the documentation
- Remove py3dir before copying the files to it in the prep phase
- Remove -O1 in the build phase as it is not used anymore in the Fedora
  Packaging guidelines
- Remove files rpmlint doesn't like
* Mon Nov 19 2012 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.2-1
- New package.
