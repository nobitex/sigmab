import { groth16 } from 'snarkjs';

const VKS = require('./vks.json');

const sigmab = {
    verifyECDSA: async function (publicInputs, proof) {
        if (groth16) {
            if (await groth16.verify(VKS["ECDSA_VK"], publicInputs, proof)) {
                return true;
            } else {
                return false;
            }
        }
    },

    verifyMPTLast: async function (publicInputs, proof) {
        if (groth16) {
            if (await groth16.verify(VKS["MPT_LAST_VK"], publicInputs, proof)) {
                return true;
            } else {
                return false;
            }
        }
    },

    verifyMPTPath: async function (publicInputs, proof) {
        if (groth16) {
            if (await groth16.verify(VKS["MPT_PATH_VK"], publicInputs, proof)) {
                return true;
            } else {
                return false;
            }
        }
    },

    verifySBA: async function (publicInputs, proof) {
        if (groth16) {
            if (await groth16.verify(VKS["SBA_VK"], publicInputs, proof)) {
                return true;
            } else {
                return false;
            }
        }
    },

    verifyPOL: async function (publicInputs, proof) {
        if (groth16) {
            if (await groth16.verify(VKS["POL_VK"], publicInputs, proof)) {
                return true;
            } else {
                return false;
            }
        }
    }
}

export default { sigmab };