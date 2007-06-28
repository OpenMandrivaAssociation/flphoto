%define		extraversion %nil	
#define		extraversion rc1

%define libgphoto %mklibname gphoto 2

Summary: 	All what you need for the photos from your digital camera
Name: 		flphoto
Version: 	1.2
Release: 	%mkrel 9
License: 	GPL
Group: 		Graphics
Source0: 	http://belnet.dl.sourceforge.net/sourceforge/fltk/%{name}-%{version}%{extraversion}-source.tar.bz2
#Source0: 	http://belnet.dl.sourceforge.net/sourceforge/fltk/%{name}-1.1-20030727.tar.bz2
Source1:	digicam-launch-icon.png.bz2
Patch1:		flphoto-1.2-crop-custom-ratio-div-by-zero.patch.bz2
Patch2:		flphoto-1.2-default-print-quality-best.patch.bz2
URL: 		http://www.easysw.com/~mike/flphoto/
Requires: 	%{libgphoto} >= 2.1.1
Requires:	libgphoto-hotplug
BuildRequires: 	libgphoto-devel >= 2.1.1 libfltk-devel libcups-devel libexif-devel
BuildRequires:  ImageMagick
BuildRoot: 	%{_tmppath}/%{name}-buildroot

%description
flphoto is a basic photo/image management and display program.

  - Download of photos from digital cameras or usual file systems
  - Organization in albums
  - Loss-less rotation for portrait-oriented photos
  - Basic correction tasks 
  - Printing series of photos (full access to printer settings):
      o Index prints
      o 1, 2, or 4 equally-sized images per page
      o 8 photos in different sizes on one page
      o Calendar: 1 photo per month
      o Framed/Matted photos
  - Slide-show with manual or automatic advancing
  - Web album generation
  - Integration of GPhoto2 and CUPS


%prep
rm -rf ${RPM_BUILD_DIR}/%{name}-%{version}%{extraversion}
rm -rf ${RPM_BUILD_DIR}/%{name}

%setup -q -n %{name}-%{version}%{extraversion}
#setup -q -n %{name}
# Avoid crash when setting custom ratio in crop dialog
%patch1 -p0
# Use best print quality by default
%patch2 -p0

bzcat %{SOURCE1} > icon.png

# Use /mnt/memory_card as default directory for memory cards, as
# hotplug sets up a supermount entry for memory cards to be mounted on
# /mnt/memory_card
perl -p -i -e 's:/mnt/flash:/mnt/removable:' *.cxx doc/* po/*
perl -p -i -e 's:/mnt/card:/mnt/removable:' *.cxx doc/* po/*

# Remove portuguese translation
perl -p -i -e 's:(TRANSLATIONS =.*?)\s*po/pt(.*)$:$1$2:' Makefile Makefile.in

%build

# CVS versions need "./autogen.sh"
#./autogen.sh

%configure2_5x --with-docdir=%{_datadir}/doc/%{name}-%{version}

# This the Makefile does not do automatically
%make espmsg

%make

# convert icons to required format
convert icon.png -resize 32x32 flphoto.png
convert icon.png -resize 16x16 flphoto_mini.png
convert icon.png -resize 48x48 flphoto_large.png

%install

# Do not install KDE menu entries which came with the package
perl -p -i -e 's/^(install:.*)install-desktop$/$1/' Makefile

%makeinstall docdir=%buildroot%{_datadir}/doc/%{name}-%{version} FLPHOTO_LOCALE=%buildroot%{_datadir}/locale
%find_lang %{name}

# icons
install -d $RPM_BUILD_ROOT%{_datadir}/icons
install -m 644 flphoto.png $RPM_BUILD_ROOT%{_datadir}/icons/
install -d $RPM_BUILD_ROOT%{_datadir}/icons/mini
install -m 644 flphoto_mini.png $RPM_BUILD_ROOT%{_datadir}/icons/mini/flphoto.png
install -d $RPM_BUILD_ROOT%{_datadir}/icons/large
install -m 644 flphoto_large.png $RPM_BUILD_ROOT%{_datadir}/icons/large/flphoto.png

# menu stuff
install -d $RPM_BUILD_ROOT%{_menudir}
cat <<EOF > %buildroot/%_menudir/flphoto
?package(flphoto):command="/usr/bin/flphoto" \
title="FLPhoto (GPhoto 2)" \
longtitle="All what you need for the photos from your digital camera" \
needs="x11" \
section="Multimedia/Graphics" \
%if %mdkver >= 200700
xdg=true \
%endif
icon="flphoto.png"
EOF

%if %mdkver >= 200700
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-flphoto.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=FLPhoto (GPhoto 2)
Comment=All what you need for the photos from your digital camera
Exec=/usr/bin/flphoto
Icon=flphoto.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Graphics;Graphics / Photography / 3DGraphics;Graphics;Viewer; 	
EOF
%endif

# dynamic desktop support
%define launchers /etc/dynamic/launchers/camera

mkdir -p $RPM_BUILD_ROOT%launchers
cat > $RPM_BUILD_ROOT%launchers/%name.desktop << EOF
[Desktop Entry]
Name=FLPhoto
Comment=All what you need for the photos from your digital camera
TryExec=/usr/bin/flphoto
Exec=/usr/bin/flphoto --camera
Terminal=false
Icon=flphoto.png
Type=Application
EOF

%post
%update_menus
update-alternatives --install %launchers/kde.desktop camera.kde.dynamic %launchers/%name.desktop 60
update-alternatives --install %launchers/gnome.desktop camera.gnome.dynamic %launchers/%name.desktop 60

%postun
%clean_menus
if [ $1 = 0 ]; then
  update-alternatives --remove camera.kde.dynamic %launchers/%name.desktop
  update-alternatives --remove camera.gnome.dynamic %launchers/%name.desktop
fi

%clean
rm -fr %buildroot

%files -f %{name}.lang
%defattr(-,root,root,-)
%_datadir/doc/%name-%version/*
%_datadir/locale/*/flphoto*
%_bindir/*
%_datadir/icons/*
%_menudir/*
%if %mdkver >= 200700
%{_datadir}/applications/mandriva-flphoto.desktop
%endif
%_mandir/*/*
%config(noreplace) %_sysconfdir/dynamic/launchers/camera
