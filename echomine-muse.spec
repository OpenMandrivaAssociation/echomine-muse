%define gcj_support 1
%define section free

Name:           echomine-muse
Version:        0.81
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Java API for XMPP/Jabber
License:        GPL
Group:          Development/Java
URL:            http://open.echomine.org/confluence/display/MUSE/Muse+Home
Source0:        http://download.berlios.de/muse/muse-0.81.tar.gz
Patch0:         muse-0.81-file-compare-to.patch
Requires:       jakarta-commons-logging
Requires:       jdom
Requires:       xpp3
BuildRequires:  ant
BuildRequires:  jakarta-commons-logging
BuildRequires:  jdom
BuildRequires:  xpp3
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Echomine Muse provides an easy-to-use Java API that gives you quick
and easy yet powerful access to network collaboration services.
Specifically, it allows you to communicate with XMPP/Jabber servers
to perform instant messaging and presence management in a secure
and real-time environment.

%package javadoc
Summary:        Javadoc documentation for muse
Group:          Development/Java

%description javadoc
Javadoc documentation for muse.

%prep
%setup -q -c
%patch0 -p0
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}

%build
export CLASSPATH=$(build-classpath jakarta-commons-logging jdom xpp3)
export OPT_JAR_LIST=:
%{ant} jar javadocs

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a work/muse.jar %{buildroot}%{_javadir}/muse-%{version}.jar
%{__ln_s} muse-%{version}.jar %{buildroot}%{_javadir}/muse.jar

%{__mkdir_p} %{buildroot}%{_javadocdir}/muse-%{version}
%{__cp} -a work/docs/api/* %{buildroot}%{_javadocdir}/muse-%{version}
%{__ln_s} muse-%{version} %{buildroot}%{_javadocdir}/muse

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc examples license
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/muse-%{version}
%doc %{_javadocdir}/muse
