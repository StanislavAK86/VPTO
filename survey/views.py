from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Group, UserInfo, Question, Answer, Choice
from .forms import UserInfoForm, AnswerForm, QuestionForm, ChoiceForm
import random
import logging
from django.views.generic.base import ContextMixin

class MenuMixin(ContextMixin):
    nav_menu = {
        'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.nav_menu['menu']
        return context

class GroupSelectionView(MenuMixin, TemplateView):
    template_name = 'survey/group_selection.html'
    extra_context = {'title': 'Тесты'}

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        context = self.get_context_data(groups=groups)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group')
        password = request.POST.get('password')

        try:
            group = Group.objects.get(id=group_id)
            if group.password and group.password != password:
                context = self.get_context_data(groups=Group.objects.all(), error='Неверный пароль')
                return self.render_to_response(context)
            request.session['group_id'] = group_id
            return redirect(reverse_lazy('survey:start_survey'))
        except Group.DoesNotExist:
            context = self.get_context_data(groups=Group.objects.all(), error='Группа не найдена')
            return self.render_to_response(context)

class StartSurveyView(MenuMixin, FormView):
    template_name = 'survey/start_survey.html'
    form_class = UserInfoForm

    def form_valid(self, form):
        user_info = form.save()
        self.request.session['user_info_id'] = user_info.id
        return redirect('survey:question', question_id=1)

class QuestionView(MenuMixin, View):
    template_name = 'survey/question.html'

    def get(self, request, question_id, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_info_id = request.session.get('user_info_id')
        group_id = request.session.get('group_id')
        if not user_info_id or not group_id:
            return redirect('survey:group_selection')

        user_info = UserInfo.objects.get(id=user_info_id)
        questions = Question.objects.filter(group_id=group_id, is_published=True).order_by('id')

        if question_id > len(questions):
            return redirect('survey:results')

        question = questions[question_id - 1]
        choices = list(question.choice_set.all())
        random.shuffle(choices)

        form = AnswerForm()
        context.update({'question': question, 'choices': choices, 'form': form})
        return render(request, self.template_name, context)

    def post(self, request, question_id):
        user_info_id = request.session.get('user_info_id')
        group_id = request.session.get('group_id')
        if not user_info_id or not group_id:
            return redirect('survey:group_selection')

        user_info = UserInfo.objects.get(id=user_info_id)
        questions = Question.objects.filter(group_id=group_id, is_published=True).order_by('id')

        if question_id > len(questions):
            return redirect('survey:results')

        question = questions[question_id - 1]
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user_info = user_info
            answer.question = question
            answer.save()
            next_question = questions.filter(id__gt=question.id).first()
            if next_question:
                return redirect('survey:question', question_id=questions.filter(id__lte=next_question.id).count())
            else:
                return redirect('survey:results')

        choices = list(question.choice_set.all())
        random.shuffle(choices)
        context = self.get_context_data()
        context.update({'question': question, 'choices': choices, 'form': form})
        return render(request, self.template_name, context)

class ResultsView(MenuMixin, TemplateView):
    template_name = 'survey/results.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_info_id = request.session.get('user_info_id')
        if not user_info_id:
            return redirect('group_selection')

        user_info = UserInfo.objects.get(id=user_info_id)
        answers = Answer.objects.filter(user_info=user_info)
        correct_answers = answers.filter(chosen_choice__is_correct=True).count()
        total_questions = Question.objects.filter(group_id=request.session.get('group_id'), is_published=True).count()
        incorrect_answers = total_questions - correct_answers

        questions_with_correct_answers = []
        for answer in answers:
            correct_choice = answer.question.choice_set.get(is_correct=True)
            questions_with_correct_answers.append({
                'question': answer.question,
                'correct_choice': correct_choice,
                'chosen_choice': answer.chosen_choice
            })

        context.update({
            'user_info': user_info,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'questions_with_correct_answers': questions_with_correct_answers
        })

        return render(request, self.template_name, context)

class AllResultsView(MenuMixin, TemplateView):
    template_name = 'survey/all_results.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        sort_by = request.GET.get('sort_by', 'full_name')
        if sort_by not in ['full_name', 'team']:
            sort_by = 'full_name'

        team = request.GET.get('team')
        group_name = request.GET.get('group')

        user_infos = UserInfo.objects.all()
        if team:
            user_infos = user_infos.filter(team=team)

        if group_name:
            group = Group.objects.get(name=group_name)
            user_infos = user_infos.filter(group=group)

        user_infos = user_infos.order_by(sort_by)
        results = []

        for user_info in user_infos:
            answers = Answer.objects.filter(user_info=user_info)
            questions_with_answers = []
            for answer in answers:
                correct_choice = answer.question.choice_set.filter(is_correct=True).first()
                questions_with_answers.append({
                    'question': answer.question,
                    'correct_choice': correct_choice,
                    'chosen_choice': answer.chosen_choice
                })
            results.append({
                'user_info': user_info,
                'questions_with_answers': questions_with_answers
            })

        teams = UserInfo.objects.values_list('team', flat=True).distinct()
        groups = Group.objects.all()

        context.update({
            'results': results,
            'sort_by': sort_by,
            'team': team,
            'groups': groups,
            'group': group_name,
        })

        return self.render_to_response(context)

logger = logging.getLogger(__name__)


class AddQuestionView(MenuMixin, TemplateView):
    template_name = 'survey/add_question.html'

    def get(self, request, *args, **kwargs):
        question_form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=str(i)) for i in range(4)]
        context = self.get_context_data(**kwargs)
        context.update({
            'question_form': question_form,
            'choice_forms': choice_forms,
        })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        question_form = QuestionForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(i)) for i in range(4)]

        logger.debug(f"Received POST data: {request.POST}")
        logger.debug(f"Question form data: {question_form.data}")
        logger.debug(f"Choice forms data: {[form.data for form in choice_forms]}")

        if question_form.is_valid() and all(form.is_valid() for form in choice_forms[:2]) and all(form.is_valid() or not form.data for form in choice_forms[2:]):
            logger.debug("All forms are valid.")

            new_group_name = question_form.cleaned_data.get('new_group')
            group = question_form.cleaned_data.get('group')

            logger.debug(f"New group name: {new_group_name}")
            logger.debug(f"Selected group: {group}")

            if not group and new_group_name:
                group, created = Group.objects.get_or_create(name=new_group_name)
                question_form.instance.group = group
                logger.debug(f"Created new group: {group}")

            question = question_form.save()
            logger.debug(f"Saved question: {question}")

            for form in choice_forms:
                if form.cleaned_data.get('text'):
                    choice = form.save(commit=False)
                    choice.question = question
                    choice.save()
                    logger.debug(f"Saved choice: {choice}")

            return redirect(reverse_lazy('survey:add_question'))

        else:
            logger.error(f"Question form errors: {question_form.errors}")
            for form in choice_forms:
                logger.error(f"Choice form errors: {form.errors}")

        context = self.get_context_data(**kwargs)
        context.update({
            'question_form': question_form,
            'choice_forms': choice_forms,
        })
        return render(request, self.template_name, context)