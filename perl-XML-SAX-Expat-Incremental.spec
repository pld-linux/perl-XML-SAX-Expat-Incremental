#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	SAX-Expat-Incremental
Summary:	XML::SAX::Expat-Incremental - SAX2 driver for Expat (XML::Parser)
Name:		perl-XML-SAX-Expat-Incremental
Version:	0.04
Release:	0.2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	073448591f374103a124a4a2b26992a5
BuildRequires:	perl-XML-NamespaceSupport >= 0.03
BuildRequires:	perl-XML-Parser >= 2.27
BuildRequires:	perl-XML-SAX >= 0.03
BuildRequires:	perl(XML::SAX::Base) >= 1.00
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with autodeps} || %{with tests}
BuildRequires:	perl-XML-SAX-Expat
BuildRequires:	perl-Test-Exception
BuildRequires:	perl-Test-Distribution
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an implementation of a SAX2 driver sitting on top of Expat
(XML::Parser).
# FIXME

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
%{__perl} -MXML::SAX -e "XML::SAX->add_parser(q(XML::SAX::Expat))->save_parsers()"

%postun
if [ "$1" = "0" ]; then
	umask 022
	%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::SAX::Expat))->save_parsers()"
fi

%files
%defattr(644,root,root,755)
# %%doc Changes
%{perl_vendorlib}/XML/SAX/Expat/Incremental.pm
%dir %attr(755,root,root) %{perl_vendorlib}/XML/SAX/Expat
%{perl_vendorlib}/XML/SAX/Expat/Incremental.pm
%{_mandir}/man3/*
