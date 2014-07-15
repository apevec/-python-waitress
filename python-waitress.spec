%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           python-waitress
Version:        0.8.9
Release:        4%{?dist}
Summary:        Waitress WSGI server

License:        ZPLv2.1
URL:            https://github.com/Pylons/waitress
Source0:        http://pypi.python.org/packages/source/w/waitress/waitress-%{version}.tar.gz
#md5=da3f2e62b3676be5dd630703a68e2a04

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

For more information, see %{_pkgdocdir}/docs or
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

For more information, see %{_pkgdocdir}/docs or
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
%{__python2} setup.py build

pushd %{py3dir}
%{__python3} setup.py build
popd

%install
# Run the Python 3 install first so that the Python 2 version
# of /usr/bin/waitress-server "wins":
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd

%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT


%check
# by setting the PYTHONPATH to the current dir
# we make the package waitress importable
# Usually the testsuite is run after installing
# the package in develop mode but we can't install
# in develop mode here.
PYTHONPATH=. %{__python2} setup.py nosetests

pushd %{py3dir}
PYTHONPATH=. %{__python3} setup.py nosetests
popd


%files
%doc README.rst CHANGES.txt COPYRIGHT.txt LICENSE.txt docs
%{_bindir}/waitress-serve
%{python2_sitelib}/waitress
%{python2_sitelib}/waitress-%{version}-py2.?.egg-info

%files -n python3-waitress
%doc README.rst CHANGES.txt COPYRIGHT.txt LICENSE.txt docs
%{python3_sitelib}/waitress
%{python3_sitelib}/waitress-%{version}-py3.?.egg-info


%changelog

* Mon Jul 14 2014 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.9-4
- Fix comment in %description about versioned directory for docs
- Use __python2 macro instead of __python

* Sat Jun 14 2014 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.9-3
- Run the tests with nose to avoid unclosed socket errors

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.9-1
- Update to upstream

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Dec 22 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.8-1
- Update to upstream

* Sun Dec 8 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.5-3
- Remove python3 dependency on the python-waitress python2 package

* Wed Aug 7 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.5-2
- Update description to use the new Fedora 20 _pkgdocdir macro, which
  is also defined for backwards cmompatibility

* Wed Jul 31 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.5-1
- Update to upstream

* Sat Jul 6 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.4-1
- Update to upstream
- Added waitress-serve as a binary executable in /usr/bin

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
