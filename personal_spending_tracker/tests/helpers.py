from django.urls import reverse

class LogInTester:
    def _user_is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

class NavbarTester:
    menu_urls = [
        reverse('feed'), 
        reverse('spending_history', kwargs={'timefilter':'All', 'categoryfilter':'All', 'cyclefilter':'Current'}), 
        reverse('regular_spendings_chart'), 
        reverse('spending_by_category'),
        reverse('point_history', kwargs={'timefilter':'All', 'categoryfilter':'All'}), 
        reverse('category_management_dashboard')
    ]

    def assert_navbar(self, response):
        for url in self.menu_urls:
            self.assertContains(response, url)

    def assert_no_navbar(self, response):
        for url in self.menu_urls:
            self.assertNotContains(response, url)

class TopbarTester:
    menu_urls = [
        reverse('edit_profile'), 
        reverse('log_out')
    ]

    def assert_topbar(self, response):
        for url in self.menu_urls:
            self.assertContains(response, url)

    def assert_no_topbar(self, response):
        for url in self.menu_urls:
            self.assertNotContains(response, url)
            