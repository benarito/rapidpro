# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import Prefetch, F
from temba.utils import chunk_list


def step_is_terminal(step, terminal_nodes):
    if step.step_uuid in terminal_nodes:
        return True  # an action set with no destination
    elif step.step_type == 'R' and step.left_on is None and step.rule_uuid is not None:
        return True  # a rule set that we never left even tho there was a matching rule
    else:
        return False


def populate_exit_type(apps, schema_editor):
    FlowRun = apps.get_model('flows', 'FlowRun')
    FlowStep = apps.get_model('flows', 'FlowStep')
    ActionSet = apps.get_model('flows', 'ActionSet')

    # grab ids of remaining inactive runs which may have been completed or restarted
    exited_run_ids = [r['pk'] for r in FlowRun.objects.filter(is_active=False, exit_type=None).values('pk')]

    if not exited_run_ids:
        return

    print "Fetched ids of %d potentially completed or stopped runs" % len(exited_run_ids)

    # grab UUIDs of all terminal action sets for quick lookups
    terminal_nodes = set([n['uuid'] for n in ActionSet.objects.filter(destination=None).values('uuid')])
    if terminal_nodes:
        print "Cached %d terminal nodes for run completion calculation" % len(terminal_nodes)

    # pre-fetch required for completion calculation
    steps_prefetch = Prefetch('steps', queryset=FlowStep.objects.order_by('arrived_on'))

    num_updated = 0

    for batch_ids in chunk_list(exited_run_ids, 1000):
        completed_ids = []
        stopped_ids = []

        for run in FlowRun.objects.filter(pk__in=batch_ids).prefetch_related(steps_prefetch):
            # get last step in this run
            steps = list(run.steps.all())
            last_step = steps[len(steps) - 1] if len(steps) > 0 else None

            if not last_step or step_is_terminal(last_step, terminal_nodes):
                completed_ids.append(run.pk)
            else:
                stopped_ids.append(run.pk)

        # update our batches of completed/stopped, using modified_on as approximate exited_on
        if completed_ids:
            FlowRun.objects.filter(pk__in=completed_ids).update(exited_on=F('modified_on'), exit_type='C')
        if stopped_ids:
            FlowRun.objects.filter(pk__in=stopped_ids).update(exited_on=F('modified_on'), exit_type='S')

        num_updated += len(completed_ids) + len(stopped_ids)

        print " > Updated %d of %d runs" % (num_updated, len(exited_run_ids))


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0042_flowrun_exit_fields'),
    ]

    operations = [
        migrations.RunPython(populate_exit_type)
    ]
