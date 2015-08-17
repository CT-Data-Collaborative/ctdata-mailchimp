import os
import sys
import requests
import json
import hashlib

class ListNotFoundError(Exception):
    def __init__(self):
        self.code = 200



class EmailAlreadyAddedError(Exception):
    def __init__(self):
        self.code = 314


class EmailDoesNotExistError(Exception):
    def __init__(self):
        self.code = 414


class EmailUnsubscribedError(Exception):
    def __init__(self):
        self.code = 430


class EmailPendingError(Exception):
    def __init__(self):
        self.code = 330


class MailChimpAPI(object):
    """Main class for MailChimp API 3.0 calls

    """

    api_key = ''
    api_root = ''
    default_http_method = 'GET'
    default_header_content = {}
    default_body_content = {}

    def __init__(self, apikey):
        super(MailChimpAPI, self).__init__()
        apikey = apikey
        parts = apikey.split('-')
        if len(parts) != 2:
            print "This doesn't look like an API Key: " + apikey
            print "The API Key should have both a key and a server name, separated by a dash, like this: abcdefg8abcdefg6abcdefg4-us1"
            sys.exit()
        self.api_key = apikey
        self.shard = parts[1]
        self.api_root = "https://" + self.shard + ".api.mailchimp.com/3.0/"


    def do(self, method, content=None, headers=None, http_method=None):

        request_body = self.default_body_content
        if content is not None:
            request_body.update(content)

        request_headers = self.default_header_content
        if headers is not None:
            request_headers.update(headers)

        if http_method is None:
            http_method = self.default_http_method

        request_url = self.api_root + method

        return self.do_request(http_method, request_url, request_headers, request_body)


    def do_request(self, http_method, url, headers, body):
        try:
            body = json.dumps(body)
        except (TypeError, ValueError):
            pass

        auth_data = ('apikey', self.api_key)
        if http_method.upper() == 'GET':
            r = requests.get(url, headers=headers, auth=auth_data)

        elif http_method.upper() == 'POST':
            r = requests.post(url, data=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'PATCH':
            r = requests.patch(url, data=body, headers=headers, auth=auth_data)

        else:
            raise Exception("Invalid request method")

        return self.handle_response(r)


    def handle_response(self, response):
        try:
            return response.json()
        except (ValueError, TypeError):
            return response.content


    def accountDetails(self):
        """Show account details for associated API Key"""
        return self.do('', http_method='GET')


    def getLists(self):
        """Show all lists"""
        return self.do('lists/')


    def getListsByName(self, list_name):
        """Look up for getting a specific list"""
        lists = self.getLists()['lists']
        for l in lists:
            if l['name'] == list_name:
                return l

        #else
        raise ListNotFoundError()


    def getMember(self, user_email):
        """Mailchimp API 3.0 uses MD5 hash of lowercase version of email"""

        m = hashlib.md5()
        m.update(user_email.lower())
        return m.hexdigest()

    def memberStatus(self, list_id, eid):
        """"Check status of a particular email for a given list

        The mailchimp 3.0 API stores the email address status in the 'status' slot.
        Possible values are:
           404 -> not on list
           subscribed -> on list and ready to be targeted
           unsubscribed -> used to be on list but since deactivated
           pending -> address requested to be added but hasn't confirmed subscription yet
           cleaned -> address bounced and has been removed
        """
        method = 'lists/' + list_id + '/members/' + eid
        return self.do(method, http_method='GET')['status']


    # Specific API Methods for subscribing and unsubscribing members
    def subscribeList(self, list_name, user_email, first_name, last_name):
        """Method for subscribing an email to a list

        Will first lookup the email address using MD5 hash value.
        :param str list_name: Plain language name of the list
        :param str user_email: Email address of user looking to subscribe
        :param str first_name: First name of user
        :param str last_name: Last name of user
        :return: The result of the api call.
        :rtyle: JSON
        :raises EmailAlreadyAddedError: if the email address is already associated with list
        """

        list_id = self.getListsByName(list_name)['id']

        email_id = self.getMember(user_email)
        email_status = self.memberStatus(list_id, email_id)

        if email_status == 'subscribed':
            raise EmailAlreadyAddedError()
        if email_status == 'pending':
            raise EmailPendingError()
        if email_status == 404:
            content = {'email_address': user_email, 'status': 'pending', 'merge_fields': {'FNAME': first_name, 'LNAME': last_name}}
            method = 'lists/' + list_id + '/members/'
            return self.do(method, content, http_method='POST')
        else:
            content = {'status': 'pending'}
            method = 'lists/' + list_id + '/members/' + email_id
            return self.do(method, content, http_method='PATCH')


    def unsubscribeList(self, list_name, user_email):
        """Method for unsubscribing an email from a list

        Will first lookup the email address using MD5 hash value.
        :param str list_name: Plain language name of the list
        :param str user_email: Email address of user looking to subscribe
        :return: The result of the api call.
        :rtyle: JSON
        :raises EmailDoesNotExistsError: if the email address has never been added
        :raises EmailUnsubscribedError: if the email address has already been unsubscribed
        """
        list_id = self.getListsByName(list_name)['id']
        email_id = self.getMember(user_email)
        email_status = self.memberStatus(list_id, email_id)

        if email_status == 404:
            raise EmailDoesNotExistError()
        elif email_status == 'unsubscribed':
            raise EmailUnsubscribedError()
        elif email_status == 'cleaned':
            raise EmailDoesNotExistError()
        else:
            content = {'status': 'unsubscribed'}
            method = 'lists/' + list_id + '/members/' + email_id
            return self.do(method, content, http_method='PATCH')
