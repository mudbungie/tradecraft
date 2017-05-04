from tradecraft.api import user

def test_account_exists():
    assert user.account_exists('fake_email@nota.domain') == False
