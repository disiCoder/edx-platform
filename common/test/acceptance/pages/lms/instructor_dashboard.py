# -*- coding: utf-8 -*-
"""
Instructor (2) dashboard page.
"""

from bok_choy.page_object import PageObject
from .course_page import CoursePage
import os


class InstructorDashboardPage(CoursePage):
    """
    Instructor dashboard, where course staff can manage a course.
    """
    url_path = "instructor"

    def is_browser_on_page(self):
        return self.q(css='div.instructor-dashboard-wrapper-2').present

    def select_membership(self):
        """
        Selects the membership tab and returns the MembershipSection
        """
        self.q(css='a[data-section=membership]').first.click()
        membership_section = MembershipPage(self.browser)
        membership_section.wait_for_page()
        return membership_section

    def select_data_download(self):
        self.q(css='a[data-section=data_download]').first.click()
        data_download_section = DataDownloadPage(self.browser)
        data_download_section.wait_for_page()
        return data_download_section


class MembershipPage(PageObject):
    """
    Membership section of the Instructor dashboard.
    """
    url = None
    cohort_csv_browse_button_selector = '.cohort-management .csv-upload input.file_field'
    cohort_csv_upload_button_selector = '.cohort-management .csv-upload button.submit-file-button'

    def is_browser_on_page(self):
        return self.q(css='a[data-section=membership].active-section').present

    def _get_cohort_options(self):
        """
        Returns the available options in the cohort dropdown, including the initial "Select a cohort group".
        """
        return self.q(css=".cohort-management #cohort-select option")

    def _cohort_name(self, label):
        """
        Returns the name of the cohort with the count information excluded.
        """
        return label.split(' (')[0]

    def _cohort_count(self, label):
        """
        Returns the count for the cohort (as specified in the label in the selector).
        """
        return int(label.split(' (')[1].split(')')[0])

    def get_cohorts(self):
        """
        Returns, as a list, the names of the available cohorts in the drop-down, filtering out "Select a cohort group".
        """
        return [
            self._cohort_name(opt.text)
            for opt in self._get_cohort_options().filter(lambda el: el.get_attribute('value') != "")
        ]

    def get_selected_cohort(self):
        """
        Returns the name of the selected cohort.
        """
        return self._cohort_name(
            self._get_cohort_options().filter(lambda el: el.is_selected()).first.text[0]
        )

    def get_selected_cohort_count(self):
        """
        Returns the number of users in the selected cohort.
        """
        return self._cohort_count(
            self._get_cohort_options().filter(lambda el: el.is_selected()).first.text[0]
        )

    def select_cohort(self, cohort_name):
        """
        Selects the given cohort in the drop-down.
        """
        self.q(css=".cohort-management #cohort-select option").filter(
            lambda el: self._cohort_name(el.text) == cohort_name
        ).first.click()

    def add_cohort(self, cohort_name):
        """
        Adds a new manual cohort with the specified name.
        """
        self.q(css="div.cohort-management-nav .action-create").first.click()
        textinput = self.q(css="#cohort-create-name").results[0]
        textinput.send_keys(cohort_name)
        self.q(css="div.form-actions .action-save").first.click()

    def get_cohort_group_setup(self):
        """
        Returns the description of the current cohort
        """
        return self.q(css='.cohort-management-group-setup .setup-value').first.text[0]

    def select_edit_settings(self):
        self.q(css=".action-edit").first.click()

    def add_students_to_selected_cohort(self, users):
        """
        Adds a list of users (either usernames or email addresses) to the currently selected cohort.
        """
        textinput = self.q(css="#cohort-management-group-add-students").results[0]
        for user in users:
            textinput.send_keys(user)
            textinput.send_keys(",")
        self.q(css="div.cohort-management-group-add .action-primary").first.click()

    def get_cohort_student_input_field_value(self):
        """
        Returns the contents of the input field where students can be added to a cohort.
        """
        return self.q(css="#cohort-management-group-add-students").results[0].get_attribute("value")

    def _get_cohort_messages(self, type):
        """
        Returns array of messages for given type.
        """
        title_css = "div.cohort-management-group-add .cohort-" + type + " .message-title"
        detail_css = "div.cohort-management-group-add .cohort-" + type + " .summary-item"

        return self._get_messages(title_css, detail_css)

    def get_cvs_messages(self):
        """
        Returns array of messages for given type.
        """
        title_css = "div.csv-upload .message-title"
        detail_css = "div.csv-upload .summary-item"
        return self._get_messages(title_css, detail_css)

    def _get_messages(self, title_css, details_css):
        message_title = self.q(css=title_css)
        if len(message_title.results) == 0:
            return []
        messages = [message_title.first.text[0]]
        details = self.q(css=details_css).results
        for detail in details:
            messages.append(detail.text)
        return messages

    def get_cohort_confirmation_messages(self):
        """
        Returns an array of messages present in the confirmation area of the cohort management UI.
        The first entry in the array is the title. Any further entries are the details.
        """
        return self._get_cohort_messages("confirmations")

    def get_cohort_error_messages(self):
        """
        Returns an array of messages present in the error area of the cohort management UI.
        The first entry in the array is the title. Any further entries are the details.
        """
        return self._get_cohort_messages("errors")

    def select_data_download(self):
        """
        Click on the link to the Data Download Page.
        """
        self.q(css="a.link-cross-reference[data-section=data_download]").first.click()

    def upload_correct_csv_file(self):
        """
        Selects the correct file and clicks the upload button.
        """
        correct_files_path = self.get_asset_path('cohort_users.csv')
        # Can this be "first"?
        file_input = self.q(css=self.cohort_csv_browse_button_selector).results[0]
        file_input.send_keys(correct_files_path)
        self.q(css=self.cohort_csv_upload_button_selector).results[0].click()

    def get_asset_path(self, file_name):
        """
        Returns the full path of the file to upload.
        These files have been placed in edx-platform/common/test/data/uploads/
        """
        return os.sep.join(__file__.split(os.sep)[:-5]) + '/test/data/uploads/%s' % file_name


class DataDownloadPage(PageObject):
    """
    Data Download section of the Instructor dashboard.
    """
    url = None

    def is_browser_on_page(self):
        return self.q(css='a[data-section=data_download].active-section').present
