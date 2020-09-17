
<h1>
<b>pydispo</b>
</h1>
<p> A Disposable Mailbox Powered by Pure-Python</p><br>

![language](https://img.shields.io/github/languages/top/aakash30jan/pydispo)
![Release](https://img.shields.io/github/v/release/aakash30jan/pydispo)
![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)
[![Tweet](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Faakash30jan%2Fpydispo)](https://twitter.com/intent/tweet?text=Wow%2C+check+this+out%21+%23pydispo+is+a+disposable+mailbox+powered+by+pure-%23python.+Avoid+%23spam+and+protect+your+%23privacy+with+pydispo.&url=https%3A%2F%2Fgithub.com%2Faakash30jan%2Fpydispo)

`pydispo` is a pure-pythonic way of managing disposable mailbox that allows users to create several disposable email addresses and receive emails on those. It can be directly used from the command line or imported as a python module for advanced usage. `pydispo` is platform-independent and uses python standard libraries, so if you have python installed you don't need to satisfy any additional dependencies. 

Optionally, `pydispo` can fetch attached files and there's also a provision to save emails as HTML.  By default, the emails are shown as text, optionally any standard web browser can be used to view the emails. Currently, it uses 1secmail API to receive emails, and soon it would support some other APIs.  If you want a bash-like implementation with some dependencies, please check the [tmpmail](https://github.com/sdushantha/tmpmail) script. 


## Installation
### Standalone 
Download the `pydispo` standalone script and make it executable
```bash
$ curl -L "https://git.io/pydispo" > pydispo && chmod +x pydispo
```

### PyPI
`pydispo` is also available as a python package from [https://pypi.org/project/pydispo/](https://pypi.org/project/pydispo/).
Download and install it as a system or environment package with pip
```bash
$ pip install pydispo
```

### Source
Alternatively, the `pydispo` package source tarball can be downloaded from [here](https://github.com/aakash30jan/pydispo/blob/master/pydispo-20.9a1.tar.gz?raw=true)

## Usage
```console
Usage: pydispo [-h] [-a] [-r] [-g] [-s] [-b BROWSER] [-e EMAIL] [id]

Positional arguments:
  id                    Check email with message ID (default shows mailbox)
Optional arguments:
  -h, --help            show this help message and exit
  -a, --attached        Download all attached files in the email
  -r, --recent          Check the recent email
  -g, --generate        Generate a new email address
  -s, --save            Save email in an HTML file
  -b, --browser         Browser to check the email in HTML
  -e, --email           Check mailbox of a particular email

```

### Examples
Generate a disposable email address
```console
$ pydispo -g
Generated: ma4x8pgolq@1secmail.org
```

Check the mailbox
```console
$ pydispo
Mailbox:  ma4x8pgolq@1secmail.org  Mails in Inbox: 1
Message ID       Sender                  Subject         Date
84784986         yourfriend@mail.com     About pydispo   2020-09-16 17:34:13
```

Check a particular email
```console
$ pydispo 84784986
ID:  84784986
To:  ma4x8pgolq@1secmail.org
From:  yourfriend@mail.com
Date:  2020-09-16 17:34:13
Subject:  About pydispo
Attachments:  ['pydispo_leaflet.pdf   (application/pdf)   0.2 MB ']
--------------------
Check this out
Cheers.
--------------------
```

Check the recent email
```console
$ pydispo -r
```

Check a particular email, get attached files, and save email as HTML 
```console
$ pydispo -a -s 84784986 
```

Check a particular email in a browser of choice
```console
$ pydispo 84784986 -b elinks
```

Check mailbox of another disposable email 
```console
$ pydispo -e g6cqog5utd@1secmail.net
```

## Issues:
Problems? Please raise an issue at "https://github.com/aakash30jan/pydispo/issues" and I will get back to you soon.
![Issues](https://img.shields.io/github/issues/aakash30jan/pydispo)  ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

## Why disposable emails?
To avoid SPAM. To protect your PRIVACY.  Lots of web pages, blogs, forums and services would ask you to register or provide email addresses to read comments, download content, or register account or profile. And a lot of them will use your private email address to send you spam. Disposable emails are perfect for any transaction where you want to improve your online privacy, like when you trade cryptocurrencies. These are also used by developers and testers for several time-saving reasons.
Read More : [How-To Geek](https://www.howtogeek.com/tips/protect-yourself-from-spam-with-free-disposable-email-addresses/) ,  [WIRED](https://www.wired.com/story/avoid-spam-disposable-email-burner-phone-number/) 

## Credits 
`pydispo` is a dependency-free, platform-independent replication of Siddharth's [tmpmail](https://github.com/sdushantha/tmpmail) bash-script and follows a usage pattern similar to it. 


## License
This work is licensed under a GNU General Public License Version 3 . [![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)



