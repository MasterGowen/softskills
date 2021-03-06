import json

import requests
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField('Имя пользователя', max_length=32, blank=True, default='')
    last_name = models.CharField('Фамилия пользователя', max_length=32, blank=True, default='')
    second_name = models.CharField('Отчество пользователя', max_length=32, blank=True, default='')
    SEXES = (
        ('U', 'Не выбран'),
        ('F', 'Женский'),
        ('M', 'Мужской'),
    )

    sex = models.CharField("Пол", max_length=1, choices=SEXES, default='U')
    department = models.CharField('Институт', max_length=1024, blank=True, null=True)
    group_number = models.CharField('Номер группы', max_length=1024, blank=True, null=True)
    institute = models.CharField('Университет', max_length=1024, blank=True, null=True)
    checked = models.BooleanField("Персона проверена", default=False)

    current_course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'персона'
        verbose_name_plural = 'персоны'

    def get_person_diagnostics(self):
        # sds = []
        # ds = Diagnostic.objects.all()
        # for d in ds:
        #     try:
        #         sd = StudentDiag.objects.filter(person=self, diagnostic=d)
        #         sds.append(sd)
        #     except:
        #         pass
        # return sds
        return StudentDiag.objects.filter(person=self)

    def get_person_projects(self):
        registrations = ProjectUserRegistration.objects.filter(person=self)
        projects = [r.project for r in registrations]
        return projects if projects else []

    def is_full(self):
        return all([
            self.first_name != "",
            self.last_name != ""
        ])

    def __str__(self):
        if self.first_name and self.last_name:
            if self.second_name:
                return f"{self.first_name} {self.second_name} {self.last_name}"

            return ' '.join([str(self.first_name), str(self.last_name)])

        else:
            return str(self.user)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Person.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.person.save()

    def count_open(self):
        count = 0
        for d in Diagnostic.objects.filter(published="p"):
            if not d.has_answer(self) and d.status == "open":
                count += 1
        return count


class Subevent(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )

    title = models.CharField("Название события", max_length=256, blank=False)
    description = models.TextField("Описание события", blank=True, default="")
    status = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')
    _startdate = models.DateTimeField("Начало события", blank=True, null=True)
    _enddate = models.DateTimeField("Конец события", blank=True, null=True)


class EventUserRegistration(models.Model):
    class Meta:
        verbose_name = 'регистрация пользователя на событие'
        verbose_name_plural = 'регистрации пользователей на события'

    ROLES = (
        ("student", "Студент"),
        ("staff", "Преподаватель"),
        ("admin", "Администратор"),
    )

    person = models.ForeignKey("Person", verbose_name="Персона", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", verbose_name="Событие", on_delete=models.CASCADE)
    role = models.CharField("Роль", max_length=8, choices=ROLES)

    class Meta:
        unique_together = ('person', 'event',)

    def __str__(self):
        return " ".join([str(self.person), str(self.event), str(self.role)])


class ProjectUserRegistration(models.Model):
    class Meta:
        verbose_name = 'регистрация пользователя на событие'
        verbose_name_plural = 'регистрации пользователей на события'

    ROLES = (
        ("student", "Студент"),
        ("staff", "Преподаватель"),
        ("admin", "Администратор"),
    )

    person = models.ForeignKey("Person", verbose_name="Персона", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", verbose_name="Событие", on_delete=models.CASCADE)
    role = models.CharField("Тип регистрации", max_length=8, choices=ROLES)

    class Meta:
        unique_together = ('person', 'project',)

    def __str__(self):
        return f"<{self.person} - {self.project.title} - {self.role}>"


class CourseUserRegistration(models.Model):
    class Meta:
        verbose_name = 'регистрация пользователя на курс'
        verbose_name_plural = 'регистрации пользователей на курс'

    ROLES = (
        ("student", "Студент"),
        ("staff", "Преподаватель"),
        ("admin", "Администратор"),
    )

    person = models.ForeignKey("Person", verbose_name="Персона", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", verbose_name="Курс", on_delete=models.CASCADE)
    role = models.CharField("Тип регистрации", max_length=8, choices=ROLES, default="student")

    class Meta:
        unique_together = ('person', 'course',)

    def __str__(self):
        return f"<{self.person} - {self.course.title} - {self.role}>"


class ProjectImage(models.Model):
    image = models.FileField(upload_to="images/%Y/%m/%d")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='images')


class EventImage(models.Model):
    image = models.FileField(upload_to="images/%Y/%m/%d")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='images')


class ProjectFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='files')


class EventFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='files')


class Course(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )
    TYPES = (
        ('simple', 'Обычный'),
        ('minor', "Майнор")
    )
    title = models.CharField("Название курса", max_length=256, blank=False)
    description = models.TextField("Описание курса", blank=True, default="")
    type = models.CharField("Тип курса", choices=TYPES, null=False, blank=False, default="simple", max_length=32)
    status = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')
    _startdate = models.DateTimeField("Начало курса", blank=True, null=True)
    _enddate = models.DateTimeField("Конец курса", blank=True, null=True)
    projects = models.ManyToManyField("Project", blank=True)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return f"Курс: {self.title}"

    def enroll(self, person):
        CourseUserRegistration.objects.create(
            person=person,
            course=self,
            role="student"
        )
        person.current_course = self
        person.save()

    def unenroll(self, person):
        CourseUserRegistration.objects.filter(
            person=person,
            course=self,
        ).delete()
        try:
            person.current_course = CourseUserRegistration.objects.filter(
                person=person)[0].course
        except:
            person.current_course = 0
        person.save()


class Project(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )
    title = models.CharField("Название проекта", max_length=256, blank=False)
    description = models.TextField("Описание проекта", blank=True, default="")
    status = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')
    _startdate = models.DateTimeField("Начало проекта", blank=True, null=True)
    _enddate = models.DateTimeField("Конец проекта", blank=True, null=True)

    events = models.ManyToManyField("Event", blank=True)

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

    def __str__(self):
        return self.title

    def get_students(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event__in=self.events.all(), role="student")]
        return list(registrations)

    def get_staff(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event__in=self.events.all(), role="staff")]
        registrations += [s.person for s in ProjectUserRegistration.objects.filter(project=self, role="staff")]
        return list(registrations)

    def get_images(self):
        return ProjectImage.objects.filter(project=self)

    def enumerated_events(self):
        return enumerate(self.events.all())


class Event(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )
    code = models.CharField("Короткий ИД", max_length=256, blank=True, null=True)
    title = models.CharField("Название события", max_length=256, blank=False)
    description = models.TextField("Описание события", blank=True, default="")
    status = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')
    _startdate = models.DateTimeField("Начало события", blank=True, null=True)
    _enddate = models.DateTimeField("Конец события", blank=True, null=True)

    subevents = models.ManyToManyField("Subevent", blank=True)

    def startdate(self):
        return self._startdate

    def get_students(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event=self, role="student")]
        return list(registrations)

    def get_staff(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event=self, role="staff")]
        return list(registrations)

    def get_project_students(self):
        projects = self.project_set.filter(events__in=[self])
        registrations = [s.person.id for s in ProjectUserRegistration.objects.filter(project__in=projects)]
        registrations = Person.objects.filter(pk__in=list(set(registrations)))
        return registrations

    def get_images(self):
        return EventImage.objects.filter(event=self)

    def visited_by(self, person, project):
        return Visit.objects.filter(event=self, person=person, project=project)

    def enroll(self, person):
        some_time_events = Event.objects.filter(_startdate=self._startdate)
        EventUserRegistration.objects.filter(event__in=some_time_events, person=person).delete()
        EventUserRegistration.objects.create(
            person=person,
            event=self,
            role="student"
        )

    def unenroll(self, person):
        EventUserRegistration.objects.filter(
            person=person,
            event=self,
        ).delete()

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'

    def __str__(self):
        if self.code:
            return f"{self.code} {self.title}"
        else:
            return f"{self.title}"


class Diagnostic(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )
    TYPES = (("h", "html"), ("j", "json"))
    slug = models.CharField("Slug", blank=False, null=False, default="sample", max_length=16)
    title = models.CharField("Название диагностики", max_length=1024, blank=False)
    description = models.TextField("Описание диагностики", blank=True, default="")
    short_description = models.TextField("Краткое описание диагностики", blank=True, default="")
    type = models.CharField("Тип", choices=TYPES, max_length=1, default="h")
    image = models.ImageField("Изображение", blank=True, null=True)
    html = models.TextField("Отображение", blank=True, null=True)
    json = models.TextField("json", blank=True, null=True)
    check_func = models.TextField("Функция проверки", blank=True, null=True)
    render = models.TextField("Функция отрисовки", blank=True, null=True)
    render_result = models.TextField("Функция отрисовки ответа", blank=True, null=True)

    weight = models.IntegerField("Вес", default=0, blank=False, null=False)
    startdate = models.DateTimeField("Дата начала", blank=True, null=True)
    enddate = models.DateTimeField("Дата завершения", blank=True, null=True)
    published = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')

    courses = models.ManyToManyField("Course", blank=True)

    class Meta:
        verbose_name = 'диагностика'
        verbose_name_plural = 'диагностики'

    def has_answer(self, person):
        return StudentDiag.objects.filter(diagnostic=self, person=person).exists()

    @property
    def status(self):
        if self.enddate:
            if self.enddate > timezone.now() > self.startdate:
                return "open"
            else:
                return "close"
        else:
            if timezone.now() > self.startdate:
                return "open"
            else:
                return "close"

    @classmethod
    def get_for_course(cls, course):
        cls.objects.filter(Q(courses=None) | Q(courses=course)).filter(published="p").order_by("weight")


class StudentDiag(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, )
    answer = models.TextField("Ответ студента", null=True, blank=True)
    analisys = models.TextField("Анализ диагностики", null=True, blank=True)
    result = models.TextField("Результат диагностики", null=True, blank=True)
    is_checked = models.BooleanField("Проверена", default=False)

    def send_by_slug(self):
        q = json.loads(self.answer)
        q.pop('csrfmiddlewaretoken', None)
        self.answer = json.dumps(q)

        r = requests.post(f'http://softskills-ural.ru:5051/v1/ssd/{self.diagnostic.slug}/', data={"answer": self.answer})
        try:
            if r.status_code == 200:
                self.analisys = r.json()["result"]["result"]
                self.is_checked = True
                self.save()
        except:
            pass

    def send(self):
        q = json.loads(self.answer)
        q.pop('csrfmiddlewaretoken', None)
        self.answer = json.dumps(q)

        r = requests.post(f'http://softskills-ural.ru:5051/v1/ssd/check/', data={"answer": self.answer, "check_func": self.diagnostic.check_func})
        try:
            if r.status_code == 200:
                self.analisys = r.json()["result"]["result"]
                self.is_checked = True
                self.save()
        except:
            pass


class Visit(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=True)
    event = models.ForeignKey("Event", on_delete=models.CASCADE, null=True)
    person = models.ForeignKey("Person", on_delete=models.CASCADE, null=True)


class PrTheme(models.Model):
    theme = models.CharField("Тема проектной работы", max_length=4096, blank=False)
    description = models.TextField("Описание", blank=True)
    chief = models.ForeignKey("Person", verbose_name="Руководитель", on_delete=models.CASCADE, null=True, related_name='prtheme_chief')
    max_take = models.PositiveIntegerField("Максимальное количество студентов", null=True, blank=True)
    close_register_datetime = models.DateTimeField("Закрытие регистрации", null=True, blank=True)
    course = models.ForeignKey("Course", blank=True, on_delete=models.CASCADE, null=True)

    students = models.ManyToManyField("Person", blank=True)

    class Meta:
        verbose_name = 'тема проектной работы'
        verbose_name_plural = 'темы проектных работ'

    def __str__(self):
        return self.theme

    def choice(self, person, course):

        if self.max_take:
            if self.students.count > self.max_take:
                return False

        if self.close_register_datetime:
            if timezone.now() > self.close_register_datetime:
                return False

        for t in PrTheme.objects.filter(course=course):
            t.students.remove(person)
        self.students.add(person)
        return True
