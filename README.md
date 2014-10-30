iPhone 6 Availability Crawler
=============================

> Crawler that will send you email notifications as soon as iPhone 6 becomes available for reservation in particular Apple Store. Currently works only with German stores, but can be easily extended. Why yet another notification service? It's damn fast, so more chances to actually reserve something!

**TL;DR**

    git clone git@github.com:MA3STR0/iPhone-6-availability-crawler.git
    cd iPhone-6-availability-crawler
    cp config.json.example config.json
    vim config.json   # edit config.json file to set up your nofitication preferences
    sudo pip install tornado
    python crawler.py

About
-----

Apple has a pretty poor availability of their new products in offline stores. To get a model of your choice it's best to reserve it online. This crawler will notify you per email as soon as an iPhone of particular color and memory option will becode avaiable for reservation. Then you have around 5 minutes to reserve it.
There are many online services that do the similar iphone6-notification thing, but none of them worked fast enough for me. So I created this standalone server. It's damn fast.

Currenlty works only for German stores, but this can be easily extended. Just send me a pull request or open up an issue and I will try add your country.

Set it up
---------

_Following steps have been tested on Mac and Linux_

- Clone this repo (`git clone git@github.com:MA3STR0/iPhone-6-availability-crawler.git`) or download and unpack archive
- Taking `config.json.example` as a template, create a file `config.json` and correct configuration according to your preferences:
  - `from_email`, `from_pwd`, `from_smtp_host`, `from_smtp_port`: email account configuration that crawler should use for sending notifications
  - `to_email`: your email, will be used as a recipient of notifications
  - `products`: list of Apple products you are interested in. Currenlty can be `["iphone6", "iphone6plus"]`
  - `colors`: color option to track, `["silver", "gold", "spacegray"]`
  - `memory`: memory option to track, `["16gb", "64gb", "128gb"]`
  - `stores`: names of stores to track, eg `["altmarkt-galerie"]`. Look for options here: [https://reserve.cdn-apple.com/DE/de_DE/reserve/iPhone/availability]

- Crawler runs on Python 2.7-3.4 and tornado framework, assuming that you already have Python/pip, just get tornado with `sudo pip install tornado`. You can also set up virtual-env if you like.
- Run with `python crawler.py`
- Get availability notifications and react quickly
- Enjoy your new iPhone
