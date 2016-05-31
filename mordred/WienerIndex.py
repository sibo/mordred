from ._base import Descriptor
from ._graph_matrix import DistanceMatrix


__all__ = ('WienerIndex',)


class WienerIndex(Descriptor):
    r"""Wiener index.

    :type polarity: bool
    :param polarity: use polarity Wiener index
    """

    explicit_hydrogens = False

    @classmethod
    def preset(cls):
        yield cls(False)
        yield cls(True)

    def __str__(self):
        return 'WPol' if self._polarity else 'WPath'

    __slots__ = ('_polarity',)

    def __reduce_ex__(self, version):
        return self.__class__, (self._polarity,)

    def __init__(self, polarity=False):
        self._polarity = polarity

    def dependencies(self):
        return {'D': DistanceMatrix(self.explicit_hydrogens)}

    def calculate(self, mol, D):
        if self._polarity:
            return int(0.5 * (D == 3).sum())
        else:
            return int(0.5 * D.sum())

    rtype = int
