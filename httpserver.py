from flask import Flask, request, jsonify
from PySide2.QtCore import *


class HttpServer(QObject):
    """Класс для работы с HTTP запросами в отдельном от основного потоке"""

    def __init__(self, app, port: int):
        QObject.__init__(self)

    @Slot()
    def runHttpServer(self, app, port: int):
        flaskApp = Flask(__name__)

        @flaskApp.route("/transaction-start/<string:docName>", methods=["GET"])
        def transactionStart(docName: str):
            return app.transactionStart(docName)

        @flaskApp.route("/transaction-stop/<int:transactionId>", methods=["GET"])
        def transactionStop(transactionId: int):
            return app.transactionStop(transactionId)

        @flaskApp.route("/add/<int:transactionId>/<string:type>/<string:label>", methods=['POST'])
        def add(transactionId: int, type: str, label: str):
            """Добавление объекта в документ"""
            return app.add(transactionId, type, label, request.json)

        @flaskApp.route("/modify/<int:transactionId>/<string:objectId>/<string:action>", methods=['PUT'])
        def modify(transactionId: int, objectId: str, action: str):
            """Добавление объекта в документ"""
            return app.modify(transactionId, objectId, action, request.json)

        @flaskApp.route("/modify/<int:transactionId>/<string:objectId>", methods=['DELETE'])
        def delete(transactionId: int, objectId: str):
            """Добавление объекта в документ"""
            return app.delete(transactionId, objectId)

        # все готово, запускаем сервис
        flaskApp.run(port=port, use_reloader=False)
