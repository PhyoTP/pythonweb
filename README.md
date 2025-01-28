# PhyoAPI
![logo](phyoapi.png)<br>
this is my backend for:
## PhyoID
a user management system for my apps (and future websites) Multicards and Academ<br>
website: https://auth.phyotp.dev
### Usage
base url is `api.phyotp.dev/phyoid`. If JWT token is required, it has to be in the Authorisation header as Bearer `JWT token`.
#### /register (POST)
Registers a new user and returns a JWT token.
#### /login (POST)
Logs in a user and returns a new JWT token.
#### /update/`data` (PATCH)
Updates the specified data. JWT required.
#### /userdata (GET)
Returns user data. Specific data can be specified by using `/userdata/<data>`. JWT required.
#### /refresh (POST)
idk how to use this
#### /delete (POST)
Deletes user. Password **and** JWT token are required, so password has to be in the body.
## Multicards
a database for public sets. find out more at https://github.com/PhyoTP/Multicards<br>
website: https://multicards.phyotp.dev
## StickyNotes
the webscraping and coupon finding part of [Sticky Notes](github.com/PhyoTP/StickyNotes)
