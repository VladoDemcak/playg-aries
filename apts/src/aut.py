"""AUT (Agent Under Test) Backchannel Implementation."""

import aiohttp
import time
import json
import requests
import base64
from urllib.parse import urlparse, parse_qs

from protocol_tests.backchannel import (
    Backchannel, SubjectConnectionInfo
)
from protocol_tests.connection.backchannel import ConnectionsBackchannel
from protocol_tests.discover_features.backchannel import DiscoverFeaturesBackchannel
from protocol_tests.issue_credential.backchannel import IssueCredentialBackchannel


class AUTBackchannel(Backchannel, ConnectionsBackchannel, DiscoverFeaturesBackchannel, IssueCredentialBackchannel):
    """
    Backchannel for communicating with the AUT (Agent Under Test)
    """

    async def setup(self, config, suite):
        """
        Here is where you perform any setup required to run the test suite to communicate with your AUT (Agent Under Test).
        This includes resetting the state of your AUT from any previous runs.
        """
        print("Setup: config: {}".format(config))

    async def new_connection(self, offer, parameters=None):
        """
        The AUT is receiving a connection offer from APTS.
        The AUT must accept the offer and return a SubjectConnectionInfo object.
        """
        print("The AUT received a connection offer: {}".format(offer))
        offer_asdict = offer._asdict()
        data = {
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
            "recipientKeys": [
                offer_asdict['verkey']
            ],
            "label": offer_asdict['label'],
            "alias": offer_asdict['did'],
            "serviceEndpoint": offer_asdict['endpoint']
        }
        post_call = requests.post("http://172.26.0.7:8081/connections/receive-invitation?auto_accept=true", json=data).json()
        didid = requests.get("http://172.26.0.7:8081/wallet/did?did="+post_call['my_did']).json()

        # return SubjectConnectionInfo(did, recipients, routing_keys, endpoint)
        return SubjectConnectionInfo(post_call['my_did'], [didid['results'][0]['verkey']],[didid['results'][0]['verkey']],  'http://172.26.0.7:8001')

    async def connections_v1_0_inviter_start(self) -> str:
        """
        The AUT creates an invitation and returns the invitation URL.
        """

        post_call = requests.post("http://172.26.0.7:8081/connections/create-invitation?auto_accept=true").json()
        return post_call['invitation_url']

    async def connections_v1_0_invitee_start(self, invitation_url):
        """
        The AUT accepts an invitation URL.
        """
        print("Invitation URL: {}".format(invitation_url))
        parsed_url = urlparse(invitation_url)
        parsed = parse_qs(parsed_url.query)
        invitation = base64.b64decode(parsed['c_i'][0])

        connection_id = None
        post_call = requests.post("http://172.26.0.7:8081/connections/receive-invitation", data=invitation).json()
        connection_id = post_call['connection_id']

        requests.post("http://172.26.0.7:8081/connections/"+connection_id+"/accept-invitation").json()


    async def discover_features_v1_0_requester_start(self, conn, query=".*", comment=""):
        """
        The AUT sends a discover features query over the 'conn' connection.
        Use either conn.did or conn.verkey_b58 to look up the connection in the AUT.
        """
        print("Discover features: conn={}", conn)  # TODO check with original
        raise Exception("TODO: implement")

    async def issue_credential_v1_0_issuer_create_cred_schema(self, name, version, attrNames) -> str:
        """
        The AUT creates a credential schema and returns the schema_id.
        """
        data = {
            'attributes': attrNames,
            'schema_version': version,
            "schema_name": name
        }
        post_call = requests.post("http://172.26.0.7:8081/schemas", json=data).json()
        return post_call['schema_id']

    async def issue_credential_v1_0_issuer_create_cred_def(self, schema_id: str) -> str:
        """
        The AUT creates a credential definition and returns the cred_def_id.
        """
        data = {
            'tag': 'ID',
            'schema_id': schema_id,
            #   'support_revocation': False  # TODO Looks like there is no way to test revocable credentials
        }
        response = requests.post("http://172.26.0.7:8081/credential-definitions", json=data)
        return response.json()['credential_definition_id']

    async def issue_credential_v1_0_issuer_send_cred_offer(self, conn, cred_def_id, attrs) -> str:
        """
        The AUT sends a credential offer to APTS.
        Use either conn.did or conn.verkey_b58 to look up the connection in the AUT.
        """

        response = requests.get("http://172.26.0.7:8081/connections?invitation_key="+conn.verkey_b58).json()
        connection_id = response['results'][0]['connection_id']
        offer = {
            "comment": "strinfaeg",
            "credential_preview": {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
                "attributes": [
                    {
                        'name': 'name',
                        'value': 'Alice'
                    },
                    {
                        'name': 'age',
                        'value': '21'
                    }
                ]
            },
            "connection_id": connection_id,
            "auto_remove": False,
            "trace": False,
            "cred_def_id": cred_def_id,
            "auto_issue": True
        }

        post_call = requests.post("http://172.26.0.7:8081/issue-credential/send-offer", json=offer)
        # raise Exception("TODO: implement")

    async def issue_credential_v1_0_holder_accept_cred_offer(self, id: str):
        """
        The AUT as the holder accepts a credential offer from APTS.
        Use either conn.did or conn.verkey_b58 to look up the connection in the AUT.
        The 'id' parameter is the "@id" field of the "offer-credential" message.
        """
        raise Exception("TODO: implement")

    async def issue_credential_v1_0_holder_verify_cred_is_stored(self, id: str):
        """
        The AUT as the holder verifies that credential 'id' was stored successfully.
        Throw an exception if the credential was NOT stored successfully.
        """
        raise Exception("TODO: implement")

    async def present_proof_v1_0_verifier_send_proof_request(self, conn, proof_req) -> str:
        """
        The AUT as the verifier sends a proof request via a "request-presentation" message to APTS.
        """
        raise Exception("TODO: implement")

    async def present_proof_v1_0_prover_send_proof(self, id):
        """
        The AUT as the prover sends a proof via a "presentation" message to APTS.
        """
        raise Exception("TODO: implement")

    async def present_proof_v1_0_verifier_verify_proof(self, id: str) -> [dict]:
        """
        The AUT as the verifier verifies the proof sent to it via thread 'id'.
        """
        raise Exception("TODO: implement")
