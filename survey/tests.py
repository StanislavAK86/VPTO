from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from survey.models import Group, UserInfo, Question, Choice, Answer
from survey.forms import AnswerForm, UserInfoForm
from survey.views import StartSurveyView


class QuestionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Test Group')
        self.user_info = UserInfo.objects.create(full_name='Test User', team='Test Team', institution='Test Institution', group_id=self.group)
        self.question1 = Question.objects.create(text='Question 1', group=self.group, is_published=True)
        self.question2 = Question.objects.create(text='Question 2', group=self.group, is_published=True)
        self.choice1 = Choice.objects.create(question=self.question1, text='Choice 1', is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question1, text='Choice 2')
        self.choice3 = Choice.objects.create(question=self.question2, text='Choice 3', is_correct=True)
        self.choice4 = Choice.objects.create(question=self.question2, text='Choice 4')

        self.session = self.client.session
        self.session['user_info_id'] = self.user_info.id
        self.session['group_id'] = self.group.id
        self.session.save()

    def test_get_question_view(self):
        response = self.client.get(reverse('survey:question', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey/question.html')
        self.assertContains(response, 'Question 1')
        self.assertContains(response, 'Choice 1')
        self.assertContains(response, 'Choice 2')

    def test_post_question_view_valid_form(self):
        data = {'chosen_choice': self.choice1.id}
        response = self.client.post(reverse('survey:question', args=[1]), data)
        print(response.content)  # Отладочное сообщение
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('survey:question', args=[2]))

    def test_post_question_view_invalid_form(self):
        data = {}  # Invalid data
        response = self.client.post(reverse('survey:question', args=[1]), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey/question.html')
        self.assertContains(response, 'Question 1')
        self.assertContains(response, 'Choice 1')
        self.assertContains(response, 'Choice 2')

    def test_redirect_to_results_if_no_more_questions(self):
        data = {'chosen_choice': self.choice3.id}
        response = self.client.post(reverse('survey:question', args=[2]), data)
        print(response.content)  # Отладочное сообщение
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('survey:results'))

    def test_redirect_to_group_selection_if_no_session(self):
        self.client.session.flush()
        response = self.client.get(reverse('survey:question', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('survey:group_selection'))

    def test_redirect_to_results_if_question_id_exceeds_length(self):
        response = self.client.get(reverse('survey:question', args=[3]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('survey:results'))

    def test_load_with_high_number_of_questions(self):
        for i in range(100):
            Question.objects.create(text=f'Question {i+3}', group=self.group, is_published=True)

        response = self.client.get(reverse('survey:question', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey/question.html')
        self.assertContains(response, 'Question 1')
        self.assertContains(response, 'Choice 1')
        self.assertContains(response, 'Choice 2')





class StartSurveyViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.group = Group.objects.create(name='Test Group')
        self.question = Question.objects.create(text='Test Question', group=self.group, is_published=True)
        self.user_info_data = {
            'full_name': 'Test User',
            'institution': 'Test Institution',
            'team': 'Test Team'
        }

    def test_start_survey_view_get(self):
        response = self.client.get(reverse('survey:start_survey'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey/start_survey.html')
        self.assertIsInstance(response.context['form'], UserInfoForm)

    def test_start_survey_view_post_valid(self):
        response = self.client.post(reverse('survey:start_survey'), data=self.user_info_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('user_info_id', self.client.session)
        self.assertIn(reverse('survey:question', kwargs={'question_id': 1}), response.url)

    def test_start_survey_view_post_invalid(self):
        invalid_data = {
            'full_name': '',
            'institution': '',
            'team': ''
        }
        response = self.client.post(reverse('survey:start_survey'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'survey/start_survey.html')
        self.assertFormError(response, 'form', 'full_name', 'This field is required.')
        self.assertFormError(response, 'form', 'institution', 'This field is required.')
        self.assertFormError(response, 'form', 'team', 'This field is required.')

    def test_start_survey_view_session(self):
        response = self.client.post(reverse('survey:start_survey'), data=self.user_info_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('user_info_id', self.client.session)
        user_info_id = self.client.session['user_info_id']
        self.assertTrue(UserInfo.objects.filter(id=user_info_id).exists())

    def test_start_survey_view_load(self):
        # Simulate load testing by sending multiple requests
        for _ in range(100):
            response = self.client.post(reverse('survey:start_survey'), data=self.user_info_data)
            self.assertEqual(response.status_code, 302)
            self.assertIn('user_info_id', self.client.session)

if __name__ == '__main__':
    TestCase.main()