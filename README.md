# PyAnchor (Latest: 0.1.5)

Dead links are an annoyance for websites with an extensive amount of content. A side from the
negative impact on SEO, dead links are an annoyance for any user that clicks on one.

PyAnchor is primarily for checking the HTTP response on all links on a page. You can integrate it
into your development workflow so that users never see a 404 in the first place.

## Install

PyAnchor requires Python 3.6 and above.

MacOS / Linux:

```shell
$ python3 -m pip install pyanchor
```

Windows:

```cmd
> python -m pip install pyanchor
```

## Using the CLI

The CLI can be invoked with the `pyanchor` command. A URL must be provided.

Basic example for a single page:

```shell
> pyanchor https://mysite.com/
```

> Note: all provided URLs must include a valid HTTP scheme.

If you want to check all links on a website, and not just a single page, a `sitemap.xml` URL may be
provided and flagged with `--sitemap`.

Example:

```shell
> pyanchor https://mysite.com/sitemap.xml --sitemap
```

## But wait, there's more...

To integrate PyAnchor into your application, you can import the `LinkResults` class. `LinkResults`
requires a URL.

Example:

```
>>> from pyanchor.link_checker import LinkResults
>>> r = LinkResults("https://mysite.com/")
>>> r.results
{"https://mysite.com/about/": 200, "https://mysite.com/contact/": 200, "https://mysite.com/blog/": 200, ...}
```

As you can see the `results` attribute is a dictionary containing all links with their HTTP response
code.

## What's next?

The plan for PyAnchor is to add further analysis of anchor tags, such as missing attributes and
security considerations.

After that... who knows? 🤷‍♂️

## Feedback

If you find a bug, please [file an issue](https://github.com/EndlessTrax/pyanchor/issues).

If you have feature requests, please [file an issue](https://github.com/EndlessTrax/pyanchor/issues)
and use the appropriate label.

## Support

If you would like to show your support for the project, I would be very grateful if you would donate
to a charity close to my heart, [Walk AS One](https://walkasone.org/donate/).

And if you would prefer to donate to me personally instead,
[buy me a coffee](https://ko-fi.com/endlesstrax)? 🤓
