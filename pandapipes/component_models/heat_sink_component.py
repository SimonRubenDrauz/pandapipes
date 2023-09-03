# Copyright (c) 2020-2023 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

import numpy as np
from numpy import dtype

from pandapipes.component_models import HeatExchanger, FlowControlComponent, get_fluid
from pandapipes.component_models.junction_component import Junction
from pandapipes.idx_branch import D, TL, TINIT_OUT, FROM_NODE_T
from pandapipes.idx_node import TINIT as TINIT_NODE


class HeatSink(HeatExchanger, FlowControlComponent):
    """

    """

    @classmethod
    def table_name(cls):
        return "heat_sink"

    @classmethod
    def get_connected_node_type(cls):
        return Junction

    @classmethod
    def create_pit_branch_entries(cls, net, branch_pit):
        """
        Function which creates pit branch entries with a specific table.
        :param net: The pandapipes network
        :type net: pandapipesNet
        :param branch_pit:
        :type branch_pit:
        :return: No Output.
        """
        hs_pit = HeatExchanger().create_pit_branch_entries(net, branch_pit)
        hs_pit = FlowControlComponent().create_pit_branch_entries(net, hs_pit)
        return hs_pit


    @classmethod
    def adaption_before_derivatives_hydraulic(cls, net, branch_pit, node_pit, idx_lookups, options):
        """

        :param net:
        :type net:
        :param branch_component_pit:
        :type branch_component_pit:
        :param node_pit:
        :type node_pit:
        :return:
        :rtype:
        """
        -(rho * area * cp * v_init * (-t_init_i + t_init_i1 - tl)
          - alpha * (t_amb - t_m) * length + qext)

        f, t = idx_lookups[cls.table_name()]
        hs_pit = branch_pit[f:t, :]
        from_nodes = hs_pit[:, FROM_NODE_T].astype(np.int32)

        mask_qext = ~np.isnan(hs_pit[:, QEXT])
        mask_deltat = ~np.isnan(hs_pit[:, DELTAT])
        mask_t_return = ~np.isnan(hs_pit[:, TRETURN])
        mask_mass = ~np.isnan(hs_pit[:, MASS])
        hs_pit[mask_t_return | mask_deltat, JAC_DERIV_DT1] = 0
        hs_pit[mask_t_return, TINIT_OUT] = hs_pit[mask_t_return, TINIT_OUT] - hs_pit[mask_t_return, DELTAT]


    @classmethod
    def adaption_before_derivatives_thermal(cls, net, branch_pit, node_pit, idx_lookups, options):
        f, t = idx_lookups[cls.table_name()]
        hs_pit = branch_pit[f:t, :]
        mask_t_return = ~np.isnan(hs_pit[:, TRETURN])
        hs_pit[mask_t_return, TINIT_OUT] = hs_pit[mask_t_return, TINIT_OUT] - hs_pit[mask_t_return, DELTAT]


    @classmethod
    def adaption_after_derivatives_thermal(cls, net, branch_pit, node_pit, idx_lookups, options):
        """

        :param net:
        :type net:
        :param branch_component_pit:
        :type branch_component_pit:
        :param node_pit:
        :type node_pit:
        :return:
        :rtype:
        """
        -(rho * area * cp * v_init * (-t_init_i + t_init_i1 - tl)
          - alpha * (t_amb - t_m) * length + qext)

        f, t = idx_lookups[cls.table_name()]
        hs_pit = branch_pit[f:t, :]
        from_nodes = hs_pit[:, FROM_NODE_T].astype(np.int32)

        mask_qext = ~np.isnan(hs_pit[:, QEXT])
        mask_deltat = ~np.isnan(hs_pit[:, DELTAT])
        mask_t_return = ~np.isnan(hs_pit[:, TRETURN])
        mask_mass = ~np.isnan(hs_pit[:, MASS])
        hs_pit[mask_t_return | mask_deltat, JAC_DERIV_DT1] = 0


    @classmethod
    def get_component_input(cls):
        """

        Get component input.

        :return:
        :rtype:
        """
        return [("name", dtype(object)),
                ("from_junction", "u4"),
                ("to_junction", "u4"),
                ("controlled_mdot_kg_per_s", "f8"),
                ("qext_w", 'f8'),
                ("deltat_k", 'f8'),
                ("t_retrun_k", 'f8'),
                ("diameter_m", "f8"),
                ("control_active", "bool"),
                ("in_service", 'bool'),
                ("type", dtype(object))]

    @classmethod
    def get_result_table(cls, net):
        """

        Gets the result table.

        :param net: The pandapipes network
        :type net: pandapipesNet
        :return: (columns, all_float) - the column names and whether they are all float type. Only
                if False, returns columns as tuples also specifying the dtypes
        :rtype: (list, bool)
        """
        if get_fluid(net).is_gas:
            output = ["v_from_m_per_s", "v_to_m_per_s", "v_mean_m_per_s", "p_from_bar", "p_to_bar",
                      "t_from_k", "t_to_k", "mdot_from_kg_per_s", "mdot_to_kg_per_s",
                      "vdot_norm_m3_per_s", "reynolds", "lambda", "normfactor_from",
                      "normfactor_to"]
        else:
            output = ["v_mean_m_per_s", "p_from_bar", "p_to_bar", "t_from_k", "t_to_k",
                      "mdot_from_kg_per_s", "mdot_to_kg_per_s", "vdot_norm_m3_per_s", "reynolds",
                      "lambda"]
        return output, True
