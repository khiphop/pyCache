# coding: utf-8
import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


if __name__ == '__main__':
    pass
