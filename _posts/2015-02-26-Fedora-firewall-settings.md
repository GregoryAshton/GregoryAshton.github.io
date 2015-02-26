---
layout: post
title: Fedora firewall settings
tags:
- Fedora
- Setup
---

I experienced issues connecting to various networks and vpn's when using Fedora
21. This was fixed by advise from [ask.fedoraproject](https://ask.fedoraproject
.org/en/question/62909/cant-connect-to-vpn-on-fedora-21/). I will repeat the
fix here since I suspect I may run into this error again and I have a terrible
memory!

    $ ll-cmd --direct --add-rule ipv4 filter INPUT 0 -p gre -j ACCEPT
    $ firewall-cmd --direct --add-rule ipv6 filter INPUT 0 -p gre -j ACCEPT
    $ firewall-cmd --reload
