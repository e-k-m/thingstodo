import unittest

from hypothesis import given
import schemathesis

import common

fixure = common.TestFixure()
fixure.setUp()
app = fixure.app

schema = schemathesis.from_wsgi("/api/v0.0/openapi.yml", app)


class TestOpenAPI(common.TestFixure):
    def test_openapi(self):
        def test_it(case):
            response = case.call_wsgi()
            assert response.status_code < 500

        for e in schema.values():
            for strategy in e.values():
                given(case=strategy.as_strategy())(test_it)()


if __name__ == "__main__":
    unittest.main()
