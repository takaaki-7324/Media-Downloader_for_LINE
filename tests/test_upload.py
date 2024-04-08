import setting as s
import time

def test_music_folder_upload(gcp_info):
    auth,string = gcp_info
    up_test_file = auth.CreateFile({'title': 'UPLOAD_TEST_FILE.txt',"parents": [{"id": s.MUSIC_FOLDER_ID}]})
    up_test_file.SetContentString(string)
    up_test_file.Upload()
    check_string = up_test_file.GetContentString()
    time.sleep(5)
    up_test_file.Delete()
    assert check_string == "This is upload test file."

def test_video_folder_upload(gcp_info):
    auth,string = gcp_info
    up_test_file = auth.CreateFile({'title': 'UPLOAD_TEST_FILE.txt',"parents": [{"id": s.VIDEO_FOLDER_ID}]})
    up_test_file.SetContentString(string)
    up_test_file.Upload()
    check_string = up_test_file.GetContentString()
    time.sleep(5)
    up_test_file.Delete()
    assert check_string == "This is upload test file."