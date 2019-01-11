%define _disable_ld_no_undefined 1

%define py3verflags %(python3 -c "import sysconfig; print(sysconfig.get_config_var('SOABI'))")
%define py2verflags -python2.7
%define api 5.12

Summary:	The PySide project provides LGPL-licensed Python bindings for Qt5
Name:		shiboken2
Version:	5.12.0
Release:	1
License:	LGPLv2+
Group:		Development/KDE and Qt
Url:		https://wiki.qt.io/Qt_for_Python
Source0:	https://download.qt.io/official_releases/QtForPython/shiboken2/PySide2-%{version}-src/pyside-setup-everywhere-src-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
BuildRequires:	cmake
BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-setuptools
BuildRequires:	pkgconfig(python3)
BuildRequires:  python-setuptools 
BuildRequires:	python-sphinx
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5XmlPatterns)
BuildRequires:	python-numpy-devel
BuildRequires:	python2-numpy-devel
BuildRequires:	clang-devel
BuildRequires:	llvm-devel
%description
The PySide project provides LGPL-licensed Python bindings for the Qt
cross-platform application and UI framework. PySide Qt bindings allow both free
open source and proprietary software development and ultimately aim to support
all of the platforms as Qt itself.

%files
%{_bindir}/%{name}
%{_bindir}/shiboken_tool.py
%{py_platsitedir}/%{name}
%{py_platsitedir}/%{name}_generator
%{_mandir}/man1/*

%define libmajor %api
%define libname %mklibname %{name} %{libmajor}

%package -n %{libname}
Summary:        Shiboken Generator core lib
Group:          System/Libraries

%description -n %{libname}
Shiboken Generator core lib.

%files -n %{libname}
%{_libdir}/lib%{name}*cpython*.so.%{libmajor}*

#------------------------------------------------------------------------------

%define libmajor %api
%define libname_py2 %mklibname %{name}_python2.7 %{libmajor}

%package -n %{libname_py2}
Summary:        Shiboken Generator core lib
Group:          System/Libraries

%description -n %{libname_py2}
Shiboken Generator core lib.

%files -n %{libname_py2}
%{_libdir}/lib%{name}*python2*.so.%{libmajor}*


%package -n python2-shiboken2
Summary:        PySide shiboken2 module
Group:          Development/KDE and Qt

%description -n python2-shiboken2
PySide shiboken2 module.

%files -n python2-shiboken2
%{_bindir}/%{name}-%py2ver
%py2_platsitedir/%{name}
%py2_platsitedir/%{name}_generator

#------------------------------------------------------------------------------


%package devel
Summary:        PySide devel files
Group:          Development/KDE and Qt
Requires:       %{name} = %{version}-%{release}
Requires:       python2-shiboken2 = %{version}-%{release}
Requires:       %{libname} = %{version}-%{release}
Requires:       %{libname_py2} = %{version}-%{release}

%description devel
PySide devel files.

%files devel
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/*

#------------------------------------------------------------------------------


%prep
%setup -qn pyside-setup-everywhere-src-%{version}

cp -a . %py2dir

%build

pushd %{py2dir}/sources/shiboken2
%cmake -DBUILD_TESTS=OFF \
    -DUSE_PYTHON_VERSION=2
%make

popd

pushd sources/shiboken2
%cmake -DBUILD_TESTS=OFF \
     -DUSE_PYTHON_VERSION=3
%make

popd

%install
%makeinstall_std -C %{py2dir}/sources/shiboken2/build
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-%{python2_version}
mv %{buildroot}%{_mandir}/man1/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}-%{python2_version}.1

%makeinstall_std -C sources/shiboken2/build

