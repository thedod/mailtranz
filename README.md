This is a simple script that can serve as the success/fail callbacks required for Tranzilla transactions.
[If you don't know what Tranzilla is, consider yourself lucky ;)]

It **should be served via SSL** (if Tranzilla sales/support/etc. tell you otherwise - *don't listen*. You can get sued by buyers for following that ill advice).

Essentially, what it does is mail the transaction details to the merchant (*not* to the buyer, at least at the moment).

This script is GPL licensed, so I hope Tranzilla would implement it (or something similar) on their own servers,
so that merchants can use Tranzilla from their non-SSL sites without risking the privacy of their buyers
(as *falsely* stated in their documentation).

#### To install

* Clone this into a web-accessible (via SSL) .htaccess-enabled folder and cd to that folder.
* `git submodule update --init` (to install pystache).
* `cp mtconf-example.py mtconf.py` and edit `mtconf.py` to your liking.
* At Tranzilla admin, provide the **SSL** urls that lead to `succes.cgi` and `fail.cgi` (both are symlinks to `mailtranz.py`, but script name affects functionality). Method should be POST.

P.S. If your site is *already* integrated with Tranzilla and you *don't* have SSL, please [contact me](https://swatwt.com/sod).
The privacy of your buyers is at risk.

KTHXBYE
