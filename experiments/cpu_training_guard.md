# CPU training safety guard

The training script now blocks configurations above three steps when CUDA is unavailable, unless the configuration explicitly sets `allow_slow_cpu: true`. Experiment 002 sets this value to `false`, so it cannot accidentally consume the machine for a long CPU run.
