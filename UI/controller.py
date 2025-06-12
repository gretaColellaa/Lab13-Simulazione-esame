import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno = None

    def handleDDYearSelection(self):
        try: int(self._view._ddAnno.value)
        except: self._view.create_alert.controls.appennd(ft.Text(f"Selezionare un anno"))
        self._anno = self._view._ddAnno.value


    def handleCreaGrafo(self,e):
        self.handleDDYearSelection()
        self._model.creaGrafo(self._anno)
        self._view.txt_result.controls.append(ft.Text(f"il grafo ha {self._model.getNumNodes()} nodi"
                                                 f" e {self._model.getNumEdges()} archi"))
        bestp, best = self._model.getBest()
        self._view.txt_result.controls.append(ft.Text(f"Best driver {bestp} con un punteggio di: {best}"))
        self._view.update_page()



    def handleCerca(self, e):
        pass


    def fillDDYear(self):
        anni = self._model.getAnni()
        for a in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(a))
        self._view.update_page()