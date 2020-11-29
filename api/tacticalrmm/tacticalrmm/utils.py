import json
import os
import subprocess
from typing import List
from loguru import logger

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from agents.models import Agent

logger.configure(**settings.LOG_CONFIG)

notify_error = lambda msg: Response(msg, status=status.HTTP_400_BAD_REQUEST)

WEEK_DAYS = {
    "Sunday": 0x1,
    "Monday": 0x2,
    "Tuesday": 0x4,
    "Wednesday": 0x8,
    "Thursday": 0x10,
    "Friday": 0x20,
    "Saturday": 0x40,
}


def get_bit_days(days: List[str]) -> int:
    bit_days = 0
    for day in days:
        bit_days |= WEEK_DAYS.get(day)
    return bit_days


def reload_nats():
    users = [{"user": "tacticalrmm", "password": settings.SECRET_KEY}]
    agents = Agent.objects.prefetch_related("user").only("pk", "agent_id")
    for agent in agents:
        try:
            users.append(
                {"user": agent.agent_id, "password": agent.user.auth_token.key}
            )
        except:
            logger.critical(
                f"{agent.hostname} does not have a user account, NATS will not work"
            )

    if not settings.DOCKER_BUILD:
        domain = settings.ALLOWED_HOSTS[0].split(".", 1)[1]
        cert_path = f"/etc/letsencrypt/live/{domain}"
    else:
        cert_path = "/opt/tactical/certs"

    config = {
        "tls": {
            "cert_file": f"{cert_path}/fullchain.pem",
            "key_file": f"{cert_path}/privkey.pem",
        },
        "authorization": {"users": users},
        "max_payload": 2048576005,
    }

    conf = os.path.join(settings.BASE_DIR, "nats-rmm.conf")
    with open(conf, "w") as f:
        json.dump(config, f)

    if not settings.DOCKER_BUILD:
        subprocess.run(
            ["/usr/local/bin/nats-server", "-signal", "reload"], capture_output=True
        )
