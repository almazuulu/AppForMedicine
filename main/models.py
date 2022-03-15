from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.urls import reverse
from django.utils.datetime_safe import date


class Pediatrist(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, null=True, verbose_name="Пользователь", on_delete=models.SET_NULL
    )
    name = models.CharField(
        max_length=50, verbose_name="Имя"
    )
    rank = models.CharField(
        max_length=50, verbose_name="Звание"
    )
    workPlace = models.CharField(
        max_length=100, verbose_name="Место работы"
    )
    phone = models.CharField(
        max_length=20, verbose_name="Контакты"
    )

    def __str__(self):
        return self.name


class KinderGarden(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, null=True, verbose_name="Пользователь", on_delete=models.SET_NULL
    )
    name = models.CharField(
        max_length=50, verbose_name="Имя садика"
    )
    address = models.CharField(
        max_length=50, verbose_name="Адрес"
    )

    def __str__(self):
        return self.name


class Parent(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, null=True, verbose_name="Пользователь", on_delete=models.SET_NULL
    )
    name = models.CharField(
        max_length=50, verbose_name="Имя"
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон"
    )


class Child(models.Model):
    SEX_CHOICES = (("Мужской", "Мужской"), ("Женский", "Женский"))
    name = models.CharField(
        max_length=50, verbose_name="Имя"
    )
    birthData = models.DateField(
        verbose_name="Дата рождения"
    )
    kinder_garden = models.ForeignKey(
        KinderGarden, verbose_name="Детский сад", on_delete=models.CASCADE
    )
    parent1 = models.ForeignKey(
        Parent, verbose_name="Родитель 1", on_delete=models.CASCADE, related_name="father"
    )
    parent2 = models.ForeignKey(
        Parent, verbose_name="Родитель 2", on_delete=models.CASCADE, related_name="mother"
    )
    sex = models.CharField(
        max_length=15, verbose_name="Пол", choices=SEX_CHOICES
    )

    blood_type = models.CharField(
        max_length=5, verbose_name="Группа крови"
    )

    height = models.CharField(
        max_length=3, verbose_name="Рост"
    )

    weight = models.CharField(
        max_length=20, verbose_name="Вес"
    )




    def __str__(self):
        return self.name

    def calculate_age(self):
        today = date.today()
        return today.year - self.birthData.year - ((today.month, today.day) < (self.birthData.month, self.birthData.day))


class Survey(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Название"
    )
    description = models.CharField(
        max_length=250, verbose_name="Телефон"
    )
    surveyDate = models.DateField(
        verbose_name="Дата обследования"
    )
    isValid = models.BooleanField(
        default=False, verbose_name="Утверджен"
    )
    pediatrist = models.ForeignKey(
        Pediatrist, on_delete=models.CASCADE, verbose_name="Педиатр"
    )


class Form26(models.Model):
    child = models.ForeignKey(
        Child, on_delete=models.CASCADE, verbose_name="Ребенок"
    )
    inspection = models.TextField(
        verbose_name="Осмотр"
    )
    recommendation = models.TextField(
        verbose_name="Рекомендации"
    )
    creation_date = models.DateField(
        verbose_name="Дата создания"
    )

    def get_absolute_url(self):
        return reverse('dashboard')

    # general_info = models.CharField(
    #     max_length=250, verbose_name="Общие сведения"
    # )
    # Anamnesis = models.CharField(
    #     max_length=250, verbose_name="Анамнез"
    # )
    # medical_examination = models.CharField(
    #     max_length=250, verbose_name="Диспансеризация"
    # )
    # mandatory_treatment = models.CharField(
    #     max_length=250, verbose_name="Обязательное лечение"
    # )
    # immunoprophylaxis = models.CharField(
    #     max_length=250, verbose_name="Иммунопрофилактика"
    # )
    # scheduled_medical_examinations = models.CharField(
    #     max_length=250, verbose_name="Плановые медосмотры"
    # )
    # profession_medical_consultations = models.CharField(
    #     max_length=250, verbose_name="Врачебные консультации о профпригодности"
    # )
    # sport_recommendation = models.CharField(
    #     max_length=250, verbose_name="Рекомендации спортивной деятельности"
    # )
    # military_preparation = models.CharField(
    #     max_length=250, verbose_name="Подготовка к военной службе"
    # )
    # medical_records = models.CharField(
    #     max_length=250, verbose_name="Врачебные записи"
    # )
    # screening_studies = models.CharField(
    #     max_length=250, verbose_name="Скрининговые исследования"
    # )

class DoctorKinderGarden(models.Model):
    pediatrist = models.ForeignKey(
        Pediatrist, on_delete=models.CASCADE, verbose_name="Педиатр",
    )
    kinder_garden = models.ForeignKey(
        KinderGarden, verbose_name="Детский сад", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.kinder_garden.name}_{self.pediatrist.name}"