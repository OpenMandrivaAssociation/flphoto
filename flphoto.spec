%define extraversion %nil

Summary:	All what you need for the photos from your digital camera
Name:		flphoto
Version:	1.3.1
Release:	16
License:	GPLv2+
Group:		Graphics
URL:		http://www.easysw.com/~mike/flphoto/
Source0:	http://belnet.dl.sourceforge.net/sourceforge/fltk/%{name}-%{version}%{extraversion}-source.tar.bz2
Source1:	digicam-launch-icon.png
Patch0:		flphoto-1.3.1-glibc-2.8.patch
Patch1:		flphoto-1.3.1-use-ldflags.patch
Patch2:		flphoto-1.3.1-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		espmsg.patch
Patch4:		flphoto-1.3.1-compile.patch
Requires:	libgphoto-common
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	fltk-devel
BuildRequires:	pkgconfig(libexif)
BuildRequires:	cups-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils

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
%patch4 -p1 -b .compile~
autoconf

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
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

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


%changelog
* Thu May 31 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.3.1-13
+ Revision: 801489
- Make it build in current environment

  + Oden Eriksson <oeriksson@mandriva.com>
    - attempt to relink against libpng15.so.15
    - rebuild

* Sun May 08 2011 Funda Wang <fwang@mandriva.org> 1.3.1-10
+ Revision: 672345
- add gentoo patches to make it build

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-9mdv2011.0
+ Revision: 605155
- rebuild

* Wed Feb 17 2010 Frederic Crozat <fcrozat@mandriva.com> 1.3.1-8mdv2010.1
+ Revision: 507146
- force rebuild

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-7mdv2010.1
+ Revision: 488753
- rebuilt against libjpeg v8

* Sun Aug 16 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-6mdv2010.0
+ Revision: 416852
- P2: fix build with -Werror=format-security
- rebuilt against libjpeg v7

* Sun Dec 14 2008 Funda Wang <fwang@mandriva.org> 1.3.1-5mdv2009.1
+ Revision: 314133
- use ldflags when linking
- fix build with glibc 2.8

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Thierry Vignaud <tv@mandriva.org>
    - fix BR for x86_64
    - rebuild for new fltk
    - rebuild for new fltk

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 1.3.1-3mdv2009.0
+ Revision: 218423
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Jan 21 2008 Funda Wang <fwang@mandriva.org> 1.3.1-3mdv2008.1
+ Revision: 155596
- rebuild against latest gnutls

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.3.1-2mdv2008.1
+ Revision: 149728
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Jun 28 2007 Adam Williamson <awilliamson@mandriva.org> 1.3.1-1mdv2008.0
+ Revision: 45329
- rebuild for 2008
- unversioned doc dir
- package lang files correctly
- fd.o icons
- clean up menu entry stuff
- new release 1.3.1
- Import flphoto



* Tue Aug 29 2006 Till Kamppeter <till@mandriva.com> 1.2-9mdv2007.0
- Rebuilt for libgphoto2 2.2.x generation.
- Added XDG menus.

* Sun May 14 2006 Stefan van der Eijk <stefan@eijk.nu> 1.2-8mdk
- rebuild for sparc

* Sun Jan 08 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.2-7mdk
- Rebuild

* Wed Nov 23 2005 Till Kamppeter <till@mandriva.com> 1.2-6mdk
- Rebuilt against openssl-0.9.8a.

* Mon Sep  5 2005 Till Kamppeter <till@mandrakesoft.com> 1.2-5mdk
- Avoid crash when setting custom ratio in crop dialog (patch 1).
- Use best print quality by default, normal quality has already
  easily visible pixelization (patch 2).

* Mon Apr  4 2005 Till Kamppeter <till@mandrakesoft.com> 1.2-4mdk
- Removed portuguese (pt) translation, it is unusable (bug 15199).

* Thu Mar 31 2005 Till Kamppeter <till@mandrakesoft.com> 1.2-3mdk
- Added "Requires: libgphoto-hotplug" (bug 15135).

* Thu Mar  3 2005 Till Kamppeter <till@mandrakesoft.com> 1.2-2mdk
- Set default directory for USB storage devices to /mnt/removable.

* Thu Nov 25 2004 Till Kamppeter <till@mandrakesoft.com> 1.2-1mdk
- Updated to 1.2.

* Tue Dec 16 2003 Till Kamppeter <till@mandrakesoft.com> 1.2-0.2mdk
- Set default directory for memory cards to /mnt/memory_card.
- Added "--camera" to flphoto call by dynamic desktop icon.

* Mon Dec 15 2003 Till Kamppeter <till@mandrakesoft.com> 1.2-1mdk
- Updated to 1.2rc1.

* Thu Oct  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1-2mdk
- fix deps

* Thu Sep 17 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-1mdk
- Updated to 1.1 final.
- Some spec file clean-up.

* Thu Sep 11 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.12mdk
- Changed icon to a digital photo camera icon (thanks to Fabian 
  Mandelbaum for the icon).

* Thu Sep  4 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.11mdk
- Updated to 1.1rc2.

* Thu Sep  3 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.10mdk
- Makefile patch to add forgotten installation for .po files, now
  the translations work.

* Thu Sep  3 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.9mdk
- Let FLPhoto come up when clicking on the camera icon on the desktop
- New icon

* Thu Sep  3 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.8mdk
- Updated to 1.1rc1.

* Thu Aug 28 2003 David Baudens <baudens@mandrakesoft.com> 1.1-0.7mdk
- Move menu entry used in task oriented menu in mandrake_desk

* Thu Jul 27 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.6mdk
- Rebuilt for libexif 0.5.10.
- Updated to CVS from 27/07/2003.

* Thu Jun 12 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.5mdk
- Rebuilt for GPhoto2 2.1.2.
- Updated to CVS from 12/06/2003.

* Fri Feb 21 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.4mdk
- Added entry for "What to do" menu.

* Fri Feb 21 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.3mdk
- Updated to CVS from 21/02/2003 (Bug fixes).
- Added hint that this is a GUI for GPhoto2 to the menu entry.

* Sat Feb  1 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.2mdk
- Corrected "Requires:" to "libexif8".

* Sat Feb  1 2003 Till Kamppeter <till@mandrakesoft.com> 1.1-0.1mdk
- Updated to CVS from 01/02/2003 (Internationalization).

* Sat Jan  4 2003 Till Kamppeter <till@mandrakesoft.com> 1.0-1mdk
- Updated to released version 1.0.

* Thu Dec 19 2002 Till Kamppeter <till@mandrakesoft.com> 0.9-1mdk
- Updated to released version 0.9.

* Thu Dec  5 2002 Till Kamppeter <till@mandrakesoft.com> 0.9-0.1mdk
- Initial release.
