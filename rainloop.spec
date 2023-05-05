Name:           rainloop
Version:        1.14.0
Release:        1%{?dist}
Summary:        Simple, modern & fast web-based email client.
License:        AGPLv3+
Group:          Networking/WWW
URL:            http://rainloop.net
Source:         https://github.com/Rainloop/rainloop-webmail/releases/download/v%{version}/%{name}-community-%{version}.zip
Requires:       httpd
Requires:       php
#Requires:       php-mysql
#Requires:       php-ldap
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python
BuildArch:      noarch

%description
RainLoop Webmail
Simple, modern & fast web-based email client. Modest system requirements,
decent performance, simple installation and upgrade, no database required -
all these make RainLoop Webmail a perfect choice for your email solution.

%prep
rm -rf %{name}-%{version}
#mkdir %{name}-%{version}
#cd %{name}-%{version}
#unzip %{SOURCE0}
%setup

%build
# Nothing to do!!

%install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r * %{buildroot}%{_datadir}/%{name}

# apache configuration
install -d -p %{buildroot}%{_sysconfdir}/httpd/conf.d
cat <<EOF >%{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
# rainloop configuration

Alias /%{name} %{_datadir}/%{name}

# Redirect to https
RewriteEngine On
RewriteRule ^/%{name}(/.*)?$  https://%{HTTP_HOST}/%{name}$1  [L,R=301]

<Directory %{_datadir}/%{name}>
    Require all granted
    php_admin_value post_max_size 25M
    php_admin_value upload_max_filesize 25M
</Directory>
<Directory %{_datadir}/%{name}/data>
    Require all denied
</Directory>
EOF

%files
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/data
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf

%post
/usr/sbin/semanage fcontext -a -t httpd_sys_rw_content_t '%{_datadir}/%{name}/data(/.*)?' 2>/dev/null || :
/usr/sbin/restorecon -R %{_datadir}/%{name} || :
/sbin/service httpd condrestart > /dev/null 2>&1 || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
  /usr/sbin/semanage fcontext -d -t httpd_sys_rw_content_t '%{_datadir}/%{name}/data(/.*)?' 2>/dev/null || :
fi
/sbin/service httpd condrestart > /dev/null 2>&1 || :

%changelog
* Tue Jun 02 2020 Glen Johnson <gfjohnson@redwain.com> 1.14.0-el7
- upstream to 1.14.0

* Thu Aug 22 2019 Glen Johnson <gfjohnson@redwain.com> 1.13.0-el7
- support selinux
- upstream to 1.13.0

* Sun Sep 02 2018 stephane de labrusse <stephdl@de-labrusse.fr> 1.12.1-el7
- upstream upgrade

* Thu May 10 2018 stephane de Labrusse <stephdl@de-labrusse.fr> 1.12.0-el7
- First release of rainloop
