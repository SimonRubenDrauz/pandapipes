# Copyright (c) 2020 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.

method_transfer_dict = {"n": "Nikuradse", "nik": "Nikuradse", "nikuradse": "Nikuradse",
                        "pc": "Prandtl-Colebrook", "prandtl": "Prandtl-Colebrook", "colebrook": "Prandtl-Colebrook",
                        "prandtl-colebrook": "Prandtl-Colebrook", "sj": "Swamee-Jain", "swamee": "Swamee-Jain",
                        "jain": "Swamee-Jain", "s": "Swamee-Jain", "j": "Swamee-Jain", "swamee-jain": "Swamee-Jain"}


def log_result_upon_loading(logger, converter, method, logging_level="debug"):
    if converter == "stanet":
        method_str = method_transfer_dict[method.lower()] if method.lower() in method_transfer_dict \
            else logger.error("method %s has not been considered so far" %method)

        if logging_level.lower() == "info" and method_str != "Swamee-Jain":
            logger.info("%s results are from %s calculation mode." % (converter.capitalize, method_str))
        elif method_str == "Swamee-Jain":
            logger.debug("%s results are not existent for %s calculation mode." % (converter.capitalize, method_str))
        else:
            logger.debug("%s results are from %s calculation mode."
                         % (converter.capitalize, method_str))

    elif converter == 'openmodelica':
        method_str = method_transfer_dict[method.lower()] if method.lower() in method_transfer_dict \
            else logger.error("method %s has not been considered so far" % method)

        if logging_level.lower() == "info" and method_str != "Nikuradse":
            logger.info("%s results are from %s calculation mode." % (converter.capitalize, method_str))
        elif method_str == "Nikuradse":
            logger.debug("%s results are not existent for %s calculation mode." % (converter.capitalize, method_str))
        else:
            logger.debug("%s results are from %s calculation mode." % (converter.capitalize, method_str))

    elif converter == 'sincal':
        method_str = method_transfer_dict[method.lower()] if method.lower() in method_transfer_dict \
            else logger.error("method %s has not been considered so far" % method)

        if logging_level.lower() == "info" and method_str == "Prandtl-Colebrook":
            logger.info("%s results are from %s calculation mode." % (converter.capitalize, method_str))
        elif method_str != "Prandtl-Colebrook":
            logger.debug("%s results are not existent for %s calculation mode." % (converter.capitalize, method_str))
        else:
            logger.debug("%s results are from %s calculation mode." % (converter.capitalize, method_str))

    else:
        raise(UserWarning('converter %s is not available' %converter))
    return method_str


