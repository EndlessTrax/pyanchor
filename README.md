# PyAnchor

[![PyPI version](https://badge.fury.io/py/pyanchor.svg)](https://badge.fury.io/py/pyanchor)
![GitHub](https://img.shields.io/github/license/endlesstrax/pyanchor)

Dead links are an annoyance for websites with an extensive amount of content. A side from the
negative impact on SEO, dead links are an annoyance for any user that clicks on one.

PyAnchor is primarily for checking the HTTP response on all links on a page. You can integrate it
into your development workflow so that users never see a 404 in the first place.

## Install

> Requires Python 3.8 and above.

It is recommended that you install this package in a virtual or isoloated environment. The easiest way to do this 
is with pipx.

```shell
pipx install pyanchor
```

Alternatively, you can install it with pip into your virtual environment:

MacOS / Linux:

```shell
python3 -m pip install pyanchor
```

Windows:

```pwsh
python -m pip install pyanchor
```

## Using the CLI

The CLI can be invoked with the `pyanchor` command. A URL **must** be provided unless it's the help page.

To get the help page:

```shell
pyanchor --help
```

![Example Gif](/assets/example-help.gif)

Basic example for a single page:

> Note: all provided URLs must include a valid HTTP scheme.

```shell
pyanchor https://mysite.com/
```

![Example Gif](/assets/example-single-page.gif)

If you want to check all links on a website, and not just a single page, a `sitemap.xml` URL may be provided and 
flagged with `--sitemap`.

Example:

```shell
pyanchor https://mysite.com/sitemap.xml --sitemap
```

![Example Gif](/assets/example-sitemap.gif)

By default, successful requests are not printed to the terminal. To see all urls with a `200`
response add the `--verbose` flag.

```shell 
pyanchor https://mysite.com --verbose
```
![Example Gif](/assets/example-single-page-verbose.gif)

```shell
pyanchor https://mysite.com/sitemap.xml --sitemap --verbose
```

![Example Gif](/assets/example-sitemap-verbose.gif)

If you wish the output the results to a csv file, instead of to the terminal (default), then you may wish to use 
the `--output-csv` flag:

```shell
pyanchor https://mysite.com --output-csv output/path/to/file
```

## But wait, there's more...

To integrate PyAnchor into your application, you can import the `LinkResults` class. `LinkResults`
requires a URL.

Example:

```
>>> from pyanchor.link_checker import LinkResults
>>> r = LinkResults("https://mysite.com/")
>>> r.results
{200: ["https://mysite.com/about/", "https://mysite.com/contact/"], 500: ["https://mysite.com/doh!/"]}
```

As you can see the `results` attribute is a dictionary containing all response codes returned as a
dictionary key, with a list of URLs that achieve that response code as the dictionary value.

### Analyzing Links

PyAnchor give you the ability to use the `LinkAnalysis` class to check the links in a given URL for unsafe and obsolete attributes.

To check for obsolete attributes use the `obsolete_attrs` property:

```
>>> from pyanchor.link_checker import LinkAnalysis
>>> r = LinkAnalysis("https://mysite.com/")
>>> r.obsolete_attrs
{'/about/link-1': ['charset', 'rev'], '/about/link-2': ['name']}
```

Likewise you can check for unsafe linkes with `unsafe_attrs`:

```
>>> from pyanchor.link_checker import LinkAnalysis
>>> r = LinkAnalysis("https://mysite.com/")
>>> r.unsafe_attrs
{<a href="/about/link-4" target="_blank">Link 4</a>: True, <a href="/about/link-5" rel="noreferrer noopener" target="_blank">Link 5</a>: False}
```

Any link that **does not** include `rel="noopener"` when the `target` attribute is used will return `True`. As in, **it is True that this link is unsafe**. Therfore, links with appropriate attributes will return `False`.

## Feedback

If you find a bug, please [file an issue](https://github.com/EndlessTrax/pyanchor/issues).

If you have feature requests, please [file an issue](https://github.com/EndlessTrax/pyanchor/issues)
and use the appropriate label.

## Support

If you would like to show your support for the project, 
[you can sponsor me on Github](https://github.com/sponsors/EndlessTrax)? 🤓

## How to Contribute

Please **raise an issue before making a PR**, so that the issue and implementation can be discussed before you write any code. This will save you time, and increase the chances of your PR being merged without significant changes.

Please **make PR's on a new branch**, and _not_ on main/master.

Please **include tests** for any PR's that include code (unless current tests cover your code contribution).

Please **add documentation** for any new features or flags.

## Contributors

Thank you to:

- [Zingzy](https://github.com/Zingzy) for PR [#55](https://github.com/EndlessTrax/pyanchor/pull/55)
- [mrbazzan](https://github.com/mrbazzan) for PR [#25](https://github.com/EndlessTrax/pyanchor/pull/25)
- [Icelain](https://github.com/Icelain) for PR [#11](https://github.com/EndlessTrax/pyanchor/pull/11)
- [wevnasc](https://github.com/wevnasc) for PR [#8](https://github.com/EndlessTrax/pyanchor/pull/8)
- [muditshamz](https://github.com/muditshamz) for PR [#6](https://github.com/EndlessTrax/pyanchor/pull/6)
  