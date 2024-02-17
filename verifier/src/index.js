import { groth16 } from 'snarkjs';


const sigmab = {
    verifySigmaB: function () {
        if (groth16) { 
            alert("Groth16 is available!");
        }
        

    }
}

export default sigmab;