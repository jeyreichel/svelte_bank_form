from types import NoneType
from typing import Generator

import httpx
from config import (
    CLE_PARTENAIRE_ZENIOO,
    CODE_COURTIER_ZENIOO,
    CODE_PARTENAIRE_ZENIOO,
    LOGIN_COURTIER_ZENIOO,
    ZENIOO_API_URL,
)


class Auth(httpx.Auth):
    requires_response_body = True

    def __init__(self):
        self.token = None

    def build_refresh_request(self) -> httpx.Request:
        uri = "Mortgage/rest/v1/GetToken"
        request = httpx.Request(
            method="POST",
            url=ZENIOO_API_URL + uri,
            json={
                "Cle_partenaire": CLE_PARTENAIRE_ZENIOO,
                "Code_partenaire": CODE_PARTENAIRE_ZENIOO,
            },
        )
        return request

    def update_token(self, response: httpx.Response) -> NoneType:
        if response.status_code == 200:
            re = response.json()
            self.token = re["GetTokenResponse"]["token"]
        else:
            raise Exception("IMPOSSIBLE DE SE CONNECTER A ZENIOO")

    def auth_flow(self, request) -> Generator[httpx.Request, httpx.Response, None]:
        if self.token is None:
            refresh_response = yield self.build_refresh_request()
            self.update_token(refresh_response)

        request.headers["Authorization"] = self.token
        response = yield request

        too_many_requests = False
        try:
            response_json = response.json()
            if response_json["erreur"] == "400":
                too_many_requests = True
        except KeyError:
            pass

        if response.status_code in [403, 401, 400] or too_many_requests:
            refresh_response = yield self.build_refresh_request()
            self.update_token(refresh_response)

            request.headers["Authorization"] = self.token
            yield request


client = httpx.AsyncClient(auth=Auth(), timeout=30)


async def _make_request(uri, content: dict[str, str]):
    return await client.post(ZENIOO_API_URL + uri, json=content)


async def send_simulation(data):
    uri = "Mortgage/rest/v1/GetTariffs"
    return await _make_request(uri, data)


async def send_subscription(data):
    uri = "Mortgage/rest/v1/GoToSubscriptionForm"
    return await _make_request(uri, data)


def get_data_for_zenioo(
    contrat, beneficiaires, simulation, prets, garanties
) -> dict[str, str]:
    return {
        "login_courtier_zenioo": LOGIN_COURTIER_ZENIOO,
        "code_courtier_zenioo": CODE_COURTIER_ZENIOO,
        "contrat": contrat,
        "beneficiaires": beneficiaires,
        "prets": prets,
        "garanties": garanties,
    } | simulation
