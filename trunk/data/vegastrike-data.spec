Name: vegastrike-data
Summary: Vegastrike - a free 3D space fight simulator (data files)
Version: 0.2.9CVS
Release: 1
Copyright: GPL
Group: X11/GL/Games
Source: vegastrike-data.tar.gz
URL: http://vegastrike.sourceforge.net
Packager: Daniel Horn <hellcatv@hotmail.com>
BuildRoot: /tmp/vsdata
Prefix: /usr/local
Provides: vegastrike-data

%description
Vega Strike Celeste - Trade, Fight and Explore the Universe

Vegastrike is a free 3D Space Fight Simulator/RPG under the GPL


this archive contains the data files necessary to play Vegastrike.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n vegastrike-data

%build
echo "nothing to build"

%install
echo "Installing"
mkdir -p $RPM_BUILD_ROOT/usr/local/share/doc/vegastrike/
mkdir -p $RPM_BUILD_ROOT/usr/local/man/man1/
mkdir -p $RPM_BUILD_ROOT/usr/local/share/vegastrike/data
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/
cp vegastrike.1 $RPM_BUILD_ROOT/usr/local/man/man1/
cp vsinstall.1 $RPM_BUILD_ROOT/usr/local/man/man1/
cp vssetup.1 $RPM_BUILD_ROOT/usr/local/man/man1/
cp vslauncher.1 $RPM_BUILD_ROOT/usr/local/man/man1/
cp readme.txt $RPM_BUILD_ROOT/usr/local/share/doc/vegastrike/
cp vsinstall $RPM_BUILD_ROOT/usr/local/bin/
cp -R . $RPM_BUILD_ROOT/usr/local/share/vegastrike/data


%clean
rm -rf $RPM_BUILD_ROOT

%files
%docdir /usr/local/share/doc/vegastrike
/usr/local/share/doc/vegastrike/readme.txt
%doc /usr/local/man/man1/vegastrike.1
%doc /usr/local/man/man1/vssetup.1
%doc /usr/local/man/man1/vslauncher.1
%doc /usr/local/man/man1/vsinstall.1
/usr/local/bin/vsinstall
# Normal files
/usr/local/share/vegastrike/data
