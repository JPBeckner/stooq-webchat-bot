import csv
from urllib.parse import quote, urlencode
from csv import reader

from django.conf.urls import url
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from requests import get


class Stooq:

    def __init__(
        self,
        stock: str,
        symbol: bool = True,
        date: bool = False,
        time: bool = False,
        open: bool = False,
        high: bool = False,
        low: bool = False,
        close: bool = True,
        volume: bool = False,
        export: str = 'csv',
    ) -> None:
        values_to_search = []
        if symbol:
            values_to_search.append('s')
        if date:
            values_to_search.append('d2')
        if time:
            values_to_search.append('t2')
        if open:
            values_to_search.append('o')
        if high:
            values_to_search.append('h')
        if low:
            values_to_search.append('l')
        if close:
            values_to_search.append('c')
        if volume:
            values_to_search.append('v')

        parameters = {
            's': stock,
            'e': export,
            'f': ''.join(values_to_search),
        }
        parameters = urlencode(parameters)
        self.__url = "https://stooq.com/q/l/?{parameters}&h".format(parameters=parameters)

    @property
    def url(self) -> str:
        return self.__url

    def get_stock_quote(self) -> dict:
        response = get(
            url=self.url
        )
        return response.text

    def parse_csv(self, data: str) -> dict:
        parsed_data = list(csv.reader(  # parse the data
            data.splitlines()  # split the csv lines
        ))
        header = parsed_data.pop(0)
        content = parsed_data.pop(0)

        return dict(zip(header, content))

    def get_message(self, stock: str, price: str) -> str:
        if price == 'N/D':
            return f"{stock.upper()} quote not found."
        return f"{stock.upper()} quote is ${price} per share."


class Command(ViewSet):
    """
    Return data from Stooq API based on command provided.
    """
    command_name = 'stock'

    @action(detail=False, methods=['post'])
    def command(self, request: Request) -> Response:
        # check if the received command is the expected.
        try:
            command_received = request.data.get('command', '')
            if command_received != self.command_name:
                return Response(
                    data={"error": "Command not avaliable."},
                    status=HTTP_400_BAD_REQUEST
                )

            parameter = request.data.get('parameter', '')
            chat_room = request.data.get('room', '')
            # check if any data is unavaliable.
            if any(is_empty(value=value) for value in [command_received, parameter, chat_room]):
                return Response(
                    data={"error": "Wrong data received."},
                    status=HTTP_400_BAD_REQUEST
                )

            stooq = Stooq(stock=parameter)
            quote_data = stooq.get_stock_quote()
            quote_data = stooq.parse_csv(quote_data)
            message = stooq.get_message(stock=quote_data.get('Symbol'), price=quote_data.get('Close'))

            self.send_message(message=message)
            return Response(data={"msg": message}, status=HTTP_200_OK)

        except Exception as exc:
            print(exc)
            return Response(
                data={"error": "Service unavaliable."},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    def send_message(self, message: str):
        print(message)


def is_empty(value: str) -> bool:
    return not bool(value.strip())
