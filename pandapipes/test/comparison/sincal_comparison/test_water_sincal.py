# Copyright (c) 2020 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

import numpy as np
import pytest

import pandapipes.networks.simple_water_networks as nw
from pandapipes.pipeflow import logger as pf_logger
from pandapipes.test.comparison.pipeflow_comparison import pipeflow_comparison

try:
    import pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
pf_logger.setLevel(logging.WARNING)


# ---------- TEST AREA: combined networks ----------
# district_PC
@pytest.mark.xfail
def test_case_district_grid_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_district_grid(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)

# versatility_PC
@pytest.mark.xfail
def test_case_versatility_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_combined_versatility(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)

# mixed_net_PC
@pytest.mark.xfail
def test_case_mixed_net_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_combined_mixed(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# ---------- TEST AREA: meshed networks ----------
# pumps_PC
@pytest.mark.xfail
def test_case_pumps_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_meshed_pumps(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# delta_PC
@pytest.mark.xfail
def test_case_delta_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_meshed_delta(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# two_valves_PC
@pytest.mark.xfail
def test_case_meshed_2valves_pc(log_results=False):
    net = nw.water_meshed_2valves(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# heights_PC
@pytest.mark.xfail
def test_case_meshed_heights_pc(log_results=False):
    net = nw.water_meshed_heights(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# ---------- TEST AREA: one pipe ----------
# pipe_1_PC
@pytest.mark.xfail
def test_case_one_pipe1_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_one_pipe1(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# pipe_2_PC
@pytest.mark.xfail
def test_case_one_pipe2_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_one_pipe2(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# pipe_3_PC
@pytest.mark.xfail
def test_case_one_pipe3_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_one_pipe3(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# ---------- TEST AREA: strand net ----------
# strand_net_PC
@pytest.mark.xfail
def test_case_simple_strand_net_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_simple_strand_net(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# strand_two_pipes_PC
@pytest.mark.xfail
def test_case_two_pipes_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_strand_2pipes(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# strand_cross_PC
@pytest.mark.xfail
def test_case_cross_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_strand_cross(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# strand_pump_PC
@pytest.mark.xfail
def test_case_pump_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_strand_pump(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# ---------- TEST AREA: t_cross ----------
# t-cross_PC
@pytest.mark.xfail
def test_case_tcross_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_tcross(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


# ---------- TEST AREA: two pressure junctions ----------
# two_pipes_PC
@pytest.mark.xfail
def test_case_2eg_two_pipes_pc(log_results=False):
    """

    :param log_results:
    :type log_results:
    :return:
    :rtype:
    """
    net = nw.water_2eg_two_pipes(results_from='sincal', method="pc")
    p_diff, v_diff_abs = pipeflow_comparison(net, 'sincal',log_results, friction_model="colebrook",
                                             consider_only_abs_values=True)
    assert np.all(p_diff < 0.002)
    assert np.all(v_diff_abs < 0.006)


if __name__ == "__main__":
    pytest.main([r'pandapipes/test/sincal_comparison/test_water_sincal.py'])