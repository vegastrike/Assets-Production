Name: vegastrike-data
Summary: Vegastrike - a free 3D space fight simulator (data files)
Version: 0.2.9CVS
Release: 1
Copyright: GPL
Group: X11/GL/Games
Source: vegastrike-data.tar.gz
URL: http://vegastrike.sourceforge.net
Packager: Jonathan Hunt <jhuntnz@users.sourceforge.net>
BuildRoot: /tmp/vsdata
Prefix: /usr/local
Provides: vegastrike-data

%description
Vegastrike is a free 3D space fight simulator under the GPL

Vega Strike is an Interactive Flight Simulator/Real Time Stratagy being
 developed for Linux and Windows in 3d OpenGL...

this archive contains the data files necessary to play Vegastrike.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n vegastrike-data

%build
echo "nothing to build"

%install
echo "Installing"
mkdir -p $RPM_BUILD_ROOT/usr/local/share/doc/vegastrike/
mkdir -p $RPM_BUILD_ROOT/usr/local/share/vegastrike/data
cp readme.txt $RPM_BUILD_ROOT/usr/local/share/doc/vegastrike/
cp -R . $RPM_BUILD_ROOT/usr/local/share/vegastrike/data


%clean
rm -rf $RPM_BUILD_ROOT

%files
%docdir /usr/local/share/doc/vegastrike
/usr/local/share/doc/vegastrike/readme.txt
# Normal files
/usr/local/share/vegastrike/data
