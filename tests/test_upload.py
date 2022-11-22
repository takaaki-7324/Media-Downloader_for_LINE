
def test_upload(gcp_info):
    auth,string = gcp_info
    up_test_file = auth.CreateFile({'title': 'UPLOAD_TEST_FILE.txt'})
    up_test_file.SetContentString(string)
    up_test_file.Upload()
    check_string = up_test_file.GetContentString()
    up_test_file.Delete()
    assert check_string == "This is upload test file."