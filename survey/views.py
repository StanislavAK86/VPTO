import random
from .models import Group, UserInfo, Question, Answer, Choice
from .forms import UserInfoForm, AnswerForm, QuestionForm, ChoiceForm
from blog.views import MenuMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin
from django.db.models import Prefetch

class GroupSelectionView(MenuMixin, TemplateView):
    template_name = 'survey/group_selection.html'
    extra_context = {'title': 'Тесты'}

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all().prefetch_related('question_set')
        context = self.get_context_data(groups=groups)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group')
        password = request.POST.get('password')

        try:
            group = Group.objects.select_related().get(id=group_id)
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



class QuestionView(MenuMixin, TemplateView):
    template_name = 'survey/question.html'

    def get(self, request, question_id, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_info_id = request.session.get('user_info_id')
        group_id = request.session.get('group_id')
        if not user_info_id or not group_id:
            return redirect('survey:group_selection')

        user_info = UserInfo.objects.get(id=user_info_id)
        questions = list(Question.objects.filter(group_id=group_id, is_published=True).order_by('id').prefetch_related('choice_set'))

        
        if 'random_questions' not in request.session:
            random_questions = random.sample(questions, min(10, len(questions)))
            request.session['random_questions'] = [q.id for q in random_questions]
        else:
            random_questions = [q for q in questions if q.id in request.session['random_questions']]

        if question_id > len(random_questions):
            return redirect('survey:results')

        question = random_questions[question_id - 1]
        choices = list(question.choice_set.all())
        random.shuffle(choices)

        form = AnswerForm()
        context.update({'question': question, 'choices': choices, 'form': form})

        return self.render_to_response(context)

    def post(self, request, question_id):
        user_info_id = request.session.get('user_info_id')
        group_id = request.session.get('group_id')
        if not user_info_id or not group_id:
            return redirect('survey:group_selection')

        user_info = UserInfo.objects.get(id=user_info_id)
        questions = list(Question.objects.filter(group_id=group_id, is_published=True).order_by('id').prefetch_related('choice_set'))

        
        random_questions = [q for q in questions if q.id in request.session['random_questions']]

        if question_id > len(random_questions):
            return redirect('survey:results')

        question = random_questions[question_id - 1]
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user_info = user_info
            answer.question = question
            answer.save()

            
            if question_id < len(random_questions):
                return redirect('survey:question', question_id=question_id + 1)
            else:
                return redirect('survey:results')

        choices = list(question.choice_set.all())
        random.shuffle(choices)
        context = self.get_context_data()
        context.update({'question': question, 'choices': choices, 'form': form})

        return self.render_to_response(context)

class ResultsView(MenuMixin, TemplateView):
    template_name = 'survey/results.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_info_id = request.session.get('user_info_id')
        if not user_info_id:
            return redirect('group_selection')

        user_info = UserInfo.objects.get(id=user_info_id)
        random_questions_ids = request.session.get('random_questions', [])
        answers = Answer.objects.filter(user_info=user_info, question_id__in=random_questions_ids).select_related('question', 'chosen_choice')
        correct_answers = answers.filter(chosen_choice__is_correct=True).count()
        incorrect_answers = len(random_questions_ids) - correct_answers

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
        active_tab = 'survey:all_results'
        context['active_tab'] = active_tab

        sort_by = request.GET.get('sort_by', 'full_name')
        if sort_by not in ['full_name', 'team']:
            sort_by = 'full_name'

        team = request.GET.get('team')
        survey_name = request.GET.get('survey_name')

        user_infos = UserInfo.objects.all()
        if team:
            user_infos = user_infos.filter(team=team)

        user_infos = user_infos.order_by(sort_by)
        results = []

        for user_info in user_infos:
            random_questions_ids = request.session.get('random_questions', [])
            answers = Answer.objects.filter(user_info=user_info, question_id__in=random_questions_ids).select_related('question', 'chosen_choice')
            if survey_name:
                answers = answers.filter(question__group__name=survey_name)

            questions_with_answers = []
            correct_answers_count = 0
            incorrect_answers_count = 0
            survey_names = set()

            for answer in answers:
                correct_choice = answer.question.choice_set.filter(is_correct=True).first()
                questions_with_answers.append({
                    'question': answer.question,
                    'correct_choice': correct_choice,
                    'chosen_choice': answer.chosen_choice
                })
                if answer.chosen_choice == correct_choice:
                    correct_answers_count += 1
                else:
                    incorrect_answers_count += 1
                survey_names.add(answer.question.group.name)

            for survey_name in survey_names:
                results.append({
                    'user_info': user_info,
                    'questions_with_answers': questions_with_answers,
                    'correct_answers_count': correct_answers_count,
                    'incorrect_answers_count': incorrect_answers_count,
                    'survey_name': survey_name
                })

        teams = UserInfo.objects.values_list('team', flat=True).distinct()
        surveys = Group.objects.all()

        context.update({
            'results': results,
            'sort_by': sort_by,
            'team': team,
            'surveys': surveys,
            'survey_name': survey_name,
        })

        return self.render_to_response(context)


class AddQuestionView(MenuMixin, TemplateView):
    template_name = 'survey/add_question.html'

    def get(self, request, *args, **kwargs):
        question_form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=str(i)) for i in range(4)]
        active_tab = 'add_question'
        context = self.get_context_data(**kwargs)
        context.update({
            'question_form': question_form,
            'choice_forms': choice_forms,
            'active_tab': active_tab
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        question_form = QuestionForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(i)) for i in range(4)]

        if question_form.is_valid() and all(form.is_valid() for form in choice_forms[:2]) and all(form.is_valid() or not form.data for form in choice_forms[2:]):
            new_group_name = question_form.cleaned_data.get('new_group')
            group = question_form.cleaned_data.get('group')

            if not group and new_group_name:
                group, created = Group.objects.get_or_create(name=new_group_name)
                question_form.instance.group = group

            question = question_form.save()

            for form in choice_forms:
                if form.cleaned_data.get('text'):
                    choice = form.save(commit=False)
                    choice.question = question
                    choice.save()

            return redirect(reverse_lazy('survey:add_question'))

        context = self.get_context_data(**kwargs)
        context.update({
            'question_form': question_form,
            'choice_forms': choice_forms,
        })
        return self.render_to_response(context)