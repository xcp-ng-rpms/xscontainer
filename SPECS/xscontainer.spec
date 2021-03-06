Name:    xscontainer
Version: 10.0.4
Release: 1%{?dist}
Summary: XenServer Container Manager
License: BSD
Source0: https://code.citrite.net/rest/archive/latest/projects/xsu/repos/xscontainer/archive?at=deae3969b8b6908410429c274373b4a8e8e3a9d0&format=tar.gz#/%{name}-%{version}.tar.gz
Source1: 80-xscontainer.preset
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: systemd-devel

Requires: python-paramiko
Requires: mkisofs


%description
xscontainer is the back-end of XenServer's Container Management.


%prep
%autosetup -p1 -c


%build
make


%install
python2 setup.py install -O2 --skip-build --root=%{buildroot}
install -d -m 755 %{buildroot}/%{_presetdir}
install -m 644 %{SOURCE1} %{buildroot}/%{_presetdir}


%post
%systemd_post xscontainer-monitor.service

# Start the monitor service if we're running in a real XenServer environment
# and it has not been explicitly disabled.
if systemctl is-active xapi.service 2>&1 > /dev/null && \
   systemctl is-enabled xscontainer-monitor.service 2>&1 > /dev/null; then
    systemctl start xscontainer-monitor.service
fi


%preun
%systemd_preun xscontainer-monitor.service


%postun
%systemd_postun_with_restart xscontainer-monitor.service


%files
%{_bindir}/*
%{_sysconfdir}/xensource/bugtool/*
%{_sysconfdir}/xapi.d/plugins/*
%{python_sitelib}
%{_unitdir}/*
%{_presetdir}/*


%changelog
