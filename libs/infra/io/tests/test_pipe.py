from io import StringIO
from libs.infra.io.pipe import IOPipe


MOCK_FD = 99999999


def test_pipe_read_ok(mocker):
    """
    IO Pipe read ok test
    """
    expected_text = "OK"

    pipe = IOPipe()
    mock_file = StringIO(expected_text)

    mocker.patch('msvcrt.open_osfhandle', return_value=MOCK_FD)
    mocker.patch('os.fdopen', return_value=mock_file)

    assert pipe.read() == expected_text
