from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

# TO DO LIST
# pridani fotky
# checklist
# kdo ze zaměstnanců udělal daný úkon

TELEFON_REGEX = RegexValidator(r'^[+]\d{3}( \d{3}){3}$', 'Nesprávně zadané telefonní číslo')
PSC_REGEX = RegexValidator(r'^\d{5}$', 'Nesprávně zadané poštovní směrovací číslo')


class Mistnost(models.Model):
    jmeno = models.CharField(max_length=50, verbose_name='Název místnosti',
                             error_messages={'blank': 'Jméno místnosti musí být vyplněno'})
    kapacita = models.IntegerField(default=0, verbose_name='Kapacita', help_text='Kapacita musí být vyplněna')

    class Meta:
        ordering = ['jmeno']
        verbose_name = 'Místnost'
        verbose_name_plural = 'Místnosti'

    def __str__(self):
        return self.jmeno


class Osoba(models.Model):
    STATUS = [
        ('zakaznik', 'Zákazník'),
        ('zamestnanec', 'Zaměstnanec'),
        ('brigadnik', 'Brigádník'),
        ('cvicitel', 'Cvičitel'),
    ]
    PREDPLATNE = [
        ('ucet', 'Účet'),
        ('permanentka', 'Permanentka'),
        ('clen', 'Člen'),
    ]
    status = models.CharField(max_length=15, choices=STATUS, default='zakaznik', verbose_name='Typ účtu')
    predplatne = models.CharField(max_length=15, choices=PREDPLATNE, default='ucet', verbose_name='Typ předplatného')
    jmeno = models.CharField(max_length=100, verbose_name='Jméno', help_text='')
    prijmeni = models.CharField(max_length=100, verbose_name='Přijmení', help_text='Zadejte přijmení uživatele')
    telefon = models.CharField(max_length=16, verbose_name='Telefon', validators=[TELEFON_REGEX],
                               help_text='Zadejte telefon v podobě: +420 777 777 777',)
    email = models.EmailField(unique=True, verbose_name='Email',
                              error_messages={'unique': 'E-mailová adresa musí být jedinečná',
                                              'invalid': 'Neplatná e-mailová adresa',
                                              'blank': 'Pole nesmí být prázdné'}
                              )
    adresa = models.CharField(max_length=100, blank=True, verbose_name='Adresa')
    psc = models.PositiveIntegerField(verbose_name='PSČ', help_text='Zadejte poštovní směrovací číslo (bez mezery)',
                                      validators=[PSC_REGEX])
    info = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['prijmeni', 'jmeno']
        verbose_name = 'Osoba'
        verbose_name_plural = 'Osoba'

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"


class Lekce(models.Model):
    nazev = models.CharField(max_length=100, verbose_name='Název lekce', help_text='Zadejte název lekce')
    mistnost = models.ForeignKey(Mistnost, on_delete=models.CASCADE, verbose_name='Místnosti',
                                 error_messages={'blank': 'Místnost musí být zvolena'})
    cvicitel = models.ForeignKey(Osoba, on_delete=models.CASCADE, verbose_name='Cvičitel',
                                 error_messages={'blank': 'Cvičitel musí být zvolen'})
    start = models.DateTimeField()
    konec = models.DateTimeField()

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Lekce'
        verbose_name_plural = 'Lekce'

    def __str__(self):
        return f"{self.nazev} : {self.mistnost}"


class Rezervace(models.Model):
    zakaznik = models.ForeignKey(Osoba, on_delete=models.CASCADE, verbose_name='Jméno zákazníka')
    lekce = models.ForeignKey(Lekce, on_delete=models.CASCADE, verbose_name='Název lekce')

    class Meta:
        ordering = ['zakaznik']
        verbose_name = 'Rezervace'
        verbose_name_plural = 'Rezervace'

    def __str__(self):
        return f"{self.zakaznik} registrovan na lekci {self.lekce}"
