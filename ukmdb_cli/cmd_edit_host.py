#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330
"""usage: ukm_cli [--debug ...] edit_host [--help] <fqdn>

Arguments:
  fqdn                fqdn of the host

Options:
  -h --help                Show this edit_host command screen.
  -d --debug               Show debug information.
"""
import logging
from schema import Schema, Optional, And, Use
from ukmdb_worker import worker
from ukmdb_cli.cmd_base import conv_dict

UKMDB_LOG = logging.getLogger("ukmdb")

SCHEMA = Schema({
    'edit_host': bool,
    '<fqdn>': Use(str),
    Optional('--help'): bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
})


def cmd(args):
    UKMDB_LOG.debug("starting command 'edit_host'")
    (msg_uuid, obj_dict, expires) = conv_dict('kvm@ikom',  # app_domain
                                              'vhost',  # app_type
                                              'kvm@adm000-kvm16f',  # app_name
                                              args['<fqdn>'],  # app_id
                                              {'tags': [
                                                  'ddd', 'eee', 'fff']},  # props
                                              'Alien vs. Predator',  # comment
                                              )
    worker.edit_object.apply_async((obj_dict,),
                                   exchange='ukmdb_all_in',
                                   expires=expires)
    UKMDB_LOG.debug(str(args))
    UKMDB_LOG.debug("command 'edit_host' stopped")
    return str(msg_uuid)
