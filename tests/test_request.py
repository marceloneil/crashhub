import github
import os
import pytest

request = r"""
{
    "app_version": "b'3.0.3-367-g3838fdb'3.1", 
    "description": "Test", 
    "exc_string": "division by zero", 
    "id": {
      "file": "C:/Users/bauerj/Documents/GitHub/electrum\\gui\\qt\\main_window.py", 
      "name": "show_about", 
      "type": "ZeroDivisionError"
    }, 
    "locale": "de_DE", 
    "os": "Windows-10-10.0.16299-SP0", 
    "stack": "  File \"C:/Users/bauerj/Documents/GitHub/electrum\\gui\\qt\\main_window.py\", line 544, in show_about\n    1/0\n", 
    "wallet_type": "standard"
}
"""

request2 = r"""
{
  "exc_string": "'str' object cannot be interpreted as an integer",
  "stack": "  File \"/home/marcel/workspace/electrum/gui/qt/main_window.py\", line 2136, in <lambda>\n    b.clicked.connect(lambda: self.do_encrypt(message_e, pubkey_e, encrypted_e))\n  File \"/home/marcel/workspace/electrum/gui/qt/main_window.py\", line 2099, in do_encrypt\n    hex('error')\n",
  "id": {
    "file": "/home/marcel/workspace/electrum/gui/qt/main_window.py",
    "name": "do_encrypt",
    "type": "TypeError"
  },
  "app_version": "3.1.5",
  "os": "Linux-4.15.6-1-ARCH-x86_64-with-arch-Arch-Linux",
  "wallet_type": "standard",
  "locale": "en_US",
  "description": "Test description"
}
"""

def test_create(crashhub_client):
    response = crashhub_client.post("/crash", data=request)
    assert b"You can track further progress on" in response.data
    github.Github.return_value.get_repo.return_value.create_issue.assert_called_once()
    github.Github.return_value.get_repo.return_value.get_issue.assert_not_called()

#def test_updated(crashhub_client):
#    for _ in range(2):
#        response = crashhub_client.post("/crash", data=request2)
#    github.Github.return_value.get_repo.return_value.create_issue.assert_called_once()
#    github.Github.return_value.get_repo.return_value.get_issue.assert_called_once()
def test_updated(crashhub_client):
    response = crashhub_client.post("/crash", data=request2)
    github.Github.return_value.get_repo.return_value.create_issue.assert_called_once()

def test_rate_limit(crashhub_client):
    for _ in range(5):
        response = crashhub_client.post("/crash", data=request)
    assert b"You can track further progress on" not in response.data
