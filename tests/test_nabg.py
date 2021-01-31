import nabg


def test_nab_ionize_returns_correctly():
    result = nabg.ionize()
    assert type(result) == str, "ionize() didn't return text"
    assert len(nabg.ionize()) != 0, "ionize() returned nothing"
