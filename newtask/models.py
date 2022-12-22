from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=128)


class Task(models.Model):
    name = models.CharField(max_length=128)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="tasks_created")
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="tasks_assigned")
    #ForeignKey = vezme ID Category a uloží ho - proto pouze jedna kategorie
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ISSUE_ASSIGNED = "ass"
    ISSUE_DONE = "don"
    ISSUE_CANCELED = "can"
    ISSUE_CREATED = "cre"
    ISSUE_STATE_CHOICES = (
        (ISSUE_ASSIGNED, _("Assigned")),
        (ISSUE_DONE, _("Done")),
        (ISSUE_CANCELED, _("Canceled")),
        (ISSUE_CREATED, _("Created"))
    )
    state = models.CharField(max_length=3, choices=ISSUE_STATE_CHOICES, default=ISSUE_CREATED)
    description = models.CharField(max_length=128)
    #záleží na F, zda bude prázdné nebo defaultní hodnota
    assigned_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField()

    def clean(self):
        if self.state is 'ISSUE_ASSIGNED':
            if self.assigned is None:
                raise ValidationError(_('State ISSUE ASSIGNED but no one assigned'))

