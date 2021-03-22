# Generated by Django 3.1 on 2021-03-09 08:31

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='текст вопроса')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='позиция')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_surveys.question_set+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
            ],
            options={
                'verbose_name': 'опрос',
                'verbose_name_plural': 'опросы',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_surveys.useranswer_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
            ],
            options={
                'verbose_name': 'вопрос с одиночным выбором',
                'verbose_name_plural': 'вопросы с одиночным выбором',
            },
            bases=('surveys.question',),
        ),
        migrations.CreateModel(
            name='InputChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
            ],
            options={
                'verbose_name': 'вопрос с одиночным выбором и пользовательским вводом',
                'verbose_name_plural': 'вопросы с одиночным выбором и пользовательским вводом',
            },
            bases=('surveys.question',),
        ),
        migrations.CreateModel(
            name='InputMultiChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
            ],
            options={
                'verbose_name': 'вопрос с множественным выбором и пользовательским вводом',
                'verbose_name_plural': 'вопросы с множественным выбором и пользовательским вводом',
            },
            bases=('surveys.question',),
        ),
        migrations.CreateModel(
            name='InputQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
            ],
            options={
                'verbose_name': 'вопрос с пользовательским вводом',
                'verbose_name_plural': 'вопросы с пользовательским вводом',
            },
            bases=('surveys.question',),
        ),
        migrations.CreateModel(
            name='MultiChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.question')),
            ],
            options={
                'verbose_name': 'вопрос с множественным выбором',
                'verbose_name_plural': 'вопросы с множественным выбором',
            },
            bases=('surveys.question',),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='surveys.survey', verbose_name='опрос'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='текст ответа')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
            },
        ),
        migrations.CreateModel(
            name='UserMultiChoiceAnswer',
            fields=[
                ('useranswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.useranswer')),
                ('answers', models.ManyToManyField(related_name='user_multi_choices', to='surveys.Answer', verbose_name='ответы')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='surveys.multichoicequestion', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'выбранный ответ пользователя',
                'verbose_name_plural': 'выбранные ответы пользователя',
            },
            bases=('surveys.useranswer',),
        ),
        migrations.CreateModel(
            name='UserInputMultiChoiceAnswer',
            fields=[
                ('useranswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.useranswer')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст')),
                ('answers', models.ManyToManyField(related_name='user_input_multi_choices', to='surveys.Answer', verbose_name='ответы')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='surveys.inputmultichoicequestion', verbose_name='вопрос')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.useranswer',),
        ),
        migrations.CreateModel(
            name='UserInputChoiceAnswer',
            fields=[
                ('useranswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.useranswer')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст')),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_input_choices', to='surveys.answer', verbose_name='ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='surveys.inputchoicequestion', verbose_name='вопрос')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('surveys.useranswer',),
        ),
        migrations.CreateModel(
            name='UserInputAnswer',
            fields=[
                ('useranswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.useranswer')),
                ('text', models.TextField(verbose_name='текст')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='surveys.inputquestion', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'текстовый ответ пользователя',
                'verbose_name_plural': 'текстовые ответы пользователя',
            },
            bases=('surveys.useranswer',),
        ),
        migrations.CreateModel(
            name='UserChoiceAnswer',
            fields=[
                ('useranswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='surveys.useranswer')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_choices', to='surveys.answer', verbose_name='ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='surveys.choicequestion', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'выбранный ответ пользователя',
                'verbose_name_plural': 'выбранные ответы пользователя',
            },
            bases=('surveys.useranswer',),
        ),
    ]
