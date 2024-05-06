from circuits import AbstractCircuit


class MPTPathCircuit(AbstractCircuit):
    MAX_BLOCKS = 4

    def generate_witness(self, salt, lower, upper, is_top):
        numLowerLayerBytes = len(lower)
        numUpperLayerBytes = len(upper)
        lowerLayer = list(lower) + (MAX_BLOCKS * 136 - len(lower)) * [0]
        upperLayer = list(upper) + (MAX_BLOCKS * 136 - len(upper)) * [0]

        return super().generate_witness(
            salt=str(salt),
            numLowerLayerBytes=numLowerLayerBytes,
            numUpperLayerBytes=1 if is_top else numUpperLayerBytes,
            lowerLayerBytes=lowerLayer,
            upperLayerBytes=[0] * MAX_BLOCKS * 136 if is_top else upperLayer,
            isTop=1 if is_top else 0,
        )
