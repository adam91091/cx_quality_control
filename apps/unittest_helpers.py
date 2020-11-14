from django.urls import reverse


def assert_response_get(test_case, url_name, exp_status_code, exp_template=None, id=None):
    if id is not None:
        response = test_case.view_client.get(reverse(url_name, args=[id, ]))
    else:
        response = test_case.view_client.get(reverse(url_name))
    test_case.assertEqual(response.status_code, exp_status_code)
    if exp_template is not None:
        test_case.assertTemplateUsed(response, exp_template)
    return response


def assert_response_post(test_case, url_name, exp_status_code, data, id=None):
    if id is not None:
        response = test_case.view_client.post(reverse(url_name, args=[id, ]), data=data)
    else:
        response = test_case.view_client.post(reverse(url_name), data=data)
    test_case.assertEqual(response.status_code, exp_status_code)
    return response
