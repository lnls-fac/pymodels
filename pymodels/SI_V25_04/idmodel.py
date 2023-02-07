"""Insertion Device Models."""

from pyaccel import elements as _pyacc_ele


class IDModel:
    """ID Model (currently based on Kickmap files)."""
    class SUBSECTIONS:
        # See https://wiki-sirius.lnls.br/mediawiki/index.php/Table:Storage_ring_straight_sections_allocation
        ID05SA = 'ID05SA'
        ID06SB = 'ID06SB'
        ID07SP = 'ID07SP'
        ID08SB = 'ID08SB'
        ID09SA = 'ID09SA'
        ID10SB = 'ID10SB'
        ID11SP = 'ID11SP'
        ID14SB = 'ID14SB'
        ID17SA = 'ID17SA'
        ALL = (
            ID05SA, ID06SB, ID07SP, ID08SB, ID09SA,
            ID10SB, ID11SP, ID14SB, ID17SA)

    def __init__(self,
            subsec, file_name, fam_name=None,
            nr_steps=1, rescale_kicks=1.0, rescale_length=1.0,
            termination_kicks=None):
        if subsec not in IDModel.SUBSECTIONS.ALL:
            raise ValueError('Invalid subsection definition')
        if termination_kicks is None:
            termination_kicks = [0, 0, 0, 0]
        self._subsec = subsec
        self._file_name = file_name
        self._fam_name = fam_name or 'ID'
        self._nr_steps = nr_steps
        self._rescale_kicks = rescale_kicks
        self._rescale_length = rescale_length
        self._termination_kicks = termination_kicks

    @property
    def subsec(self):
        """Subsection where ID is installed."""
        return self._subsec

    @property
    def file_name(self):
        """ID kickmap filename."""
        return self._file_name

    @property
    def fam_name(self):
        """Model family name of ID."""
        return self._fam_name

    @property
    def nr_steps(self):
        """Nr of steps used in ID kickmap."""
        return self._nr_steps

    @property
    def rescale_kicks(self):
        """Kick rescale factor applied to kickmap data from file.."""
        return self._rescale_kicks

    @property
    def rescale_length(self):
        """Length rescale factor applied to kickmap data from file.."""
        return self._rescale_length

    @property
    def kickx_upstream(self):
        """Return kick in [T2m2] units."""
        return self._rescale_kicks * self._termination_kicks[0]

    @property
    def kicky_upstream(self):
        """Return kick in [T2m2] units."""
        return self._rescale_kicks * self._termination_kicks[1]

    @property
    def kickx_downstream(self):
        """Return kick in [T2m2] units."""
        return self._rescale_kicks * self._termination_kicks[2]

    @property
    def kicky_downstream(self):
        """Return kick in [T2m2] units."""
        return self._rescale_kicks * self._termination_kicks[3]

    def get_half_kickmap(self):
        """Return trackcpp half-kickmap withou border kicks."""
        # NOTE: rescale_length is multipled by the total length in kickmap
        # file. An additional 0.5 factor is in order to account for half
        # kickmap model. Same for kicks rescaling.
        half_rescale_length = 0.5 * self._rescale_length
        half_rescale_kicks = 0.5 * self._rescale_kicks
        kickmap = _pyacc_ele.kickmap(
            fam_name=self._fam_name,
            kicktable_fname=self._file_name,
            nr_steps=self._nr_steps,
            rescale_kicks=half_rescale_kicks,
            rescale_length=half_rescale_length)
        return kickmap

    def __str__(self):
        """."""
        strs = ''
        strs += f'fam_name        : {self.fam_name}\n'
        strs += f'subector        : {self.subsec}\n'
        strs += f'file_name       : {self.file_name}\n'
        strs += f'nr_steps        : {self.nr_steps}\n'
        strs += f'rescale_kicks   : {self.rescale_kicks}\n'
        strs += f'rescale_length  : {self.rescale_length}\n'
        strs += f'kickx_upstream  : {self.kickx_upstream}\n'
        strs += f'kicky_upstream  : {self.kicky_upstream}\n'
        strs += f'kickx_downtream : {self.kickx_downstream}\n'
        strs += f'kicky_downtream : {self.kicky_downstream}'
        return strs
