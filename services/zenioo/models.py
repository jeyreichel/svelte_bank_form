from enum import Enum
from typing import assert_never

from common.models.simulation import Garantie


class PackageGaranties(Enum):
    DC = "DC"  # Décès PTIA
    DC_IPT = "DC-IPT"  # Décès PTIA, IPT ITT
    DC_IPT_MNO = "DC-IPT-MNO"  # Décès PTIA, IPT ITT, Dos et Psy
    DC_IPT_IPP = "DC-IPT-IPP"  # Décès PTIA, IPT ITT, IPP
    DC_IPT_IPP_MNO = "DC-IPT-IPP-MNO"  # Décès PTIA, IPT ITT, IPP, Dos et Psy
    DC_IPT_IPPRO = "DC-IPT-IPPRO"  # Décès PTIA, IPT ITT, IP PRO
    DC_IPT_IPPRO_MNO = "DC-IPT-IPPRO-MNO"  # Décès PTIA, IPT ITT, IP PRO, Dos et Psy

    @classmethod
    def to_zenioo(cls, garantie: Garantie):
        match garantie:
            case Garantie.DC_PTIA:
                return PackageGaranties.DC
            case Garantie.DC_PTIA_IPT_ITT:
                return PackageGaranties.DC_IPT
            case Garantie.DC_PTIA_IPT_ITT_MNO:
                return PackageGaranties.DC_IPT_MNO
            case Garantie.DC_PTIA_IPT_ITT_IPP:
                return PackageGaranties.DC_IPT_IPP
            case Garantie.DC_PTIA_IPT_ITT_IPP_MNO:
                return PackageGaranties.DC_IPT_IPP_MNO
            case _ as unreachable:
                assert_never(unreachable)

    def from_zenioo(self) -> Garantie:
        match self:
            case PackageGaranties.DC:
                return Garantie.DC_PTIA
            case PackageGaranties.DC_IPT_MNO:
                return Garantie.DC_PTIA_IPT_ITT_MNO
            case PackageGaranties.DC_IPT_IPP_MNO:
                return Garantie.DC_PTIA_IPT_ITT_IPP_MNO
            case PackageGaranties.DC_IPT:
                return Garantie.DC_PTIA_IPT_ITT
            case PackageGaranties.DC_IPT_IPP:
                return Garantie.DC_PTIA_IPT_ITT_IPP
            case PackageGaranties.DC_IPT_IPPRO | PackageGaranties.DC_IPT_IPPRO_MNO:
                raise ValueError("Cette garantie n'est pas proposée")
            case _ as unreachable:
                assert_never(unreachable)
