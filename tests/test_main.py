import os
import unittest.mock
import tempfile
import sys



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import parse_arguments, cron_job, clone_folder


def test_parser(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "-PO", "origin_path", "-PT", "target_path"])
    args = parse_arguments()
    assert args.path_origin == "origin_path"
    assert args.path_target == "target_path"
    assert args.time is None

    monkeypatch.setattr("sys.argv", ["main.py", "-PO", "origin_path", "-PT", "target_path","-t", "10"])
    args = parse_arguments()
    assert args.path_origin == "origin_path"
    assert args.path_target == "target_path"
    assert args.time == "10"
    


@unittest.mock.patch("main.CronTab")
def test_cron_job(mock_cron_tab):
    mock_instance = mock_cron_tab.return_value

    cron_job("5", "your_command")

    print(f"This is the mock {mock_instance.method_calls}") 

    mock_instance.new.assert_called_once_with(command="your_command")
    mock_instance.new.return_value.minute.every.assert_called_once_with("5")


def test_clone_folder(caplog):
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as path_origin, tempfile.TemporaryDirectory() as path_target:
        # Create temporary files inside origin_dir
        with open(os.path.join(path_origin, "file1.txt"), "w", encoding="utf8") as f:
            f.write("Hello, world!")

        # Call clone_folder function
        clone_folder(path_origin, path_target)

        # Check if file was copied
        assert os.path.exists(os.path.join(path_target, "file1.txt"))

       


if __name__ == "__main__":
    # Run tests using pytest
    import pytest
    pytest.main()
