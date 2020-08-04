# Copyright (c) 2020 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

import numpy as np
import pandas as pd

import pandapipes
from pandapipes.component_models import Pipe
from pandapipes.properties.fluids import get_fluid

try:
    import pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)


def pipeflow_comparison(net, converter_name='stanet', log_results=True, friction_model='nikuradse', mode='hydraulics',
                        only_update_hydraulic_matrix=False, consider_only_abs_values=False,
                        **kwargs):
    """
        Comparison of the calculations of pandapipes and another pipeflow calculating tool a net
        has been converted from.

        :param net: converted network
        :type net: pandapipesNet
        :param converter_name: used converter
        :type converter_name: str, "stanet"
        :param log_results:
        :type log_results: bool, True
        :param friction_model:
        :type friction_model: str, "nikuradse"
        :param mode:
        :type mode: str, "hydraulics"
        :param only_update_hydraulic_matrix:
        :type only_update_hydraulic_matrix: bool, False
        :return: p_diff, v_diff_abs
        :rtype: one-dimensional ndarray with axis labels
        :param consider_valve_results: compare the valve results as well
        :type log_results: bool, True
        :param consider_only_abs_values: compare only the absolute results with each other
        :type log_results: bool, True
    """
    pandapipes.pipeflow(net, mode=mode, stop_condition="tol", iter=100, tol_p=1e-7,
                        tol_v=1e-7, friction_model=friction_model,
                        only_update_hydraulic_matrix=only_update_hydraulic_matrix, **kwargs)

    logger.debug(net.res_junction)
    logger.debug(net.res_pipe)

    p_conv = net.junction['p' + '_' + converter_name]
    p_valid = pd.notnull(p_conv)
    p_conv = p_conv.loc[p_valid]

    if get_fluid(net).is_gas:
        if 'pipe' in net:
            v_diff_from_pipe, v_diff_to_pipe, v_diff_mean_pipe, v_diff_abs_pipe, \
            v_mean_pandapipes_pipe, v_conv_pipe = retrieve_velocity(net, converter_name, 'pipe',
                                                                    consider_only_abs_values)

            T_diff_mean_pipe = retrieve_temperature(net, converter_name)
        else:
            v_diff_abs_pipe = pd.Series(dtype="float64")
            v_conv_pipe = pd.Series(dtype="float64")
            v_mean_pandapipes_pipe = pd.Series(dtype="float64")
            v_diff_from_pipe = pd.Series(dtype="float64")
            v_diff_to_pipe = pd.Series(dtype="float64")
            v_diff_mean_pipe = pd.Series(dtype="float64")

            T_diff_mean_pipe = pd.Series(dtype="float64")

        diff_results_v_pipe = pd.DataFrame(
            {"diff_v_from_pipe": v_diff_from_pipe, "diff_v_to_pipe": v_diff_to_pipe,
             "diff_v_mean_pipe": v_diff_mean_pipe, "diff_v_abs_pipe": v_diff_abs_pipe})

        if ('valve' in net) & (('v_' + converter_name) in net['valve']):
            v_diff_from_valve, v_diff_to_valve, v_diff_mean_valve, v_diff_abs_valve, \
            v_mean_pandapipes_valve, v_conv_valve = retrieve_velocity(net, converter_name, 'valve',
                                                                      consider_only_abs_values)
        else:
            v_diff_abs_valve = pd.Series(dtype="float64")
            v_conv_valve = pd.Series(dtype="float64")
            v_mean_pandapipes_valve = pd.Series(dtype="float64")
            v_diff_from_valve = pd.Series(dtype="float64")
            v_diff_to_valve = pd.Series(dtype="float64")
            v_diff_mean_valve = pd.Series(dtype="float64")

        diff_results_v_valve = pd.DataFrame(
            {"diff_v_from_valve": v_diff_from_valve, "diff_v_to_valve": v_diff_to_valve,
             "diff_v_mean_valve": v_diff_mean_valve, "diff_v_abs_valve": v_diff_abs_valve})

    else:
        if 'pipe' in net:
            v_diff_mean_pipe, v_diff_abs_pipe, v_mean_pandapipes_pipe, v_conv_pipe = \
                retrieve_velocity(net, converter_name, 'pipe', consider_only_abs_values)
            T_diff_mean_pipe = retrieve_temperature(net, converter_name)
        else:
            v_diff_abs_pipe = pd.Series(dtype="float64")
            v_conv_pipe = pd.Series(dtype="float64")
            v_mean_pandapipes_pipe = pd.Series(dtype="float64")
            v_diff_mean_pipe = pd.Series(dtype="float64")

            T_diff_mean_pipe = pd.Series(dtype="float64")

        if ('valve' in net) and (('v_' + converter_name) in net['valve']):
            v_diff_mean_valve, v_diff_abs_valve, v_mean_pandapipes_valve, v_conv_valve = \
                retrieve_velocity(net, converter_name, 'valve', consider_only_abs_values)
        else:
            v_diff_abs_valve = pd.Series(dtype="float64")
            v_conv_valve = pd.Series(dtype="float64")
            v_mean_pandapipes_valve = pd.Series(dtype="float64")
            v_diff_mean_valve = pd.Series(dtype="float64")

        diff_results_v_pipe = pd.DataFrame({"diff_v_mean_pipe": v_diff_mean_pipe,
                                            "diff_v_abs_pipe": v_diff_abs_pipe})
        diff_results_v_valve = pd.DataFrame({"diff_v_mean_valve": v_diff_mean_valve,
                                             "diff_v_abs_valve": v_diff_abs_valve})

    p_pandapipes = net.res_junction.p_bar.loc[p_valid].values.astype(np.float64).round(4)
    p_diff = np.abs(1 - p_pandapipes / p_conv)
    v_diff_abs = v_diff_abs_pipe.append(v_diff_abs_valve, ignore_index=True)
    v_diff_abs.dropna(inplace=True)

    # Avoiding division by zero

    if log_results:
        logger.info("p_sta %s" % p_conv)
        logger.info("p_PP %s" % p_pandapipes)
        logger.info("v_%s_pipe %s" % (converter_name, v_conv_pipe))
        logger.info("v_%s_valve %s" % (converter_name, v_conv_valve))
        logger.info("v_PP_pipe %s" % v_mean_pandapipes_pipe)
        logger.info("v_PP_valve %s" % v_mean_pandapipes_valve)

        logger.info("pressure difference: %s" % p_diff)
        logger.info("velocity difference pipe: \n %s" % diff_results_v_pipe)
        logger.info("velocity difference valve: \n %s" % diff_results_v_valve)

    results = (p_diff, v_diff_abs) if mode == "hydraulics" else (p_diff, v_diff_abs, T_diff_mean_pipe)
    return results


def retrieve_velocity(net, converter_name='stanet', element='pipe', consider_only_abs_values=False):
    """
        Get the calculated velocities for a fluid in pandapipes and the corresponding pipeflow calculating
        tool. Calculate the absolute and relative errors.

        :param net: converted network
        :type net: pandapipesNet
        :param element: either pipe or valve
        :type element: str, default "pipe"
        :return: relative and absolute error (v_diff_mean, v_diff_abs) of average velocities,
        calculated velocities from pandapipes and pipeflow calculation tool (v_mean_pandapipes, v_conv)
        :rtype: one-dimensional ndarray with axis labels
    """
    if ('v_' + converter_name) not in net[element]:
        net[element]['v_' + converter_name] = []
    v_conv = net[element]['v_' + converter_name]
    v_valid = pd.notnull(v_conv)
    v_conv = v_conv.loc[v_valid]

    res_element = net['res_' + element].loc[v_valid, :]

    if consider_only_abs_values:
        v_mean_pandapipes = np.abs(res_element.v_mean_m_per_s.values.astype(np.float64).round(4))
    else:
        v_mean_pandapipes = res_element.v_mean_m_per_s.values.astype(np.float64).round(4)
    v_mean_pandapipes[v_mean_pandapipes == 0] += 0.0001
    v_conv[v_conv == 0] += 0.0001
    v_diff_mean = np.abs(1 - v_mean_pandapipes / v_conv)
    v_diff_abs = np.abs(v_conv - v_mean_pandapipes)

    if get_fluid(net).is_gas:
        if consider_only_abs_values:
            v_from_pandapipes = res_element.v_from_m_per_s.values.astype(np.float64).round(4)
            v_to_pandapipes = res_element.v_to_m_per_s.values.astype(np.float64).round(4)
        else:
            v_from_pandapipes = np.abs(res_element.v_from_m_per_s.values.astype(np.float64).round(4))
            v_to_pandapipes = np.abs(res_element.v_to_m_per_s.values.astype(np.float64).round(4))
        v_from_pandapipes[v_from_pandapipes == 0] += 0.0001
        v_to_pandapipes[v_to_pandapipes == 0] += 0.0001
        v_diff_from = np.abs(1 - v_from_pandapipes / v_conv)
        v_diff_to = np.abs(1 - v_to_pandapipes / v_conv)
        return v_diff_from, v_diff_to, v_diff_mean, v_diff_abs, v_mean_pandapipes, v_conv

    return v_diff_mean, v_diff_abs, v_mean_pandapipes, v_conv


def retrieve_temperature(net, converter_name='stanet'):
    """
        Get the calculated temperatures for a fluid in pandapipes and the corresponding pipeflow calculating
        tool. Calculate the absolute and relative errors.

        :param net: converted network
        :type net: pandapipesNet
        :return: relative and absolute error (T_diff_mean, T_diff_abs) of average velocities,
        calculated velocities from pandapipes and pipeflow calculation tool (T_mean_pandapipes, T_conv)
        :rtype: one-dimensional ndarray with axis labels
    """
    if ('T_' + converter_name) not in net['pipe']:
        return np.nan
    T_conv = net.pipe["T_" + converter_name]
    T_mean_conv = T_conv.apply(np.mean)
    T_mean_pandapipes = np.zeros_like(T_mean_conv)

    for i in net.pipe.index:
        pipe_res = Pipe.get_internal_results(net, [i])
        T_mean_pandapipes[i] += np.mean(pipe_res["TINIT"][:,1])

    T_diff_mean = np.abs(1 - T_mean_pandapipes.astype(np.int) / T_mean_conv.astype(np.int) )
    return T_diff_mean
