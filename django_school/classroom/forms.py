from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Answer, Question, Student, StudentAnswer,
                              Subject, User, Teacher)


class TeacherSignUpForm(UserCreationForm):

    email = forms.CharField()
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        teacher = Teacher.objects.create(user=user,
                                         email=self.cleaned_data.get('email'),
                                         first_name=self.cleaned_data.get('first_name'),
                                         last_name=self.cleaned_data.get('last_name'),)


        return user


class StudentSignUpForm(UserCreationForm):
    """Форма для создания интересов"""
    email = forms.CharField()
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    group = forms.CharField(label="Группа")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        """Интересы юзера добавляются"""
        student = Student.objects.create(user=user,
                                         email=self.cleaned_data.get('email'),
                                         first_name=self.cleaned_data.get('first_name'),
                                         last_name=self.cleaned_data.get('last_name'),
                                         group=self.cleaned_data.get('group'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ()
        #widgets = {
        #    'interests': forms.CheckboxSelectMultiple
        #}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'type', 'image')
        widgets = {
          'type': forms.Textarea(attrs={'rows':1, 'cols':10}),
        }


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Отметьте хотя бы один ответ как правильный.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None,
        label="Ответ")

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
