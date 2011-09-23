Name:		warsow
Summary:	A fast-paced first-person-shooter game
Version:	0.61
Release:	%mkrel 1
License:	GPLv2
Group:		Games/Other 
URL:		http://www.warsow.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Source0:	warsow_%{version}_sdk.zip
Source1:	warsow.desktop

# From http://bugs.frugalware.org/task/1828
Source2:	warsow.png
#BuildRequires:	unzip SDL-devel openal-devel xorg-x11-devel curl-devel 
BuildRequires:	unzip SDL-devel openal-devel curl-devel 
BuildRequires:	libjpeg-devel
BuildRequires:	libxinerama-devel
BuildRequires:	openssl-devel
BuildRequires:	x11-server-devel
#BuildRequires:	libxorg-x11-devel
BuildRequires:	libvorbis-devel
Requires:	warsow-data = 0.61

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

%prep
%setup -q -c


cd $RPM_BUILD_DIR/warsow-%{version}/source
# From http://sources.gentoo.org/viewcvs.py/gentoo-x86/games-fps/warsow/
#% patch0 -p0
sed -i -e "/fs_basepath =/ s:\.:%{_datadir}/%{name}:" qcommon/files.c
sed -i s/--as-needed// Makefile

%build
cd  $RPM_BUILD_DIR/warsow-%{version}/source
make \
	BUILD_CLIENT=YES \
	BUILD_SERVER=YES \
	BUILD_TV_SERVER=YES \
	BUILD_IRC=YES \
	BUILD_SND_OPENAL=YES \
	BUILD_SND_QF=YES \
	DEBUG_BUILD=NO

%install
cd  $RPM_BUILD_DIR/warsow-%{version}/source/release

mkdir -p %{buildroot}/usr/share/{applications,pixmaps} 
mkdir -p %{buildroot}/%{_bindir}

# Should be using libdir.
mkdir -p %{buildroot}/%{_libdir}/%{name}
#mkdir -p % {buildroot}/ % {_datadir}/ % {name}/libs/

install -m 644 %{SOURCE2} %{buildroot}/%{_datadir}/pixmaps

install -m 755 warsow.* %{buildroot}/%{_bindir}/%{name}
install -m 755 wsw_server.* %{buildroot}/%{_bindir}/%{name}-server
install -m 755 wswtv_server.* %{buildroot}/%{_bindir}/%{name}-tv-server

cp %SOURCE1 "%{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop"


install -m 755 libs/irc_*.so %{buildroot}/%{_libdir}/%{name}/
install -m 755 libs/snd_qf_*.so %{buildroot}/%{_libdir}/%{name}/
install -m 755 libs/snd_openal_*.so %{buildroot}/%{_libdir}/%{name}/
#install -m 755 libs/irc_*.so % {buildroot}/ % {_datadir}/ % {name}/libs/
#install -m 755 libs/snd_qf_*.so % {buildroot}/ % {_datadir}/ % {name}/libs/
#install -m 755 libs/snd_openal_*.so % {buildroot}/ % {_datadir}/ % {name}/libs/



%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs/*
%{_bindir}/%{name}
%{_bindir}/%{name}-server
%{_bindir}/%{name}-tv-server
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/*.desktop
%{_libdir}/%{name}/
# % {_datadir}/ % {name}/libs/
