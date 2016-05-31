from collections import defaultdict

from rdkit.Chem import HybridizationType

from ._base import Descriptor


__all__ = (
    'CarbonTypes', 'HybridizationRatio',
)


class CarbonTypesBase(Descriptor):
    explicit_hydrogens = False
    kekulize = True


class CarbonTypesCache(CarbonTypesBase):
    __slots__ = ()

    def __reduce_ex__(self, version):
        return self.__class__, ()

    _hybridization = {
        HybridizationType.SP: 1,
        HybridizationType.SP2: 2,
        HybridizationType.SP3: 3,
        HybridizationType.SP3D: 3,
        HybridizationType.SP3D2: 3,
    }

    def calculate(self, mol):
        r = defaultdict(lambda: defaultdict(int))
        for a in mol.GetAtoms():
            if a.GetAtomicNum() != 6:
                continue

            carbon = sum(
                other.GetAtomicNum() == 6
                for other in a.GetNeighbors()
            )

            SP = self._hybridization.get(a.GetHybridization())

            r[SP][carbon] += 1

        return r


class CarbonTypes(CarbonTypesBase):
    r"""carbon types descriptor.

    :type nCarbon: int
    :param nCarbon: count `n`-carbon bonded carbon

    :type SP: int
    :param SP: count :math:`{\rm SP}n` carbon
    """

    @classmethod
    def preset(cls):
        return map(lambda args: cls(*args), [
            (1, 1), (2, 1),
            (1, 2), (2, 2), (3, 2),
            (1, 3), (2, 3), (3, 3), (4, 3),
        ])

    def __str__(self):
        return 'C{}SP{}'.format(self._nCarbon, self._SP)

    __slots__ = ('_nCarbon', '_SP',)

    def __reduce_ex__(self, version):
        return self.__class__, (self._nCarbon, self._SP)

    def __init__(self, nCarbon=1, SP=3):
        assert SP in [1, 2, 3]

        self._nCarbon = nCarbon
        self._SP = SP

    def dependencies(self):
        return {'CT': CarbonTypesCache()}

    def calculate(self, mol, CT):
        return CT[self._SP][self._nCarbon]

    rtype = int


class HybridizationRatio(CarbonTypesBase):
    r"""hybridization ratio descriptor.

    .. math::

        {\rm HybRatio} = \frac{N_{\rm SP3}}{N_{\rm SP2} + N_{\rm SP3}}

    :returns: NaN when :math:`N_{\rm SP2} + N_{\rm SP3} = 0`.
    """

    __slots__ = ()

    @classmethod
    def preset(cls):
        yield cls()

    def __str__(self):
        return 'HybRatio'

    def __reduce_ex__(self, version):
        return self.__class__, ()

    def dependencies(self):
        return {'CT': CarbonTypesCache()}

    def calculate(self, mol, CT):
        Nsp3 = float(sum(CT[3].values()))
        Nsp2 = float(sum(CT[2].values()))

        if Nsp3 == Nsp2 == 0:
            return float('nan')

        return Nsp3 / (Nsp2 + Nsp3)

    rtype = float
