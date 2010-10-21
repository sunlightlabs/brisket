### Campaign Finance Methodology ###

This document describes the process we use to compute aggregate information from single contributions. The information provided in this document should be detailed enough to allow a dedicated user to reproduce the figures in Influence Explorer using the underlying data provided in [Transparency Data][1].


#### Background ####

In order to understand the complexities involved in processing campaign finance data it's important to understand the steps the data goes through to reach Transparency Data. At the federal level, when individuals or organizations give to a politician or a political action committee (PAC), the recipient asks the donor to provide information such as name, address, occupation and employer. Federal campaign finance disclosure laws require the recipient to report any contribution over $200 to the Federal Election Commission (FEC). The FEC releases this information to the public in the form of a large database dump. The FEC makes no attempt at data cleanup or standardization, making the raw data very difficult to use effectively. 

Our partner organization for federal data, [Center for Responsive Politics][2] (CRP), goes to great lengths to clean the FEC data, standardize names, and assign unique identifiers to some individuals and organizations. A similar process happens in each of the 50 states, with varying disclosure rules in each. Our partner organization for state-level data, [National Institute for Money in State Politics][3] (NIMSP), combines and standardizes this data across all 50 states. The Sunlight Foundation combines these and other data sets and makes them easily accessible through the Transparency Data website and APIs. The format for the underlying contribution records is described in the [Transparency Data documentation][7].


#### Matching Entities with Contributions  ####

An 'entity' is any individual, organization or politician with a page in Influence Explorer. Every entity is identified by a name, and sometimes also by a unique identifier from one of our partner organizations. To find contributions that an entity was involved in, we search the database for records with matching names or IDs. 

Organizations have an additional level of complexity, in that they may be a subsidiary of a larger organization. In this case we associate the contribution with *both* the organization and the parent organization. This is an imperfect solution and can lead to strange results, such as when the Top Contributors table for a politician lists a company and its parent company, when there was really only one set of contributions. 


#### Summing Contributions between Entities  ####

The campaign finance data includes records for many sorts of transactions other than a typical donation to a politician. Some examples include transfers between party and politician committees, independent expenditures for or against a candidate, or transfers of money from one election cycle to another. When we talk about the amount of money raised by a politician, or the amount of money a certain industry gave, we want to include only straightforward contributions from an individual or organization to a politician or PAC. 

In deciding what contributions to include, we attempt to follow the methodology of CRP and NIMSP:

* For federal contributions from individuals, we only count contributions with an FEC transaction type of 11, 15, 15e, 15j, or 22y.
* For federal contributions from organizations, we only count contributions with an FEC transaction type of 24k, 24r or 24z.
* For state contributions, we ignore all contributions with a category code of Z2100, Z2200, Z2300, Z2400, Z7777, Z8888, Z9010, Z9020, Z9030, Z9040, Z9100, Z9500, Z9600, Z9700, or Z9999.

For an admittedly cryptic guide to FEC codes see [here][4] and [here][5]. For a list of category codes see [here][6].


#### What Could Go Wrong ####

Say we're trying to find the total amount of money that 'Acme Widget Crop' gave to 'John Smith'. There are a number of ways in which our calculations could be inaccurate:

* If either the contributor or recipient name is written in a non-standard way, then the contribution will be missed. Contributions from 'John P Smith' or to 'Acme Widgets', for example, might not be included. CRP and NIMSP go to great effort to standardize names, but they are far from covering all of the 40+ million records in the database.
* If a different real-world entity shares the same name, then those contributions will be erroneously included. This is especially problematic for common names, such as in this example.
* If there has been a name change over time, the previous names will not be included. This applies mostly to organizations, which undergo mergers, acquisitions, and name changes, but also to individuals who change their names through marriage or divorce.
* Contributions under $200 are never reported to the FEC, and so aren't included in our totals.
* The data may simply be missing or inaccurate. For a contribution record to reach us, the contributor must disclose their name and employer, the recipient must report it to the FEC or state agency, and then the record must pass through various formats and databases from the government, to our partner organizations, and on to us.


#### Why Don't Influence Explorer Totals Match the Totals on OpenSecrets and FollowTheMoney? ####

Given that Influence Explorer is built on data from CRP and NIMSP, it is reasonable to expect that the figures on the sites would exactly match. Unfortunately this is often not the case, for a variety of reasons:

* Our numbers include both state and federal data, whereas OpenSecrets is only federal data and FollowTheMoney is primarily state data.
* The data may be out of sync. The bulk databases provided to us by CRP and NIMSP are not necessarily the same version of the data that appears on their websites. The data they provide us may be newer or older, depending on when they last updated a particular page.
* OpenSecret's Heavy Hitters pages are based on a large amount of manual research to overcome the shortcomings listed in the section above. We do not have access to this research, and their numbers are likely to be more accurate than ours for organization on the Heavy Hitters list. (See CRP's Heavy Hitters [methodology page][8].)
* The time span may be different. Pages on OpenSecrets may display career totals, 6-year senate term totals, 2-year election cycles totals, or single-year totals. Influence Explorer groups all data into either 2-year cycles or career totals.
* We have made a best-effort attempt to match the methodology of our data providers. But there may still be unintentional methodology differences. The algorithms for importing, storing and working with this data are complex, and our systems cannot be guaranteed to function in exactly the same way in every case.


[1]: http://transparencydata.com
[2]: http://www.opensecrets.com
[3]: http://www.followthemoney.org
[4]: http://www.fec.gov/finance/disclosure/ftpdet.shtml
[5]: ftp://ftp.fec.gov/FEC/indiv_dictionary.txt
[6]: http://assets.transparencydata.org.s3.amazonaws.com/docs/catcodes-20100402.csv
[7]: http://transparencydata.com/docs/contributions/
[8]: http://www.opensecrets.org/orgs/methodology.php

