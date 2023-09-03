# Copyright (c) 2020-2023 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel, and University of Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

import numpy as np
from numpy import linalg
from scipy.sparse.linalg import spsolve

from pandapipes.idx_branch import ACTIVE as ACTIVE_BR, FROM_NODE, TO_NODE, FROM_NODE_T, \
    TO_NODE_T, VINIT, TINIT_OUT, VINIT_T
from pandapipes.idx_node import PINIT, TINIT, ACTIVE as ACTIVE_ND
from pandapipes.pf.build_system_matrix import build_system_matrix
from pandapipes.pf.derivative_calculation import calculate_derivatives_hydraulic, calculate_derivatives_thermal
from pandapipes.pf.pipeflow_setup import get_net_option, get_net_options, set_net_option, \
    init_options, create_internal_results, write_internal_results, get_lookup, create_lookups, \
    initialize_pit, check_connectivity, reduce_pit, \
    set_user_pf_options, init_all_result_tables
from pandapipes.pf.result_extraction import extract_all_results, extract_results_active_pit
from pandapower.auxiliary import ppException

try:
    import pandaplan.core.pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)


def set_logger_level_pipeflow(level):
    """
    Set logger level from outside to reduce/extend pipeflow() printout.
    :param level: levels according to 'logging' (i.e. DEBUG, INFO, WARNING, ERROR and CRITICAL)
    :type level: str
    :return: No output

    EXAMPLE:
        set_logger_level_pipeflow('WARNING')

    """
    logger.setLevel(level)


def pipeflow(net, sol_vec=None, **kwargs):
    """
    The main method used to start the solver to calculate the velocity, pressure and temperature\
    distribution for a given net. Different options can be entered for \\**kwargs, which control\
    the solver behaviour (see function :func:`init_options` for more information).

    :param net: The pandapipes net for which to perform the pipeflow
    :type net: pandapipesNet
    :param sol_vec: Initializes the start values for the heating network calculation
    :type sol_vec: numpy.ndarray, default None
    :param kwargs: A list of options controlling the solver behaviour
    :return: No output

    :Example:
        >>> pipeflow(net, mode="hydraulics")

    """
    local_params = dict(locals())

    # Inputs & initialization of variables
    # ------------------------------------------------------------------------------------------

    # Init physical constants and options
    init_options(net, local_params)

    # init result tables
    net["converged"] = False
    init_all_result_tables(net)
    create_internal_results(net)

    create_lookups(net)
    node_pit, branch_pit = initialize_pit(net)
    if (len(node_pit) == 0) & (len(branch_pit) == 0):
        logger.warning("There are no node and branch entries defined. This might mean that your net"
                       " is empty")
        return
    calculation_mode = get_net_option(net, "mode")
    calculate_hydraulics = calculation_mode in ["hydraulics", "all"]
    calculate_heat = calculation_mode in ["heat", "all", "bidirectional"]
    calculate_bidrect = calculation_mode == "bidirectional"

    if get_net_option(net, "check_connectivity"):
        nodes_connected, branches_connected = check_connectivity(
            net, branch_pit, node_pit, check_heat=calculate_heat)
    else:
        nodes_connected = node_pit[:, ACTIVE_ND].astype(bool)
        branches_connected = branch_pit[:, ACTIVE_BR].astype(bool)

    reduce_pit(net, node_pit, branch_pit, nodes_connected, branches_connected)

    if calculation_mode == "heat" and not net.user_pf_options["hyd_flag"]:
        raise UserWarning("Converged flag not set. Make sure that hydraulic calculation results "
                          "are available.")
    elif calculation_mode == "heat" and net.user_pf_options["hyd_flag"]:
        net["_active_pit"]["node"][:, PINIT] = sol_vec[:len(node_pit)]
        net["_active_pit"]["branch"][:, VINIT] = sol_vec[len(node_pit):]

    if not (calculate_hydraulics | calculate_heat | calculate_bidrect):
        raise UserWarning("No proper calculation mode chosen.")
    elif calculate_bidrect:
        pass
    else:
        if calculate_hydraulics:
            converged, _ = hydraulics(net)
            if not converged:
                raise PipeflowNotConverged("The hydraulic calculation did not converge to a solution.")
        if calculate_heat:
            converged, _ = heat_transfer(net)
            if not converged:
                raise PipeflowNotConverged("The heat transfer calculation did not converge to a "
                                           "solution.")

    extract_results_active_pit(net, node_pit, branch_pit, nodes_connected, branches_connected)
    extract_all_results(net, nodes_connected, branches_connected)


def bidirectional(net):
    max_iter, nonlinear_method, tol_p, tol_v, tol_res = get_net_options(
        net, "iter", "nonlinear_method", "tol_p", "tol_v", "tol_res")

    niter = 0
    create_internal_results(net)
    if not get_net_option(net, "reuse_internal_data") or "_internal_data" not in net:
        net["_internal_data"] = dict()

    if net.fluid.is_gas:
        logger.info("Caution! Temperature calculation does currently not affect hydraulic "
                    "properties!")

    error_v, error_p, error_t, error_t_out, residual_norm = [], [], [], [], None


def newton_raphson(net, funct, solver, *vars):
    tol_names = np.char.add('tol_', vars)
    options = get_net_options(net, "iter", "nonlinear_method", "tol_res", *tol_names)
    max_iter, nonlinear_method, tol_res = next(options), next(options), next(options)
    tols = [next(options) for _ in tol_names]
    niter = 0
    # This branch is used to stop the solver after a specified error tolerance is reached
    errors = dict.fromkeys(vars, [])
    residual_norm = None
    converged = False
    set_net_option(net, "converged", converged)
    # This loop is left as soon as the solver converged
    while not get_net_option(net, "converged") and niter <= max_iter:
        logger.debug("niter %d" % niter)
        # solve_hydraulics is where the calculation takes place
        results = np.array(funct(net))
        logger.debug("residual: %s" % results[-1].round(4))
        residual_norm = linalg.norm(results[-1] / len(results[-1]))

        vals_new = results[np.arange(len(vars))]
        vals_old = results[np.arange(len(vars), len(vars) * 2)]
        for var, val_new, val_old in zip(vars, vals_new, vals_old):
            dval = np.abs(val_new - val_old)
            errors[var].append(linalg.norm(dval) / len(dval) if len(dval) else 0)
        converged = finalize_iteration(net, niter, residual_norm, nonlinear_method,
                                       errors=errors, tols=tols,  tol_res=tol_res,
                                       vals_old=vals_old, vars=vars)
        niter += 1
    net['converged'] = converged
    write_internal_results(net, **errors)
    log_final_results(net, net['converged'], niter, residual_norm, tol_names, solver)
    return niter, residual_norm


def hydraulics(net):
    # Start of nonlinear loop
    # ---------------------------------------------------------------------------------------------
    if not get_net_option(net, "reuse_internal_data") or "_internal_data" not in net:
        net["_internal_data"] = dict()
    niter, residual_norm = newton_raphson(net, solve_hydraulics, 'hydraulics', 'v', 'p')
    write_internal_results(net, iterations=niter, residual_norm=residual_norm)
    if net['converged']:
        set_user_pf_options(net, hyd_flag=True)

    if not get_net_option(net, "reuse_internal_data"):
        net.pop("_internal_data", None)

    return net['converged'], niter


def heat_transfer(net):
    # Start of nonlinear loop
    # ---------------------------------------------------------------------------------------------

    if net.fluid.is_gas:
        logger.info("Caution! Temperature calculation does currently not affect hydraulic "
                    "properties!")
    niter, residual_norm = newton_raphson(net, solve_temperature, 'heat', 'Tin', 'Tout')
    write_internal_results(net, iterations_T=niter, residual_norm_T=residual_norm)

    return net['converged'], niter


def solve_hydraulics(net):
    """
    Create and solve the linearized system of equations (based on a jacobian in form of a scipy
    sparse matrix and a load vector in form of a numpy array) in order to calculate the hydraulic
    magnitudes (pressure and velocity) for the network nodes and branches.

    :param net: The pandapipesNet for which to solve the hydraulic matrix
    :type net: pandapipesNet
    :return:

    """
    options = net["_options"]
    branch_pit = net["_active_pit"]["branch"]
    node_pit = net["_active_pit"]["node"]

    branch_lookups = get_lookup(net, "branch", "from_to_active")
    for comp in net['component_list']:
        comp.adaption_before_derivatives_hydraulic(
            net, branch_pit, node_pit, branch_lookups, options)
    calculate_derivatives_hydraulic(net, branch_pit, node_pit, options)
    for comp in net['component_list']:
        comp.adaption_after_derivatives_hydraulic(
            net, branch_pit, node_pit, branch_lookups, options)
    jacobian, epsilon = build_system_matrix(net, branch_pit, node_pit, False)

    v_init_old = branch_pit[:, VINIT].copy()
    p_init_old = node_pit[:, PINIT].copy()

    x = spsolve(jacobian, epsilon)
    branch_pit[:, VINIT] += x[len(node_pit):]
    node_pit[:, PINIT] += x[:len(node_pit)] * options["alpha"]

    return branch_pit[:, VINIT], node_pit[:, PINIT], v_init_old, p_init_old, epsilon


def solve_temperature(net):
    """
    This function contains the procedure to build and solve a linearized system of equation based on
    an underlying net and the necessary graph data structures. Temperature values are calculated.
    Returned are the solution vectors for the new iteration, the original solution vectors and a
    vector containing component indices for the system matrix entries

    :param net: The pandapipesNet for which to solve the temperature matrix
    :type net: pandapipesNet
    :return: branch_pit

    """

    options = net["_options"]
    branch_pit = net["_active_pit"]["branch"]
    node_pit = net["_active_pit"]["node"]
    branch_lookups = get_lookup(net, "branch", "from_to_active")

    # Negative velocity values are turned to positive ones (including exchange of from_node and
    # to_node for temperature calculation
    branch_pit[:, VINIT_T] = branch_pit[:, VINIT]
    branch_pit[:, FROM_NODE_T] = branch_pit[:, FROM_NODE]
    branch_pit[:, TO_NODE_T] = branch_pit[:, TO_NODE]
    mask = branch_pit[:, VINIT] < 0
    branch_pit[mask, VINIT_T] = -branch_pit[mask, VINIT]
    branch_pit[mask, FROM_NODE_T] = branch_pit[mask, TO_NODE]
    branch_pit[mask, TO_NODE_T] = branch_pit[mask, FROM_NODE]

    for comp in net['component_list']:
        comp.adaption_before_derivatives_thermal(
            net, branch_pit, node_pit, branch_lookups, options)
    calculate_derivatives_thermal(net, branch_pit, node_pit, options)
    for comp in net['component_list']:
        comp.adaption_after_derivatives_thermal(
            net, branch_pit, node_pit, branch_lookups, options)
    jacobian, epsilon = build_system_matrix(net, branch_pit, node_pit, True)

    t_init_old = node_pit[:, TINIT].copy()
    t_out_old = branch_pit[:, TINIT_OUT].copy()

    x = spsolve(jacobian, epsilon)
    node_pit[:, TINIT] += x[:len(node_pit)] * options["alpha"]
    branch_pit[:, TINIT_OUT] += x[len(node_pit):]

    return branch_pit[:, TINIT_OUT], t_out_old, node_pit[:, TINIT], t_init_old, epsilon


def set_damping_factor(net, niter, errors):
    """
    Set the value of the damping factor (factor for the newton step width) from current results.

    :param net: the net for which to perform the pipeflow
    :type net: pandapipesNet
    :param niter:
    :type niter:
    :param error: an array containing the current residuals of all field variables solved for
    :return: No Output.

    EXAMPLE:
        set_damping_factor(net, niter, [error_p, error_v])
    """
    error_increased = []
    for error in errors:
        error_increased.append(error[niter] > error[niter - 1])
    current_alpha = get_net_option(net, "alpha")
    if np.all(error_increased):
        set_net_option(net, "alpha", current_alpha / 10 if current_alpha >= 0.1 else current_alpha)
    else:
        set_net_option(net, "alpha", current_alpha * 10 if current_alpha <= 0.1 else 1.0)
    return error_increased


def finalize_iteration(net, niter, residual_norm, nonlinear_method,
                       errors, tols, tol_res, vals_old, vars):
    converged = False
    # Control of damping factor
    if nonlinear_method == "automatic":
        errors_increased = set_damping_factor(net, niter, errors)
        logger.debug("alpha: %s" % get_net_option(net, "alpha"))
        for error_increased, var, val in zip(errors_increased, vars, vals_old):
            if error_increased: net["_active_pit"]["node"][:, var + 'INIT'] = val
        if get_net_option(net, "alpha") != 1:
            set_net_option(net, "converged", False)
            return converged
    elif nonlinear_method != "constant":
        logger.warning("No proper nonlinear method chosen. Using constant settings.")
    for error, var, tol in zip(errors.values(), vars, tols):
        converged = error[niter] <= tol
        if not converged: break
        logger.debug("error_%s: %s" % var, error[niter])
    converged = converged and residual_norm <= tol_res
    set_net_option(net, "converged", converged)
    return converged


def log_final_results(net, converged, niter, residual_norm, solver, tol_names):
    logger.debug("--------------------------------------------------------------------------------")
    if not converged:
        logger.debug("Maximum number of iterations reached but %s solver did not converge."
                     % solver)
        logger.debug("Norm of residual: %s" % residual_norm)
    else:
        logger.debug("Calculation completed. Preparing results...")
        logger.debug("Converged after %d iterations." % niter)
        logger.debug("Norm of residual: %s" % residual_norm)
        for tol in tol_names:
            logger.debug("%s: %s" % (tol, get_net_option(net, tol)))


class PipeflowNotConverged(ppException):
    """
    Exception being raised in case pipeflow did not converge.
    """
    pass
