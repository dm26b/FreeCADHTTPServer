import FreeCAD
from PySide2.QtCore import *
from httpserver import HttpServer
from dataclasses import dataclass

@dataclass
class TransactionData:
    id:int
    doc:FreeCAD.Document


class Application(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.__transactions:dict[int,TransactionData] = {}
        self.__transCounter = 0


    def startHttpServer(self, port):
        self.httpServ = HttpServer(self, port)
        self.thread = QThread(self)
        self.httpServ.moveToThread(self.thread)
        self.thread.started.connect(self.httpServ.runHttpServer)
        self.thread.start()

    @Slot(result=int)
    def transactionStart(self,docName:str):
        doc=None
        try:
            doc=FreeCAD.getDocument(docName)
        except:
            doc=FreeCAD.newDocument(docName)
        self.__transCounter += 1
        self.__transactions[self.__transCounter]=TransactionData(self.__transCounter, doc)
        return self.__transCounter

    @Slot()
    def transactionStop(self, transactionId:int):
        self.__transactions[transactionId].doc.recompute()
        self.__transactions.pop(transactionId)

    @Slot(result=dict):
    def add(self,transactionId:int, type:str, label:str, json:dict):
        doc = self.__transactions[transactionId].doc
        res = FreeCAD.activeDocument().addObject(type, label)
        for p, v in json.items():
            setattr(res, p, v)
        return res


if __name__ == '__main__':
    print(__name__)
    app = Application()
    app.startHttpServer(8080)