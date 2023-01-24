# CS50W - Web Programming with Python and JavaScript
## Commerce

https://cs50.harvard.edu/web/2020/projects/2/commerce/

This is my implementation of the third project in the CS50w course – a simple Django-powered eBay-like online auction site.

![screenshot_1](https://i.ibb.co/pwLGJjg/aa1.png)
### Requirements
Required Python packages are listed in `requirements.txt` file.

### Usage
The default route of this app lets users view all of the currently active auction listings. Clicking on a listing takes users to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price.

Signed-in users can then bid on the item, leave a comment or add/remove the listing from their watchlist. 

They can also create a new listing – specify a title, a text-based description, what the starting bid should be, and optionally specify a category and/or provide a URL for an image; or they can close their listings, which makes the highest bidder the winner of the auction.

![screenshot_2](https://i.ibb.co/wRRg2Dp/aa2.png)

