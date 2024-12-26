# United-domains.de simple rest api

## Why is this a thing?

A couple of days ago, I needed to transfer a domain to United-domains.de.
This domain contains more than 200 entries (several `A` and `AAAA` records).
From the old registrar I got the zonefile, but I would have to manually enter
**every** single entry of the zonefile. As you can imagine, this would have
been a tedious task that can be easily automated. Too bad that United-domains.de
does not provide a way to do bulk edits or an official RestAPI.

These is a very small collection of Python3 script that I used to save me time.

## How to use

- You need Python3

```console
pip install aiohttp
```

### Preparing the cookies & CSRF token

Because my account has 2FA enabled and I didn't want to solve that in the script
(I tried to save as much time as possible), the easiest way is to use the
cookies and CSRF from the browser session.

- log in with firefox (chrome does not have the following menu)
- open the dev tools and in the network tab select *XHR*
- Open the DNS setting of one of your domains (doesn't matter which)
- A new request is done, click on the request to see the request details
- under *response headers* make a right-click and select *Copy all*
- Open a new file with the text editor of your choice
- paste the copied content
- save the file as `/tmp/browser.json` or similar
- The `browser_request` argument of these command line tools expect
    the path to this file. You should not take long between this
    and calling the scripts, the sessions are short lived


## Disclaimer

Use this scripts at your own risk. I will not be held resposible for any damages
caused to your domains and/or your United-domains.de account because you are using
this scripts.

This repository exists for the purpose of documentation only!
