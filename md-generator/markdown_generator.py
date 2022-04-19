#
# Copyright (c) 2022 Software AG, Darmstadt, Germany and/or its licensors
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from mdutils.mdutils import MdUtils
from datetime import datetime, timezone
from tc_client import TechCommunityClient

class MarkdownGenerator():

    def __init__(self):
        self.cat_list = []
        self.tc_client = TechCommunityClient()

    def read_md_file(self):
        file = self.mdFile.read_md_file('./README.md')
        return file

    def create_md_file(self, repos):

        repos = self.filter_repo_list(repos)

        mdFile = MdUtils(file_name='../README.md', title='Cumulocity IoT Open-Source Repository Overview')
        # mdFile.new_header(level=1, title='Cumulocity IoT Open-Source Repository Overview')
        mdFile.new_paragraph(
            "This Repository generates on a daily basis a Table of all Open-Source Repositories for Cumulocity-IoT "
            "having the topic 'cumulocity-iot'. It should give a brief overview of all available IoT Open-Source "
            "Repositories for Cumulocity IoT including additional content at TechCommunity.")

        mdFile.new_paragraph("Please use this [link](https://github.com/SoftwareAG/cumulocity-os-repo-overview/blob/main/README.md) to have a proper view on the table.")
        mdFile.new_paragraph(
            "Number of Open-Source Repos: **" + str(len(repos)) + "**")
        mdFile.new_header(level=1, title='Open-Source Repository Table')
        list = self.build_table_list(repos)
        mdFile.new_table(9, len(repos) + 1, list)
        mdFile.create_md_file()

    def filter_repo_list(self, repos):
        filtered_list = []
        for repo in repos:
            if repo['visibility'] == 'public':
                if "cumulocity" in repo['name'] or "c8y" in repo['name'] or "cumulocity-iot" in repo[
                    'topics'] or "cumulocity" in repo['topics']:
                    filtered_list.append(repo)
        filtered_list = sorted(filtered_list, key=lambda d: d['stargazers_count'], reverse=True)
        return filtered_list

    def build_table_list(self, repos):
        text_list = ['Repo Name', 'Description', 'Category', 'Topics', 'Language', 'Last Updated', 'Stars',
                     'References', 'Relation']
        for repo in repos:

            name = repo['name']
            desc = repo['description']
            topics = repo['topics']
            cat_list = []
            cat = '-'
            if 'cumulocity-microservice' in topics or 'microservice' in name or 'microservice' in topics:
                cat = 'Microservice'
                cat_list.append(cat)
            if 'cumulocity-widget' in topics or 'widget' in name or 'widget' in topics or 'widgets' in topics:
                cat = 'Widget'
                cat_list.append(cat)
            if 'cumulocity-webapp' in name or 'cumulocity-webapp' in topics or 'webapp' in name or 'webapp' in topics:
                cat = 'WebApp'
                cat_list.append(cat)
            if 'cumulocity-agent' in name or 'cumulocity-agent' in topics or 'agent' in name or 'agent' in topics:
                cat = 'Agent'
                cat_list.append(cat)
            if 'cumulocity-example' in topics or 'example' in name or 'example' in topics:
                cat = 'Example'
                cat_list.append(cat)
            if 'cumulocity-client' in topics or 'client' in name or'api' in name or 'api' in topics:
                cat = 'Client'
                cat_list.append(cat)
            if 'cumulocity-simulator' in topics or 'simulator' in name or 'simulator' in topics:
                cat = 'Simulator'
                cat_list.append(cat)
            if 'cumulocity-tutorial' in topics or 'tutorial' in name or 'tutorial' in topics:
                cat = 'Tutorial'
                cat_list.append(cat)
            if 'cumulocity-extension' in topics or 'extension' in topics or 'remote-access' in name or 'remote-access' in topics:
                cat = 'Extension'
                cat_list.append(cat)
            if 'cumulocity-cli' in topics or 'cli' in topics:
                cat = 'CLI'
                cat_list.append(cat)
            self.cat_list = cat_list
            if len(cat_list) > 0:
                cat = " <br> ".join(str(cat) for cat in cat_list)
            else:
                cat = 'Other'
            if len(topics) > 0:
                topic_string = " ".join(str(topic) for topic in topics)
            else:
                topic_string = '-'
            lang = repo['language']
            last_updated = repo['pushed_at']
            date_time_obj = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
            date_string = date_time_obj.strftime('%Y-%m-%d %H:%M:%S %Z')
            stars = repo['stargazers_count']
            url = repo['html_url']
            tc_references = self.tc_client.get_all_entries_for_repo(url)
            if tc_references:
                references_string = " ".join('['+reference['title']+']('+reference['topic_url']+') <br>' for reference in tc_references)
            else:
                references_string = '-'
            owner = repo['owner']['login']
            if owner == 'SoftwareAG':
                relation = 'SAG-Org Repo'
            elif owner == 'reubenmiller' or owner == 'TryManuZ':
                relation = 'Trusted-Contributor Repo'
            else:
                relation = 'Open-Source Repo'
            # relation = 'SAG-Org Repo'
            text_list.extend(["[" + name + "](" + url + ")", desc, cat, topic_string, lang, date_string, stars, references_string, relation])
        return text_list
