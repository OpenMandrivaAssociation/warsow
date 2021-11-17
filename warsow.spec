%define		debug_package	%nil

# Workaround duplicate symbols
%global optflags %{optflags} -fcommon

Name:		warsow
Summary:	A fast-paced first-person-shooter game
Version:	2.1.2
Release:	1
License:	GPLv2
Group:		Games/Other
URL:		http://www.warsow.net/
Source0:	https://warsow.net/warsow_21_sdk.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png

BuildRequires:	jpeg-devel
BuildRequires:	stdc++-devel
BuildRequires:	stdc++-static-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xxf86dga)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xi)
BuildRequires:	imagemagick
Requires:	%{name}-data = %{version}

%description
Warsow is a free standalone first person shooter game based on the Qfusion 3D
engine (a modification of the Quake 2 GPL engine), and aimed on the competitive
scene, or the e-sports community.

The base gameplay is focused around the art of movement; speed and tricks play
a big part in the gameplay. Besides this, mapcontrol, aim, teamplay and
fragging skills play their role too.

Another twist in gameplay is the weapon system. Warsow has two firing
modes for each weapon; by picking up a weapon, you will be equipped with the
standard (weak) ammo for the weapon, but when you pick up an ammo pack, you
will equip your weapon with special (strong) ammo. Weapons may have different
damage or slightly different behaviour depending on which ammo you use.

To keep the focus on competitive gaming, visibility is important in Warsow.
Cell-shaded, cartoon-like styles on the maps, textures, and models combine for
good visibility, suitable for competitive gameplay.

%files
%doc docs/*
%{_gamesbindir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*.desktop
%{_libdir}/games/%{name}/libs

#----------------------------------------------------------------

%package server
Group:		Games/Arcade
Summary:	Dedicated server for TurtleArena
Requires:	%{name}-data => %{version}

%description server
Turtle Arena (working title) is a free and open source cross-platform 
third-person action game using a modified version of the ioquake3 engine.
Turtle Arena is currently focused on multiplayer (with multiple game modes) 
and can be played with human players over a network, splitscreen, or with AI 
players. In the future there will also be a single player / cooperative reach 
the end of the level mode with AI enemies.

This package contains the dedicated server for TurtleArena.

%files server
%{_gamesbindir}/%{name}-server
%{_gamesbindir}/%{name}-tv-server

#----------------------------------------------------------------

%prep
%setup -q -n warsow_21_sdk
sed -i -e "/fs_basepath =/ s:\.:%{_libdir}/games/%{name}:" source/source/qcommon/files.c

%build
export CC=gcc
export CXX=g++
pushd source/source
mkdir -p cmake_build
cd cmake_build 
cmake -DQFUSION_GAME=Warsow .. 
make
popd

%install
pushd warsow_21_sdk/source/source/build
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,64x64,128x128,256x256}/apps
mkdir -p %{buildroot}%{_gamesbindir}
mkdir -p %{buildroot}%{_libdir}/games/%{name}/libs

install -m 0644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png
convert -scale 128x128 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
convert -scale 64x64 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
convert -scale 32x32 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png

install -m 755 warsow.* %{buildroot}%{_gamesbindir}/%{name}
install -m 755 wsw_server.* %{buildroot}%{_gamesbindir}/%{name}-server
install -m 755 wswtv_server.* %{buildroot}%{_gamesbindir}/%{name}-tv-server

cp %{SOURCE1} %{buildroot}%{_datadir}/applications/

install -m 755 libs/*.so %{buildroot}%{_libdir}/games/%{name}/libs/
popd
