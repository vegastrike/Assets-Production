Name: vegastrike-data
Summary: Vegastrike - a free 3D space fight simulator (data files)
Version: 0.3.1
Release: common
Copyright: GPL
Group: Amusements/Games
Source: vegastrike-data.tar.gz
URL: http://vegastrike.sourceforge.net
Packager: Daniel Horn <hellcatv@hotmail.com>
BuildRoot: /tmp/data
Prefix: /usr/local
Provides: vegastrike-data
Requires: vegastrike

%description
Vega Strike Celeste - Trade, Fight and Explore the Universe

Vega Strike is a 3d OpenGL GPL Action RPG space sim for Windows/Linux that allows a player to trade and bounty hunt in the spirit of Elite. You start in an old beat up Wayfarer cargo ship, with endless possibility before you and just enough cash to scrape together a life. Yet danger lurks in the space beyond.

this archive contains the data files necessary to play Vegastrike.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n data

%build
echo "nothing to build"

%install
echo "Installing"
mkdir -p $RPM_BUILD_ROOT/usr/local/games/vegastrike/data
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/
mkdir -p $RPM_BUILD_ROOT/usr/local/man/man1/
cp vslauncher $RPM_BUILD_ROOT/usr/local/bin/
cp vsinstall $RPM_BUILD_ROOT/usr/local/bin/
cp vsinstall.1 $RPM_BUILD_ROOT/usr/local/man/man1/
cp vslauncher.1 $RPM_BUILD_ROOT/usr/local/man/man1/
cp -R . $RPM_BUILD_ROOT/usr/local/games/vegastrike/data

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc /usr/local/man/man1/vslauncher.1
%doc /usr/local/man/man1/vsinstall.1
# Normal files
/usr/local/games/vegastrike/data
/usr/local/bin/vslauncher
/usr/local/bin/vsinstall
