import factory
import models.input
from locust import FastHttpUser, task
from loguru import logger


class AssurlandUser(FastHttpUser):
    @task
    def simulate(self):
        with factory.Faker.override_default_locale("fr_FR"):
            simulation = models.input.SimulationFactory()
            with self.rest(
                headers={"X-API-KEY": "XJyuf2bGtdp-54m978Qkym9LN_exf2VvB2EUJ-W8Nco"},
                method="POST",
                url="/simulation",
                data=simulation.model_dump_json(),
            ) as resp:
                if resp.status_code != 200:
                    logger.error(resp.js)
