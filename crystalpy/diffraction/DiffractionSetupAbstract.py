"""
Represents a diffraction setup abstract class.
The super class should implement the methods to calculate structure factors
Except for energy, all units are in SI.
"""

from collections import OrderedDict
from copy import deepcopy
import numpy

from crystalpy.util.Vector import Vector


class DiffractionSetupAbstract(object):

    def __init__(self, geometry_type=None, crystal_name="", thickness=1e-6,
                 miller_h=1, miller_k=1, miller_l=1,
                 asymmetry_angle=0.0,
                 azimuthal_angle=0.0,
                 debye_waller=1.0):
        """
        Constructor.
        :param geometry_type: GeometryType (BraggDiffraction,...).
        :param crystal_name: The name of the crystal, e.g. Si.
        :param thickness: The crystal thickness.
        :param miller_h: Miller index H.
        :param miller_k: Miller index K.
        :param miller_l: Miller index L.
        :param asymmetry_angle: The asymmetry angle between surface normal and Bragg normal (radians).
        :param azimuthal_angle: The angle between the projection of the Bragg normal
                                on the crystal surface plane and the x axis (radians).
        """
        self._geometry_type = geometry_type
        self._crystal_name = crystal_name
        self._thickness = thickness
        self._miller_h = miller_h
        self._miller_k = miller_k
        self._miller_l = miller_l
        self._asymmetry_angle = asymmetry_angle  # degrees.
        self._azimuthal_angle = azimuthal_angle  # degrees
        self._debyeWaller = debye_waller

    #
    # setters and getters
    #
    def geometryType(self):
        """
        Returns the GeometryType, e.g. BraggDiffraction, LaueTransmission,...
        :return: The GeometryType.
        """
        return self._geometry_type

    def crystalName(self):
        """
        Return the crystal name, e.g. Si.
        :return: Crystal name.
        """
        return self._crystal_name

    def thickness(self):
        """
        Returns the crystal thickness,
        :return: The crystal thickness.
        """
        return self._thickness

    def millerH(self):
        """
        Returns the Miller H index.
        :return: Miller H index.
        """
        return self._miller_h

    def millerK(self):
        """
        Returns the Miller K index.
        :return: Miller K index.
        """
        return self._miller_k

    def millerL(self):
        """
        Returns the Miller L index.
        :return: Miller L index.
        """
        return self._miller_l

    def asymmetryAngle(self):
        """
        Returns the asymmetry angle between surface normal and Bragg normal.
        :return: Asymmetry angle.
        """
        return self._asymmetry_angle

    def azimuthalAngle(self):
        """
        Returns the angle between the Bragg normal projection on the crystal surface plane and the x axis.
        :return: Azimuthal angle.
        """
        return self._azimuthal_angle

    #
    # abstract methods to be implemented by the super class
    #
    def angleBragg(self, energy=8000.0):
        """
        Returns the Bragg angle for a given energy.
        :param energy: Energy to calculate the Bragg angle for.
        :return: Bragg angle.
        """
        raise NotImplementedError()

    def F0(self, energy=8000.0):
        """
        Calculate F0 from Zachariasen.
        :param energy: photon energy in eV.
        :return: F0
        """
        raise NotImplementedError()


    def FH(self, energy=8000.0):
        """
        Calculate FH from Zachariasen.
        :param energy: photon energy in eV.
        :return: FH
        """

        raise NotImplementedError()

    def FH_bar(self, energy=8000.0):
        """
        Calculate FH_bar from Zachariasen.
        :param energy: photon energy in eV.
        :return: FH_bar
        """

        raise NotImplementedError()

    def dSpacing(self):
        """
        Returns the lattice spacing d.
        :return: Lattice spacing.
        """

        raise NotImplementedError()


    def unitcellVolume(self):
        """
        Returns the unit cell volume.

        :return: Unit cell volume
        """
        raise NotImplementedError()

    #
    #
    #

    def normalBragg(self,return_normalized=False):
        """
        Calculates the B_H vecor, normal on the reflection lattice plane, with modulus 2 pi / d_spacing .

        normal to Bragg planes obtained by rotating vnor an angle equal to minuns asymmetry angle (-alphaXOP)
        around X using rodrigues rotation (in the screw direction (cw) when looking in the axis direction),
        and then an angle phi (azimuthal angle) around Z

        :param return_normalized: if True the returned vector is normalized.
        :return: B_H vector
        """
        # Edoardo: I use the geometrical convention from
        # M.Sanchez del Rio et al., J.Appl.Cryst.(2015). 48, 477-491.


        g_modulus = 2.0 * numpy.pi / (self.dSpacing() * 1e-10)
        # Let's start from a vector parallel to the surface normal (z axis).
        temp_normal_bragg = Vector(0, 0, 1).scalarMultiplication(g_modulus)

        # Let's now rotate this vector of an angle alphaX around the y axis (according to the right-hand-rule).
        alpha_x = self.asymmetryAngle()
        axis = self.parallelSurface().crossProduct(self.normalSurface())  # should be Vector(1, 0, 0)
        temp_normal_bragg = temp_normal_bragg.rotateAroundAxis(axis, -alpha_x)

        # Let's now rotate this vector of an angle phi around the z axis (following the ISO standard 80000-2:2009).
        phi = self.azimuthalAngle()
        normal_bragg = temp_normal_bragg.rotateAroundAxis(Vector(0, 0, 1), phi)

        if return_normalized:
            return normal_bragg.getNormalizedVector()
        else:
            return normal_bragg

    def normalSurface(self):
        """
        Returns the normal to the surface. (0,0,1) by definition.
        :return: Vector instance with Surface normal Vnor.
        """
        # Edoardo: I use the geometrical convention from
        # M.Sanchez del Rio et al., J.Appl.Cryst.(2015). 48, 477-491.
        normal_surface = Vector(0, 0, 1)
        return normal_surface

    def parallelSurface(self):
        """
        Returns the direction parallel to the crystal surface. (0,1,0) by definition.
        :return: Vector instance with Surface normal Vtan.
        """
        # Edoardo: I use the geometrical convention from
        # M.Sanchez del Rio et al., J.Appl.Cryst.(2015). 48, 477-491.
        parallel_surface = Vector(0, 1, 0)
        return parallel_surface

    def toDictionary(self):
        """
        Returns this setup in InfoDictionary form.
        :return: InfoDictionary form of this setup.
        """
        info_dict = OrderedDict()
        info_dict["Geometry Type"] = self.geometryType().description()
        info_dict["Crystal Name"] = self.crystalName()
        info_dict["Thickness"] = str(self.thickness())
        info_dict["Miller indices (h,k,l)"] = "(%i,%i,%i)" % (self.millerH(),
                                                              self.millerK(),
                                                              self.millerL())
        info_dict["Asymmetry Angle"] = str(self.asymmetryAngle())
        info_dict["Azimuthal Angle"] = str(self.azimuthalAngle())

        return info_dict

    def getK0(self, energy):
        return self.incomingPhotonDirection(energy,0.0)

    def incomingPhotonDirection(self, energy, deviation):
        """
        Calculates the direction of the incoming photon. Parallel to k_0.
        :param energy: Energy to calculate the Bragg angle for.
        :param deviation: Deviation from the Bragg angle.
        :return: Direction of the incoming photon.
        """
        # Edoardo: I use the geometrical convention from
        # M.Sanchez del Rio et al., J.Appl.Cryst.(2015). 48, 477-491.

        # # DONE: vectorize this part as in https://github.com/srio/CRYSTAL/blob/master/crystal3.F90
        # # angle between the incoming photon direction and the surface normal (z axis).
        # # a positive deviation means the photon direction lies closer to the surface normal.
        # angle = numpy.pi / 2.0 - (self.angleBragg(energy) + self.asymmetryAngle() + deviation)
        # # the photon comes from left to right in the yz plane.
        # photon_direction_old = Vector(0,numpy.sin(angle),-numpy.cos(angle))


        # Let's now rotate -BH of an angle (90-BraggAngle) around the x axis
        minusBH = self.normalBragg().scalarMultiplication(-1.0)
        minusBH = minusBH.getNormalizedVector()
        axis = self.parallelSurface().crossProduct(self.normalSurface())  # should be Vector(1, 0, 0)
        # TODO check why deviation has minus
        photon_direction = minusBH.rotateAroundAxis(axis, (numpy.pi/2)-self.angleBragg(energy)-deviation)

        # print("PHOTON DIRECTION ",photon_direction_old.components(),photon_direction.components())
        # Let's now rotate this vector of an angle phi around the z axis (following the ISO standard 80000-2:2009).
        # photon_direction = photon_direction.rotateAroundAxis(Vector(0, 0, 1), self.azimuthalAngle() )

        return photon_direction

    def __eq__(self, candidate):
        """
        Determines if two setups are equal.
        :param candidate: Instance to compare to.
        :return: True if the two instances are equal. False otherwise.
        """
        if self._geometry_type != candidate.geometryType():
            return False

        if self._crystal_name != candidate.crystalName():
            return False

        if self._thickness != candidate.thickness():
            return False

        if self._miller_h != candidate.millerH():
            return False

        if self._miller_k != candidate.millerK():
            return False

        if self._miller_l != candidate.millerL():
            return False

        if self._asymmetry_angle != candidate.asymmetryAngle():
            return False

        if self._azimuthal_angle != candidate.azimuthalAngle():
            return False

        # All members are equal so are the instances.
        return True

    def __ne__(self, candidate):
        """
        Determines if two setups are not equal.
        :param candidate: Instance to compare to.
        :return: True if the two instances are not equal. False otherwise.
        """
        return not self == candidate

    def clone(self):
        """
        Returns a copy of this instance.
        :return: A copy of this instance.
        """
        return deepcopy(self)

    def deviationOfIncomingPhoton(self, photon_in):
        """
        Given an incoming photon its deviation from the Bragg angle is returned.
        :param photon_in: Incoming photon.
        :return: Deviation from Bragg angle.
        """
        # this holds for every incoming photon-surface normal plane.
        total_angle = photon_in.unitDirectionVector().angle(self.normalBragg())

        energy = photon_in.energy()
        angle_bragg = self.angleBragg(energy)

        deviation = total_angle - angle_bragg - numpy.pi / 2
        return deviation

if __name__ == "__main__":
    a = DiffractionSetupAbstract(geometry_type=0, crystal_name="Si", thickness=1e-5,
                 miller_h=1, miller_k=1, miller_l=1,
                 asymmetry_angle=0.0,
                 azimuthal_angle=0.0,)

    print(a.angleBragg(1000))