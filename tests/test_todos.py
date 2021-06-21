import unittest

import flask

import common

url_for = flask.url_for

HEADERS_POST_PUT = {
    "text-type": "application/json",
    "Authorization": f"Bearer {common.TOKEN}",
}


HEADERS = {"Authorization": f"Bearer {common.TOKEN}"}


class TestTodos(common.TestFixure):
    def test_get(self):
        resp = self.client.get(url_for("todos.get_todos"), headers=HEADERS,)
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.json), ["next", "value"])
        self.assertEqual(len(resp.json["value"]), 10)
        self.assertEqual(resp.json["value"][0]["text"], "0 hacker")
        self.assertFalse(resp.json["value"][0]["completed"])
        self.assertTrue(resp.json["value"][0]["date"])

    def test_get_filter(self):
        resp = self.client.get(
            url_for("todos.get_todos", filter="text eq '0 hacker'"),
            headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.json), ["next", "value"])
        self.assertEqual(len(resp.json["value"]), 1)
        self.assertEqual(resp.json["value"][0]["text"], "0 hacker")
        self.assertFalse(resp.json["value"][0]["completed"])

        resp = self.client.get(
            url_for("todos.get_todos", filter="text like '0%'"),
            headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.json), ["next", "value"])
        self.assertEqual(len(resp.json["value"]), 1)
        self.assertEqual(resp.json["value"][0]["text"], "0 hacker")
        self.assertFalse(resp.json["value"][0]["completed"])

        resp = self.client.get(
            url_for("todos.get_todos", filter="text like 10"), headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.json), ["next", "value"])
        self.assertEqual(len(resp.json["value"]), 0)

        resp = self.client.get(
            url_for("todos.get_todos", filter="completed eq 0"),
            headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["value"]), 10)

        resp = self.client.get(
            url_for("todos.get_todos", filter="completed eq 1"),
            headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["value"]), 0)

    def test_get_paging(self):
        resp = self.client.get(
            url_for("todos.get_todos", page=1, limit=2), headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.json), ["next", "value"])
        self.assertEqual(len(resp.json["value"]), 2)
        self.assertEqual(resp.json["value"][0]["text"], "0 hacker")
        self.assertFalse(resp.json["value"][0]["completed"])

        resp = self.client.get(
            url_for("todos.get_todos", page=1, limit=2, count=True),
            headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.json), ["count", "next", "value"])
        self.assertEqual(resp.json["count"], 10)

    def test_get_ordering(self):
        resp = self.client.get(
            url_for("todos.get_todos", order="text desc"), headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(list(resp.json), ["next", "value"])
        self.assertEqual(len(resp.json["value"]), 10)
        self.assertEqual(resp.json["value"][0]["text"], "9 hacker")
        self.assertFalse(resp.json["value"][0]["completed"])

    def test_post(self):
        payload = {"text": "Get these tests completed"}

        def f(resp):
            self.assertTrue(resp.json["id"])
            self.assertEqual(resp.json["text"], payload["text"])
            self.assertFalse(resp.json["completed"])

        resp = self.client.post(
            url_for("todos.post_todos"), json=payload, headers=HEADERS_POST_PUT
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.headers)
        f(resp)

        resp = self.client.get(resp.headers["Location"], headers=HEADERS,)
        self.assertEqual(resp.status_code, 200)
        f(resp)


class TestTodo(common.TestFixure):
    def test_get(self):
        resp = self.client.get(
            url_for("todos.get_todo", id_=self.should.id), headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["id"], self.should.id)
        self.assertEqual(resp.json["text"], self.should.text)
        self.assertEqual(resp.json["completed"], self.should.completed)

        resp = self.client.get(
            url_for("todos.get_todo", id_=self.should.id),
            headers={
                **HEADERS,
                **{"Authorization": f"Bearer {common.OTHER_TOKEN}"},
            },
        )
        self.assertEqual(resp.status_code, 403)

    def test_put(self):
        payload = {"text": "Buy milk"}

        def f(resp):
            self.assertEqual(resp.json["text"], payload["text"])

        resp = self.client.put(
            url_for("todos.put_todo", id_=self.should.id),
            json=payload,
            headers=HEADERS_POST_PUT,
        )
        self.assertEqual(resp.status_code, 201)
        f(resp)

        resp = self.client.get(
            url_for("todos.put_todo", id_=self.should.id), headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 200)
        f(resp)

        resp = self.client.put(
            url_for("todos.put_todo", id_=self.should.id),
            json=payload,
            headers={
                **HEADERS_POST_PUT,
                **{"Authorization": f"Bearer {common.OTHER_TOKEN}"},
            },
        )
        self.assertEqual(resp.status_code, 403)

    def test_delete(self):
        resp = self.client.delete(
            url_for("todos.delete_todo", id_=self.should.id,), headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(resp.data)

        resp = self.client.get(
            url_for("todos.get_todo", id_=self.should.id), headers=HEADERS,
        )
        self.assertEqual(resp.status_code, 404)

        resp = self.client.delete(
            url_for("todos.delete_todo", id_=self.should.id,),
            headers={
                **HEADERS,
                **{"Authorization": f"Bearer {common.OTHER_TOKEN}"},
            },
        )


class TestExceptionCases(common.TestFixure):
    def assert_it(self, resp, status_code):
        self.assertEqual(resp.status_code, status_code)
        self.assertListEqual(list(resp.json), ["error"])
        self.assertListEqual(list(resp.json["error"]), ["code", "message"])

    def test_get_not_found(self):
        resp = self.client.get("/api/v1/hackers", headers=HEADERS,)
        self.assert_it(resp, 404)

    def test_get_args_bad_request_filter(self):
        resp = self.client.get(
            url_for("todos.get_todos", filter="text yal '0'",),
            headers=HEADERS,
        )
        self.assert_it(resp, 400)

    def test_get_args_bad_request_page(self):
        resp = self.client.get(
            url_for("todos.get_todos", page=-1, limit=2), headers=HEADERS,
        )
        self.assert_it(resp, 400)

        resp = self.client.get(
            url_for("todos.get_todos", page=0, limit=-1), headers=HEADERS,
        )
        self.assert_it(resp, 400)

        resp = self.client.get(
            url_for("todos.get_todos", page=0, limit=2000), headers=HEADERS,
        )
        self.assert_it(resp, 400)

        resp = self.client.get(
            url_for("todos.get_todos", page="hack", limit=2000,),
            headers=HEADERS,
        )
        self.assert_it(resp, 400)

        resp = self.client.get(
            url_for("todos.get_todos", page=0, limit=2, count="",),
            headers=HEADERS,
        )
        self.assert_it(resp, 400)

    def test_get_args_bad_request_order(self):
        resp = self.client.get(
            url_for("todos.get_todos", order="yal desc"), headers=HEADERS,
        )
        self.assert_it(resp, 400)

        resp = self.client.get(
            url_for("todos.get_todos", order="text hack"), headers=HEADERS,
        )
        self.assert_it(resp, 400)

    def test_get_view_args_bad_request_id(self):
        resp = self.client.get(
            url_for("todos.get_todo", id_=666), headers=HEADERS,
        )
        self.assert_it(resp, 400)

        resp = self.client.get(
            url_for("todos.get_todo", id_="%0A"), headers=HEADERS,
        )
        self.assert_it(resp, 400)

    def test_post_payload_bad_request(self):
        payload = {"id": "yal"}
        resp = self.client.post(
            url_for("todos.post_todos"), json=payload, headers=HEADERS_POST_PUT
        )
        self.assert_it(resp, 400)
        payload = {}
        resp = self.client.post(
            url_for("todos.post_todos"), json=payload, headers=HEADERS_POST_PUT
        )
        self.assert_it(resp, 400)

        payload = {"completed": True}
        resp = self.client.post(
            url_for("todos.post_todos"), json=payload, headers=HEADERS_POST_PUT
        )
        self.assert_it(resp, 400)

        payload = {"hack": "hack"}
        resp = self.client.post(
            url_for("todos.post_todos"), json=payload, headers=HEADERS_POST_PUT
        )
        self.assert_it(resp, 400)


if __name__ == "__main__":
    unittest.main()
