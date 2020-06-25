# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ResultResidue(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, qmean: float=None, pdb_resnum: int=None, uniprot_resnum: int=None):  # noqa: E501
        """ResultResidue - a model defined in Swagger

        :param qmean: The qmean of this ResultResidue.  # noqa: E501
        :type qmean: float
        :param pdb_resnum: The pdb_resnum of this ResultResidue.  # noqa: E501
        :type pdb_resnum: int
        :param uniprot_resnum: The uniprot_resnum of this ResultResidue.  # noqa: E501
        :type uniprot_resnum: int
        """
        self.swagger_types = {
            'qmean': float,
            'pdb_resnum': int,
            'uniprot_resnum': int
        }

        self.attribute_map = {
            'qmean': 'qmean',
            'pdb_resnum': 'pdb_resnum',
            'uniprot_resnum': 'uniprot_resnum'
        }
        self._qmean = qmean
        self._pdb_resnum = pdb_resnum
        self._uniprot_resnum = uniprot_resnum

    @classmethod
    def from_dict(cls, dikt) -> 'ResultResidue':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The result_residue of this ResultResidue.  # noqa: E501
        :rtype: ResultResidue
        """
        return util.deserialize_model(dikt, cls)

    @property
    def qmean(self) -> float:
        """Gets the qmean of this ResultResidue.


        :return: The qmean of this ResultResidue.
        :rtype: float
        """
        return self._qmean

    @qmean.setter
    def qmean(self, qmean: float):
        """Sets the qmean of this ResultResidue.


        :param qmean: The qmean of this ResultResidue.
        :type qmean: float
        """

        self._qmean = qmean

    @property
    def pdb_resnum(self) -> int:
        """Gets the pdb_resnum of this ResultResidue.


        :return: The pdb_resnum of this ResultResidue.
        :rtype: int
        """
        return self._pdb_resnum

    @pdb_resnum.setter
    def pdb_resnum(self, pdb_resnum: int):
        """Sets the pdb_resnum of this ResultResidue.


        :param pdb_resnum: The pdb_resnum of this ResultResidue.
        :type pdb_resnum: int
        """

        self._pdb_resnum = pdb_resnum

    @property
    def uniprot_resnum(self) -> int:
        """Gets the uniprot_resnum of this ResultResidue.


        :return: The uniprot_resnum of this ResultResidue.
        :rtype: int
        """
        return self._uniprot_resnum

    @uniprot_resnum.setter
    def uniprot_resnum(self, uniprot_resnum: int):
        """Sets the uniprot_resnum of this ResultResidue.


        :param uniprot_resnum: The uniprot_resnum of this ResultResidue.
        :type uniprot_resnum: int
        """

        self._uniprot_resnum = uniprot_resnum
