""" Obtains a list of the user emails from the provided github.io HTML files. """

from bs4 import BeautifulSoup
import json
import re
import os


def get_user_emails(site_dir='github_site_data'):
    """ Obtains a list of user emails and then dumps them
        into a JSON file.

        Args:
            site_dir: The directory containing site information,
                default github_site_data
    """
    c_dir = os.getcwd()
    html_dir = os.path.join(c_dir, site_dir)
    email_regex = '[^@]+@[^@]+\\.[^@]+'
    email = 'email'
    name = 'name'
    json_obj = list()

    for _, _, files in os.walk(html_dir):
        for file in files:
            if 'INVALID' not in file:
                # Valid HTML: parse it!
                user_dict = dict()

                full_path = os.path.join(html_dir, file)
                with open(full_path, 'rb') as html_read_file:
                    soup = BeautifulSoup(html_read_file, 'html.parser')
                    html_read_file.close()

                for title in soup.find_all('title'):
                    # Find all titles to get user's name
                    user_dict[name] = title.text
                    break # Only get first <title> element

                for link in soup.find_all('a'):
                    # Look in <a> tag for mailto: regex
                    href = link.get('href')
                    if href:
                        matches = re.findall(f'mailto:{email_regex}', href)
                        if matches:
                            user_dict[email] = matches[0].replace('mailto:', '')
                            break # Only use first mailto
                if not email in user_dict.keys() and name in user_dict.keys():
                    user_dict[email] = 'not found'
                json_obj.append(user_dict)
        break # Prevent subdirectory descent
    json_path = os.path.join(c_dir, 'emails.json')
    with open(json_path, 'w') as json_write_file:
        json.dump(json_obj, json_write_file)
        json_write_file.close()

get_user_emails()