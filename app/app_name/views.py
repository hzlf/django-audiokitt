# app_name/views.py
import sys
from django.shortcuts import redirect
from django.contrib import messages
from django.core.management import call_command
from cStringIO import StringIO

COMMAND_MAP = {
    'task-a': 'check',
    'task-b': 'showmigrations',
}

def run_task(request, task):

    if request.user.is_superuser:

        command = COMMAND_MAP.get(task)

        # call_command outputs to stdout - if you want to give feedback in admin you somehow have to capture the output
        old_stdout = sys.stdout
        sys.stdout = my_stdout = StringIO()
        call_command(command)
        sys.stdout = old_stdout

        messages.add_message(request, messages.INFO, '{}'.format(my_stdout.getvalue()))

    return redirect('/admin')