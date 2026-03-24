"""Backward compatibility: training is merged into training.py (use --noneq, --pseudotensors, --data-augmentation)."""

from training import get_args, main

if __name__ == "__main__":
    main(get_args())
