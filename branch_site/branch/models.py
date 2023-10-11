
from django.db import models


class Peoples(models.Model):
    full_name = models.TextField(blank=True, null=True)
    born_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    source_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peoples'

    def __str__(self):
        return f' {self.id}. {self.full_name} ( {self.born_date} : {self.death_date})'


class Relationships(models.Model):
    parent = models.ForeignKey(Peoples, models.DO_NOTHING, blank=True, null=True)
    child = models.ForeignKey(Peoples, models.DO_NOTHING, related_name='relationships_child_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relationships'

    def __str__(self):
        return f'Relationship {self.id}: {self.parent} -> {self.child}'
