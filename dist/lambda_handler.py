import kernels
import numpy as np

def run_demo(event, context):
    test_input_one = 4.0
    test_square = kernels.square(4)

    test_input_two = np.asarray([1.0, 2.0, 3.0])
    test_square_array = kernels.squarearr(test_input_two)

    return {
        'squared_number': test_square,
        'squared_array': test_square_array.tolist()
    }

# Uncomment this if you just want to run locally, i.e.
# something like python lambda_handler.py, instead
# of actually running in lambda
if __name__ == '__main__':
    print run_demo(None, None)
