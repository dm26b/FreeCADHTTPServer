from flask import Flask, request, jsonify
from PySide2.QtCore import *


class HttpServer(QObject):
    """Класс для работы с HTTP запросами в отдельном от основного потоке"""

    def __init__(self, app, port: int):
        QObject.__init__(self)
        self.__app = app
        self.__port = port

    @Slot()
    def runHttpServer(self):
        flaskApp = Flask(__name__)
        app = self.__app
        @flaskApp.route("/transaction-start/<string:docName>", methods=["GET"])
        def transactionStart(docName: str):
            """Старт серии действий с документом"""
            return app.transactionStart(docName)

        @flaskApp.route("/transaction-stop/<int:transactionId>", methods=["GET"])
        def transactionStop(transactionId: int):
            """Завершение серии действий"""
            return app.transactionStop(transactionId)

        @flaskApp.route("/add/<int:transactionId>/<string:type>/<string:label>", methods=['POST'])
        def add(transactionId: int, type: str, label: str):
            """Добавление объекта в документ"""
            return app.add(transactionId, type, label, request.json)

        @flaskApp.route("/modify/<int:transactionId>/<string:objectId>/<string:action>", methods=['PUT'])
        def modify(transactionId: int, objectId: str, action: str):
            """Изменение объекта"""
            return app.modify(transactionId, objectId, action, request.json)

        @flaskApp.route("/modify/<int:transactionId>/<string:objectId>", methods=['DELETE'])
        def delete(transactionId: int, objectId: str):
            """Удаление объекта"""
            return app.delete(transactionId, objectId)

        # все готово, запускаем сервис
        flaskApp.run(port=self.__port, use_reloader=False)
