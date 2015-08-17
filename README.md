# MailChimp Integration

This is a reinterpretation of the Aldryn Mailchimp [plugin](https://github.com/aldryn/aldryn-mailchimp). Changes were made to limit functionality to just the subscribe and unsubscribe functions that we want to offer to our members.

The `pyrate` api, upon which Aldryn's functionality was built, is only compatible with MailChimp 2.0. A significant re-write was required to conform with the 3.0 API conventions.

To activate MailChimp integration:

* Set an `API Key` via an environmental variable
* create an CMS page for hooking the app (navigate to ``Advanced Settings -> Application`` on CMS edit page)

When all above is done, you can add the Subscribe and Unsubscribe plugins to pages.
