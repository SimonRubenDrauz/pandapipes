# Copyright (c) 2020 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

import os
from pandapipes.io.file_io import from_json
from pandapipes import pp_dir
from pandapipes.networks.nw_aux import log_result_upon_loading

try:
    import pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)
water_stanet_path = os.path.join(pp_dir, "networks", "network_files", "stanet_test_networks",
                                 "water_cases")
water_sincal_path = os.path.join(pp_dir, "networks", "simple_test_networks", "sincal_test_networks",
                                 "water_cases")
water_modelica_colebrook_path = os.path.join(pp_dir, "networks", "network_files",
                                   "openmodelica_test_networks", "water_cases_colebrook")

water_modelica_swamee_path = os.path.join(pp_dir, "networks", "network_files",
                                   "openmodelica_test_networks", "water_cases_swamee-jain")


# -------------- combined networks --------------
def water_district_grid(results_from="stanet", method="nikuradse"):
    """

    :param method: Which results should be loaded: nikuradse or prandtl-colebrook
    :type method: str, default "nikuradse"
    :return: net - STANET network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_district_grid(method="pc")

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "district_N.json" if method_str == "Nikuradse" else "district_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "district_grid_PC.json"
        path = water_sincal_path
    return from_json(os.path.join(path, "combined_networks", net_name))


def water_combined_mixed(results_from="openmodelica", method="colebrook"):
    """

    :param method: Which results should be loaded: prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_combined_mixed(method="swamee-jain")

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from == 'openmodelica':
        net_name = "mixed_net.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    elif results_from == 'sincal':
        net_name = "mixed_net_PC.json"
        path = water_sincal_path
    return from_json(os.path.join(path, "combined_networks", net_name))


def water_combined_versatility(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_combined_versatility(method="")

    """

    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "sincal":
        net_name = "versatility_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "stanet":
        path = water_stanet_path
        net_name = "versatility_N.json" if method_str == "Nikuradse" else "versatility_PC.json"
    elif results_from.lower() == "openmodelica":
        net_name = "versatility.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "combined_networks", net_name))


# -------------- meshed networks --------------
def water_meshed_delta(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_meshed_delta(results_from="stanet")

    """

    method = "n" if results_from.lower() == "stanet" else method
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "sincal":
        net_name = 'delta_PC.json'
        path = water_sincal_path
    elif results_from.lower() == "stanet":
        net_name = 'delta_N.json'
        path = water_stanet_path
    elif results_from.lower() == "openmodelica":
        net_name = 'delta.json'
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "meshed_networks", net_name))


def water_meshed_pumps(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_meshed_pumps(method="swamee")

    """
    method = "n" if results_from.lower() == "stanet" else method
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "pumps_N.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "pumps_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "pumps.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "meshed_networks", net_name))


def water_meshed_heights(results_from='openmodelica', method="colebrook"):
    """
    :param method: which results should be loaded: prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_meshed_heights()

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)
    if results_from == 'sincal':
        net_name = "heights_PC.json"
        path = water_sincal_path
    elif results_from == 'openmodelica':
        net_name = "heights.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "meshed_networks", net_name))


def water_meshed_2valves(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_meshed_2valves(method="swamee-jain")

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "two_valves_N.json" if method_str == "Nikuradse" else "two_valves_PC.json"
        path = water_stanet_path
    elif results_from.lower() == 'sincal':
        net_name = "two_valves_PC.json"
        path = water_sincal_path
    elif results_from.lower() == 'openmodelica':
        net_name = "two_valves.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "meshed_networks", net_name))


# -------------- one pipe --------------
def water_one_pipe1(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_one_pipe1(method="pc", results_from="stanet")

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "pipe_1_N.json" if method_str == "Nikuradse" else "pipe_1_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "pipe_1_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "pipe_1.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "one_pipe", net_name))


def water_one_pipe2(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_one_pipe2()

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "pipe_2_N.json" if method_str == "Nikuradse" else "pipe_2_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "pipe_2_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "pipe_2.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "one_pipe", net_name))


def water_one_pipe3(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_one_pipe3(method="")

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "pipe_3_N.json" if method_str == "Nikuradse" else "pipe_3_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "pipe_3_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "pipe_3.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "one_pipe", net_name))


# -------------- strand net --------------
def water_simple_strand_net(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_simple_strand_net()

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "strand_net_N.json" if method_str == "Nikuradse" else "strand_net_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "strand_net_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "strand_net.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "strand_net", net_name))


def water_strand_2pipes(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> nikuradse or prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_strand_2pipes()

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "two_pipes_N.json" if method_str == "Nikuradse" else "two_pipes_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "strand_two_pipes_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "two_pipes.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "strand_net", net_name))


def water_strand_cross(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network (method = "prandtl-colebrook")
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_strand_cross(results_from="stanet")

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "cross_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "strand_cross_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "cross_3ext.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "strand_net", net_name))


def water_strand_net_2pumps(method="colebrook"):
    """
    :param method: Which results should be loaded: prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_strand_net_2pumps()

    """
    method_str = log_result_upon_loading(logger, method=method, converter="openmodelica")

    net_name = 'two_pumps.json'
    path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "strand_net", net_name))


def water_strand_pump(results_from='stanet', method="colebrook"):
    """

    :return: net - STANET network converted to a pandapipes network  (method = "nikuradse")
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_meshed_pump()

    """
    log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "pump_N.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "strand_pump_PC.json"
        path = water_sincal_path
    return from_json(os.path.join(path, "strand_net", net_name))


# -------------- t_cross --------------
def water_tcross(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_tcross()

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "t_cross_N.json" if method_str == "Nikuradse" else "t_cross_PC.json"
        path = water_stanet_path
    elif results_from.lower() == "sincal":
        net_name = "t_cross_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "t_cross.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "t_cross", net_name))


def water_tcross_valves(method="colebrook"):
    """
    :param method: Which results should be loaded: prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_tcross_valves()

    """
    method_str = log_result_upon_loading(logger, method=method, converter="openmodelica")
    net_name = "valves.json"
    path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "t_cross", net_name))


# -------------- two pressure junctions --------------
def water_2eg_two_pipes(results_from="openmodelica", method="colebrook"):
    """

    :param results_from: Which converted net should be loaded: openmodelica or stanet
    :type results_from: str, default "openmodelica"
    :param method: results_from = "stanet" -> prandtl-colebrook, results_from = "openmodelica" -> prandtl-colebrook or swamee-jain
    :type method: str, default "colebrook"
    :return: net - STANET resp. OpenModelica network converted to a pandapipes network
    :rtype: pandapipesNet

    :Example:
        >>> pandapipes.networks.simple_water_networks.water_2eg_two_pipes()

    """
    method_str = log_result_upon_loading(logger, method=method, converter=results_from)

    if results_from.lower() == "stanet":
        net_name = "two_pipes_N.json" if method_str == "Nikuradse" else "two_pipes_PC.json"
        path = water_stanet_path
    elif results_from.lower() == 'sincal':
        net_name = "two_pipes_PC.json"
        path = water_sincal_path
    elif results_from.lower() == "openmodelica":
        net_name = "two_pipes.json"
        path = water_modelica_colebrook_path if method_str == "Prandtl-Colebrook" else water_modelica_swamee_path
    return from_json(os.path.join(path, "two_pressure_junctions", net_name))
