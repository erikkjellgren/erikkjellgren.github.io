---
layout: post
title: Overlap between Danish investment funds
lang: en
lang-ref: overlap of danish funds
tag: dkfinance
---

Given the selection of Danish investment funds from [Sparindex](https://sparindex.dk/) and [Danske Invest](https://www.danskeinvest.dk/w/show_pages.front?p_nId=75),
it can be difficult to see how different the funds are.

As a measure of similarity, one can calculate the overlap between two funds.
The overlap between fund $$ A $$ and fund $$ B $$ will be calculated as:

$$ S_{AB} = \sum_{i} \sqrt{w_{A, i} \cdot w_{B, i}} $$

Here, $$ w_{A, i} $$ is the weight of stock $$ i $$ in fund $$ A $$.
This metric has the property that it is equal to $$ 1 $$ if the two funds are identical and $$ 0 $$ if the two funds do not contain any of the same shares.

## Processing of the data
The data for the holdings of the funds is taken directly from [Sparindex](https://sparindex.dk/) and [Danske Invest](https://www.danskeinvest.dk/w/show_pages.front?p_nId=75).
The raw retrieved data can be found here: [danish_funds_assets](https://github.com/erikkjellgren/erikkjellgren.github.io/tree/main/assets/python_scripts/data/danish_funds_assets).

In order for two funds assets to be matched, all the assets must be given an unique identification, for which Yahoo-Finance ticker was choosen to identify the assets.
This was done by simplifying the names i.e. remove *LTD*, *A/S*, etc. and search via. an [Yahoo-Finance query](https://query2.finance.yahoo.com/v1/finance/).
This method has the advantage that A- and B-shares will be given the same ticker, and that tickers will also origin stock exchange for a given company.
This avoids artificially low overlap if the funds buys the (same) shares from different stock exchanges.

The script for retrieving data from Yahoo-Finance can be found here: [get_yahoo_tickers.py]({{site.baseurl}}/assets/python_scripts/get_yahoo_tickers.py)

Share names with assigned tickers can be found here: [name2yahooticker.txt]({{site.baseurl}}/assets/python_scripts/data/name2yahooticker.txt)

For some of the shares a ticker could not be assigned via. the method described above. These tickers were assigned manually. The list for these can be found here: [manual_added_name2yahooticker.txt]({{site.baseurl}}/assets/python_scripts/data/manual_added_name2yahooticker.txt)

Some of the stocks were not assigned a ticker. A list of those can be found here: [notfound_name2yahooticker.txt]({{site.baseurl}}/assets/python_scripts/data/notfound_name2yahooticker.txt)


## Overlap of the funds

The calculated overlap of the funds can be seen in the figure below.
It should be noted that the accumulating funds that have a distributing version are excluded from the figure.

<p align = "center">
<img src = "{{site.baseurl}}/assets/plots/overlap_of_danish_funds.svg">
</p>

In the figure above, the fund names can be difficult to read.
The figure can be seen in large: [Overlap Funds Large Figure]({{site.baseurl}}/assets/plots/overlap_of_danish_funds.svg)

Version of the figure that is colorblind friendly can be found here: [Colorblind Version Large Figure]({{ site.baseurl }}/assets/plots/overlap_of_danish_funds_colorblind_friendly.svg)

The Funds are clustered via [linkage](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html)
The script for figure can be found here: [overlap_of_danish_funds.py]({{site.baseurl}}/assets/python_scripts/overlap_of_danish_funds.py)

One can clearly see the expected structure with groups such as Europe, Denmark, Japan and emerging markets.
It is worth noting that the USA and the global fund in general has a very large overlap.

It is also worth noting that Danske Invest has many funds that are almost identical!
