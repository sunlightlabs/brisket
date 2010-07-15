
### Lobbying Methodology ###

This document describes the process we use to compute aggregate information from quarterly lobbying reports. It would be helpful to first read the [campaign finance methodology][5] section, as many of the issues there apply to lobbying data as well. The information provided in these two documents should be detailed enough to allow a dedicated user to reproduce the figures in Influence Explorer using the underlying data provided in [Transparency Data][1].


#### Background ####

Any organization that lobbies congress, or hires a firm to lobby on its behalf, is required to register with both the [Senate Office of Public Records][2] (SOPR) and the [House Office of the Clerk][3]. Registrants file quarterly reports, listing information such as the individual lobbyists involved and the issues and bills lobbied on. Firms that lobby on behalf of clients report each client separately, along with the amount the firm was paid for lobbying. Organizations that lobby on their own behalf ("in-house lobbying") report the total amount spent on their lobbying efforts. In either case, disclosure rules require the filer to report dollar amounts to the nearest $20,000. Spending or income under $10,000 may be reported as $0.  

Our partner organization for lobbying data, [Center for Responsive Politics][4] (CRP), cleans the data from SOPR, and standardizes the names of individuals and organizations to be consistent with CRP's campaign finance data sets. Details on CRP's methodology can be found [here][7]. The Sunlight Foundation combines CRP's lobbying data with other data sets and makes it easily accessible through the Transparency Data website and APIs. The format for the underlying lobbying records is described in the [Transparency Data documentation][6].


#### Summing Lobbying Reports ####

Influence Explorer provides three different views of the lobbying data. Individual lobbyists have one view. Organizations display one of two possible views, depending on whether or not the organizations is primarily a lobbying firm (as determined by the `registrant_is_firm` field.)

- Organizations that are primarily lobbying firms display the total amount *earned* through lobbying. This is simply the total over all records where the firm is listed as the registrant. Top clients, lobbyists and issues are also computed by matching on the firm as a registrant.
- Organizations that are not primarily lobbying firms display the total amount *spent*. This information is encoded in the database in a somewhat unintuitive manner: reports that list the same organization as both the registrant and the client are actually reports of total spending by the organization. Summing the amounts gives the total spent. Some organizations do not file as registrants at all, and are only listed as clients of lobbying firms. In this case, the sum of the reports listing the organization as a client is used as the total spent. Top firms, lobbyists, and issues tables are computed by matching against records that have the organization listed as a *client*.
- Individual lobbyist are not associated directly with dollar amounts. Instead we list the top registrant and client firms, as well as the top issues, that appear in reports listing that lobbyist.


In all of these cases it is important to use only the most up-to-date records, since reports are often amended after first submission. *To do: I wanted to say here that you have to include only records where CRP's 'Ind' field is true. But code is actually checking that the 'use' field is true. I'm confused about which is right--I went back and forth on this about a month ago, and can't remember how I arrived at what's there now.*












[1]: http://transparencydata.com
[2]: http://www.senate.gov/pagelayout/legislative/g_three_sections_with_teasers/lobbyingdisc.htm
[3]: http://clerk.house.gov/public_disc/index.html
[4]: http://opensecrets.org
[5]: /about/methodology/campaign_finance/
[6]: http://transparencydata.com/docs/lobbying/
[7]: http://www.opensecrets.org/lobby/methodology.php
