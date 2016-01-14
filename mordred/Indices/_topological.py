from .._base import Descriptor
from .._common import Radius as _R, Diameter as _D


class Radius(Descriptor):
    '''
    radius descriptor

    Returns:
        int: graph radius
    '''

    explicit_hydrogens = False
    descriptor_name = 'Radius'

    @property
    def dependencies(self):
        return dict(
            R=_R.make_key(
                self.explicit_hydrogens,
                False, False)
        )

    def calculate(self, mol, R):
        return int(R)


class Diameter(Descriptor):
    '''
    diameter descriptor

    Returns:
        int: graph diameter
    '''

    explicit_hydrogens = False
    descriptor_name = 'Diameter'

    @property
    def dependencies(self):
        return dict(
            D=_D.make_key(
                self.explicit_hydrogens,
                False, False)
        )

    def calculate(self, mol, D):
        return int(D)


class TopologicalShapeIndex(Descriptor):
    r'''
    topological shape index descriptor

    .. math::

        I_{\rm topo} = \frac{D - R}{R}

    where
    :math:`R` is graph radius,
    :math:`D` is graph diameter.

    Returns:
        float: topological shape index
    '''

    explicit_hydrogens = False
    descriptor_name = 'TopoShapeIndex'

    @property
    def dependencies(self):
        args = [self.explicit_hydrogens, False, False]

        return dict(
            R=_R.make_key(*args),
            D=_D.make_key(*args)
        )

    def calculate(self, mol, R, D):
        return float(D - R) / float(R)


class PetitjeanIndex(Descriptor):
    r'''
    Petitjean index descriptor

    .. math::

        I_{\rm Petitjean} = \frac{D - R}{D}

    where
    :math:`R` is graph radius,
    :math:`D` is graph diameter.

    Returns:
        float: Petitjean index
    '''

    explicit_hydrogens = False
    descriptor_name = 'PetitjeanIndex'

    @property
    def dependencies(self):
        args = [self.explicit_hydrogens, False, False]

        return dict(
            R=_R.make_key(*args),
            D=_D.make_key(*args)
        )

    def calculate(self, mol, R, D):
        return float(D - R) / float(D)
