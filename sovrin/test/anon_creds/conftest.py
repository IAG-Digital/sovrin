import json

import pytest
from anoncreds.protocol.utils import encodeAttrs

from plenum.client.signer import SimpleSigner
from plenum.common.txn import ORIGIN, TARGET_NYM, ROLE, TXN_TYPE, DATA, TXN_ID
from plenum.common.util import randomString, adict
from plenum.test.eventually import eventually
from plenum.test.helper import genHa, checkSufficientRepliesRecvd, genTestClient
from sovrin.common.txn import USER, NYM
from sovrin.test.helper import submitAndCheck


# TODO Make a fixture for creating a client with a anon-creds features
#  enabled.

@pytest.fixture(scope="module")
def issuerSigner():
    signer = SimpleSigner()
    return signer


@pytest.fixture(scope="module")
def proverSigner():
    signer = SimpleSigner()
    return signer


@pytest.fixture(scope="module")
def verifierSigner():
    signer = SimpleSigner()
    return signer


@pytest.fixture(scope="module")
def issuerHA():
    return genHa()


@pytest.fixture(scope="module")
def proverHA():
    return genHa()


@pytest.fixture(scope="module")
def verifierHA():
    return genHa()


@pytest.fixture(scope="module")
def proverAttributeNames():
    return sorted(['name', 'age', 'sex', 'country'])


@pytest.fixture(scope="module")
def proverAttributes():
    return {'name': 'Mario', 'age': '25', 'sex': 'Male', 'country': 'Italy'}


@pytest.fixture(scope="module")
def encodedProverAttributes(proverAttributes):
    return encodeAttrs(proverAttributes)


@pytest.fixture(scope="module")
def addedIPV(looper, genned, addedSponsor, sponsor, sponsorSigner,
             issuerSigner, proverSigner, verifierSigner, issuerHA, proverHA,
             verifierHA):
    """
    Creating nyms for issuer, prover and verifier on Sovrin.
    """
    sponsNym = sponsorSigner.verstr
    iNym = issuerSigner.verstr
    pNym = proverSigner.verstr
    vNym = verifierSigner.verstr

    for nym, ha in ((iNym, issuerHA), (pNym, proverHA), (vNym, verifierHA)):
        op = {
            ORIGIN: sponsNym,
            TARGET_NYM: nym,
            TXN_TYPE: NYM,
            ROLE: USER,
            DATA: json.dumps({'ha': ha})
        }
        submitAndCheck(looper, sponsor, op, identifier=sponsNym)

# @pytest.fixture(scope="module")
# def issuerAddedPK_I(addedIPV, looper, nodeSet, issuerAdded,
#                     proverAttributeNames):
#     req, = addedIssuer.addPkiToLedger(proverAttributeNames)
#     looper.run(eventually(checkSufficientRepliesRecvd,
#                           issuerAdded.inBox,
#                           req.reqId,
#                           nodeSet.f,
#                           retryWait=1,
#                           timeout=5))
#     reply, = addedIssuer.getReply(req.reqId)
#     r = adict()
#     r[TXN_ID] = reply.result[TXN_ID]
#     return r