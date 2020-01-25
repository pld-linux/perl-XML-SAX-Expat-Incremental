#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	XML
%define		pnam	SAX-Expat-Incremental
Summary:	XML::SAX::Expat::Incremental - non-blocking (incremental) parsing
Summary(pl.UTF-8):	XML::SAX::Expat::Incremental - nieblokująca (przyrostowa) analiza
Name:		perl-XML-SAX-Expat-Incremental
Version:	0.05
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	f6f4c46190510c23a4990ef5e3fc54b3
URL:		http://search.cpan.org/dist/XML-SAX-Expat-Incremental/
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
XML::SAX::Expat::Incremental is an XML::SAX::Expat subclass for
non-blocking (incremental) parsing, with XML::Parser::ExpatNB.

%description -l pl.UTF-8
XML::SAX::Expat::Incremental to podklasa XML::SAX::Expat do
nieblokującej (przyrostowej) analizy z użyciem XML::Parser::ExpatNB.

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
%dir %{perl_vendorlib}/XML/SAX/Expat
%{perl_vendorlib}/XML/SAX/Expat/Incremental.pm
%{_mandir}/man3/*
