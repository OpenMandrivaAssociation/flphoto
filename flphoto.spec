%define extraversion %nil

Summary:	All what you need for the photos from your digital camera
Name:		flphoto
Version:	1.3.1
Release:	22
License:	GPLv2+
Group:		Graphics
Url:		http://www.easysw.com/~mike/flphoto/
Source0:	http://belnet.dl.sourceforge.net/sourceforge/fltk/%{name}-%{version}%{extraversion}-source.tar.bz2
Source1:	digicam-launch-icon.png
Patch0:		flphoto-1.3.1-glibc-2.8.patch
Patch1:		flphoto-1.3.1-use-ldflags.patch
Patch2:		flphoto-1.3.1-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		espmsg.patch
Patch4:		flphoto-1.3.1-compile.patch

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	cups-devel
BuildRequires:	fltk-devel
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libgphoto2)
Requires:	libgphoto-common

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
%setup -qn %{name}-%{version}%{extraversion}
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p0
%patch4 -p1 -b .compile~
autoconf

# Use /mnt/memory_card as default directory for memory cards, as
# hotplug sets up a supermount entry for memory cards to be mounted on
# /mnt/memory_card
sed -i -e 's:/mnt/flash:/media/removable:' *.cxx doc/* po/*
sed -i -e 's:/mnt/card:/media/removable:' *.cxx doc/* po/*

# Remove portuguese translation
perl -p -i -e 's:(TRANSLATIONS =.*?)\s*po/pt(.*)$:$1$2:' Makefile.in

# correct icon name
sed -i -e 's,%{name}.png,%{name},g' %{name}.desktop

%build
# CVS versions need "./autogen.sh"
#./autogen.sh

%configure2_5x \
	--with-docdir=%{_datadir}/doc/%{name}

# This the Makefile does not do automatically
%make espmsg

%make

%install
%makeinstall_std

%find_lang %{name} || touch %{name}.lang

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale 48 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cp %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor="" \
	--add-category="Photography" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

# dynamic desktop support
%define launchers /etc/dynamic/launchers/camera

mkdir -p %{buildroot}%{launchers}
cat > %{buildroot}%{launchers}/%{name}.desktop << EOF
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
update-alternatives --install %{launchers}/kde.desktop camera.kde.dynamic %{launchers}/%{name}.desktop 60
update-alternatives --install %{launchers}/gnome.desktop camera.gnome.dynamic %{launchers}/%{name}.desktop 60

%postun
if [ $1 = 0 ]; then
  update-alternatives --remove camera.kde.dynamic %{launchers}/%{name}.desktop
  update-alternatives --remove camera.gnome.dynamic %{launchers}/%{name}.desktop
fi

%files -f %{name}.lang
%lang(de) %{_datadir}/locale/de/*
%lang(en_CA) %{_datadir}/locale/en_CA/*
%lang(en_GB) %{_datadir}/locale/en_GB/*
%lang(es) %{_datadir}/locale/es/*
%lang(fr) %{_datadir}/locale/fr/*
%lang(it) %{_datadir}/locale/it/*
%lang(nl) %{_datadir}/locale/nl/*
%lang(sv) %{_datadir}/locale/sv/*
%{_datadir}/doc/%{name}/*
%{_bindir}/*
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_datadir}/applications/flphoto.desktop
%{_mandir}/*/*
%config(noreplace) %{_sysconfdir}/dynamic/launchers/camera

