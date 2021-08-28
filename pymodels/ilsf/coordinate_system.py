
def parameters(accelerator_prefix):
    """Parameters to transform the particle position with respect to
    the upstream accelerator's coordinate system to local coordinates.

    Returns delta_rx[m] and delta_angle[rad]
    """
    if accelerator_prefix == 'LI':
        delta_rx = 0.0000
        delta_angle = 0.0000
    elif accelerator_prefix == 'TB':
        delta_rx = 0.0000
        delta_angle = 0.0000
    elif accelerator_prefix == 'BO':
        delta_rx = -0.0300
        delta_angle = 0.0143
    elif accelerator_prefix == 'TS':
        delta_rx = -0.0220
        delta_angle = -0.0050
    elif accelerator_prefix == 'SI':
        delta_rx = -0.0165
        delta_angle = 0.00537
    else:
        delta_rx = None
        delta_angle = None
    return delta_rx, delta_angle
