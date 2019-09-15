# Tests for the randomized response
import pytest

from differential_privacy.randomized_response.generalized import GeneralRandomizedResponse

def seq_floats(start, stop, step=1):
    stop = stop - step;
    number = int(round((stop - start)/float(step)))
    if number > 1:
        return([start + step*i for i in range(number+1)])
    elif number == 1:
        return([start])
    else:
        return([])

def test_wrong_matrix():
    with pytest.raises(Exception):
        _ = GeneralRandomizedResponse(p_00=1.0, p_01=1.0, p_10=1.0, p_11=1.0)

    with pytest.raises(Exception):
        _ = GeneralRandomizedResponse(p_00=1.1, p_01=0.9, p_10=1.0, p_11=1.0)

def test_good_matrix():
    _ = GeneralRandomizedResponse(p_00=.9, p_01=.1, p_10=.1, p_11=.9)


def test_eps_privacy():
    # this should be maximum privacy since the responses have 0 utility
    max_privacy = GeneralRandomizedResponse(p_00=.5, p_01=.5, p_10=.5, p_11=.5)

    is_true = max_privacy.check_eps_privacy(0.0)

    assert is_true == True

    # this should be maximum utility since the responses are equivalent to direct questions
    max_utility = GeneralRandomizedResponse(p_00=1.0, p_01=.0, p_10=0.0, p_11=1.0)

    is_false = max_utility.check_eps_privacy(100.0)

    assert is_false == False

    # this should correspond to infinite epsilon
    is_big = max_utility.check_eps_privacy(float('inf'))

    assert is_big == True


def test_optimal_rr():
    a_privacy = GeneralRandomizedResponse()

    target_eps = 1.0
    a_privacy.set_optimal_utility(target_eps)

    is_true = a_privacy.check_eps_privacy(target_eps,tol=5e-16)

    assert is_true == True


def test_mass_rr():
    max_util_grr = GeneralRandomizedResponse(p_00=1.0, p_01=.0, p_10=0.0, p_11=1.0)

    # percentage of yes in truth
    for pi_1 in seq_floats(0.0,1.1,0.1):
        P_X = max_util_grr.get_P_X_mass(pi_1=pi_1)

        assert round(P_X['P(Y=0)'],1)==round(1.0-pi_1,1)
        assert round(P_X['P(Y=1)'],1)==round(pi_1,1)

    # percentage of no in truth
    for pi_0 in seq_floats(0.0,1.1,0.1):
        P_X = max_util_grr.get_P_X_mass(pi_0=pi_0)

        assert round(P_X['P(Y=0)'],1)== round(pi_0,1)
        assert round(P_X['P(Y=1)'],1)== round(1.0-pi_0,1)


    # this should be maximum privacy since the responses have 0 utility
    max_privacy_grr = GeneralRandomizedResponse(p_00=.5, p_01=.5, p_10=.5, p_11=.5)

    # percentage of yes in truth
    for pi_1 in seq_floats(0.0,1.1,0.1):
        # the proportion doesn't matter because they are blind responding
        P_X = max_privacy_grr.get_P_X_mass(pi_1=pi_1)

        assert round(P_X['P(Y=1)'], 1) == 0.5

