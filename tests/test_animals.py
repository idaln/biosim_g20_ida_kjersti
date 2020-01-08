# -*- coding: utf-8 -*-


__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"


def test_ageing():
    """ Checks that animal is one year older than last year."""
    pass


def test_weight_loss():
    """ Checks that weight after weight loss is less than initial weight"""
    pass


def test_eat():
    """ Checks that animal has gained weight after eating."""
    pass


def test_fitness():
    """ Checks that fitness is between 0 and 1."""
    pass

def test_give_birth():
    """ Before birth we check that no birth takes place if there is only one
    animal in the cell or the mother's weight is less than a given limit.
    After birth, we check that no birth took place if the predicted baby weight
    times xi is larger than the mother's weight. If birth has taken place,
    we check that we mother has lost weight xi * baby's birth weight. """
    pass


    