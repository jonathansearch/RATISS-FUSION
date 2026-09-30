"""Tests RATISS-FUSION : Bosch-Hale réel, froid=0 events, chaud=burn. MIT."""
import os as _os, pathlib as _pl  # RATISS: chemins portables (dépôts clonés côte à côte, ou RATISS_HOME)
_RATISS_HOME = _os.environ.get('RATISS_HOME') or str(_pl.Path(__file__).resolve().parents[2])
import sys
sys.path.insert(0, (_RATISS_HOME + '/RATISS-FUSION'))


def test_bosch_hale_10kev():
    from fusion.bosch_hale import sigma_v
    sv = float(sigma_v(10.0))
    assert 1e-23 < sv < 1e-21, sv  # ≈1.1e-22 m³/s


def test_froid_zero():
    from fusion.run import run
    s, pl = run(n=500, T_end=10e-12, A_imp=0.0, Tkev=0.3, quiet=True)
    assert pl.events == 0, pl.events


def test_implosion_compresse():
    from fusion.run import run
    s, pl = run(n=500, T_end=20e-12, A_imp=1e-10, quiet=True)
    assert s[-1]['R'] < s[0]['R'], (s[0]['R'], s[-1]['R'])
    assert s[-1]['T'] > s[0]['T'], (s[0]['T'], s[-1]['T'])


def test_chaud_burn():
    from fusion.run import run
    s, pl = run(n=800, T_end=60e-12, A_imp=6e-10, Tkev=0.5, quiet=True)
    assert pl.events > 0, 'pas de fusion à chaud !'
    assert pl.E_out > 0
