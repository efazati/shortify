async def test_shortify_view(client):
    invalid_forms = [
        {'url': 'test'},
        {'url': 'google.com'},
        {'url': 'http:/google.com'},
        {'url': 'http://googlecom'},
        {'url': 'https://googlecom'}
    ]
    valid_forms = [
        {'url': 'http://google.com'},
        {'url': 'https://google.com'},
        {'url': 'https://www.google.com'},
        {'url': 'http://abc.def'},
    ]

    for invalid_form in invalid_forms:
        resp = await client.post('/shortify', data=invalid_form)
        assert resp.status == 400
        assert 'url is not valid' in await resp.text()

    for valid_form in valid_forms:
        resp = await client.post('/shortify', data=valid_form)
        assert resp.status == 200
        assert 'Short Address' in await resp.text()


async def test_unshortify_view(client):
    short_code = 'abcd5'
    resp = await client.get(f'/{short_code}')
    assert resp.status == 200
    assert str(resp.url) == "http://www.google.com/"
