%define		extraversion %nil	
#define		extraversion rc1

%define name	flphoto
%define version	1.3.1
%define release	%mkrel 10

%define libgphoto %mklibname gphoto 2

Summary: 	All what you need for the photos from your digital camera
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPLv2+
Group: 		Graphics
Source0: 	http://belnet.dl.sourceforge.net/sourceforge/fltk/%{name}-%{version}%{extraversion}-source.tar.bz2
#Source0: 	http://belnet.dl.sourceforge.net/sourceforge/fltk/%{name}-1.1-20030727.tar.bz2
Source1:	digicam-launch-icon.png
Patch0:		flphoto-1.3.1-glibc-2.8.patch
Patch1:		flphoto-1.3.1-use-ldflags.patch
Patch2:		flphoto-1.3.1-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		espmsg.patch
URL: 		http://www.easysw.com/~mike/flphoto/
Requires: 	%{libgphoto} >= 2.1.1
Requires:	libgphoto-hotplug
BuildRequires: 	libgphoto-devel >= 2.1.1 fltk-devel libcups-devel libexif-devel
BuildRequires:  imagemagick desktop-file-utils
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
%setup -q -n %{name}-%{version}%{extraversion}
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p0

# Use /mnt/memory_card as default directory for memory cards, as
# hotplug sets up a supermount entry for memory cards to be mounted on
# /mnt/memory_card
perl -p -i -e 's:/mnt/flash:/media/removable:' *.cxx doc/* po/*
perl -p -i -e 's:/mnt/card:/media/removable:' *.cxx doc/* po/*

# Remove portuguese translation
perl -p -i -e 's:(TRANSLATIONS =.*?)\s*po/pt(.*)$:$1$2:' Makefile Makefile.in

# correct icon name
perl -p -i -e 's,%{name}.png,%{name},g' %{name}.desktop

%build

# CVS versions need "./autogen.sh"
#./autogen.sh

%configure2_5x --with-docdir=%{_datadir}/doc/%{name}

# This the Makefile does not do automatically
%make espmsg

%make

%install
rm -fr %buildroot
%makeinstall_std
%find_lang %{name}

# icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale 48 %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp %{name}.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor="" \
  --add-category="Photography" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# dynamic desktop support
%define launchers /etc/dynamic/launchers/camera

mkdir -p $RPM_BUILD_ROOT%launchers
cat > $RPM_BUILD_ROOT%launchers/%name.desktop << EOF
[Desktop Entry]
Name=FLPhoto
Comment=All you need for the photos from your digital camera
TryExec=/usr/bin/flphoto
Exec=/usr/bin/flphoto --camera
Terminal=false
Icon=flphoto
Type=Application
EOF

%post
%if %mdkversion < 200900
%update_menus
%update_icon_cache hicolor
%endif
update-alternatives --install %launchers/kde.desktop camera.kde.dynamic %launchers/%name.desktop 60
update-alternatives --install %launchers/gnome.desktop camera.gnome.dynamic %launchers/%name.desktop 60

%postun
%if %mdkversion < 200900
%clean_menus
%clean_icon_cache hicolor
%endif
if [ $1 = 0 ]; then
  update-alternatives --remove camera.kde.dynamic %launchers/%name.desktop
  update-alternatives --remove camera.gnome.dynamic %launchers/%name.desktop
fi

%clean
rm -fr %buildroot

%files -f %{name}.lang
%defattr(-,root,root,-)
%lang(de) %_datadir/locale/de/*
%lang(en_CA) %_datadir/locale/en_CA/*
%lang(en_GB) %_datadir/locale/en_GB/*
%lang(es) %_datadir/locale/es/*
%lang(fr) %_datadir/locale/fr/*
%lang(it) %_datadir/locale/it/*
%lang(nl) %_datadir/locale/nl/*
%lang(sv) %_datadir/locale/sv/*
%_datadir/doc/%name/*
%_bindir/*
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_datadir}/applications/flphoto.desktop
%_mandir/*/*
%config(noreplace) %_sysconfdir/dynamic/launchers/camera
