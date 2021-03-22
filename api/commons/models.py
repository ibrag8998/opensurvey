from django.db.models import CASCADE


def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    """ Disables polymorphic behavior on cascading delete """
    return CASCADE(collector, field, sub_objs.non_polymorphic(), using)
